from . import ma

class GeneSchema(ma.Schema):
    class Meta:
        fields = ('id', 'gene_name', 'sequence')

gene_schema = GeneSchema()
genes_schema = GeneSchema(many=True)