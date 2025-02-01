class FuncionarioLogado:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.funcionario = None
        return cls._instance

    def set_funcionario(self, funcionario):
        self.funcionario = funcionario

    def get_funcionario(self):
        return self.funcionario

    def get_id(self):
        return self.funcionario["ID"] if self.funcionario else None

    def get_nome(self):
        return self.funcionario["Nome"] if self.funcionario else None