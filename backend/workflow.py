"""Incremental multi-agent documentation generation workflow"""
import asyncio
import json
import os
import re
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime

from backend.agents.codebase_summarizer import CodebaseSummarizerAgent
from backend.agents.headings_selector import HeadingsSelectorAgent
from backend.agents.section_writer import SectionWriterAgent
from backend.agents.manager import ManagerAgent
from backend.agents.final_reviewer import FinalReviewerAgent
from backend.agents.license_writer import LicenseWriterAgent
from backend.agents.contributing_writer import ContributingWriterAgent
from backend.agents.code_of_conduct_writer import CodeOfConductWriterAgent
from backend.agents.security_writer import SecurityWriterAgent
from backend.agents.support_writer import SupportWriterAgent
from backend.agents.codeowners_writer import CodeownersWriterAgent
from backend.agents.community_manager import CommunityManagerAgent
from backend.agents.community_final_reviewer import CommunityFinalReviewerAgent
from backend.github_client import GitHubClient
from backend.config import settings
from backend.logger import logger


class WorkflowStatus:
    """Workflow status constants"""
    PENDING = "pending"
    CLONING = "cloning"
    SUMMARIZING = "summarizing"
    SELECTING_HEADINGS = "selecting_headings"
    WRITING_SECTIONS = "writing_sections"
    MANAGER_REVIEW = "manager_review"
    FINAL_REVIEW = "final_review"
    COMMUNITY_FILES = "community_files"
    COMPLETED = "completed"
    FAILED = "failed"


def _safe_dir_name(name: str) -> str:
    """Convert a string to a safe directory name."""
    return re.sub(r'[^\w\-]', '_', name)[:60]


class DocumentationWorkflow:
    """Orchestrates the incremental multi-agent documentation generation workflow."""

    def __init__(self, job_id: str):
        self.job_id = job_id
        self.status = WorkflowStatus.PENDING
        self.progress = 0
        self.result = None
        self.error = None
        self.status_callback: Optional[Callable] = None

        # GitHub client
        self.github_client = GitHubClient()

        # Storage (set properly in execute once we know repo_name)
        self._base_storage = settings.storage_path
        self.storage_dir: str = ''

        logger.info(f"Workflow initialized for job {job_id}")

    def set_status_callback(self, callback: Callable):
        """Set callback for status updates (called by the API layer)."""
        self.status_callback = callback

    # ------------------------------------------------------------------
    # Status / progress helpers
    # ------------------------------------------------------------------

    async def _update_status(
        self,
        status: str,
        progress: int,
        message: str = '',
        agent_update: Optional[Dict] = None,
    ):
        """Broadcast a status update via the callback."""
        self.status = status
        self.progress = progress

        logger.workflow_step("Status Update", f"{status} — {progress}% — {message}")

        if self.status_callback:
            payload: Dict[str, Any] = {
                'job_id': self.job_id,
                'status': status,
                'progress': progress,
                'message': message,
                'timestamp': datetime.now().isoformat(),
            }
            if agent_update:
                payload['agent_update'] = agent_update
            await self.status_callback(payload)

    # ------------------------------------------------------------------
    # Storage helpers
    # ------------------------------------------------------------------

    def _agent_dir(self, agent_folder: str) -> str:
        """Return (and create) the storage dir for a specific agent."""
        path = os.path.join(self.storage_dir, agent_folder)
        os.makedirs(path, exist_ok=True)
        return path

    def _save_text(self, agent_folder: str, filename: str, content: str):
        """Save plain-text content to an agent's storage folder."""
        try:
            filepath = os.path.join(self._agent_dir(agent_folder), filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.file_process(filepath, 'Saved')
        except Exception as exc:
            logger.error(f"Failed to save {filename}: {exc}")

    def _save_json(self, agent_folder: str, filename: str, data: Any):
        """Save JSON data to an agent's storage folder."""
        try:
            filepath = os.path.join(self._agent_dir(agent_folder), filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            logger.file_process(filepath, 'Saved JSON')
        except Exception as exc:
            logger.error(f"Failed to save {filename}: {exc}")

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    async def execute(self, repo_url: str) -> Dict[str, Any]:
        """
        Execute the complete incremental documentation workflow.

        Workflow:
          1. Clone repo
          2. Agent 1 (Codebase Summarizer): one LLM call per file → codebase.txt
          3. Agent 2 (Headings Selector): select N headings → headings.txt
          4. Agents 3…N (Section Writers): one agent per heading → section files
          5. Manager: review each section individually (up to 3 retries per section)
          6. Agent N+1 (Final Reviewer): review full README (up to 3 full cycles)
        """
        try:
            logger.info(f"🚀 Starting workflow for {repo_url}")
            loop = asyncio.get_running_loop()

            # ----------------------------------------------------------------
            # Step 1: Clone repository
            # ----------------------------------------------------------------
            await self._update_status(WorkflowStatus.CLONING, 5, "Cloning repository…")
            repo_path = await loop.run_in_executor(
                None, self.github_client.clone_repository, repo_url
            )
            repo_name = self.github_client.extract_repo_name(repo_url)

            # Set up per-repo storage directory
            safe_repo = _safe_dir_name(repo_name)
            self.storage_dir = os.path.join(self._base_storage, safe_repo)
            os.makedirs(self.storage_dir, exist_ok=True)

            # ----------------------------------------------------------------
            # Step 2: Discover files
            # ----------------------------------------------------------------
            await self._update_status(WorkflowStatus.SUMMARIZING, 8, "Discovering files…")
            files = await loop.run_in_executor(
                None, self.github_client.get_repository_files, repo_path
            )
            if not files:
                raise ValueError("No supported files found in repository")

            # Respect max_files_to_analyze setting
            max_files = settings.max_files_to_analyze
            if len(files) > max_files:
                logger.info(f"Limiting to {max_files} files out of {len(files)}")
                files = files[:max_files]

            # ----------------------------------------------------------------
            # Step 3: Codebase Summarizer (Agent 1) — one LLM call per file
            # ----------------------------------------------------------------
            codebase_summary = await self._run_codebase_summarizer(files, loop)
            self._save_text('codebase_summarizer', 'codebase.txt', codebase_summary)

            # ----------------------------------------------------------------
            # Step 4: Headings Selector (Agent 2)
            # ----------------------------------------------------------------
            await self._update_status(
                WorkflowStatus.SELECTING_HEADINGS, 40,
                "Selecting documentation headings…",
                agent_update={
                    'agent_id': 'headings_selector',
                    'agent_name': '📋 Headings Selector',
                    'agent_status': 'working',
                },
            )
            headings_selector = HeadingsSelectorAgent()
            headings_result = await loop.run_in_executor(
                None, headings_selector.run,
                {'codebase_summary': codebase_summary, 'repo_name': repo_name},
            )
            headings: List[str] = headings_result['headings']
            self._save_text('headings_selector', 'headings.txt', headings_result['headings_txt'])

            await self._update_status(
                WorkflowStatus.SELECTING_HEADINGS, 42,
                f"Selected {len(headings)} headings",
                agent_update={
                    'agent_id': 'headings_selector',
                    'agent_name': '📋 Headings Selector',
                    'agent_status': 'completed',
                },
            )

            # ----------------------------------------------------------------
            # Steps 5–7: Section writing + manager review loop
            # Up to 3 full cycles driven by the Final Reviewer
            # ----------------------------------------------------------------
            max_full_cycles = 1
            final_readme = ''
            final_review_result: Dict = {}
            improvement_details = ''

            for cycle in range(1, max_full_cycles + 1):
                logger.info(f"Starting documentation cycle {cycle}/{max_full_cycles}")

                # Section writing + manager review for every heading
                approved_sections = await self._write_and_review_sections(
                    headings=headings,
                    codebase_summary=codebase_summary,
                    repo_name=repo_name,
                    cycle=cycle,
                    global_improvement=improvement_details,
                    loop=loop,
                )

                # Combine sections into a full README
                final_readme = self._combine_sections(repo_name, approved_sections)
                self._save_text('final_reviewer', f'readme_cycle_{cycle}.md', final_readme)

                # Final Reviewer
                prog = 88 + (cycle - 1) * 3
                await self._update_status(
                    WorkflowStatus.FINAL_REVIEW,
                    prog,
                    f"Final review — cycle {cycle}/{max_full_cycles}…",
                    agent_update={
                        'agent_id': 'final_reviewer',
                        'agent_name': '🔍 Final Reviewer',
                        'agent_status': 'working',
                    },
                )

                final_reviewer = FinalReviewerAgent()
                final_review_result = await loop.run_in_executor(
                    None, final_reviewer.run,
                    {
                        'readme_content': final_readme,
                        'codebase_summary': codebase_summary,
                        'repo_name': repo_name,
                    },
                )
                self._save_json(
                    'final_reviewer',
                    f'final_review_cycle_{cycle}.json',
                    final_review_result,
                )

                if final_review_result.get('approved', False):
                    logger.success(f"Final Reviewer APPROVED on cycle {cycle}")
                    await self._update_status(
                        WorkflowStatus.FINAL_REVIEW,
                        prog + 2,
                        "README approved by Final Reviewer!",
                        agent_update={
                            'agent_id': 'final_reviewer',
                            'agent_name': '🔍 Final Reviewer',
                            'agent_status': 'completed',
                        },
                    )
                    break
                else:
                    improvement_details = final_review_result.get('improvement_details', '')
                    logger.warning(
                        f"Final Reviewer REJECTED on cycle {cycle}. "
                        f"Improvement notes: {improvement_details[:200]}"
                    )
                    await self._update_status(
                        WorkflowStatus.FINAL_REVIEW,
                        prog + 1,
                        f"README rejected — restarting cycle {cycle + 1}…"
                        if cycle < max_full_cycles
                        else "README rejected — using best attempt",
                        agent_update={
                            'agent_id': 'final_reviewer',
                            'agent_name': '🔍 Final Reviewer',
                            'agent_status': 'working' if cycle < max_full_cycles else 'completed',
                        },
                    )
                    if cycle == max_full_cycles:
                        logger.warning("Max cycles reached — using last README draft")

            # ----------------------------------------------------------------
            # Save final README
            # ----------------------------------------------------------------
            self._save_text('final_reviewer', 'README.md', final_readme)

            await self._update_status(WorkflowStatus.COMMUNITY_FILES, 95, "README complete — generating community files…")

            # ----------------------------------------------------------------
            # Community file generation (LICENSE, CONTRIBUTING, etc.)
            # ----------------------------------------------------------------
            repo_owner = repo_name.split('/')[0] if '/' in repo_name else repo_name
            community_files = await self._generate_community_files(
                repo_name=repo_name,
                repo_owner=repo_owner,
                codebase_summary=codebase_summary,
                loop=loop,
            )

            await self._update_status(WorkflowStatus.COMPLETED, 100, "Documentation complete!")

            result = {
                'job_id': self.job_id,
                'repo_name': repo_name,
                'repo_url': repo_url,
                'readme': final_readme,
                'community_files': community_files,
                'files_analyzed': len(files),
                'headings': headings,
                'final_review': {
                    'approved': final_review_result.get('approved', False),
                    'completeness_score': final_review_result.get('completeness_score', 0),
                    'accuracy_score': final_review_result.get('accuracy_score', 0),
                },
                'storage_path': self.storage_dir,
                'timestamp': datetime.now().isoformat(),
            }
            self.result = result
            logger.success(f"✅ Workflow completed for {repo_name}")
            return result

        except Exception as exc:
            logger.error(f"Workflow failed: {exc}", exc_info=True)
            self.status = WorkflowStatus.FAILED
            self.error = str(exc)
            await self._update_status(WorkflowStatus.FAILED, self.progress, f"Error: {exc}")
            raise

        finally:
            self.github_client.cleanup()

    # ------------------------------------------------------------------
    # Codebase Summarizer helper
    # ------------------------------------------------------------------

    async def _run_codebase_summarizer(
        self, files: List[Dict], loop: asyncio.AbstractEventLoop
    ) -> str:
        """Run Agent 1: one LLM call per file, build codebase.txt."""
        summarizer = CodebaseSummarizerAgent()
        total = len(files)
        lines: List[str] = []

        for idx, file_info in enumerate(files):
            progress = 8 + int((idx / total) * 30)  # 8 → 38%
            await self._update_status(
                WorkflowStatus.SUMMARIZING,
                progress,
                f"Summarizing {file_info['relative_path']} ({idx + 1}/{total})…",
                agent_update={
                    'agent_id': 'codebase_summarizer',
                    'agent_name': '👁️ Codebase Summarizer',
                    'agent_status': 'working',
                    'agent_progress': int((idx / total) * 100),
                },
            )
            try:
                content = await loop.run_in_executor(
                    None, self.github_client.read_file_content, file_info['path']
                )
                if content:
                    result = await loop.run_in_executor(
                        None, summarizer.run,
                        {'file_path': file_info['relative_path'], 'file_content': content},
                    )
                    lines.append(f"{result['file_path']} = {result['summary']}")
            except Exception as exc:
                logger.error(f"Failed to summarize {file_info['relative_path']}: {exc}")
                continue

        await self._update_status(
            WorkflowStatus.SUMMARIZING,
            38,
            f"Codebase summary complete ({len(lines)} files)",
            agent_update={
                'agent_id': 'codebase_summarizer',
                'agent_name': '👁️ Codebase Summarizer',
                'agent_status': 'completed',
                'agent_progress': 100,
            },
        )
        return '\n'.join(lines)

    # ------------------------------------------------------------------
    # Section writing + manager review loop
    # ------------------------------------------------------------------

    async def _write_and_review_sections(
        self,
        headings: List[str],
        codebase_summary: str,
        repo_name: str,
        cycle: int,
        global_improvement: str,
        loop: asyncio.AbstractEventLoop,
    ) -> List[Dict[str, str]]:
        """
        For every heading:
          1. SectionWriterAgent writes the section.
          2. ManagerAgent reviews it (up to 3 retries with improvement notes).
        Returns a list of {'heading': ..., 'content': ...} dicts.
        """
        total_headings = len(headings)
        approved_sections: List[Dict[str, str]] = []
        manager = ManagerAgent()
        max_section_retries = 3

        # Base progress range: 45 → 85% spread across headings
        progress_per_heading = int(40 / max(total_headings, 1))

        for h_idx, heading in enumerate(headings):
            base_prog = 45 + h_idx * progress_per_heading
            agent_id = f"section_writer_{_safe_dir_name(heading)}"
            agent_folder = f"section_writer_{_safe_dir_name(heading)}"

            improvement_notes = global_improvement  # carry forward global notes on cycle > 1
            section_content = ''

            for attempt in range(1, max_section_retries + 1):
                # --- Write section ---
                await self._update_status(
                    WorkflowStatus.WRITING_SECTIONS,
                    base_prog,
                    f"[Cycle {cycle}] Writing '{heading}' (attempt {attempt}/{max_section_retries})…",
                    agent_update={
                        'agent_id': agent_id,
                        'agent_name': f'✍️ Section Writer: {heading}',
                        'agent_status': 'working',
                    },
                )

                writer = SectionWriterAgent(heading)
                writer_result = await loop.run_in_executor(
                    None, writer.run,
                    {
                        'heading': heading,
                        'codebase_summary': codebase_summary,
                        'repo_name': repo_name,
                        'improvement_notes': improvement_notes,
                    },
                )
                section_content = writer_result['content']
                self._save_text(
                    agent_folder,
                    f'section_cycle{cycle}_attempt{attempt}.md',
                    section_content,
                )

                # --- Manager review ---
                await self._update_status(
                    WorkflowStatus.MANAGER_REVIEW,
                    base_prog + 1,
                    f"[Cycle {cycle}] Manager reviewing '{heading}'…",
                    agent_update={
                        'agent_id': 'manager',
                        'agent_name': '👔 Manager',
                        'agent_status': 'working',
                    },
                )

                review = await loop.run_in_executor(
                    None, manager.run,
                    {
                        'heading': heading,
                        'section_content': section_content,
                        'codebase_summary': codebase_summary,
                        'repo_name': repo_name,
                    },
                )
                self._save_json(
                    'manager',
                    f'review_{_safe_dir_name(heading)}_cycle{cycle}_attempt{attempt}.json',
                    review,
                )

                if review.get('approved', False):
                    logger.success(
                        f"Manager APPROVED '{heading}' on attempt {attempt}"
                    )
                    await self._update_status(
                        WorkflowStatus.MANAGER_REVIEW,
                        base_prog + 2,
                        f"'{heading}' approved ✓",
                        agent_update={
                            'agent_id': agent_id,
                            'agent_name': f'✍️ Section Writer: {heading}',
                            'agent_status': 'completed',
                        },
                    )
                    break
                else:
                    improvement_notes = review.get('improvement_notes', '')
                    logger.warning(
                        f"Manager REJECTED '{heading}' on attempt {attempt}. "
                        f"Notes: {improvement_notes[:150]}"
                    )
                    if attempt == max_section_retries:
                        logger.warning(
                            f"Max retries reached for '{heading}' — using last attempt"
                        )
                        await self._update_status(
                            WorkflowStatus.MANAGER_REVIEW,
                            base_prog + 2,
                            f"'{heading}' used after max retries",
                            agent_update={
                                'agent_id': agent_id,
                                'agent_name': f'✍️ Section Writer: {heading}',
                                'agent_status': 'completed',
                            },
                        )

            approved_sections.append({'heading': heading, 'content': section_content})

        return approved_sections

    # ------------------------------------------------------------------
    # Community file generation
    # ------------------------------------------------------------------

    async def _generate_community_files(
        self,
        repo_name: str,
        repo_owner: str,
        codebase_summary: str,
        loop: asyncio.AbstractEventLoop,
    ) -> List[Dict[str, str]]:
        """
        Generate the 6 community health files with manager review (up to 3 retries
        per file) and a final reviewer (up to 3 full cycles).

        Returns a list of {'filename': ..., 'content': ...} dicts.
        """
        # Define the 6 writer agents
        writer_factories = [
            ('LICENSE',             LicenseWriterAgent),
            ('CONTRIBUTING.md',     ContributingWriterAgent),
            ('CODE_OF_CONDUCT.md',  CodeOfConductWriterAgent),
            ('SECURITY.md',         SecurityWriterAgent),
            ('SUPPORT.md',          SupportWriterAgent),
            ('CODEOWNERS',          CodeownersWriterAgent),
        ]

        max_full_cycles = 3
        approved_files: List[Dict[str, str]] = []
        community_improvement = ''

        for cycle in range(1, max_full_cycles + 1):
            logger.info(f"Community files — cycle {cycle}/{max_full_cycles}")
            approved_files = []

            for filename, WriterClass in writer_factories:
                agent_id = f"community_{filename.replace('.', '_').lower()}"

                await self._update_status(
                    WorkflowStatus.COMMUNITY_FILES,
                    95,
                    f"[Cycle {cycle}] Writing {filename}…",
                    agent_update={
                        'agent_id': agent_id,
                        'agent_name': f'📄 {filename}',
                        'agent_status': 'working',
                    },
                )

                improvement_notes = community_improvement
                file_content = ''
                max_retries = 3
                manager = CommunityManagerAgent()

                for attempt in range(1, max_retries + 1):
                    writer = WriterClass()
                    writer_result = await loop.run_in_executor(
                        None, writer.run,
                        {
                            'repo_name': repo_name,
                            'repo_owner': repo_owner,
                            'codebase_summary': codebase_summary,
                            'improvement_notes': improvement_notes,
                        },
                    )
                    file_content = writer_result['content']
                    self._save_text(
                        'community_files',
                        f'{filename}_cycle{cycle}_attempt{attempt}',
                        file_content,
                    )

                    # Manager review
                    review = await loop.run_in_executor(
                        None, manager.run,
                        {
                            'filename': filename,
                            'content': file_content,
                            'repo_name': repo_name,
                            'repo_owner': repo_owner,
                        },
                    )

                    if review.get('approved', False):
                        logger.success(f"Community Manager APPROVED {filename} on attempt {attempt}")
                        break
                    else:
                        improvement_notes = review.get('improvement_notes', '')
                        logger.warning(f"Community Manager REJECTED {filename} on attempt {attempt}")
                        if attempt == max_retries:
                            logger.warning(f"Max retries for {filename} — using last attempt")

                approved_files.append({'filename': filename, 'content': file_content})

                await self._update_status(
                    WorkflowStatus.COMMUNITY_FILES,
                    96,
                    f"{filename} done ✓",
                    agent_update={
                        'agent_id': agent_id,
                        'agent_name': f'📄 {filename}',
                        'agent_status': 'completed',
                    },
                )

            # Community Final Reviewer
            await self._update_status(
                WorkflowStatus.COMMUNITY_FILES,
                98,
                f"Final review of community files — cycle {cycle}…",
                agent_update={
                    'agent_id': 'community_final_reviewer',
                    'agent_name': '🔍 Community Final Reviewer',
                    'agent_status': 'working',
                },
            )

            final_reviewer = CommunityFinalReviewerAgent()
            final_result = await loop.run_in_executor(
                None, final_reviewer.run,
                {
                    'community_files': approved_files,
                    'repo_name': repo_name,
                    'repo_owner': repo_owner,
                },
            )
            self._save_json('community_files', f'final_review_cycle_{cycle}.json', final_result)

            await self._update_status(
                WorkflowStatus.COMMUNITY_FILES,
                99,
                "Community files approved!" if final_result.get('approved') else f"Retrying community files (cycle {cycle + 1})…",
                agent_update={
                    'agent_id': 'community_final_reviewer',
                    'agent_name': '🔍 Community Final Reviewer',
                    'agent_status': 'completed' if final_result.get('approved') or cycle == max_full_cycles else 'working',
                },
            )

            if final_result.get('approved', False):
                logger.success(f"Community Final Reviewer APPROVED on cycle {cycle}")
                break
            else:
                community_improvement = final_result.get('improvement_details', '')
                logger.warning(f"Community Final Reviewer REJECTED on cycle {cycle}")
                if cycle == max_full_cycles:
                    logger.warning("Max community cycles reached — using last set")

        # Save final community files
        for file_dict in approved_files:
            self._save_text('community_files', file_dict['filename'], file_dict['content'])

        return approved_files

    # ------------------------------------------------------------------
    # Combine sections
    # ------------------------------------------------------------------

    def _combine_sections(self, repo_name: str, sections: List[Dict[str, str]]) -> str:
        """Combine all approved sections into a single README string."""
        parts = [f"# {repo_name}\n"]
        seen_headings: set = set()
        for section in sections:
            heading_key = section['heading'].lower()
            if heading_key in seen_headings:
                continue
            seen_headings.add(heading_key)
            parts.append(section['content'])
            parts.append('')  # blank line between sections

        # Footer: "Made with ❤️ by username" only — no tech-stack badges at the bottom
        username = repo_name.split('/')[0] if '/' in repo_name else repo_name
        parts.append('---')
        parts.append('')
        parts.append(
            f'<p align="center">Made with ❤️ by '
            f'<a href="https://github.com/{username}">{username}</a></p>'
        )
        return '\n'.join(parts)
