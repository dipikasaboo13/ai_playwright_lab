"""
FastAPI Server for Project 15: Multi-File Import and Error Report Validation.
Provides web UI for uploading employee CSV files, validating record fields, displaying
row-level processing summaries and error tables, and downloading detailed CSV error reports.
"""

import csv
import io
import re
from typing import List, Dict, Any
from fastapi import FastAPI, UploadFile, File, Response
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="Multi-File Import & Error Reporting Portal")

# Global in-memory storage for generated error reports
LATEST_ERROR_REPORT_CSV: str = ""


@app.get("/health")
def health_check():
    """Health check endpoint to verify server initialization."""
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def get_index():
    """Render the main File Import & Error Reporting Dashboard."""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-File Import & Error Reporting Portal</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f7f6;
            margin: 0;
            padding: 20px;
            color: #333;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            margin-top: 0;
        }
        .upload-section {
            border: 2px dashed #3498db;
            padding: 25px;
            text-align: center;
            border-radius: 6px;
            background-color: #ebf5fb;
            margin-bottom: 25px;
        }
        .upload-section input[type="file"] {
            margin-bottom: 15px;
        }
        .btn {
            background-color: #3498db;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 15px;
            text-decoration: none;
            display: inline-block;
        }
        .btn:hover {
            background-color: #2980b9;
        }
        .btn-download {
            background-color: #e74c3c;
            margin-top: 15px;
        }
        .btn-download:hover {
            background-color: #c0392b;
        }
        .summary-banner {
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
            display: none;
        }
        .summary-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .summary-error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        th, td {
            text-align: left;
            padding: 10px;
            border: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
            color: #333;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Multi-File Import & Error Reporting Portal</h1>
        <p>Select a CSV file containing employee records to import into the system.</p>

        <div class="upload-section">
            <input type="file" id="file-upload-input" accept=".csv" />
            <br/>
            <button id="btn-import-file" class="btn" onclick="uploadFile()">Upload & Process File</button>
        </div>

        <div id="import-success-summary" class="summary-banner summary-success">
            <h3>Import Successful</h3>
            <p id="success-counter-text">Successfully imported 0 records.</p>
        </div>

        <div id="import-error-summary" class="summary-banner summary-error">
            <h3>Import Completed with Errors</h3>
            <p id="error-counter-text">Failed records: 0</p>
            
            <table id="error-table">
                <thead>
                    <tr>
                        <th>CSV Row</th>
                        <th>Employee ID</th>
                        <th>Error Description</th>
                    </tr>
                </thead>
                <tbody id="error-table-body">
                </tbody>
            </table>

            <a id="btn-download-error-report" class="btn btn-download" href="/api/v1/download-error-report" download="error_report.csv" style="display:none;">
                Download Detailed Error Report (CSV)
            </a>
        </div>
    </div>

    <script>
        async function uploadFile() {
            const fileInput = document.getElementById('file-upload-input');
            const successSummary = document.getElementById('import-success-summary');
            const errorSummary = document.getElementById('import-error-summary');
            const successCounterText = document.getElementById('success-counter-text');
            const errorCounterText = document.getElementById('error-counter-text');
            const errorTableBody = document.getElementById('error-table-body');
            const downloadBtn = document.getElementById('btn-download-error-report');

            successSummary.style.display = 'none';
            errorSummary.style.display = 'none';
            errorTableBody.innerHTML = '';
            downloadBtn.style.display = 'none';

            if (!fileInput.files || fileInput.files.length === 0) {
                alert('Please select a file to import.');
                return;
            }

            const formData = new FormData();
            formData.append('file', fileInput.files[0]);

            try {
                const response = await fetch('/api/v1/import', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();

                if (result.error_count === 0) {
                    successCounterText.textContent = `Successfully imported ${result.success_count} records.`;
                    successSummary.style.display = 'block';
                } else {
                    errorCounterText.textContent = `Failed records: ${result.error_count} (out of ${result.total_records} total records)`;
                    
                    result.errors.forEach(err => {
                        const tr = document.createElement('tr');
                        tr.innerHTML = `<td>Row ${err.row}</td><td>${err.id || 'N/A'}</td><td>${err.error}</td>`;
                        errorTableBody.appendChild(tr);
                    });

                    errorSummary.style.display = 'block';
                    downloadBtn.style.display = 'inline-block';
                }
            } catch (err) {
                alert('An error occurred during file upload: ' + err);
            }
        }
    </script>
</body>
</html>"""
    return HTMLResponse(content=html_content)


@app.post("/api/v1/import")
async def import_file(file: UploadFile = File(...)):
    """
    Parse uploaded CSV file, validate record fields, record line errors,
    and update global error report CSV payload.
    """
    global LATEST_ERROR_REPORT_CSV

    content = await file.read()
    decoded = content.decode('utf-8')
    reader = csv.DictReader(io.StringIO(decoded))

    seen_ids = set()
    errors: List[Dict[str, Any]] = []
    success_count = 0
    total_records = 0

    # Pattern for simple email format validation
    email_regex = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

    for row_idx, row in enumerate(reader, start=2):  # Header is row 1
        total_records += 1
        emp_id = (row.get("id") or "").strip()
        name = (row.get("name") or "").strip()
        email = (row.get("email") or "").strip()
        salary_str = (row.get("salary") or "").strip()

        row_errors = []

        # Rule 1: ID required
        if not emp_id:
            row_errors.append("Missing required employee ID")
        # Rule 2: ID unique
        elif emp_id in seen_ids:
            row_errors.append(f"Duplicate employee ID '{emp_id}'")
        else:
            seen_ids.add(emp_id)

        # Rule 3: Valid email format
        if not email or not email_regex.match(email):
            row_errors.append(f"Invalid email address format '{email}'")

        # Rule 4: Salary must be positive integer
        try:
            salary = int(salary_str)
            if salary <= 0:
                row_errors.append("Salary must be a positive integer")
        except ValueError:
            row_errors.append(f"Invalid numeric salary '{salary_str}'")

        if row_errors:
            for err_msg in row_errors:
                errors.append({
                    "row": row_idx,
                    "id": emp_id,
                    "error": err_msg
                })
        else:
            success_count += 1

    # Generate CSV error report string
    output_stream = io.StringIO()
    writer = csv.writer(output_stream)
    writer.writerow(["row", "employee_id", "error_message"])
    for err in errors:
        writer.writerow([err["row"], err["id"], err["error"]])

    LATEST_ERROR_REPORT_CSV = output_stream.getvalue()

    status = "success" if len(errors) == 0 else "error"

    return JSONResponse(content={
        "status": status,
        "total_records": total_records,
        "success_count": success_count,
        "error_count": len(errors),
        "errors": errors
    })


@app.get("/api/v1/download-error-report")
def download_error_report():
    """Return the generated error report CSV file download."""
    global LATEST_ERROR_REPORT_CSV
    content = LATEST_ERROR_REPORT_CSV if LATEST_ERROR_REPORT_CSV else "row,employee_id,error_message\n"
    return Response(
        content=content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=error_report.csv"}
    )
