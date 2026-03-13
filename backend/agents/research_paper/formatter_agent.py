"""Research Paper Formatter Agent - Assembles, polishes, generates LaTeX/PDF/DOCX"""
import asyncio
import json
import os
import subprocess
import tempfile
from typing import Dict, Any, List
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class ResearchPaperFormatterAgent(BaseAgent):
    """
    Assembles all approved sections into a research paper.
    Produces: .tex, .pdf (via pdflatex), and .docx (via Node.js docx package).
    """

    def __init__(self):
        super().__init__("Research Paper Formatter Agent", settings.model_flash_lite)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format the research paper.

        Args:
            input_data: {
                'sections': List[{name, content}],
                'selected_title': str,
                'repo_name': str,
                'repo_url': str,
                'job_dir': str,       # absolute path to job directory
            }

        Returns:
            {
                'tex_content': str,
                'tex_path': str,
                'pdf_path': str | None,
                'docx_path': str | None,
                'latex_errors': str,
            }
        """
        sections = input_data.get('sections', [])
        selected_title = input_data.get('selected_title', 'Research Paper')
        repo_name = input_data.get('repo_name', 'Unknown')
        repo_url = input_data.get('repo_url', '')
        job_dir = input_data.get('job_dir', tempfile.gettempdir())

        logger.workflow_step("Research Paper Formatter", "Assembling paper")

        # Step 1: Polish content via LLM
        polished_sections = self._polish_content(sections, selected_title)

        # Step 2: Generate LaTeX
        tex_content = self._generate_latex(polished_sections, selected_title, repo_name, repo_url)
        tex_path = os.path.join(job_dir, 'research_paper.tex')
        with open(tex_path, 'w', encoding='utf-8') as f:
            f.write(tex_content)

        # Step 3: Compile PDF
        pdf_path, latex_errors = self._compile_pdf(tex_path, job_dir)

        # Log errors
        errors_log = os.path.join(job_dir, 'formatter_latex_errors.log')
        with open(errors_log, 'w', encoding='utf-8') as f:
            f.write(latex_errors or 'No errors')

        # Step 4: Generate DOCX
        docx_path = self._generate_docx(polished_sections, selected_title, repo_name, job_dir)

        return {
            'tex_content': tex_content,
            'tex_path': tex_path,
            'pdf_path': pdf_path,
            'docx_path': docx_path,
            'latex_errors': latex_errors,
        }

    def _polish_content(self, sections: List[Dict], title: str) -> List[Dict]:
        """Use LLM to fix grammar, consistency and tone across all sections."""
        polished = []
        for sec in sections:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are an academic editor. Polish the provided section for grammar, "
                        "spelling, punctuation, consistent academic tone, and smooth transitions. "
                        "Do not change the substance. Return only the corrected section text."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Paper: {title}\nSection: {sec['name']}\n\n{sec['content']}"
                    ),
                },
            ]
            try:
                polished_content = self._call_llm(messages, max_tokens=1500, temperature=0.2)
                polished.append({'name': sec['name'], 'content': polished_content.strip()})
            except Exception as e:
                logger.warning(f"Could not polish section '{sec['name']}': {e}")
                polished.append(sec)
        return polished

    def _generate_latex(
        self,
        sections: List[Dict],
        title: str,
        repo_name: str,
        repo_url: str,
    ) -> str:
        """Generate a complete IEEE-formatted LaTeX document."""
        # Escape title for LaTeX
        safe_title = self._latex_escape(title)
        author = repo_name.split('/')[0] if '/' in repo_name else repo_name

        # Build section bodies
        body_parts = []
        abstract_content = ''
        references_content = ''
        other_sections = []

        for sec in sections:
            name_lower = sec['name'].lower()
            if name_lower == 'abstract':
                abstract_content = self._latex_escape(sec['content'])
            elif name_lower == 'references':
                references_content = sec['content']
            else:
                other_sections.append(sec)

        for sec in other_sections:
            sec_title = self._latex_escape(sec['name'])
            sec_body = self._latex_escape(sec['content'])
            body_parts.append(f'\\section{{{sec_title}}}\n{sec_body}\n')

        body = '\n'.join(body_parts)

        # Build references
        ref_body = self._format_references_latex(references_content, repo_url)

        tex = f"""\\documentclass[conference]{{IEEEtran}}
\\usepackage{{cite}}
\\usepackage{{amsmath,amssymb,amsfonts}}
\\usepackage{{algorithmic}}
\\usepackage{{graphicx}}
\\usepackage{{textcomp}}
\\usepackage{{xcolor}}
\\usepackage{{hyperref}}
\\usepackage{{listings}}
\\usepackage{{booktabs}}

\\title{{{safe_title}}}
\\author{{{self._latex_escape(author)}}}
\\date{{\\today}}

\\begin{{document}}
\\maketitle

\\begin{{abstract}}
{abstract_content}
\\end{{abstract}}

{body}

\\begin{{thebibliography}}{{99}}
{ref_body}
\\end{{thebibliography}}

\\end{{document}}
"""
        return tex

    def _latex_escape(self, text: str) -> str:
        """Escape special LaTeX characters in plain text."""
        # Order matters — escape backslash first
        replacements = [
            ('\\', r'\textbackslash{}'),
            ('&', r'\&'),
            ('%', r'\%'),
            ('$', r'\$'),
            ('#', r'\#'),
            ('^', r'\textasciicircum{}'),
            ('~', r'\textasciitilde{}'),
        ]
        for old, new in replacements:
            text = text.replace(old, new)
        return text

    def _format_references_latex(self, references_content: str, repo_url: str) -> str:
        """Convert references content to LaTeX bibitem entries."""
        if not references_content.strip():
            return f'\\bibitem{{repo}} Repository: \\url{{{repo_url}}}'

        lines = []
        idx = 1
        for line in references_content.strip().splitlines():
            stripped = line.strip()
            if stripped and (stripped[0].isdigit() or stripped.startswith('[')):
                # Remove leading number/bracket
                clean = stripped.lstrip('0123456789[].) ')
                lines.append(f'\\bibitem{{ref{idx}}} {self._latex_escape(clean)}')
                idx += 1
        return '\n'.join(lines) if lines else f'\\bibitem{{repo}} Repository: \\url{{{repo_url}}}'

    def _compile_pdf(self, tex_path: str, job_dir: str) -> tuple:
        """Run pdflatex up to 3 times. Returns (pdf_path_or_None, error_log)."""
        pdf_path = tex_path.replace('.tex', '.pdf')
        errors = ''
        max_retries = 3

        for attempt in range(1, max_retries + 1):
            try:
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', '-output-directory', job_dir,
                     tex_path],
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                errors = result.stdout + result.stderr
                if result.returncode == 0 and os.path.exists(pdf_path):
                    logger.success(f"PDF compiled successfully on attempt {attempt}")
                    # Run second pass for references
                    subprocess.run(
                        ['pdflatex', '-interaction=nonstopmode', '-output-directory', job_dir,
                         tex_path],
                        capture_output=True,
                        text=True,
                        timeout=120,
                    )
                    return pdf_path, ''
                else:
                    logger.warning(f"pdflatex attempt {attempt} failed: {result.returncode}")
            except FileNotFoundError:
                logger.warning("pdflatex not installed — skipping PDF compilation")
                return None, 'pdflatex not installed on system'
            except subprocess.TimeoutExpired:
                logger.warning(f"pdflatex timed out on attempt {attempt}")
                errors = 'pdflatex timed out'
            except Exception as e:
                logger.error(f"pdflatex error: {e}")
                errors = str(e)

        logger.warning(f"PDF compilation failed after {max_retries} attempts")
        return None, errors

    def _generate_docx(
        self,
        sections: List[Dict],
        title: str,
        repo_name: str,
        job_dir: str,
    ) -> str | None:
        """Generate DOCX via a Node.js script using the docx package."""
        script_path = os.path.join(job_dir, '_generate_docx.cjs')
        docx_path = os.path.join(job_dir, 'research_paper.docx')

        # Serialize sections data as JSON for the script
        sections_json = json.dumps(sections)
        author = repo_name.split('/')[0] if '/' in repo_name else repo_name

        node_script = f"""
const path = require('path');
let docx;
try {{
  docx = require('docx');
}} catch(e) {{
  // try relative node_modules
  docx = require(path.join('{os.getcwd()}', 'node_modules', 'docx'));
}}
const {{ Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
         Header, Footer, PageNumber, NumberFormat }} = docx;

const sections = {sections_json};
const title = {json.dumps(title)};
const author = {json.dumps(author)};
const today = new Date().toLocaleDateString('en-US', {{year:'numeric',month:'long',day:'numeric'}});

const children = [];

// Cover page
children.push(new Paragraph({{
  children: [new TextRun({{ text: title, bold: true, size: 48, font: 'Times New Roman' }})],
  alignment: AlignmentType.CENTER,
  spacing: {{ before: 2000, after: 400 }},
}}));
children.push(new Paragraph({{
  children: [new TextRun({{ text: author, size: 28, font: 'Times New Roman' }})],
  alignment: AlignmentType.CENTER,
  spacing: {{ after: 200 }},
}}));
children.push(new Paragraph({{
  children: [new TextRun({{ text: today, size: 24, font: 'Times New Roman' }})],
  alignment: AlignmentType.CENTER,
  spacing: {{ after: 200 }},
}}));
children.push(new Paragraph({{
  children: [new TextRun({{ text: 'Generated by Dr. Document', italics: true, size: 20, font: 'Times New Roman', color: '666666' }})],
  alignment: AlignmentType.CENTER,
}}));

// Page break
children.push(new Paragraph({{ pageBreakBefore: true }}));

// Sections
for (const sec of sections) {{
  const isAbstract = sec.name.toLowerCase() === 'abstract';
  children.push(new Paragraph({{
    text: sec.name,
    heading: isAbstract ? HeadingLevel.HEADING_2 : HeadingLevel.HEADING_1,
    spacing: {{ before: 240, after: 120 }},
  }}));
  // Split content into paragraphs
  const paragraphs = sec.content.split(/\\n\\n+/);
  for (const para of paragraphs) {{
    const lines = para.split(/\\n/);
    const cleaned = lines.join(' ').trim();
    if (cleaned) {{
      children.push(new Paragraph({{
        children: [new TextRun({{ text: cleaned, font: 'Times New Roman', size: 24 }})],
        spacing: {{ after: 120 }},
      }}));
    }}
  }}
}}

const doc = new Document({{
  styles: {{
    default: {{
      document: {{ run: {{ font: 'Times New Roman', size: 24 }} }},
    }},
    paragraphStyles: [
      {{
        id: 'Heading1',
        run: {{ size: 32, bold: true, font: 'Times New Roman' }},
        paragraph: {{ spacing: {{ before: 240, after: 120 }}, outlineLevel: 0 }},
      }},
      {{
        id: 'Heading2',
        run: {{ size: 28, bold: true, font: 'Times New Roman' }},
        paragraph: {{ spacing: {{ before: 180, after: 90 }}, outlineLevel: 1 }},
      }},
    ],
  }},
  sections: [{{
    properties: {{
      page: {{
        size: {{ width: 11906, height: 16838 }},
        margin: {{ top: 1440, right: 1440, bottom: 1440, left: 1440 }},
      }},
    }},
    footers: {{
      default: new Footer({{
        children: [new Paragraph({{
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({{ children: [PageNumber.CURRENT], font: 'Times New Roman', size: 20 }}),
          ],
        }})],
      }}),
    }},
    children,
  }}],
}});

Packer.toBuffer(doc).then(buf => {{
  require('fs').writeFileSync({json.dumps(docx_path)}, buf);
  console.log('DOCX written to {docx_path}');
}}).catch(err => {{
  console.error('DOCX generation failed:', err);
  process.exit(1);
}});
"""

        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(node_script)

            result = subprocess.run(
                ['node', script_path],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode == 0 and os.path.exists(docx_path):
                logger.success("DOCX generated successfully")
                return docx_path
            else:
                logger.warning(f"DOCX generation failed: {result.stderr}")
                return None
        except FileNotFoundError:
            logger.warning("node not found — skipping DOCX generation")
            return None
        except Exception as e:
            logger.error(f"DOCX generation error: {e}")
            return None
        finally:
            # Clean up temp script
            if os.path.exists(script_path):
                os.remove(script_path)
