```markdown
# Security Policy

## Supported Versions

The following versions of Dr. Document are currently receiving security updates:

| Version | Supported          | Notes |
|---------|--------------------|-------|
| 1.0.x   | ✅ Yes             | Current stable release with active maintenance |
| < 1.0   | ❌ No              | End-of-life; no security patches provided |

> **Note**: Only the latest patch version of the `1.0.x` series receives security updates. Older minor versions (e.g., `1.0.0`, `1.0.1`) are not supported.

## Reporting a Vulnerability

We take the security of Dr. Document seriously. If you discover a security vulnerability, please **do not disclose it publicly** until we have had time to address it.

### Preferred Reporting Method

Use **GitHub's private vulnerability reporting** feature:

1. Go to the repository: [https://github.com/H0NEYP0T-466/Dr.Document](https://github.com/H0NEYP0T-466/Dr.Document)
2. Click on **"Security"** in the repository header
3. Select **"Report a vulnerability"**
4. Fill out the form with as much detail as possible (steps to reproduce, affected versions, potential impact)

This ensures your report is handled confidentially and directly by the maintainers.

### What to Include in Your Report

- Description of the vulnerability
- Steps to reproduce
- Affected versions
- Potential impact
- Suggested fix (if known)
- Any proof-of-concept or exploit code

We aim to acknowledge receipt of your report within **48 hours** and provide a preliminary assessment within **7 days**.

## Disclosure Policy

We follow a **responsible disclosure** model:

- Upon receiving a valid vulnerability report, we will:
  - Confirm receipt and assess severity
  - Develop and test a fix
  - Coordinate public disclosure with the reporter
- We will **not** disclose the vulnerability publicly until:
  - A fix is available, **or**
  - 90 days have passed since initial report (whichever comes first)
- If the reporter does not respond within 30 days of initial contact, we may proceed with disclosure

We appreciate your patience and cooperation in helping us keep Dr. Document secure.

## Security Response Process

After a vulnerability is reported:

1. **Acknowledgment (within 48 hours)**  
   You’ll receive confirmation that we’ve received your report.

2. **Assessment & Triage (within 7 days)**  
   We evaluate the severity and scope of the issue.

3. **Fix Development**  
   A patch is developed, tested, and reviewed.

4. **Coordination (if needed)**  
   We work with you to verify the fix and prepare disclosure.

5. **Public Disclosure**  
   Once resolved, we’ll:
   - Release a security advisory
   - Update the changelog
   - Credit the reporter (if desired)

6. **Post-Mortem & Prevention**  
   We review the issue to improve future security practices.

## Out of Scope

The following are **not considered security vulnerabilities** and will not be addressed:

- False positives or non-critical bugs
- Issues arising from:
  - Misconfigured deployments
  - Unauthorized access to user data (e.g., API keys, secrets)
  - Third-party services (e.g., GitHub API, OpenAI)
- Social engineering attacks
- Physical security concerns
- Denial-of-service via legitimate usage patterns
- Vulnerabilities requiring elevated privileges or system access not granted by the application

## Security Best Practices

To use Dr. Document securely:

- **Never commit API keys or secrets** to your repository
- Use environment variables for configuration (as defined in `backend/config.py`)
- Keep dependencies updated by regularly pulling the latest changes
- Run Dr. Document in a secure, isolated environment (e.g., containerized or virtualized)
- Review generated files before merging into your main branch
- Enable GitHub’s secret scanning and Dependabot alerts in your repositories

---

Thank you for helping make Dr. Document safer for everyone! 🔐
```