
class Carro:

    def __init__(self, cor, modelo, ano="Ano não informado"):
        self.cor = cor
        self.modelo = modelo
        self.ano = ano
        self.ligado = False
        self.velocidade = 0
        self.velocidade_maxima = 220
        self.combustivel = 0
        self.combustivel_maximo = 100

    def ligar(self):
        if not self.ligado and self.combustivel > 0:
            self.ligado = True
            return "O carro está ligado."
        elif self.ligado:
            return "O carro já está ligado."
        else:
            return "Carro sem combustível."

    def desligar(self):
        if self.ligado:
            self.ligado = False
            self.velocidade = 0
            return "O carro está desligado."
        else:
            return "O carro já está desligado."

    def acelerar(self, valor_velocidade, consumo_combustivel):
        if self.ligado and self.combustivel >= consumo_combustivel:
            nova_velocidade = self.velocidade + valor_velocidade
            if nova_velocidade <= self.velocidade_maxima:
                self.velocidade = nova_velocidade
                self.combustivel -= consumo_combustivel
                return "Acelerando..."
            else:
                self.velocidade = self.velocidade_maxima
                self.combustivel -= consumo_combustivel
                return "Velocidade máxima atingida!"
        else:
            self.velocidade = 0
            return "Não é possível acelerar. Carro desligado ou sem combustível."

    def painel(self):
        pass
    
    def frear(self, valor):
        if self.velocidade - valor >= 0:
            self.velocidade -= valor
            return "Freando..."
        else:
            self.velocidade = 0
            return "O carro parou."
    
    def abastecer(self):
        if self.combustivel < self.combustivel_maximo:
            self.combustivel = self.combustivel_maximo
            return "Tanque cheio!"
        else:
            return "Tanque já está cheio."

    def status(self):
        status_ligado = 'Ligado' if self.ligado else 'Desligado'
        return f"Modelo: {self.modelo} | Cor: {self.cor} | Status: {status_ligado}"