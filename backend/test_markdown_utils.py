"""Unit tests for backend.agents.markdown_utils

Run with:
    cd /path/to/Dr.Document
    python -m pytest backend/test_markdown_utils.py -v
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from backend.agents.markdown_utils import latex_escape, inline_markdown_to_latex, markdown_to_latex


# ---------------------------------------------------------------------------
# latex_escape — ASCII special characters (existing behaviour)
# ---------------------------------------------------------------------------

class TestLatexEscapeAscii:
    def test_backslash(self):
        assert latex_escape('a\\b') == r'a\textbackslash{}b'

    def test_braces(self):
        assert latex_escape('{x}') == r'\{x\}'

    def test_ampersand(self):
        assert latex_escape('a & b') == r'a \& b'

    def test_percent(self):
        assert latex_escape('50%') == r'50\%'

    def test_dollar(self):
        assert latex_escape('$100') == r'\$100'

    def test_hash(self):
        assert latex_escape('#1') == r'\#1'

    def test_underscore(self):
        assert latex_escape('foo_bar') == r'foo\_bar'

    def test_caret(self):
        assert latex_escape('x^2') == r'x\textasciicircum{}2'

    def test_tilde(self):
        assert latex_escape('foo~bar') == r'foo\textasciitilde{}bar'

    def test_less_than(self):
        assert latex_escape('a<b') == r'a\textless{}b'

    def test_greater_than(self):
        assert latex_escape('a>b') == r'a\textgreater{}b'

    def test_plain_text_unchanged(self):
        assert latex_escape('Hello, World!') == 'Hello, World!'


# ---------------------------------------------------------------------------
# latex_escape — Unicode mathematical symbols
# ---------------------------------------------------------------------------

class TestLatexEscapeUnicode:
    """Verify that Unicode chars that pdflatex cannot process are converted
    to their LaTeX equivalents."""

    def test_less_than_or_equal(self):
        assert latex_escape('x ≤ 10') == r'x $\leq$ 10'

    def test_greater_than_or_equal(self):
        assert latex_escape('x ≥ 0') == r'x $\geq$ 0'

    def test_not_equal(self):
        assert latex_escape('a ≠ b') == r'a $\neq$ b'

    def test_approx(self):
        assert latex_escape('π ≈ 3.14') == r'$\pi$ $\approx$ 3.14'

    def test_arrow_right(self):
        assert latex_escape('A → B') == r'A $\rightarrow$ B'

    def test_arrow_double(self):
        assert latex_escape('A ⇒ B') == r'A $\Rightarrow$ B'

    def test_times(self):
        assert latex_escape('2 × 3') == r'2 $\times$ 3'

    def test_divide(self):
        assert latex_escape('6 ÷ 2') == r'6 $\div$ 2'

    def test_plus_minus(self):
        assert latex_escape('±1') == r'$\pm$1'

    def test_infinity(self):
        assert latex_escape('∞') == r'$\infty$'

    def test_set_membership(self):
        assert latex_escape('x ∈ S') == r'x $\in$ S'

    def test_subset(self):
        assert latex_escape('A ⊆ B') == r'A $\subseteq$ B'

    def test_intersection(self):
        assert latex_escape('A ∩ B') == r'A $\cap$ B'

    def test_union(self):
        assert latex_escape('A ∪ B') == r'A $\cup$ B'

    def test_for_all(self):
        assert latex_escape('∀x') == r'$\forall$x'

    def test_there_exists(self):
        assert latex_escape('∃x') == r'$\exists$x'

    def test_greek_alpha(self):
        assert latex_escape('α') == r'$\alpha$'

    def test_greek_beta(self):
        assert latex_escape('β') == r'$\beta$'

    def test_greek_pi(self):
        assert latex_escape('π') == r'$\pi$'

    def test_greek_omega(self):
        assert latex_escape('ω') == r'$\omega$'

    def test_greek_uppercase_sigma(self):
        assert latex_escape('Σ') == r'$\Sigma$'

    def test_greek_uppercase_delta(self):
        assert latex_escape('Δ') == r'$\Delta$'

    def test_en_dash(self):
        assert latex_escape('2013\u2013year') == '2013--year'

    def test_em_dash(self):
        assert latex_escape('now\u2014then') == 'now---then'

    def test_left_double_quote(self):
        assert latex_escape('\u201chello\u201d') == "``hello''"

    def test_ellipsis(self):
        assert latex_escape('wait…') == r'wait\ldots{}'

    def test_bullet(self):
        assert latex_escape('• item') == r'\textbullet{} item'

    def test_degree(self):
        assert latex_escape('90°') == r'90$^\circ$'

    def test_superscript_2(self):
        assert latex_escape('x²') == r'x$^2$'

    def test_copyright(self):
        assert latex_escape('© 2024') == r'\textcopyright{} 2024'

    def test_trademark(self):
        assert latex_escape('Foo™') == r'Foo\texttrademark{}'

    def test_checkmark(self):
        assert latex_escape('✓') == r'$\checkmark$'

    def test_mixed_unicode_and_ascii(self):
        """A sentence with both ASCII specials and Unicode math symbols."""
        result = latex_escape('f(x) ≤ g(x) & h(x) ≥ 0')
        assert r'$\leq$' in result
        assert r'$\geq$' in result
        assert r'\&' in result

    def test_no_double_escaping(self):
        """Unicode replacements introduce braces and backslashes that must not be re-escaped."""
        result = latex_escape('≤')
        assert result == r'$\leq$'
        # The braces from $\leq$ should NOT be further escaped
        assert r'\{' not in result
        assert r'\}' not in result


# ---------------------------------------------------------------------------
# inline_markdown_to_latex — Unicode inside markdown spans
# ---------------------------------------------------------------------------

class TestInlineMarkdownToLatexUnicode:
    def test_bold_with_unicode(self):
        result = inline_markdown_to_latex('**x ≤ 10**')
        assert r'$\leq$' in result
        assert r'\textbf{' in result

    def test_italic_with_unicode(self):
        result = inline_markdown_to_latex('*α value*')
        assert r'$\alpha$' in result
        assert r'\textit{' in result

    def test_plain_text_with_unicode(self):
        result = inline_markdown_to_latex('value ≥ 0')
        assert r'$\geq$' in result


# ---------------------------------------------------------------------------
# markdown_to_latex — Unicode in document sections
# ---------------------------------------------------------------------------

class TestMarkdownToLatexUnicode:
    def test_unicode_in_heading(self):
        result = markdown_to_latex('## Condition: x ≤ 10')
        assert r'$\leq$' in result

    def test_unicode_in_list_item(self):
        result = markdown_to_latex('- value ≥ 0')
        assert r'$\geq$' in result

    def test_unicode_in_paragraph(self):
        result = markdown_to_latex('The angle θ is measured in degrees °.')
        assert r'$\theta$' in result
        assert r'$^\circ$' in result


# ---------------------------------------------------------------------------
# Control-character stripping — guard against null bytes from LLM output
# ---------------------------------------------------------------------------

class TestControlCharStripping:
    """Ensure null bytes and other pdflatex-invalid control characters are
    stripped at every processing layer so they never reach the .tex file."""

    # -- latex_escape --

    def test_markdown_to_latex_strips_null_bytes_end_to_end(self):
        # latex_escape intentionally does NOT strip null bytes — that is
        # handled upstream by inline_markdown_to_latex / markdown_to_latex /
        # sanitize_content so that the \x00 placeholder delimiters used
        # internally by inline_markdown_to_latex are never accidentally removed.
        # Direct callers (headings, title, etc.) receive pre-cleaned text.
        # Verify that the stripping at markdown_to_latex level works end-to-end:
        result = markdown_to_latex("foo\x00bar")
        assert '\x00' not in result
        assert "foobar" in result

    def test_markdown_to_latex_strips_control_chars(self):
        # Control char stripping is handled at the markdown_to_latex /
        # inline_markdown_to_latex level, not inside latex_escape itself.
        controls = "\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0e\x1f\x7f"
        result = markdown_to_latex(f"a{controls}b")
        for ch in controls:
            assert ch not in result
        assert "ab" in result

    def test_latex_escape_preserves_newline_tab(self):
        result = latex_escape("line\nnext\ttab")
        assert "line" in result
        assert "next" in result

    # -- inline_markdown_to_latex --

    def test_inline_markdown_strips_null_bytes_in_plain_text(self):
        result = inline_markdown_to_latex("Error\x00 notifications")
        assert '\x00' not in result
        assert "Error" in result
        assert "notifications" in result

    def test_inline_markdown_strips_null_bytes_in_bold(self):
        result = inline_markdown_to_latex("**Error\x00 notifications**")
        assert '\x00' not in result
        assert r'\textbf{' in result

    def test_inline_markdown_strips_null_bytes_in_code(self):
        result = inline_markdown_to_latex("`code\x00value`")
        assert '\x00' not in result
        assert r'\texttt{' in result

    def test_inline_markdown_safety_net_for_leaked_placeholder(self):
        """Even if a \x00SPAN\x00 placeholder somehow is not restored,
        the safety net should remove the null bytes."""
        # Force a scenario where the placeholder text itself has a null byte
        # by passing a pre-formed placeholder-lookalike as plain text.
        # inline_markdown_to_latex strips leading \x00 from the input first,
        # so the placeholder would be incomplete and the safety net fires.
        text = "\x00SPAN0\x00: Error notifications with detailed messages"
        result = inline_markdown_to_latex(text)
        assert '\x00' not in result

    # -- markdown_to_latex --

    def test_markdown_to_latex_strips_null_bytes_in_paragraph(self):
        result = markdown_to_latex("Error\x00 notifications with detailed messages")
        assert '\x00' not in result
        assert "Error" in result

    def test_markdown_to_latex_strips_null_bytes_in_heading(self):
        result = markdown_to_latex("## Error\x00 notifications")
        assert '\x00' not in result

    def test_markdown_to_latex_strips_null_bytes_in_list(self):
        result = markdown_to_latex("- Error\x00 notifications with detailed messages")
        assert '\x00' not in result
        assert "Error" in result
