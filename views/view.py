#aqui ficara a logica 
from datetime import date
from sqlmodel import Session, select
import __init__
from models.database import engine
from models.model import Assinaturas, Pagamentos

class Assinatura_service:
    def __init__(self, engine):
        self.engine = engine

    def crate(self, assinatura: Assinaturas):
        #with é um gerenciador de contexto que fecha o banco de dados automaticamente 
        with Session(self.engine) as session:
            session.add(assinatura) #aqui adiciona a assinatura no banco de dados 
            session.commit() # aqui salva a assinatura no banco de dados
            return assinatura
        
    def list_all(self):
        with Session(self.engine) as session:
            statement = select(Assinaturas) # aqui é a função que seleciona todas as assinaturas do banco de dados 
            results = session.exec(statement).all() # aqui executa a função select e mostra todas as assinaturas
        return results

    def _has_pay(self, results):
        for result in results:
            if result.date.month == date.today().month:
                return True
        return False
    
    def pay(self, assinatura: Assinaturas):
        with Session(self.engine) as session:
            statement = select(Pagamentos).where(Assinaturas.empresa == assinatura.empresa)
            results = session.exec(statement).all()

            if self._has_pay(results):
                questions = input('Essa assinatura já foi paga esse mês, deseja pagar novamente? (s/n)')

                #se o usuário digitar 's' ele vai pagar a assinatura novamente, senao ele vai sair da função 
                if not questions.upper() =='S':
                    return
            
            pay = Pagamentos(assinatura_id=assinatura.id, data_pagamento=date.today())
            session.add(pay)
            session.commit()

ss = Assinatura_service(engine) 

#assinatura = Assinaturas(empresa="netflix", site="www.netflix.com.br", data_assinatura=date.today(), valor=30)

#ss.crate(assinatura) # aqui é chamado a função que cria a assinatura no banco de dados

#print(ss.list_all()) # aqui é chamado a função que lista todas as assinaturas do banco de dados

ss.pay(assinatura) # aqui é chamado a função que mostra os pagamentos da assinatura