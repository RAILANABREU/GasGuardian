import sqlite3
import os
from entidades.tanqueCombustivel import TanqueCombustivel

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
diretorio_pai = os.path.dirname(diretorio_atual)

class ControladorTanqueCombustivel:
    def __init__(self):
        self.conn = sqlite3.connect(diretorio_pai + '/dados/DADOS.sqlite')
        self.cursor = self.conn.cursor()
        self.__tanque = TanqueCombustivel
        self.conn.commit()

    @property
    def novo_tanque(self):
        return self.__tanque
    
    def adicionar_tanque(self, nome, capacidadeMaxima, porcentagemAlerta, tipoCombustivel, volumeAtual):

        novo_tanque = TanqueCombustivel(nome,capacidadeMaxima, porcentagemAlerta, tipoCombustivel, volumeAtual)

        try:
            with self.conn:
                self.cursor.execute("INSERT INTO Tanques (nome, capacidadeMaxima, porcentagemAlerta, tipoCombustivel_nome, volumeAtual) VALUES (?, ?, ?, ?, ?)",
                                    (novo_tanque.nome, novo_tanque.capacidadeMaxima, novo_tanque.porcentagemAlerta, novo_tanque.tipoCombustivel, novo_tanque.volumeAtual))
                self.conn.commit()
        except sqlite3.IntegrityError as e:
            # Se houver uma violação de integridade (como chave duplicada), lança uma exceção
            if 'UNIQUE constraint failed: Tanques.capacidadeMaxima' in str(e):
                raise ValueError("Erro: Capacidade Máxima já cadastrada.")
            elif 'UNIQUE constraint failed: Tanques.porcentagemAlerta' in str(e):
                raise ValueError("Erro: Porcentagem de Alerta já cadastrada.")
            else:
                raise

    def listar_tanques(self):
        # Executar a consulta SQL para obter todos os tanques com o nome do combustível
        self.cursor.execute("""
            SELECT t.id, t.nome, t.porcentagemAlerta, t.capacidadeMaxima, c.nome AS tipoCombustivel_nome, t.volumeAtual
            FROM Tanques t
            JOIN tipoCombustivel c ON t.tipoCombustivel_nome = c.nome
        """)
        
        # Obter todos os dados
        tanques = self.cursor.fetchall()

        # Adicionar o cálculo de Status para cada tanque
        tanques_atualizados = []
        for tanque in tanques:
            id, nome,porcentagemAlerta, capacidade, combustivel, volume_atual = tanque
            status = (volume_atual / capacidade) * 100 if capacidade else 0
            tanque_atualizado = (nome, porcentagemAlerta, capacidade, combustivel, volume_atual, status, id)
            tanques_atualizados.append(tanque_atualizado)
        
        return tanques_atualizados
    
    
    def buscar_tanque(self, identificadorTanque):
        # Buscar um tanque específico pelo Identificador
        self.cursor.execute("SELECT * FROM Tanques WHERE id = ?", (identificadorTanque,))
        return self.cursor.fetchone()
    
    def buscar_volume_atual_tanque(self, identificadorTanque):
        # Buscar o volume atual de um tanque específico pelo Identificador
        self.cursor.execute("SELECT volumeAtual FROM Tanques WHERE id = ?", (identificadorTanque,))
        return self.cursor.fetchone()

    def atualizar_volume_tanque(self, identificador_tanque, litros):
        try:
            # Obter o volume atual do tanque
            self.cursor.execute("SELECT volumeAtual FROM Tanques WHERE id = ?", (identificador_tanque,))
            resultado = self.cursor.fetchone()
            
            if resultado:
                volume_atual = resultado[0]
                novo_volume = volume_atual - litros
                
                # Atualizar o volume do tanque
                with self.conn:
                    self.cursor.execute("UPDATE Tanques SET volumeAtual = ? WHERE id = ?", (novo_volume, identificador_tanque))
                    self.conn.commit()
                    
                    if self.cursor.rowcount > 0:
                        print("Tanque atualizado com sucesso!")
                        return True
                    else:
                        print("Nenhum tanque encontrado com o identificador fornecido.")
                        return False
            else:
                print("Nenhum tanque encontrado com o identificador fornecido.")
                return False
                
        except sqlite3.Error as e:
            print(f"Erro ao atualizar o tanque: {e}")
            return False

        
    def remover_tanque(self, identificadorTanque):
        # Remover um tanque pelo Identificador
        try:
            with self.conn:
                self.cursor.execute("DELETE FROM Tanques WHERE id = ?", (identificadorTanque,))
                return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            return e    
    def atualizar_tanque(self,nome, capacidadeMaxima, porcentagemAlerta, tipoCombustivel, volumeAtual, identificadorTanque):
        tanque = TanqueCombustivel(nome, capacidadeMaxima, porcentagemAlerta, tipoCombustivel, volumeAtual)

        try:
            with self.conn:
                update_query = "UPDATE Tanques SET"
                update_values = []
                if tanque.nome is not None:
                    update_query += " nome = ?,"
                    update_values.append(tanque.nome)
                if tanque.capacidadeMaxima is not None:
                    update_query += " capacidadeMaxima = ?,"
                    update_values.append(tanque.capacidadeMaxima)
                if tanque.porcentagemAlerta is not None:
                    update_query += " porcentagemAlerta = ?,"
                    update_values.append(tanque.porcentagemAlerta)
                if tanque.tipoCombustivel is not None:
                    update_query += " tipoCombustivel_nome = ?,"
                    update_values.append(tanque.tipoCombustivel)
                if tanque.volumeAtual is not None:
                    update_query += " volumeAtual = ?,"
                    update_values.append(tanque.volumeAtual)
                update_query = update_query.rstrip(",") + " WHERE id = ?"
                update_values.append(identificadorTanque)
                self.cursor.execute(update_query, update_values)
                self.conn.commit()
                if self.cursor.rowcount > 0:
                    print("Tanque atualizado com sucesso!")
                    return True
                else:
                    print("Nenhum tanque encontrado com o identificador fornecido.")
                    return False
        except sqlite3.Error as e:
            print(f"Erro ao atualizar o tanque: {e}")
            return False

    def __del__(self):
        self.conn.close()
