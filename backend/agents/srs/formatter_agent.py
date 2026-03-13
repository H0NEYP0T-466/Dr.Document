"""SRS Formatter Agent - Generates IEEE 830 SRS as LaTeX/PDF/DOCX"""
import json
import os
import subprocess
import tempfile
from typing import Dict, Any, List
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class SRSFormatterAgent(BaseAgent):
    """
    Assembles SRS sections into formatted documents.
    Produces: .tex, .pdf, .docx
    Includes revision history table in DOCX title page.
    """

    def __init__(self):
        super().__init__("SRS Formatter Agent", settings.model_flash_lite)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format the SRS document.

        Args:
            input_data: {
                'sections': List[{name, content}],
                'selected_title': str,
                'repo_name': str,
                'repo_url': str,
                'job_dir': str,
            }

        Returns:
            {
                'tex_path': str,
                'pdf_path': str | None,
                'docx_path': str | None,
                'latex_errors': str,
            }
        """
        sections = input_data.get('sections', [])
        selected_title = input_data.get('selected_title', 'Software Requirements Specification')
        repo_name = input_data.get('repo_name', 'Unknown')
        repo_url = input_data.get('repo_url', '')
        job_dir = input_data.get('job_dir', tempfile.gettempdir())

        logger.workflow_step("SRS Formatter", "Assembling SRS document")

        # Generate LaTeX
        tex_content = self._generate_latex(sections, selected_title, repo_name)
        tex_path = os.path.join(job_dir, 'srs.tex')
        with open(tex_path, 'w', encoding='utf-8') as f:
            f.write(tex_content)

        # Compile PDF
        pdf_path, latex_errors = self._compile_pdf(tex_path, job_dir)

        errors_log = os.path.join(job_dir, 'formatter_latex_errors.log')
        with open(errors_log, 'w', encoding='utf-8') as f:
            f.write(latex_errors or 'No errors')

        # Generate DOCX
        docx_path = self._generate_docx(sections, selected_title, repo_name, job_dir)

        return {
            'tex_path': tex_path,
            'pdf_path': pdf_path,
            'docx_path': docx_path,
            'latex_errors': latex_errors,
        }

    def _latex_escape(self, text: str) -> str:
        """Escape special LaTeX characters."""
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

    def _generate_latex(self, sections: List[Dict], title: str, repo_name: str) -> str:
        """Generate IEEE-style article LaTeX for SRS."""
        safe_title = self._latex_escape(title)
        author = repo_name.split('/')[0] if '/' in repo_name else repo_name

        body_parts = []
        for sec in sections:
            if sec['name'].lower() in ('title page', 'table of contents'):
                continue
            sec_title = self._latex_escape(sec['name'])
            # Bold FR/NFR IDs in content
            content = sec['content']
            sec_body = self._latex_escape(content)
            body_parts.append(f'\\section{{{sec_title}}}\n{sec_body}\n')

        body = '\n'.join(body_parts)

        tex = f"""\\documentclass[12pt,a4paper]{{article}}
\\usepackage{{geometry}}
\\geometry{{margin=1in}}
\\usepackage{{hyperref}}
\\usepackage{{booktabs}}
\\usepackage{{array}}
\\usepackage{{longtable}}
\\usepackage{{enumitem}}

\\title{{{safe_title}}}
\\author{{{self._latex_escape(author)}}}
\\date{{\\today}}

\\begin{{document}}
\\maketitle
\\thispagestyle{{empty}}

\\newpage
\\tableofcontents

\\newpage
{body}

\\end{{document}}
"""
        return tex

    def _compile_pdf(self, tex_path: str, job_dir: str) -> tuple:
        """Compile PDF with pdflatex."""
        pdf_path = tex_path.replace('.tex', '.pdf')
        errors = ''

        for attempt in range(1, 4):
            try:
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', '-output-directory', job_dir, tex_path],
                    capture_output=True, text=True, timeout=120,
                )
                errors = result.stdout + result.stderr
                if result.returncode == 0 and os.path.exists(pdf_path):
                    logger.success(f"SRS PDF compiled on attempt {attempt}")
                    subprocess.run(
                        ['pdflatex', '-interaction=nonstopmode', '-output-directory', job_dir, tex_path],
                        capture_output=True, text=True, timeout=120,
                    )
                    return pdf_path, ''
                else:
                    logger.warning(f"pdflatex attempt {attempt} failed for SRS")
            except FileNotFoundError:
                return None, 'pdflatex not installed'
            except subprocess.TimeoutExpired:
                errors = 'pdflatex timed out'
            except Exception as e:
                errors = str(e)

        return None, errors

    def _generate_docx(
        self,
        sections: List[Dict],
        title: str,
        repo_name: str,
        job_dir: str,
    ) -> str | None:
        """Generate SRS DOCX with revision history table."""
        script_path = os.path.join(job_dir, '_generate_srs_docx.cjs')
        docx_path = os.path.join(job_dir, 'srs.docx')

        sections_json = json.dumps(sections)
        author = repo_name.split('/')[0] if '/' in repo_name else repo_name

        node_script = f"""
const path = require('path');
let docx;
try {{
  docx = require('docx');
}} catch(e) {{
  docx = require(path.join('{os.getcwd()}', 'node_modules', 'docx'));
}}
const {{ Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
         HeadingLevel, AlignmentType, Footer, PageNumber,
         WidthType, BorderStyle, ShadingType }} = docx;

const sections = {sections_json};
const title = {json.dumps(title)};
const author = {json.dumps(author)};
const today = new Date().toLocaleDateString('en-US', {{year:'numeric',month:'long',day:'numeric'}});

const children = [];

// Cover page
children.push(new Paragraph({{
  children: [new TextRun({{ text: title, bold: true, size: 48, font: 'Times New Roman' }})],
  alignment: AlignmentType.CENTER,
  spacing: {{ before: 1440, after: 400 }},
}}));
children.push(new Paragraph({{
  children: [new TextRun({{ text: author, size: 28, font: 'Times New Roman' }})],
  alignment: AlignmentType.CENTER,
  spacing: {{ after: 200 }},
}}));
children.push(new Paragraph({{
  children: [new TextRun({{ text: today, size: 24, font: 'Times New Roman' }})],
  alignment: AlignmentType.CENTER,
  spacing: {{ after: 400 }},
}}));
children.push(new Paragraph({{
  children: [new TextRun({{ text: 'Generated by Dr. Document', italics: true, size: 20, font: 'Times New Roman', color: '666666' }})],
  alignment: AlignmentType.CENTER,
  spacing: {{ after: 400 }},
}}));

// Revision history table
children.push(new Paragraph({{
  children: [new TextRun({{ text: 'Revision History', bold: true, size: 28, font: 'Times New Roman' }})],
  spacing: {{ before: 200, after: 120 }},
}}));

const headerRow = new TableRow({{
  children: [
    new TableCell({{ children: [new Paragraph({{ children: [new TextRun({{ text: 'Version', bold: true, font: 'Times New Roman', size: 20 }})]}})], width: {{ size: 1500, type: WidthType.DXA }}, shading: {{ type: ShadingType.CLEAR, fill: 'DDDDDD' }} }}),
    new TableCell({{ children: [new Paragraph({{ children: [new TextRun({{ text: 'Date', bold: true, font: 'Times New Roman', size: 20 }})]}})], width: {{ size: 2000, type: WidthType.DXA }}, shading: {{ type: ShadingType.CLEAR, fill: 'DDDDDD' }} }}),
    new TableCell({{ children: [new Paragraph({{ children: [new TextRun({{ text: 'Author', bold: true, font: 'Times New Roman', size: 20 }})]}})], width: {{ size: 2000, type: WidthType.DXA }}, shading: {{ type: ShadingType.CLEAR, fill: 'DDDDDD' }} }}),
    new TableCell({{ children: [new Paragraph({{ children: [new TextRun({{ text: 'Description', bold: true, font: 'Times New Roman', size: 20 }})]}})], width: {{ size: 3906, type: WidthType.DXA }}, shading: {{ type: ShadingType.CLEAR, fill: 'DDDDDD' }} }}),
  ],
}});
const dataRow = new TableRow({{
  children: [
    new TableCell({{ children: [new Paragraph({{ children: [new TextRun({{ text: '1.0', font: 'Times New Roman', size: 20 }})]}})], width: {{ size: 1500, type: WidthType.DXA }} }}),
    new TableCell({{ children: [new Paragraph({{ children: [new TextRun({{ text: today, font: 'Times New Roman', size: 20 }})]}})], width: {{ size: 2000, type: WidthType.DXA }} }}),
    new TableCell({{ children: [new Paragraph({{ children: [new TextRun({{ text: author, font: 'Times New Roman', size: 20 }})]}})], width: {{ size: 2000, type: WidthType.DXA }} }}),
    new TableCell({{ children: [new Paragraph({{ children: [new TextRun({{ text: 'Initial draft — auto-generated by Dr. Document', font: 'Times New Roman', size: 20 }})]}})], width: {{ size: 3906, type: WidthType.DXA }} }}),
  ],
}});
children.push(new Table({{ rows: [headerRow, dataRow], columnWidths: [1500, 2000, 2000, 3906] }}));
children.push(new Paragraph({{ pageBreakBefore: true }}));

// Sections
for (const sec of sections) {{
  const nameLower = sec.name.toLowerCase();
  if (['title page', 'table of contents'].includes(nameLower)) continue;
  const isSubsection = /^[\\d]+\\.[\\d]+/.test(sec.name) || sec.name.startsWith('Appendix');
  children.push(new Paragraph({{
    text: sec.name,
    heading: isSubsection ? HeadingLevel.HEADING_2 : HeadingLevel.HEADING_1,
    spacing: {{ before: 240, after: 120 }},
  }}));
  const paragraphs = sec.content.split(/\\n\\n+/);
  for (const para of paragraphs) {{
    const cleaned = para.split(/\\n/).join(' ').trim();
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
    default: {{ document: {{ run: {{ font: 'Times New Roman', size: 24 }} }} }},
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
          children: [new TextRun({{ children: [PageNumber.CURRENT], font: 'Times New Roman', size: 20 }})],
        }})],
      }}),
    }},
    children,
  }}],
}});

Packer.toBuffer(doc).then(buf => {{
  require('fs').writeFileSync({json.dumps(docx_path)}, buf);
  console.log('SRS DOCX written');
}}).catch(err => {{
  console.error('SRS DOCX failed:', err);
  process.exit(1);
}});
"""

        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(node_script)

            result = subprocess.run(
                ['node', script_path],
                capture_output=True, text=True, timeout=60,
            )
            if result.returncode == 0 and os.path.exists(docx_path):
                logger.success("SRS DOCX generated")
                return docx_path
            else:
                logger.warning(f"SRS DOCX failed: {result.stderr}")
                return None
        except FileNotFoundError:
            logger.warning("node not found")
            return None
        except Exception as e:
            logger.error(f"SRS DOCX error: {e}")
            return None
        finally:
            if os.path.exists(script_path):
                os.remove(script_path)
