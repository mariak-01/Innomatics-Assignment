from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    matches = []
    error = ""

    if request.method == "POST":
        test_string = request.form.get("test_string")
        regex_pattern = request.form.get("regex_pattern")

        try:
            matches = re.findall(regex_pattern, test_string)
        except re.error:
            error = "Invalid Regular Expression"

    return render_template("index.html", matches=matches, error=error)

if __name__ == "__main__":
    app.run(debug=True)