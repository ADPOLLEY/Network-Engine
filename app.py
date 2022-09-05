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

@app.route("/config")
def configy():
    """Serve config template."""
    return render_template("config.html")

@app.route("/contact_us")
def contact_us():
    """Serve contact_us template."""
    return render_template("contact_us.html")

@app.route("/create_backup")
def create_backup():
    """Serve create_backup template."""
    return render_template("create_backup.html")

@app.route("/management")
def management():
    """Serve management template."""
    return render_template("management.html")

@app.route("/profile")
def profile():
    """Serve profile template."""
    return render_template("profile.html")