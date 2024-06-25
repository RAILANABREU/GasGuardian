import sqlite3
from entidades.abastecimento import Abastecimento
from controladores.controladorBombaCombustivel import ControladorBombaCombustivel
from controladores.controladorTipoCombustivel import ControladorTipoCombustivel
from controladores.controladorTanqueCombustivel import ControladorTanqueCombustivel
from datetime import datetime


class ControladorAbastecimento:
    def __init__(self):
        self.controlador_bomba = ControladorBombaCombustivel()
        self.controlador_tipo_combustivel = ControladorTipoCombustivel()
        self.controlador_tanque_combustivel = ControladorTanqueCombustivel()
        self.conn = sqlite3.connect('Raillan/dados/DADOS.sqlite')
        self.cursor = self.conn.cursor()
        self.conn.commit()

    def verificar_abastecimento(self, idBomba, tipoCombustivel, preco, litros):

        if preco <= 0:
            raise Exception("O valor do abastecimento deve ser maior que zero.")
        
        bomba = self.controlador_bomba.buscar_bomba(idBomba)

        
        tanque = self.controlador_tanque_combustivel.buscar_tanque(bomba[5])
        if not tanque or tanque[4] < litros:
            raise Exception("O tanque não tem capacidade suficiente para o abastecimento solicitado.")

        return True

    def adicionar_abastecimento(self, idBomba, tipoCombustivel, data, preco, litros, cpfFuncionario):
        print(idBomba, tipoCombustivel, data, preco, litros, cpfFuncionario)

        # Verificar dados do abastecimento
        self.verificar_abastecimento(idBomba, tipoCombustivel, float(preco), float(litros))
        
        # Criar objeto Abastecimento
        abastecimento = Abastecimento(idBomba, tipoCombustivel, data, float(preco), float(litros), cpfFuncionario)
        
        # Atualizar a capacidade do tanque
        bomba = self.controlador_bomba.buscar_bomba(idBomba)
        tanque = self.controlador_tanque_combustivel.buscar_tanque(bomba[5])
        if tanque:
            self.controlador_tanque_combustivel.atualizar_volume_tanque(tanque[0], abastecimento.litros)
        
        # Adicionar o abastecimento ao banco
        try:
            with self.conn:
                self.cursor.execute(
                    "INSERT INTO Abastecimentos (idBomba, data, litros, Preco, tipoCombustivel,cpfFuncionario) VALUES (?, ?, ?, ?, ?,?)",
                    (abastecimento.idBomba, abastecimento.data, abastecimento.litros, abastecimento.preco, abastecimento.tipoCombustivel, abastecimento.cpfFuncionario)
                )
                self.conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            raise ValueError(f"erro ao registrar Abastecimento: {e}")
        return True

    def listar_abastecimentos(self):
        self.cursor.execute("""
            SELECT 
                a.id AS ID, 
                strftime('%Y-%m-%d', a.data) AS Data, 
                strftime('%H:%M:%S', a.data) AS Hora, 
                b.nomeBomba AS Bomba, 
                a.tipocombustivel AS Combustível, 
                a.litros AS Litros, 
                a.preco AS Valor 
            FROM 
                Abastecimentos a
            JOIN 
                Bombas b ON a.idBomba = b.id
        """)
        
        return self.cursor.fetchall()

    def listar_abastecimentos_por_periodo(self, data_inicio, data_fim):
        self.cursor.execute("""
            SELECT 
                a.id AS ID, 
                strftime('%Y-%m-%d', a.data) AS Data, 
                strftime('%H:%M:%S', a.data) AS Hora, 
                b.nomeBomba AS Bomba, 
                a.tipocombustivel AS Combustível, 
                a.litros AS Litros, 
                a.preco AS Valor 
            FROM 
                Abastecimentos a
            JOIN 
                Bombas b ON a.idBomba = b.id
            WHERE
                date(a.data) BETWEEN ? AND ?
        """, (data_inicio, data_fim))
        
        return self.cursor.fetchall()

    def listar_abastecimentos_por_funcionario(self, cpfFuncionario):
        self.cursor.execute("""
            SELECT 
                a.id AS ID, 
                strftime('%Y-%m-%d', a.data) AS Data, 
                strftime('%H:%M:%S', a.data) AS Hora, 
                b.nomeBomba AS Bomba, 
                a.tipocombustivel AS Combustível, 
                a.litros AS Litros, 
                a.preco AS Valor 
            FROM 
                Abastecimentos a
            JOIN 
                Bombas b ON a.idBomba = b.id
            WHERE
                a.cpfFuncionario = ?
        """, (cpfFuncionario,))
        
        return self.cursor.fetchall()
    
    def listar_abastecimentos_por_funcionario_e_periodo(self, cpfFuncionario, data_inicio, data_fim):
        self.cursor.execute("""
            SELECT 
                a.id AS ID, 
                strftime('%Y-%m-%d', a.data) AS Data, 
                strftime('%H:%M:%S', a.data) AS Hora, 
                b.nomeBomba AS Bomba, 
                a.tipocombustivel AS Combustível, 
                a.litros AS Litros, 
                a.preco AS Valor 
            FROM 
                Abastecimentos a
            JOIN 
                Bombas b ON a.idBomba = b.id
            WHERE
                a.cpfFuncionario = ? AND date(a.data) BETWEEN ? AND ?
        """, (cpfFuncionario, data_inicio, data_fim))
        
        return self.cursor.fetchall()

    def calcular_totais(self, data_inicio=None, data_fim=None):
        query = """
            SELECT SUM(preco) AS TotalVendas, SUM(litros) AS TotalLitros
            FROM Abastecimentos
        """
        params = ()
        if data_inicio and data_fim:
            query += " WHERE date(data) BETWEEN ? AND ?"
            params = (data_inicio, data_fim)
        
        self.cursor.execute(query, params)
        result = self.cursor.fetchone()
        total_vendas = result[0] if result[0] else 0.0
        total_litros = result[1] if result[1] else 0.0
        return total_vendas, total_litros