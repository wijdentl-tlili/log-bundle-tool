IOC_PATTERNS = [

    # Authentication attacks
    "failed login",
    "authentication failure",
    "invalid user",
    "unauthorized",

    # Command execution
    "powershell",
    "cmd.exe",
    "wget",
    "curl",
    "nc.exe",
    "bash -i",

    # Malware / hacking tools
    "mimikatz",
    "metasploit",
    "nmap",

    # Web attacks
    "union select",
    "../",
    "/etc/passwd",
    "wp-admin",
    "phpmyadmin",

    # Suspicious encoding
    "base64",
    "-enc",

    # Reverse shell indicators
    "socket",
    "connect back",

    # Recon activity
    "masscan",
    "nikto"
]

def scan_file(file_path):

    findings = []

    with open(file_path, "r", errors="ignore") as f:

        lines = f.readlines()

    for line_number, line in enumerate(lines, start=1):

        for pattern in IOC_PATTERNS:

            if pattern.lower() in line.lower():

                findings.append({
                    "line": line_number,
                    "pattern": pattern,
                    "content": line.strip()
                })

    return findings