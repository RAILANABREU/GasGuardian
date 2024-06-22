from entidades.tipoCombustivel import TipoCombustivel

class TanqueCombustivel:
    def __init__(self,nome, capacidadeMaxima, porcentagemAlerta,TipoCombustivel,volumeAtual ):
        self.__nome = nome
        self.__identificadorTanque = None
        self.__capacidadeMaxima = capacidadeMaxima
        self.__porcentagemAlerta = porcentagemAlerta
        self.__tipoCombustivel = TipoCombustivel #subistituir quando o paixao subir a branch para o objeto tipo de combustivel.
        self.__volumeAtual = volumeAtual

    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, value):
        self.__nome = value

    @property
    def capacidadeMaxima(self):
        return self.__capacidadeMaxima

    @capacidadeMaxima.setter
    def capacidadeMaxima(self, value):
        self.__capacidadeMaxima = value

    @property
    def porcentagemAlerta(self):
        return self.__porcentagemAlerta

    @porcentagemAlerta.setter
    def porcentagemAlerta(self, value):
        self.__porcentagemAlerta = value

    @property
    def tipoCombustivel(self):
        return self.__tipoCombustivel

    @tipoCombustivel.setter
    def tipoCombustivel(self, value):
        self.__tipoCombustivel = value

    @property
    def volumeAtual(self):
        return self.__volumeAtual

    @volumeAtual.setter
    def volumeAtual(self, value):
        self.__volumeAtual = value

    @property
    def identificadorTanque(self):
        return self.__identificadorTanque
