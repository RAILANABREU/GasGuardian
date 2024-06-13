import sqlite3
import os
from entidades.posto import PostoGasolina

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
diretorio_pai = os.path.dirname(diretorio_atual)

class ControladorPosto:
    def __init__(self):
        # Conectar ao banco de dados
        self.conn = sqlite3.connect(diretorio_pai + '/dados/DADOS.sqlite')
        self.cursor = self.conn.cursor()
        self.__posto = PostoGasolina
        self.conn.commit()

    @property
    def posto(self):
        return self.__posto
    

    def adicionar_posto(self,nomePosto, cnpj, chavePix):

        posto = PostoGasolina(nomePosto, cnpj, chavePix)

        try:
            with self.conn:
                self.cursor.execute("INSERT INTO Posto (cnpj, chavePix, nomePosto) VALUES (?, ?, ?)",
                                    (posto.cnpj, posto.chavePix, posto.nomePosto))
                self.conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            # Se houver uma violação de integridade (como chave duplicada), lança uma exceção
            if 'UNIQUE constraint failed: Posto.cnpj' in str(e):
                raise ValueError("Erro: CNPJ já cadastrado.")
            elif 'UNIQUE constraint failed: Posto.chavePix' in str(e):
                raise ValueError("Erro: Chave PIX já cadastrada.")
            else:
                raise

    def listar_posto(self):
        # Listar todos os posto do banco de dados
        posto =  self.cursor.execute("SELECT nomePosto, CNPJ, chavePix FROM Posto")
        return posto.fetchall()


    def remover_posto(self, cnpj):
        # Remover um posto pelo CNPJ
        with self.conn:
            self.cursor.execute("DELETE FROM Posto WHERE cnpj = ?", (cnpj,))
            return self.cursor.rowcount > 0  # Retorna True se um posto foi removido

    def atualizar_posto(self, cnpj, nomePosto, chavePix):

        posto = PostoGasolina(cnpj, nomePosto, chavePix)

        try:
            with self.conn:
                self.cursor.execute(
                    "UPDATE Posto SET chavePix = ?, nomePosto = ? WHERE cnpj = ?",
                    (posto.nomePosto, posto.chavePix, posto.cnpj)
                )
                self.conn.commit()  # Garantir que as mudanças sejam salvas
                if self.cursor.rowcount > 0:
                    print("Posto atualizado com sucesso!")
                    return True
                else:
                    print("Nenhum posto encontrado com o CNPJ fornecido.")
                    return False
        except sqlite3.Error as e:
            print(f"Erro ao atualizar o posto: {e}")
            return False

