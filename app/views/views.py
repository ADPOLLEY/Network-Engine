from app import app, db
from flask import redirect, render_template, request, jsonify
from app.models.models import Device

@app.route("/", methods=["GET"])
def home():
    """Serve homepage template."""
    return render_template("index.html")

@app.route("/inventory", methods=["GET"])
def inventory():
    """Serve inventory template."""
    devices = db.session.query(Device).all()
    return render_template("inventory.html", devices=devices)
1
@app.route("/submit", methods=["POST"])
def submit():
    global_device_object = Device()

    hostname = request.form["hostname"]
    subnet = request.form["subnet"]
    model = request.form["model"]
    username = request.form["username"]
    password = request.form["password"]

    device_exists = db.session.query(Device.hostname_id == hostname).filter().first()
    print(device_exists)

    #check if device already exists in db

    device = Device(hostname_id=hostname)
    hostname_id = hostname
    device = Device(hostname_id=hostname_id, subnet=subnet, model=model, username=username, password=password)
    db.session.add(device)
    db.session.commit()
    global_device_object = device

    response = f"""
    <tr>
        <td>{hostname}</td>
        <td>{subnet}</td>
        <td>{model}</td>
        <td>{username}</td>
        <td>{password}</td>
        <td>
            <button class="btn btn-primary"
                hx-get="/get-edit-form/{global_device_object.hostname_id}">
                Edit Hostname
            </button>
        </td>
        <td>
            <button hx-delete="/delete/{global_device_object.hostname_id}"
                class="btn btn-primary">
                Delete
            </button>
        </td>
    </tr>
    """
    return response

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_device(id):
    device = Device.query(id)
    db.session.delete(device)
    db.session.commit()

    return ""

@app.route("/get-edit-form/<int:id>", methods=["GET"])
def get_edit_form(id):
    device = Device.query.get(id)

    response = f"""
    <tr hx-trigger='cancel' class='editing' hx-get="/get-book-row/{id}">
  <td><input name="hostname" value="{device.hostname_id}"/></td>
  <td>{device.subnet}</td>
  <td>{device.model}</td>
  <td>{device.username}</td>
  <td>{device.password}</td>
  <td>
    <button class="btn btn-primary" hx-get="/get-book-row/{id}">
      Cancel
    </button>
    <button class="btn btn-primary" hx-put="/update/{id}" hx-include="closest tr">
      Save
    </button>
  </td>
    </tr>
    """
    return response

@app.route("/get-book-row/<int:id>", methods=["GET"])
def get_device_row(id):
    device = Device.query.get(id)

    response = f"""
    <tr>
        <td>{device.hostname_id}</td>
        <td>{device.subnet}</td>
        <td>{device.model}</td>
        <td>{device.username}</td>
        <td>{device.password}</td>
        <td>
            <button class="btn btn-primary"
                hx-get="/get-edit-form/{id}">
                Edit Title
            </button>
        </td>
        <td>
            <button hx-delete="/delete/{id}"
                class="btn btn-primary">
                Delete
            </button>
        </td>
    </tr>
    """
    return response

@app.route("/update/<int:id>", methods=["PUT"])
def update_device(id):
    db.session.query(Device).filter(Device.hostname_id == id).update({"hostname": request.form["hostname"]})
    db.session.commit()

    hostname = request.form["hostname"]
    device = Device.query.get(id)

    response = f"""
    <tr>
        <td>{device.hostname_id}</td>
        <td>{device.subnet}</td>
        <td>{device.model}</td>
        <td>{device.username}</td>
        <td>{device.password}</td>
        <td>
            <button class="btn btn-primary"
                hx-get="/get-edit-form/{id}">
                Edit Title
            </button>
        </td>
        <td>
            <button hx-delete="/delete/{id}"
                class="btn btn-primary">
                Delete
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

@app.route("/management")
def management():
    """Serve management template."""
    return render_template("management.html")

@app.route("/profile")
def profile():
    """Serve profile template."""
    return render_template("profile.html")

@app.route("/show_cli")
def show_cli():
    """Serve profile template."""
    return render_template("show_cli.html")

@app.route("/config")
def config():
    """Serve profile template."""
    return render_template("config.html")

@app.route("/config_backup")
def config_backup():
    """Serve profile template."""
    return render_template("config_backup.html")

@app.route("/export_backup")
def export_backup():
    """Serve profile template."""
    return render_template("export_backup.html")

@app.route("/delete_backup")
def delete_backup():
    """Serve profile template."""
    return render_template("delete_backup.html")