from database import db

class Filme(db.Model):
    __tablename__= "filme"
    id_filme = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(100))
    diretor = db.Column(db.String(100))
    ano_lancamento = db.Column(db.Integer)

    # construtor
    def __init__(self, titulo, diretor, ano_lancamento):
        self.titulo = titulo
        self.diretor = diretor
        self.ano_lancamento = ano_lancamento

    # representação do objeto criado...
    def __repr__(self):
        return "<Filme {}>".format(self.titulo)