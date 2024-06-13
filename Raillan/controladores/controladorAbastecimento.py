import sqlite3
import os
from entidades.abastecimento import Abastecimento
from controladores.controladorBombaCombustivel import ControladorBombaCombustivel
from controladores.controladorTipoCombustivel import ControladorTipoCombustivel
from controladores.controladorTanqueCombustivel import ControladorTanqueCombustivel
from datetime import datetime

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
diretorio_pai = os.path.dirname(diretorio_atual)

class ControladorAbastecimento:
    def __init__(self):
        self.controlador_bomba = ControladorBombaCombustivel()
        self.controlador_tipo_combustivel = ControladorTipoCombustivel()
        self.controlador_tanque_combustivel = ControladorTanqueCombustivel()
        self.conn = sqlite3.connect(diretorio_pai + '/dados/DADOS.sqlite')
        self.cursor = self.conn.cursor()
        self.conn.commit()

    def verificar_abastecimento(self, idBomba, tipoCombustivel, preco, litros):
        # Verificar se a bomba está ativa
        bomba = self.controlador_bomba.buscar_bomba(idBomba)
        print(bomba)
        if not bomba or not bomba[3]:
            raise Exception("A bomba selecionada não está ativa.")


        # Verificar se o tanque tem capacidade para o abastecimento
        tanque = self.controlador_tanque_combustivel.buscar_tanque(bomba[5])
        if not tanque or tanque[4] < litros:
            raise Exception("O tanque não tem capacidade suficiente para o abastecimento solicitado.")

        return True

    def adicionar_abastecimento(self, idBomba, tipoCombustivel, data, preco, litros):
        # Verificar dados do abastecimento
        self.verificar_abastecimento(idBomba, tipoCombustivel, float(preco), float(litros))
        
        # Criar objeto Abastecimento
        abastecimento = Abastecimento(idBomba, tipoCombustivel, data, float(preco), float(litros))
        
        # Atualizar a capacidade do tanque
        bomba = self.controlador_bomba.buscar_bomba(idBomba)
        tanque = self.controlador_tanque_combustivel.buscar_tanque(bomba[5])
        if tanque:
            self.controlador_tanque_combustivel.atualizar_volume_tanque(tanque[0], abastecimento.litros)
        
        # Adicionar o abastecimento ao banco
        try:
            with self.conn:
                self.cursor.execute(
                    "INSERT INTO Abastecimentos (idBomba, data, litros, Preco, tipoCombustivel) VALUES (?, ?, ?, ?, ?)",
                    (abastecimento.idBomba, abastecimento.data, abastecimento.litros, abastecimento.preco, abastecimento.tipoCombustivel)
                )
                self.conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Erro ao registrar Abastecimento: {e}")
        return True