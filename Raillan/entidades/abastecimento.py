from entidades.tipoCombustivel import TipoCombustivel

class Abastecimento:
    def __init__(self, idBomba: str, tipoCombustivel: str , data: str, preco: float, litros: float, cpf_funcionario):
        self.__idBomba = idBomba
        self.__tipoCombustivel = tipoCombustivel
        self.__data = data
        self.__litros = litros
        self.__preco = preco
        self.__cpf_funcionario  

    @property
    def idBomba(self):
        return self.__idBomba
    
    @property
    def tipoCombustivel(self):
        return self.__tipoCombustivel
    
    @property
    def data(self):
        return self.__data
    
    @property
    def litros(self):
        return self.__litros
    
    @property
    def preco(self):
        return self.__preco
    
    @preco.setter
    def preco(self, value):
        self.__preco = value

    @litros.setter
    def litros(self, value):
        self.__litros = value

    @data.setter
    def data(self, value):
        self.__data = value

    @property
    def cpf_funcionario(self):
        return self.__cpf_funcionario

    @cpf_funcionario.setter
    def cpf_funcionario(self, value):
        self.__cpf_funcionario = value

    
