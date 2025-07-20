from flask import Flask, render_template, request
import pdfplumber

app = Flask(__name__)

PDF_PATH = "2023ENGG_CAP2_AI_CutOff.pdf"

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
    filtered_data = []
    header_row = []

    if request.method == "POST":
        city = request.form.get("city")
        selected_branches = request.form.getlist("branches")

        with pdfplumber.open(PDF_PATH) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    if not table or len(table) < 2:
                        continue

                    header_row = table[0]  # Use header from the PDF
                    body_rows = table[1:]

                    for row in body_rows:
                        if not row: continue
                        row_text = " ".join(str(cell or "") for cell in row)

                        if city in row_text and any(branch.lower() in row_text.lower() for branch in selected_branches):
                            cleaned_row = [str(cell).replace("\n", " ").strip() if cell else "" for cell in row]
                            filtered_data.append(cleaned_row)

    return render_template("index.html", cities=cities, branches=branches, data=filtered_data, header=header_row)


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
