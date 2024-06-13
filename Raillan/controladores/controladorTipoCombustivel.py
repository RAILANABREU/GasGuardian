import sqlite3
import os
from entidades.tipoCombustivel import TipoCombustivel

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
diretorio_pai = os.path.dirname(diretorio_atual)



class ControladorTipoCombustivel:
    def __init__(self):
        self.conn = sqlite3.connect(diretorio_pai + '/dados/DADOS.sqlite')
        self.cursor = self.conn.cursor()
        self.__tipoCombustivel = TipoCombustivel
        self.conn.commit()


    def adicionar_tipo_combustivel(self, nome: str, preco: float):
        tipoCombustivel = TipoCombustivel(nome, preco)
        if not isinstance(tipoCombustivel, TipoCombustivel):
            raise ValueError("O objeto fornecido não é uma instância da classe TipoCombustivel.")
        try:
            with self.conn:
                self.cursor.execute("INSERT INTO TipoCombustivel (nome, preco) VALUES ( ?, ?)",
                                    (tipoCombustivel.nome, tipoCombustivel.preco))
                self.conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            # Se houver uma violação de integridade (como chave duplicada), lança uma exceção
            if 'UNIQUE constraint failed: TipoCombustivel.nome' in str(e):
                raise ValueError("Erro: Nome já cadastrado.")
            else:
                raise
    
    def listar_tipo_combustivel(self):
        self.cursor.execute("SELECT * FROM TipoCombustivel")
        return self.cursor.fetchall()
    
    def buscar_tipo_combustivel(self, nome: str):
        self.cursor.execute("SELECT * FROM TipoCombustivel WHERE nome = ?", (nome,))
        return self.cursor.fetchone()

    
    def remover_tipo_combustivel(self, nome: str):
        with self.conn:
            self.cursor.execute("DELETE FROM TipoCombustivel WHERE nome = ?", (nome,))
            return self.cursor.rowcount > 0
        
    
    def atualizar_tipo_combustivel(self, nome: str, preco: float):
        tipoCombustivel = TipoCombustivel(nome, preco)
        try:
            with self.conn:
                self.cursor.execute("UPDATE TipoCombustivel SET nome = ?, preco = ? WHERE nome = ?",
                                    (tipoCombustivel.nome, tipoCombustivel.preco, tipoCombustivel.nome))
                self.conn.commit()
        except sqlite3.IntegrityError as e:
            # Se houver uma violação de integridade (como chave duplicada), lança uma exceção
            if 'UNIQUE constraint failed: TipoCombustivel.nome' in str(e):
                raise ValueError("Erro: Nome já cadastrado.")
            else:
                raise

    @property
    def novo_tipo_combustivel(self):
        return self.__tipoCombustivel
    
    @novo_tipo_combustivel.setter
    def novo_tipo_combustivel(self, value):
        self.__tipoCombustivel = value

    def __del__(self):
        self.conn.close()