from flask import Flask, redirect, render_template, request


app = Flask(__name__, template_folder="templates")


@app.route("/")
def home():
    """Serve homepage template."""
    return render_template("index.html")

@app.route("/inventory")
def inventory():
    """Serve inventory template."""
    return render_template("inventory.html")
