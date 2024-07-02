# from .extensions import db

# # class Gene(db.Model):
# #     __tablename__ = 'genes'
# #     id = db.Column(db.Integer, primary_key=True)
# #     gene_name = db.Column(db.String(255), nullable=False)
# #     sequence = db.Column(db.Text, nullable=False)


# from .extensions import db

# class GeneComparison(db.Model):
#     __tablename__ = 'gene_comparisons'
#     id = db.Column(db.Integer, primary_key=True)
#     gene_id1 = db.Column(db.String(255), nullable=False)
#     gene_id2 = db.Column(db.String(255), nullable=False)
#     dotplot_data = db.Column(db.Text, nullable=False)
#     gene_structure1_html = db.Column(db.Text, nullable=False)
#     gene_structure2_html = db.Column(db.Text, nullable=False)
#     exon_intervals1 = db.Column(db.Text, nullable=False)
#     exon_intervals2 = db.Column(db.Text, nullable=False)
#     yass_output = db.Column(db.Text, nullable=False)
    
#     __table_args__ = (db.UniqueConstraint('gene_id1', 'gene_id2', name='gene_ids_unique'),)
