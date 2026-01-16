from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    name = request.args.get("name", "Guest")
    return f"""
    <h1>HELLO, {name.upper()}!</h1>
    <p>Welcome to the Flask Assignment App 🚀</p>

    <h3>Try Bonus Features:</h3>
    <ul>
        <li>/reverse?name=yourname</li>
        <li>/count?name=yourname</li>
        <li>/greet?name=yourname</li>
    </ul>
    """
@app.route("/reverse")
def reverse_name():
    name = request.args.get("name", "Guest")
    return f"<h2>Reversed: {name[::-1]}</h2>"

@app.route("/count")
def count_chars():
    name = request.args.get("name", "")
    return f"<h2>Character Count: {len(name)}</h2>"

if __name__ == "__main__":
    app.run(debug=True)
