from controladores.controladorPosto import ControladorPosto
from controladores.controladorTanqueCombustivel import ControladorTanqueCombustivel
from controladores.controladorAbastecimento import ControladorAbastecimento
from controladores.controladorBombaCombustivel import ControladorBombaCombustivel
from controladores.controladorTipoCombustivel import ControladorTipoCombustivel
from telas.telaSitemaPrincipal import MenuPrincipal
from telas.TelaLogin import TelaLogin


class ControladorSistema:
    def __init__(self) -> None:
        self.__TelaPrincipal = MenuPrincipal
        self.__controladorPosto = ControladorPosto()
        self.__controladorTanqueCombustivel = ControladorTanqueCombustivel()
        self.__controladorAbastecimento = ControladorAbastecimento()
        self.__controladorBombaCombustivel = ControladorBombaCombustivel()
        self.__controladorTipoCombustivel = ControladorTipoCombustivel()
        self.__TelaLogin = TelaLogin()

    @property
    def controladorPosto(self):
        return self.__controladorPosto
    
    @property
    def controladorTanqueCombustivel(self):
        return self.__controladorTanqueCombustivel
    
    @property
    def controladorAbastecimento(self):
        return self.__controladorAbastecimento
    
    @property
    def controladorBombaCombustivel(self):
        return self.__controladorBombaCombustivel

    @property
    def controladorTipoCombustivel(self):
        return self.__controladorTipoCombustivel
    @property
    def TelaPrincipal(self):
        return self.__TelaPrincipal
    
    @property
    def telaLogin(self):
        return self.__TelaLogin
    

    def iniciar(self):
        login = self.__TelaLogin.modal_login()
        if login[0]:
            is_gestor = login[1]
            self.__TelaPrincipal = MenuPrincipal(is_gestor)
            self.__TelaPrincipal.mainloop()
        else:
            self.iniciar()