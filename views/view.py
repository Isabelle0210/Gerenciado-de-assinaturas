from datetime import date, datetime
from sqlmodel import Session, select
import __init__
from models.database import engine
from models.model import Assinaturas, Pagamentos


class Assinatura_service:
    def __init__(self, engine):
        self.engine = engine

    def create(self, assinatura: Assinaturas):
        # Gerenciador de contexto que fecha automaticamente a conexão com o banco
        with Session(self.engine) as session:
            session.add(assinatura)  # Adiciona a assinatura no banco de dados
            session.commit()  # Salva as alterações no banco
            return assinatura

    def list_all(self):
        with Session(self.engine) as session:
            statement = select(Assinaturas)  # Seleciona todas as assinaturas
            results = session.exec(statement).all()  # Executa e retorna os resultados
        return results

    def delete(self, id):
        with Session(self.engine) as session:
            statement = select(Assinaturas).where(Assinaturas.id == id)
            result = session.exec(statement).one()
            session.delete(result)
            session.commit()
            print (result)

    def _has_pay(self, results):
        for result in results:
            # Corrigir para `data_pagamento` em vez de `date`
            if result.data_pagamento.month == date.today().month:
                return True
        return False

    def pay(self, assinatura: Assinaturas):
        with Session(self.engine) as session:
            statement = (
                select(Pagamentos)
                .join(Assinaturas)
                .where(Assinaturas.empresa == assinatura.empresa)
            )
            results = session.exec(statement).all()

            if self._has_pay(results):
                question = input(
                    "Essa assinatura já foi paga esse mês, deseja pagar novamente? (s/n): "
                )
                # Se o usuário digitar 'n', a função retorna sem realizar o pagamento
                if question.strip().lower() != "s":
                    return

            # Adiciona um novo pagamento
            pay = Pagamentos(assinatura_id=assinatura.id, data_pagamento=date.today())
            session.add(pay)
            session.commit()

    def total_pay(self):
        with Session(self.engine) as session:
            statement = select(Assinaturas)
            results = session.exec(statement).all()

            total = 0 
            for result in results:
                total += result.valor
            return float(total)


# aqui eu estou fazendo uma função para pegar os ultimos 12 meses
    def _get_last_12_months_native(self):
        today = datetime.now()
        year = today.year
        month = today.month
        last_12_months = []
        for _ in range(12):
            last_12_months.append((year, month))
            month = month - 1
            if month == 0:
                month = 12
                year = year - 1
        return last_12_months [::-1]

    #função para pegar o valor gasto em cada mes

    def _get_values_for_months(self, last_12_months):
        with Session(self.engine) as session: #sempre que for buscar algo no banco de dados precisa de uma session
            statement = select(Pagamentos)
            results = session.exec(statement).all()

            values_for_months = [] #criando uma lista vazia para armazenar os valores de cada mes 
            #iterando sobre os ultimos 12 meses
            for i in last_12_months:
                value = 0
                for result in results:
                    if result.data_pagamento.month == i[0] and result.data_pagamento.year == i[1]:
                        value += float(result.assinatura.valor)
                values_for_months.append(value)
            return values_for_months
            
    def gen_chart(self):
            last_12_months = self._get_last_12_months_native()
            values_for_months = self._get_values_for_months(last_12_months)
            
            import matplotlib.pyplot as plt
            
            plt.plot(last_12_months, values_for_months)
            plt.show()
            

# Inicialização do serviço
ss = Assinatura_service(engine)
# assinatura = Assinaturas(empresa="Empresa 1", data_assinatura=date.today(),site="www.isa", valor=1000)
# ss.create(assinatura)

print(ss.gen_chart())
