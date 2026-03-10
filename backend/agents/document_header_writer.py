"""Document Header Writer Agent - Generates the hero section at the top of the README"""
import re
from typing import Dict, Any, List

from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


# Emoji mapping for well-known heading names
_HEADING_EMOJIS: Dict[str, str] = {
    "abstract": "📄",
    "key highlights": "✨",
    "features": "✨",
    "dataset & training details": "📊",
    "dataset and training details": "📊",
    "methodology": "🔬",
    "results & visualizations": "📈",
    "results and visualizations": "📈",
    "architecture": "🏗️",
    "tech stack": "🛠",
    "dependencies & packages": "📦",
    "dependencies and packages": "📦",
    "prerequisites": "📋",
    "installation": "⚙️",
    "quick start": "🚀",
    "usage": "💡",
    "api endpoints": "🌐",
    "configuration": "⚙️",
    "environment variables": "🔧",
    "model setup & training": "🤖",
    "model setup and training": "🤖",
    "project structure": "📂",
    "documentation": "📚",
    "submodules": "🧩",
    "development": "🛠️",
    "deployment": "🚀",
    "security": "🛡",
    "contributing": "🤝",
    "code of conduct": "📜",
    "citation": "📝",
    "contact": "📬",
    "license": "📜",
    "acknowledgments": "🙏",
}


def _heading_to_anchor(heading: str) -> str:
    """
    Convert a heading string to a GitHub-compatible anchor fragment.

    GitHub's algorithm (simplified):
      1. Lowercase
      2. Remove all characters that are not letters, digits, spaces, or hyphens
      3. Replace spaces with hyphens
      4. Collapse consecutive hyphens to a single hyphen
      5. Strip leading/trailing hyphens
    """
    text = heading.lower()
    text = re.sub(r"[^\w\s-]", "", text)   # remove punctuation (keeps underscores)
    text = re.sub(r"\s+", "-", text)        # spaces → hyphens
    text = re.sub(r"-{2,}", "-", text)      # collapse multiple hyphens
    return text.strip("-")


class DocumentHeaderWriterAgent(BaseAgent):
    """
    Generates the hero section placed at the very top of the README, containing:

    - ``<h1>`` project title
    - Bold one-liner description
    - Italic tagline / elevator pitch
    - Full set of ``shields.io`` badges (repo health, activity, languages, misc)
    - ``## 🔗 Quick Links`` — anchor links to every selected heading
    - ``## 📑 Table of Contents`` — numbered anchor links to every selected heading
    """

    def __init__(self) -> None:
        super().__init__("Document Header Writer", settings.model_flash_lite)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate the README header section.

        Args:
            input_data: {
                'repo_name':        str,        # full name, e.g. "owner/project-name"
                'codebase_summary': str,        # content of codebase.txt
                'headings':         List[str],  # ordered list of selected headings
                'headings_txt':     str,        # raw content of headings.txt (newline-separated)
            }

        Returns:
            {
                'header_content': str,  # Markdown / HTML block ready to prepend to README
            }
        """
        repo_name: str = input_data.get("repo_name", "Unknown Repository")
        codebase_summary: str = input_data.get("codebase_summary", "")
        headings: List[str] = input_data.get("headings", [])
        # headings_txt is the authoritative newline-separated list from headings.txt;
        # if provided, parse it to guarantee we use the exact decided heading strings.
        headings_txt: str = input_data.get("headings_txt", "")
        if headings_txt:
            parsed = [
                re.sub(r'^[-•*\s\d.]+\s*', '', line).strip()
                for line in headings_txt.splitlines()
                if line.strip()
            ]
            if parsed:
                headings = parsed

        logger.workflow_step("Document Header Writing", f"Writing header for {repo_name}")

        # Short project name (strip owner prefix for the <h1> title)
        short_name = repo_name.split("/")[-1] if "/" in repo_name else repo_name

        # 1. LLM-generated description + tagline
        desc = self._generate_descriptions(repo_name, short_name, codebase_summary)

        # 2. Programmatic badge block
        badges_block = self._build_badges(repo_name)

        # 3. Navigation sections
        quick_links_block = self._build_quick_links(headings)
        toc_block = self._build_toc(headings)

        # 4. Assemble
        header_content = self._assemble_header(
            short_name=short_name,
            description=desc["description"],
            tagline=desc["tagline"],
            badges_block=badges_block,
            quick_links_block=quick_links_block,
            toc_block=toc_block,
        )

        logger.success(f"Document header written for {repo_name} ({len(header_content)} chars)")
        return {"header_content": header_content}

    # ------------------------------------------------------------------
    # LLM call: description + tagline
    # ------------------------------------------------------------------

    def _generate_descriptions(
        self, repo_name: str, short_name: str, codebase_summary: str
    ) -> Dict[str, str]:
        """Ask the LLM for a tight description and a one-sentence tagline."""
        prompt = (
            f'Based on the codebase summary below for the repository "{repo_name}", '
            f"write two things:\n\n"
            f"1. DESCRIPTION: A bold one-liner (max 15 words) capturing the core purpose. "
            f"This will be wrapped in <strong> tags.\n"
            f"2. TAGLINE: One italic sentence (max 25 words) giving a bit more detail. "
            f"This will be wrapped in <em> tags.\n\n"
            f"Codebase summary:\n{codebase_summary}\n\n"
            f"Return ONLY two lines in this exact format:\n"
            f"DESCRIPTION: <your description here>\n"
            f"TAGLINE: <your tagline here>\n"
            f"No other text."
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a technical writer specializing in concise, "
                    "impactful project descriptions."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        raw = self._call_llm(messages, max_tokens=200, temperature=0.5)

        # Sensible fallbacks in case the LLM does not follow the format
        description = f"{short_name} — a powerful open-source project"
        tagline = f"An automated, AI-powered solution built around {short_name}"

        for line in raw.strip().splitlines():
            upper = line.upper()
            if upper.startswith("DESCRIPTION:"):
                description = line.split(":", 1)[1].strip()
            elif upper.startswith("TAGLINE:"):
                tagline = line.split(":", 1)[1].strip()

        return {"description": description, "tagline": tagline}

    # ------------------------------------------------------------------
    # Badge block (programmatic — no LLM required)
    # ------------------------------------------------------------------

    def _build_badges(self, repo_name: str) -> str:
        """
        Build a ``<p>`` block of shields.io badges for the repository.

        Four groups are rendered, each separated by a blank line inside
        the ``<p>`` wrapper, matching the layout shown in the issue:
          • Repo health  (license, stars, forks, open issues, open PRs, contributions)
          • Activity     (last-commit, commit-activity, repo-size, code-size)
          • Languages    (top language, language count)
          • Misc         (docs, open source)
        """
        r = repo_name

        groups = [
            # Group 1 — repo health
            "\n".join([
                f'  <img src="https://img.shields.io/github/license/{r}?style=for-the-badge&amp;color=brightgreen">',
                f'  <img src="https://img.shields.io/github/stars/{r}?style=for-the-badge&amp;color=yellow">',
                f'  <img src="https://img.shields.io/github/forks/{r}?style=for-the-badge&amp;color=blue">',
                f'  <img src="https://img.shields.io/github/issues/{r}?style=for-the-badge&amp;color=red">',
                f'  <img src="https://img.shields.io/github/issues-pr/{r}?style=for-the-badge&amp;color=orange">',
                '  <img src="https://img.shields.io/badge/Contributions-Welcome-brightgreen?style=for-the-badge">',
            ]),
            # Group 2 — activity
            "\n".join([
                f'  <img src="https://img.shields.io/github/last-commit/{r}?style=for-the-badge&amp;color=purple">',
                f'  <img src="https://img.shields.io/github/commit-activity/m/{r}?style=for-the-badge&amp;color=teal">',
                f'  <img src="https://img.shields.io/github/repo-size/{r}?style=for-the-badge&amp;color=blueviolet">',
                f'  <img src="https://img.shields.io/github/languages/code-size/{r}?style=for-the-badge&amp;color=indigo">',
            ]),
            # Group 3 — languages
            "\n".join([
                f'  <img src="https://img.shields.io/github/languages/top/{r}?style=for-the-badge&amp;color=critical">',
                f'  <img src="https://img.shields.io/github/languages/count/{r}?style=for-the-badge&amp;color=success">',
            ]),
            # Group 4 — misc
            "\n".join([
                '  <img src="https://img.shields.io/badge/Docs-Available-green?style=for-the-badge&amp;logo=readthedocs&amp;logoColor=white">',
                '  <img src="https://img.shields.io/badge/Open%20Source-%E2%9D%A4-red?style=for-the-badge">',
            ]),
        ]

        body = "\n\n".join(groups)
        return f"<p>\n\n{body}\n\n</p>"

    # ------------------------------------------------------------------
    # Quick Links section
    # ------------------------------------------------------------------

    def _build_quick_links(self, headings: List[str]) -> str:
        """Build the ``## 🔗 Quick Links`` section from the selected headings."""
        if not headings:
            return ""

        lines = ["## 🔗 Quick Links\n"]
        for heading in headings:
            emoji = _HEADING_EMOJIS.get(heading.lower(), "📌")
            anchor = _heading_to_anchor(heading)
            lines.append(f'- <a href="#{anchor}">{emoji} {heading}</a>')

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Table of Contents
    # ------------------------------------------------------------------

    def _build_toc(self, headings: List[str]) -> str:
        """Build the ``## 📑 Table of Contents`` section from the selected headings."""
        if not headings:
            return ""

        lines = ["## 📑 Table of Contents\n"]
        for i, heading in enumerate(headings, 1):
            anchor = _heading_to_anchor(heading)
            lines.append(f'{i}. <a href="#{anchor}">{heading}</a>')

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Assembly
    # ------------------------------------------------------------------

    def _assemble_header(
        self,
        short_name: str,
        description: str,
        tagline: str,
        badges_block: str,
        quick_links_block: str,
        toc_block: str,
    ) -> str:
        """Combine all pieces into the final header string."""
        parts: List[str] = [
            f"<h1>{short_name}</h1>\n",
            f"<p>\n  <strong>{description}</strong>\n</p>\n",
            f"<p>\n  <em>{tagline}</em>\n</p>\n",
            f"{badges_block}\n",
            "\n---\n",
        ]

        if quick_links_block:
            parts.append(f"\n{quick_links_block}\n")
            parts.append("\n---\n")

        if toc_block:
            parts.append(f"\n{toc_block}\n")
            parts.append("\n---\n")

        return "".join(parts)
