from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
import click

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dedoca_gourmet.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelos do banco de dados
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Em processamento')

class OrderItems(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), primary_key=True)

# Comando para criar as tabelas do banco de dados
@app.cli.command("create-db")
@with_appcontext
def create_db():
    db.create_all()
    click.echo("Banco de dados criado com sucesso!")

@app.route('/')
def home():
    return "Bem-vindo ao Dedoca Gourmet!"

if __name__ == '__main__':
    app.run(debug=True)
