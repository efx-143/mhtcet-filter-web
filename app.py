from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Load data once at startup
with open("data.json", "r", encoding="utf-8") as f:
    all_data = json.load(f)

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

@app.route("/", methods=["GET", "POST"])
def index():
    filtered_data = []
    if request.method == "POST":
        city = request.form.get("city")
        selected_branches = request.form.getlist("branches")

        for row in all_data:
            if city.lower() in row.get("Institute Name", "").lower():
                for branch in selected_branches:
                    if branch.lower() in row.get("Course Name", "").lower():
                        filtered_data.append(row)
                        break

    return render_template("index.html", cities=cities, branches=branches, results=filtered_data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
