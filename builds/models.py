from pobuilds import db

class Build(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buildname = db.Column(db.String(120))
    buildvers = db.Column(db.Decimal(2,2))
