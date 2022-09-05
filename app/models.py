from app import db

class Device(db.Model):

    hostname_id = db.Column(db.String, primary_key=True, nullable=False, unique=False)
    subnet = db.Column(db.String, unique=False)
    username = db.Column(db.String, unique=False)
    password = db.Column(db.String, unique=False)
