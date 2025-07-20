from flask import Flask, render_template, request
import pdfplumber
import os

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
    results = []
    headers = []

    if request.method == "POST":
        city = request.form.get("city")
        selected_branches = request.form.getlist("branches")

        try:
            with pdfplumber.open(PDF_PATH) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        if not table or len(table) < 2:
                            continue
                        header = table[0]
                        body = table[1:]

                        for row in body:
                            if not row or len(row) < 5:
                                continue
                            row_str = " ".join([str(cell or "") for cell in row])
                            if city in row_str and any(branch.lower() in row_str.lower() for branch in selected_branches):
                                cleaned_row = [str(cell or "").replace("\n", " ").strip() for cell in row]
                                results.append(cleaned_row)
                                if not headers:
                                    headers = header

        except Exception as e:
            return f"Error: {str(e)}"

    return render_template("index.html", cities=cities, branches=branches, results=results, headers=headers)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
