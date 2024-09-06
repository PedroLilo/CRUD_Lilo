from flask import Flask, render_template, request, flash, redirect
from database import db
from flask_migrate import Migrate
from models import Filme

app = Flask(__name__)
app.config['SECRET_KEY'] = '9ebe6f92407c97b3f989420e0e6bebcf9d1976b2e230acf9faf4783f5adffe1b'

# --> drive://usuario:senha@servidor/banco_de_dados

conexao = "mysql+pymysql://alunos:cefetmg@127.0.0.1/Crud_lilo"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aula')
@app.route('/aula/<nome>')
@app.route('/aula/<nome>/<curso>')
@app.route('/aula/<nome>/<curso>/<int:ano>')
def aula(nome = 'Gabriel', curso = 'Informática', ano = '1'):
    dados = {'nome':nome, 'curso':curso, 'ano':ano}
    return render_template('aula.html', dados_curso=dados)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/dados', methods=['POST'])
def dados():
    flash('Dados Enviados!!!')
    dados = request.form
    return render_template('dados.html', dados = dados)

@app.route("/filme")
def filme():
    u = Filme.query.all()
    return render_template("filme_lista.html", dados = u)

@app.route("/filme/add")
def filme_add():
    return render_template("filme_add.html")

@app.route("/filme/save", methods=['POST'])
def filme_save():
    titulo = request.form.get('titulo')
    diretor = request.form.get('diretor')
    ano_lancamento = request.form.get('ano_lancamento')
    if titulo and diretor and ano_lancamento:
        filme = Filme(titulo, diretor, ano_lancamento)
        db.session.add(filme)
        db.session.commit()
        flash('Filme cadastrado com sucesso!! :D')
        return redirect('/filme')
    else:
        flash('Preencha todos os campos! >:(')
        return redirect('/filme/add')

@app.route("/filme/remove/<int:id>")
def filme_remove(id):
    filme = Filme.query.get(id)
    if filme:
        db.session.delete(filme)
        db.session.commit()
        flash('Filme removido com sucesso!')
        return redirect("/filme")
    else:
        flash("Caminho incorreto!")
        return redirect("/filme")

@app.route("/filme/edita/<int:id>")
def filme_edita(id):
    filme = Filme.query.get(id)
    return render_template("filme_edita.html", dados=filme)

@app.route("/filme/editasave", methods=['POST'])
def filme_editasave():
    titulo = request.form.get('titulo')
    diretor = request.form.get('diretor')
    ano_lancamento = request.form.get('ano_lancamento')
    id_filme = request.form.get('id_filme')
    if id_filme and titulo and diretor and ano_lancamento:
        filme = Filme.query.get(id)
        filme.titulo = titulo
        filme.diretor = diretor
        filme.ano_lancamento = ano_lancamento
        db.session.commit()
        flash('Dados atualizados com sucesso!')
        return redirect('/filme')
    else:
        flash('Dados incompletos.')
        return redirect("/filme")


if __name__ == '__main__':
    app.run()