from flask import Flask, render_template, request, send_file
import pdfplumber
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os
import uuid

app = Flask(__name__)

PDF_PATH = "2023ENGG_CAP2_AI_CutOff.pdf"
OUTPUT_DIR = "output"

# Sample city and branch lists (same as GUI)
cities = sorted([
    "Pune", "Mumbai", "Nagpur", "Nashik", "Aurangabad", "Amravati",
    "Kolhapur", "Sangli", "Solapur", "Jalgaon", "Ahmednagar", "Latur",
    "Beed", "Satara", "Chandrapur", "Wardha", "Yavatmal", "Akola",
    "Nanded", "Osmanabad", "Parbhani", "Dhule", "Buldhana", "Gondia",
    "Ratnagiri", "Sindhudurg", "Palghar", "Thane", "Raigad"
])

branches = sorted([
    "Computer Engineering", "Information Technology", "Artificial Intelligence",
    "Data Science", "Machine Learning", "Robotics", "Automation",
    "Electronics", "Electronics and Telecommunication", "Electrical",
    "Mechanical", "Civil", "Chemical", "Biomedical", "Biotechnology",
    "Mechatronics", "Instrumentation", "Aerospace", "Environmental", "Textile",
    "Production", "Printing", "Marine", "Metallurgy", "Automobile", "Food Technology"
])

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form.get("city")
        selected_branches = request.form.getlist("branches")
        output_file = f"{OUTPUT_DIR}/Filtered_{uuid.uuid4().hex}.pdf"

        try:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            doc = SimpleDocTemplate(output_file, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
            elements = []
            styles = getSampleStyleSheet()
            header_style = styles['Heading4']

            with pdfplumber.open(PDF_PATH) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    tables = page.extract_tables()
                    for table in tables:
                        if not table or len(table) < 2:
                            continue
                        header = table[0]
                        body_rows = table[1:]

                        filtered_rows = []
                        for row in body_rows:
                            if not row or len(row) < 2:
                                continue
                            row_str = " ".join([str(cell or "") for cell in row])
                            if city in row_str and any(branch.lower() in row_str.lower() for branch in selected_branches):
                                filtered_rows.append([str(cell).replace("\n", " ").strip() if cell else "" for cell in row])

                        if filtered_rows:
                            final_table = [header] + filtered_rows
                            t = Table(final_table, repeatRows=1)
                            t.setStyle(TableStyle([
                                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('FONTSIZE', (0, 0), (-1, -1), 7),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
                            ]))
                            elements.append(Paragraph(f"{city} - Branches - Page {page_num + 1}", header_style))
                            elements.append(t)
                            elements.append(Spacer(1, 0.2 * inch))

            doc.build(elements)
            return send_file(output_file, as_attachment=True)

        except Exception as e:
            return f"Error: {str(e)}"

    return render_template("index.html", cities=cities, branches=branches)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render will inject the PORT
    app.run(host="0.0.0.0", port=port, debug=False) 