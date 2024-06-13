from entidades.tipoCombustivel import TipoCombustivel
from entidades.tanqueCombustivel import TanqueCombustivel

class BombaCombustivel:
    def __init__(self, autoAbastecimento: bool, tipoCombustivel: str , bombaAtiva: bool, TanqueCombustivel: TanqueCombustivel, nomeBomba: str):
        self.__autoAbastecimento = autoAbastecimento
        self.__tipoCombustivel = tipoCombustivel
        self.__bombaAtiva = bombaAtiva
        self.__tanque = TanqueCombustivel
        self.__nomeBomba = nomeBomba

    @property
    def autoAbastecimento(self):
        return self.__autoAbastecimento
    
    @autoAbastecimento.setter
    def autoAbastecimento(self, value):
        self.__autoAbastecimento = value

    @property
    def tipoCombustivel(self):
        return self.__tipoCombustivel
    
    @tipoCombustivel.setter
    def tipoCombustivel(self, value):
        self.__tipoCombustivel = value
    
    @property
    def bombaAtiva(self):
        return self.__bombaAtiva
    
    @bombaAtiva.setter
    def bombaAtiva(self, value):
        self.__bombaAtiva = value

    @property
    def tanque(self):
        return self.__tanque
    
    @tanque.setter
    def tanque(self, value):
        self.__tanque = value

    @property
    def nomeBomba(self):
        return self.__nomeBomba
    
    @nomeBomba.setter
    def nomeBomba(self, value):
        self.__nomeBomba = value