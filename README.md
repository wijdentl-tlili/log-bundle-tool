# 🕵️ Log Bundle Forensic Tool

A command-line toolkit for collecting, analyzing, and reporting on log files — designed for incident response and security forensics workflows.

---

## Features

- **Log Collection** — Recursively gather log files by extension from any directory
- **Metadata Extraction** — Capture file size, SHA256 hash, timestamps, permissions, and owner
- **IOC Scanning** — Detect indicators of compromise (authentication attacks, reverse shells, web exploits, recon tools, and more)
- **Sensitive Data Detection** — Identify emails, IP addresses, API keys, and passwords via regex patterns
- **Entropy Analysis** — Flag high-entropy strings that may indicate base64-encoded payloads or obfuscated content
- **Automatic Redaction** — Write sanitized copies of log files with sensitive data replaced
- **Dual Reporting** — Generate both a structured JSON report and a styled HTML report
- **ZIP Bundling** — Package all collected files and reports into a timestamped archive

---


## Installation

```bash
git clone https://github.com/wijdentl-tlili/Log-Bundle-Tool.git
cd log-bundle-tool
pip install -r requirements.txt
```

> No external dependencies beyond the Python standard library are required.

---

## Usage

### Collect & Analyze Logs

```bash
python cli.py collect --source "path for your logs"
```

### Options

| Flag | Description | Default |
|---|---|---|
| `--source` | Directory containing log files *(required)* | — |
| `--extensions` | File extensions to collect | `.log .txt` |
| `--no-recursive` | Disable recursive directory scanning | Off |
| `--verbose` | Enable debug-level logging | Off |

### Examples

```bash
# Collect only .log files, non-recursively
python cli.py collect --source test_logs --extensions .log --no-recursive

# Collect multiple extensions with verbose output
python cli.py collect --source test_logs --extensions .log .txt .out --verbose
```

---

## Output

Each run creates a timestamped bundle under `output/`:

```
output/
├── bundle_20240101_120000/
│   ├── <original log files>
│   ├── redacted_<filename>    # Sanitized copies
│   ├── forensic_report.json   # Structured findings
│   └── forensic_report.html   # Visual HTML report
└── log_bundle_20240101_120000.zip
```

---

## IOC Patterns Detected

The scanner checks for the following categories of indicators:

| Category | Examples |
|---|---|
| Authentication attacks | `failed login`, `invalid user`, `unauthorized` |
| Command execution | `powershell`, `cmd.exe`, `wget`, `curl`, `bash -i` |
| Malware / hacking tools | `mimikatz`, `metasploit`, `nmap` |
| Web attacks | `union select`, `../`, `/etc/passwd`, `wp-admin` |
| Suspicious encoding | `base64`, `-enc` |
| Reverse shell indicators | `socket`, `connect back` |
| Recon activity | `masscan`, `nikto` |

---

## Sensitive Data Redaction

The following patterns are detected and replaced with `[REDACTED]` in output copies:

- Email addresses
- IP addresses
- API keys / tokens / secrets
- Passwords

Original files are **never modified** — redacted copies are written separately.

---
