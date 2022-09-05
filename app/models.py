from app import db

class Device(db.Model):

    hostname_id = db.Column(db.String, primary_key=True)
    subnet = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)

    def __repr__(self):
        return '<hostname: {}>'.format(self.devices)