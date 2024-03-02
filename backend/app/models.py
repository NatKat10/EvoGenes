from .extensions import db

class Gene(db.Model):
    __tablename__ = 'genes'
    id = db.Column(db.Integer, primary_key=True)
    gene_name = db.Column(db.String(255), nullable=False)
    sequence = db.Column(db.Text, nullable=False)