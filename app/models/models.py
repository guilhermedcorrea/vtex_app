from flask_sqlalchemy import SQLAlchemy,model
from datetime import datetime
from ..extensions import db
from sqlalchemy.orm import relationship
from typing import Optional
from flask import session
from flask_admin import tools


class Usuario(db.Model):
    __tablename__ = 'usuario'
    __table_args__ = {"schema": "vtex"}
    cod_usuario = db.Column(db.Integer, primary_key=True)
    senha = db.Column(db.String(100), unique=False, nullable=False)
    nome_usuario = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=False, nullable=False)
    data_alterado = db.Column(db.DateTime, unique=False, nullable=False)
    
    def __repr__(self):
      
        self.session.query(self.model)
        print(self.session.query(self.model))
        return '<Usuario %r>' % self.cod_usuario
    
  
class Marca(db.Model):
    __tablename__ = 'marca'
    __table_args__ = {"schema": "vtex"}
    cod_marca = db.Column(db.Integer, primary_key=True)
    referencia_marca = db.Column(db.Integer)
    nome_marca = db.Column(db.String(100), unique=False, nullable=False)
    data_alterado = db.Column(db.DateTime, unique=False, nullable=False)
    produtos = db.relationship('Produto',back_populates="marca")
    precos = db.relationship('Precos',back_populates="marca")

    def __repr__(self):
        return '<Marca %r>' % self.cod_marca

class Produto(db.Model):
    __tablename__ = 'produto'
    __table_args__ = {"schema": "vtex"}
    cod_produto = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100), unique=False, nullable=False)
    nome_produto = db.Column(db.String(500), unique=False, nullable=False)
    preco_lista = db.Column(db.Float)
    preco = db.Column(db.Float)
    base_preco = db.Column(db.Float)
    ref_marca = db.Column(db.Integer)
    trade_policy = db.Column(db.Integer)
    skuid = db.Column(db.Integer)
    id_listapreco = db.Column(db.Integer)
    canal_venda = db.Column(db.Integer)
    cod_marca = db.Column(db.Integer, db.ForeignKey('vtex.marca.cod_marca'), nullable=False)
    marca = db.relationship('Marca', backref='cod_produto', lazy=True)
    precosproduto = db.relationship('Precos', back_populates='produto')
    
    def __repr__(self):
        return '<Produto %r>' % self.cod_produto
    

        
class Precos(db.Model):
    __tablename__ = 'precos'
    __table_args__ = {"schema": "vtex"}
    cod_preco = db.Column(db.Integer, primary_key=True)
    novo_preco =db.Column(db.Float)
    preco =db.Column(db.Float)
    preco_base =db.Column(db.Float)
    skuid =db.Column(db.Integer)
    cod_marca = db.Column(db.Integer, db.ForeignKey('vtex.marca.cod_marca'), nullable=False)
    trade_policy = db.Column(db.Integer)
    cnt = db.Column(db.Integer)
    canal_venda_porcentagem = db.Column(db.Integer)
    custo_envio = db.Column(db.Float)
    preco_final = db.Column(db.Float)
    cod_produto = db.Column(db.Integer, db.ForeignKey('vtex.produto.cod_produto'), nullable=False)
    data_alterado = db.Column(db.DateTime, unique=False, nullable=False)
    produto = db.relationship('Produto', backref='cod_preco', lazy=True)
    marca = db.relationship('Marca', backref='cod_preco', lazy=True)
    def __repr__(self):
        return '<Precos %r>' % self.cod_preco
