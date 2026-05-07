from datetime import datetime


def generate_html_report(
    metadata_results,
    ioc_results,
    sensitive_results,
    output_file
):

    total_files = len(metadata_results)

    html = f"""
    <!DOCTYPE html>
    <html>

    <head>

        <title>Forensic Report</title>

        <style>

            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                padding: 20px;
            }}

            h1 {{
                color: #333;
            }}

            .card {{
                background: white;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}

            th, td {{
                border: 1px solid #ddd;
                padding: 10px;
                text-align: left;
            }}

            th {{
                background-color: #222;
                color: white;
            }}

            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}

            .hash {{
                font-family: monospace;
                font-size: 12px;
                word-break: break-all;
            }}

            .danger {{
                color: red;
                font-weight: bold;
            }}

        </style>

    </head>

    <body>

        <h1>Log Bundle Forensic Report</h1>

        <div class="card">

            <h2>Collection Summary</h2>

            <p>
                <strong>Generated:</strong>
                {datetime.now().isoformat()}
            </p>

            <p>
                <strong>Total Files:</strong>
                {total_files}
            </p>

        </div>

        <div class="card">

            <h2>Collected Files Metadata</h2>

            <table>

                <tr>
                    <th>File Name</th>
                    <th>Size</th>
                    <th>SHA256</th>
                    <th>Modified</th>
                    <th>Permissions</th>
                </tr>
    """

    # Metadata Table
    for metadata in metadata_results:

        html += f"""
            <tr>

                <td>{metadata['file_name']}</td>

                <td>{metadata['size_bytes']} bytes</td>

                <td class="hash">
                    {metadata['sha256']}
                </td>

                <td>{metadata['modified_time']}</td>

                <td>{metadata['permissions']}</td>

            </tr>
        """

    html += """
            </table>
        </div>
    """

    # IOC Findings
    html += """
    <div class="card">

        <h2>IOC Findings</h2>
    """

    if ioc_results:

        for result in ioc_results:

            html += f"""
            <h3>{result['file']}</h3>

            <table>

                <tr>
                    <th>Line</th>
                    <th>Pattern</th>
                    <th>Content</th>
                </tr>
            """

            for finding in result["findings"]:

                html += f"""
                <tr>

                    <td>{finding['line']}</td>

                    <td class="danger">
                        {finding['pattern']}
                    </td>

                    <td>{finding['content']}</td>

                </tr>
                """

            html += "</table><br>"

    else:

        html += "<p>No IOC findings detected.</p>"

    html += "</div>"

    # Sensitive Data Findings
    html += """
    <div class="card">

        <h2>Sensitive Data Findings</h2>
    """

    if sensitive_results:

        for result in sensitive_results:

            html += f"""
            <h3>{result['file']}</h3>

            <table>

                <tr>
                    <th>Type</th>
                    <th>Value</th>
                </tr>
            """

            for finding in result["findings"]:

                html += f"""
                <tr>

                    <td>{finding['type']}</td>

                    <td>{finding['value']}</td>

                </tr>
                """

            html += "</table><br>"

    else:

        html += "<p>No sensitive data detected.</p>"

    html += """
        </div>

    </body>

    </html>
    """

    with open(output_file, "w", encoding="utf-8") as f:

        f.write(html)