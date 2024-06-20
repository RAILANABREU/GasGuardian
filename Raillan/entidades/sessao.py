class Sessao:
    _usuario = None

    @classmethod
    def iniciar_sessao(cls, usuario):
        cls._usuario = usuario

    @classmethod
    def encerrar_sessao(cls):
        cls._usuario = None

    @classmethod
    def get_usuario_logado(cls):
        return cls._usuario