from app import app, db
from flask import redirect, render_template, request, jsonify
from app.models import Device

@app.route("/", methods=["GET"])
def home():
    """Serve homepage template."""
    return render_template("index.html")

@app.route("/inventory", methods=["GET"])
def inventory():
    """Serve inventory template."""
    devices = db.session.query(Device).filter().all()
    return render_template("inventory.html", devices=devices)

@app.route("/submit", methods=["POST"])
def submit():
    global_device_object = Device()

    hostname = request.form["hostname"]
    subnet = request.form["subnet"]
    username = request.form["username"]
    password = request.form["password"]

    device_exists = db.session.query(Device).filter().first()
    print(device_exists)

    #check if device already exists in db

    if device_exists:
        hostname_id = device_exists.hostname_id
        device = Device(hostname_id=hostname_id, subnet=subnet)
        db.session.add(device)
        db.session.commit()
        global_device_object = device
    else:
        device = Device(hostname_id=hostname)
        db.session.add(device)
        db.session.commit()

        device = Device(hostname_id=hostname_id, subnet=subnet)
        db.session.add(device)
        db.session.commit()
        global_device_object = device

    response = f"""
    <tr>
        <td>{hostname}</td>
        <td>{subnet}</td>
        <td>{username}</td>
        <td>{password}</td>
        <td>
            <button class="btn btn-primary"
                hx-get="/get-edit-form/{global_device_object.hostname_id}">
                Edit Title
            </button>
        </td>
        <td>
            <button hx-delete="/delete/{global_device_object.hostname_id}"
                class="btn btn-primary">
            </button>
        </td>
    </tr>
    """
    return response

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_device(id):
    device = Device.query.get(id)
    db.session.delete(device)
    db.session.commit()

    return ""

@app.route("/get-edit-form/int:id", methods=["GET"])
def get_edit_form(id):
    device = Device.query.get(id)

    response = f"""
    <tr hx-trigger='cancel' class='editing' hx-get="/get-device-row/{id}">
  <td><input name="hostname" value="{device.hostname}"/></td>
  <td>
    <button class="btn btn-primary" hx-get="/get-device-row/{id}">
      Cancel
    </button>
    <button class="btn btn-primary" hx-put="/update/{id}" hx-include="closest tr">
      Save
    </button>
  </td>
    </tr>
    """
    return response

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