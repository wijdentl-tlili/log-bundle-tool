from datetime import datetime
from collections import defaultdict


def generate_html_report(
    metadata_results,
    ioc_results,
    sensitive_results,
    entropy_results,
    output_file="report.html",
    css_file="../../reporting/style.css"
):

    total_files = len(metadata_results)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Forensic Report</title>
        <link rel="stylesheet" href="{css_file}">
    </head>

    <body>

        <div class="container">

        <h1>🕵️ Log Bundle Forensic Report</h1>

        <div class="card summary">
            <p><strong>Generated:</strong> {datetime.now().isoformat()}</p>
            <p><strong>Total Files:</strong> {total_files}</p>
        </div>

        <!-- ================= METADATA ================= -->
        <div class="card">
            <h2>📦 Metadata</h2>

            <table>
                <tr>
                    <th>File</th>
                    <th>Size</th>
                    <th>SHA256</th>
                    <th>Modified</th>
                    <th>Permissions</th>
                </tr>
    """

    for m in metadata_results:
        html += f"""
        <tr>
            <td>{m['file_name']}</td>
            <td>{m['size_bytes']} bytes</td>
            <td class="mono">{m['sha256']}</td>
            <td>{m['modified_time']}</td>
            <td>{m['permissions']}</td>
        </tr>
        """

    html += "</table></div>"

    # ================= ENTROPY =================
    html += """
    <div class="card">
        <h2>Entropy Analysis</h2>
    """

    if entropy_results:

        grouped = defaultdict(lambda: defaultdict(list))

        for r in entropy_results:
            file = r["file"]
            for f in r["findings"]:
                grouped[file][f["risk"]].append(f)

        for file, risks in grouped.items():

            html += f"<h3>{file}</h3>"

            html += """
            <table>
                <tr>
                    <th>Risk</th>
                    <th>Count</th>
                    <th>Details</th>
                </tr>
            """

            for risk, items in risks.items():

                html += f"""
                <tr>
                    <td class="risk {risk.lower()}">{risk}</td>
                    <td>{len(items)}</td>
                    <td>
                        <details>
                            <summary>View Details</summary>
                """

                for item in items:
                    html += f"""
                    <div class="detail-box">
                        <p><strong>Entropy:</strong> {item['entropy']}</p>
                        <p class="mono">{item['value']}</p>
                    </div>
                    <hr>
                    """

                html += """
                        </details>
                    </td>
                </tr>
                """

            html += "</table>"

    else:
        html += "<p>No entropy anomalies detected.</p>"

    html += "</div>"

    # ================= IOC =================
    html += """
    <div class="card">
        <h2>IOC Findings</h2>
    """

    if ioc_results:

        grouped = defaultdict(lambda: defaultdict(list))

        for r in ioc_results:
            file = r["file"]
            for f in r["findings"]:
                grouped[file][f["pattern"]].append(f)

        for file, patterns in grouped.items():

            html += f"<h3>{file}</h3>"

            html += """
            <table>
                <tr>
                    <th>Type</th>
                    <th>Count</th>
                    <th>Details</th>
                </tr>
            """

            for pattern, items in patterns.items():

                html += f"""
                <tr>
                    <td class="risk high">{pattern}</td>
                    <td>{len(items)}</td>
                    <td>
                        <details>
                            <summary>View Details</summary>
                """

                for item in items:
                    html += f"""
                    <div class="detail-box">
                        <p>Line: {item['line']}</p>
                        <p class="mono">{item['content']}</p>
                    </div>
                    <hr>
                    """

                html += """
                        </details>
                    </td>
                </tr>
                """

            html += "</table>"

    else:
        html += "<p>No IOC findings detected.</p>"

    html += "</div>"

    # ================= SENSITIVE =================
    html += """
    <div class="card">
        <h2>Sensitive Data</h2>
    """

    if sensitive_results:

        grouped = defaultdict(lambda: defaultdict(list))

        for r in sensitive_results:
            file = r["file"]
            for f in r["findings"]:
                grouped[file][f["type"]].append(f)

        for file, types in grouped.items():

            html += f"<h3>{file}</h3>"

            html += """
            <table>
                <tr>
                    <th>Type</th>
                    <th>Count</th>
                    <th>Details</th>
                </tr>
            """

            for t, items in types.items():

                html += f"""
                <tr>
                    <td class="risk medium">{t}</td>
                    <td>{len(items)}</td>
                    <td>
                        <details>
                            <summary>View Details</summary>
                """

                for item in items:
                    html += f"""
                    <div class="detail-box">
                        <p class="mono">{item['value']}</p>
                    </div>
                    <hr>
                    """

                html += """
                        </details>
                    </td>
                </tr>
                """

            html += "</table>"

    else:
        html += "<p>No sensitive data detected.</p>"

    html += """
        </div>
        </div>
    </body>
    </html>
    """

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)