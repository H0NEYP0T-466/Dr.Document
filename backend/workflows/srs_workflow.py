"""SRS generation workflow (IEEE 830)"""
import asyncio
import os
import re
from typing import Dict, Any, List, Callable, Optional

from backend.agents.title_agent import TitleAgent
from backend.agents.srs.headings_agent import SRSHeadingsAgent
from backend.agents.srs.section_writer_agent import SRSSectionWriterAgent
from backend.agents.srs.manager_agent import SRSManagerAgent
from backend.agents.srs.formatter_agent import SRSFormatterAgent
from backend.agents.output_validator import sanitize_content
from backend.logger import logger


class SRSWorkflow:
    """
    Orchestrates the IEEE 830 SRS generation pipeline.
    """

    def __init__(
        self,
        job_dir: str,
        codebase_summary: str,
        repo_name: str,
        repo_url: str,
        status_callback: Optional[Callable] = None,
    ):
        self.job_dir = job_dir
        self.codebase_summary = codebase_summary
        self.repo_name = repo_name
        self.repo_url = repo_url
        self.status_callback = status_callback

    async def _emit(self, event: Dict[str, Any]):
        if self.status_callback:
            try:
                await self.status_callback(event)
            except Exception as e:
                logger.warning(f"Failed to emit event: {e}")

    async def execute(self, loop: asyncio.AbstractEventLoop) -> Dict[str, Any]:
        """Run the full SRS pipeline."""
        await self._emit({'type': 'mode_started', 'mode': 'srs'})

        # Title Agent
        await self._emit({'type': 'agent_started', 'agent': 'title', 'mode': 'srs'})
        title_agent = TitleAgent()
        title_result = await loop.run_in_executor(
            None, title_agent.run,
            {'codebase_summary': self.codebase_summary, 'repo_name': self.repo_name},
        )
        selected_title = title_result['selected_title']
        title_txt = title_result['title_txt']
        self._save(title_txt, 'title.txt')

        await self._emit({
            'type': 'agent_completed',
            'agent': 'title',
            'mode': 'srs',
            'result': selected_title,
        })

        # Headings Agent
        await self._emit({'type': 'agent_started', 'agent': 'headings', 'mode': 'srs'})
        headings_agent = SRSHeadingsAgent()
        headings_result = await loop.run_in_executor(
            None, headings_agent.run,
            {
                'codebase_summary': self.codebase_summary,
                'title_txt': title_txt,
                'selected_title': selected_title,
                'repo_name': self.repo_name,
            },
        )
        sections_meta: List[Dict] = headings_result['sections']
        headings_txt: str = headings_result['headings_txt']
        system_features: List[str] = headings_result.get('system_features', [])
        self._save(headings_txt, 'srs_headings.txt')

        await self._emit({
            'type': 'agent_completed',
            'agent': 'headings',
            'mode': 'srs',
            'section_count': len(sections_meta),
        })

        # Section Writers + Manager
        approved_sections = await self._write_and_review_sections(
            sections_meta=sections_meta,
            headings_txt=headings_txt,
            selected_title=selected_title,
            system_features=system_features,
            loop=loop,
        )

        # Formatter
        await self._emit({'type': 'agent_started', 'agent': 'formatter', 'mode': 'srs'})
        await self._emit({'type': 'formatter_compiling', 'stage': 'latex', 'mode': 'srs'})

        formatter = SRSFormatterAgent()
        fmt_result = await loop.run_in_executor(
            None, formatter.run,
            {
                'sections': approved_sections,
                'selected_title': selected_title,
                'repo_name': self.repo_name,
                'repo_url': self.repo_url,
                'job_dir': self.job_dir,
            },
        )

        if fmt_result.get('latex_errors'):
            await self._emit({
                'type': 'formatter_latex_error',
                'error': fmt_result['latex_errors'][:500],
                'mode': 'srs',
            })

        await self._emit({'type': 'formatter_compiling', 'stage': 'docx', 'mode': 'srs'})

        files = {}
        if fmt_result.get('tex_path') and os.path.exists(fmt_result['tex_path']):
            files['tex'] = fmt_result['tex_path']
        if fmt_result.get('pdf_path') and os.path.exists(fmt_result['pdf_path']):
            files['pdf'] = fmt_result['pdf_path']
        if fmt_result.get('docx_path') and os.path.exists(fmt_result['docx_path']):
            files['docx'] = fmt_result['docx_path']

        await self._emit({
            'type': 'mode_completed',
            'mode': 'srs',
            'files': list(files.keys()),
        })

        return {
            'status': 'completed',
            'selected_title': selected_title,
            'sections': approved_sections,
            'files': files,
        }

    async def _write_and_review_sections(
        self,
        sections_meta: List[Dict],
        headings_txt: str,
        selected_title: str,
        system_features: List[str],
        loop: asyncio.AbstractEventLoop,
    ) -> List[Dict]:
        """Write, review, and restart SRS sections."""
        max_restarts = 3
        manager = SRSManagerAgent()

        section_states = [
            {
                'name': sec['name'],
                'brief': sec.get('brief', ''),
                'content': '',
                'restart_count': 0,
                'manager_feedback': '',
                'approved': False,
            }
            for sec in sections_meta
        ]

        async def write_section(state: Dict):
            await self._emit({
                'type': 'agent_started',
                'agent': 'section_writer',
                'section': state['name'],
                'mode': 'srs',
            })
            writer = SRSSectionWriterAgent(state['name'])
            result = await loop.run_in_executor(
                None, writer.run,
                {
                    'section_name': state['name'],
                    'section_brief': state['brief'],
                    'codebase_summary': self.codebase_summary,
                    'headings_txt': headings_txt,
                    'selected_title': selected_title,
                    'repo_name': self.repo_name,
                    'system_features': system_features,
                    'manager_feedback': state['manager_feedback'],
                },
            )
            state['content'] = result['content']
            safe_name = re.sub(r'[^\w\-]', '_', state['name'])[:60]
            self._save(state['content'], f"srs_section_{safe_name}.txt")
            await self._emit({
                'type': 'agent_completed',
                'agent': 'section_writer',
                'section': state['name'],
                'mode': 'srs',
                'word_count': result['word_count'],
            })

        await asyncio.gather(*[write_section(s) for s in section_states])

        # Sanitize section content to remove any meta chatter that leaked through
        for state in section_states:
            state['content'] = sanitize_content(state['content'])

        for _ in range(max_restarts):
            pending = [s for s in section_states if not s['approved']]
            if not pending:
                break

            for state in pending:
                review = await loop.run_in_executor(
                    None, manager.run,
                    {
                        'section_name': state['name'],
                        'section_content': state['content'],
                        'section_brief': state['brief'],
                        'codebase_summary': self.codebase_summary,
                        'restart_count': state['restart_count'],
                    },
                )
                await self._emit({
                    'type': 'manager_decision',
                    'section': state['name'],
                    'decision': review['status'],
                    'restart_count': review['restart_count'],
                    'feedback': review['feedback'],
                    'mode': 'srs',
                })
                if review['status'] in ('APPROVED', 'APPROVED_WITH_WARNING'):
                    state['approved'] = True
                else:
                    state['restart_count'] = review['restart_count']
                    state['manager_feedback'] = review['feedback']

            to_restart = [s for s in section_states if not s['approved']]
            if to_restart:
                await asyncio.gather(*[write_section(s) for s in to_restart])
                # Sanitize restarted sections
                for state in to_restart:
                    state['content'] = sanitize_content(state['content'])

        for state in section_states:
            if not state['approved']:
                logger.warning(
                    f"Force-approving section '{state['name']}' after {state['restart_count']} restarts"
                )
                state['approved'] = True

        review_lines = [f"{s['name']}_STATUS: APPROVED" for s in section_states]
        review_lines.append('PIPELINE_READY: true')
        self._save('\n'.join(review_lines), 'srs_manager_review.txt')

        return [{'name': s['name'], 'content': s['content']} for s in section_states]

    def _save(self, content: str, filename: str):
        try:
            path = os.path.join(self.job_dir, filename)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            logger.error(f"Failed to save {filename}: {e}")
