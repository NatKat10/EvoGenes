from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app import db 



class Gene(db.Model):
    __tablename__ = 'genes'
    id = db.Column(db.Integer, primary_key=True)
    gene_name = db.Column(db.String(255), nullable=False)
    sequence = db.Column(db.Text, nullable=False)

    def __init__(self, gene_name, sequence):
        self.gene_name = gene_name
        self.sequence = sequence



app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:'':F14g258h369!@localhost/my'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)



class GeneSchema(ma.Schema):
    class Meta:
        fields = ('id','gene_name','sequence')

gene_schema = GeneSchema()
gene_schema = GeneSchema(many=True)

@app.route('/',methods = ['GET'])
def get_data():
    return jsonify({"Hello":"World"})



@app.route('/add',methods = ['POST'])
def add_gene():
    data = request.get_json()
    gene_name = data['gene_name']
    sequence = data['sequence']

    # Create an instance of the Gene model with the received data
    new_gene = Gene(gene_name=gene_name, sequence=sequence)

    # Add the new gene to the session and commit it to the database
    db.session.add(new_gene)
    db.session.commit()

    return jsonify({"message": "Gene added successfully"}), 201

if __name__ == "__main__":
    app.run(debug=True)


