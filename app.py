from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    name = request.args.get("name", "Guest")
    return f"""
    <h1>HELLO, {name.upper()}!</h1>
    <p>Welcome to the Flask Assignment App</p>

    <h3>Try Bonus Features:</h3>
    <ul>
        <li>/?name=yourname</li>
        <li>/uppercase?name=yourname</li>
        <li>/reverse?name=yourname</li>
        <li>/count?name=yourname</li>
        <li>/greet?name=yourname</li>
    </ul>
    """

# convert name to uppercase
@app.route("/uppercase")
def uppercase_name():
    name = request.args.get("name", "Guest")
    return f"<h1>{name.upper()}</h1>"

# reverse the name
@app.route("/reverse")
def reverse_name():
    name = request.args.get("name", "Guest")
    return f"<h2>Reversed Name: {name[::-1]}</h2>"

# count characters
@app.route("/count")
def count_characters():
    name = request.args.get("name", "")
    return f"<h2>Character Count: {len(name)}</h2>"

# greeting
@app.route("/greet")
def greet_user():
    name = request.args.get("name", "Guest")
    return f"<h2>Hope you have a great day, {name.upper()}</h2>"

if __name__ == "__main__":
    app.run(debug=True)
