from sqlmodel import Field, Relationship, SQLModel, create_engine
from typing import Optional
from datetime import date
from decimal import Decimal
#os models serve para criar as classes que representam as tabelas do banco de dados 

class Assinaturas(SQLModel, table= True):
    id: int = Field(primary_key=True) # aqui é o id da tabela defino ele como numero inteiro e chave primaria
    empresa: str = Field(max_length=100) # aqui é o nome da empresa que vai assinar o contrato
    site: Optional[str] = None # aqui é o site da empresa que vai assinar o contrato e ele é opcional
    data_assinatura: date
    valor: Decimal # aqui é o valor do contrato que a empresa vai assinar

class Pagamentos(SQLModel, table= True):
    id: int = Field(primary_key=True)
    assinatura_id: int = Field(foreign_key="assinaturas.id") # aqui é a chave estrangeira que relaciona a tabela de pagamentos com a tabela de assinaturas 
    assinatura: Assinaturas = Relationship() # aqui é a relação entre a tabela de pagamentos e a tabela de assinaturas
    data_pagamento: date
