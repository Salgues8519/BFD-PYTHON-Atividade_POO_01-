import tkinter as tk
from tkinter import messagebox
from classe_carro import Carro

# ======================================================================
# Variáveis de Estado Global do Jogo (RAM)
# ======================================================================
# Cria as instâncias dos dois carros
CARRO_A = Carro("Preto", "Fusca", '1986')
CARRO_B = Carro("Vermelho", "Ferrari", '2025')

# Variáveis para armazenar as pontuações
JOGADORES_PAUSAS = {
    'Player 1': None, # Usará CARRO_A
    'Player 2': None  # Usará CARRO_B
}
JOGADORES = ['Player 1', 'Player 2']
JOGADOR_ATUAL_INDEX = 0

class CarroApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x400")
        self.master.configure(bg="#333333")

        self.iniciar_nova_partida()
        self.master.after(100, self.update_ui)
        
    def iniciar_nova_partida(self):
        self.jogador_atual = JOGADORES[JOGADOR_ATUAL_INDEX]
        
        # Define qual objeto Carro está sendo usado na rodada
        if self.jogador_atual == 'Player 1':
            self.meu_carro = CARRO_A
        else:
            self.meu_carro = CARRO_B

        self.meu_carro.velocidade = 0
        self.meu_carro.combustivel = 0 # Zera para forçar o abastecimento inicial
        self.meu_carro.ligado = False
        
        self.voltas_completadas = 0
        self.metros_percorridos = 0
        self.metros_por_volta = 2000
        self.pausas_abastecimento = 0

        self.setup_ui()
        self.master.title(f"Simulação de Corrida - {self.meu_carro.modelo} ({self.jogador_atual})")
        messagebox.showinfo("Início da Partida", f"Atenção, {self.jogador_atual}! Pressione OK para começar a corrida.")

    def setup_ui(self):
        # A interface é construída apenas uma vez, mas os labels são atualizados
        if not hasattr(self, 'main_frame'):
            self.main_frame = tk.Frame(self.master, bg="#333333")
            self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

            self.status_label = tk.Label(self.main_frame, text="Aperte 'Abastecer' para começar.", bg="#333333", fg="white", font=("Arial", 14))
            self.status_label.pack(pady=5)
            
            self.info_frame = tk.Frame(self.main_frame, bg="#333333")
            self.info_frame.pack(pady=5)

            self.modelo_label = tk.Label(self.info_frame, text="", bg="#333333", fg="white", font=("Arial", 12))
            self.modelo_label.pack()

            self.speed_label = tk.Label(self.info_frame, text="", bg="#333333", fg="white", font=("Arial", 12))
            self.speed_label.pack()
            
            self.fuel_label = tk.Label(self.info_frame, text="", bg="#333333", fg="white", font=("Arial", 12))
            self.fuel_label.pack()

            self.distance_label = tk.Label(self.info_frame, text="", bg="#333333", fg="white", font=("Arial", 12))
            self.distance_label.pack()

            self.laps_label = tk.Label(self.info_frame, text="", bg="#333333", fg="white", font=("Arial", 12))
            self.laps_label.pack()
            
            self.pausas_label = tk.Label(self.info_frame, text="", bg="#333333", fg="white", font=("Arial", 12))
            self.pausas_label.pack()

            # Botões de controle
            button_frame = tk.Frame(self.master, bg="#333333")
            button_frame.pack(pady=10)

            self.ligar_btn = tk.Button(button_frame, text="Ligar", command=self.ligar_carro, bg="#008080", fg="white")
            self.ligar_btn.pack(side="left", padx=5)

            self.desligar_btn = tk.Button(button_frame, text="Desligar", command=self.desligar_carro, bg="#404040", fg="white")
            self.desligar_btn.pack(side="left", padx=5)
            
            self.acelerar_frame = tk.Frame(button_frame, bg="#333333")
            self.acelerar_frame.pack(side="left", padx=10)
            
            self.acelerar_label = tk.Label(self.acelerar_frame, text="Acelerar:", bg="#333333", fg="white")
            self.acelerar_label.pack()

            self.acelerar1_btn = tk.Button(self.acelerar_frame, text="1 (5 km/h)", command=lambda: self.acelerar_carro(1), bg="#006400", fg="white")
            self.acelerar1_btn.pack(side="left", padx=2)
            
            self.acelerar2_btn = tk.Button(self.acelerar_frame, text="2 (10 km/h)", command=lambda: self.acelerar_carro(2), bg="#006400", fg="white")
            self.acelerar2_btn.pack(side="left", padx=2)
            
            self.acelerar3_btn = tk.Button(self.acelerar_frame, text="3 (15 km/h)", command=lambda: self.acelerar_carro(3), bg="#006400", fg="white")
            self.acelerar3_btn.pack(side="left", padx=2)
            
            self.frear_btn = tk.Button(button_frame, text="Frear", command=self.frear_carro, bg="#B22222", fg="white")
            self.frear_btn.pack(side="left", padx=5)

            self.abastecer_btn = tk.Button(button_frame, text="Abastecer", command=self.abastecer_carro, bg="#FFD700", fg="black")
            self.abastecer_btn.pack(side="left", padx=5)


    def update_ui(self):
        # Lógica de controle da corrida
        if self.meu_carro.combustivel < 8 and self.meu_carro.ligado:
            self.meu_carro.desligar()
            self.status_label.config(text="Combustível insuficiente! Parada obrigatória para abastecer.")
            
        self.modelo_label.config(text=f"Carro: {self.meu_carro.modelo} ({self.meu_carro.cor}) | Piloto: {self.jogador_atual}")
        self.speed_label.config(text=f"Velocidade: {self.meu_carro.velocidade} km/h")
        self.fuel_label.config(text=f"Combustível: {self.meu_carro.combustivel}%")
        self.distance_label.config(text=f"Distância: {self.metros_percorridos}m / {self.metros_por_volta}m")
        self.laps_label.config(text=f"Voltas: {self.voltas_completadas} / 3")
        self.pausas_label.config(text=f"Pausas para Abastecimento: {self.pausas_abastecimento}")

        if self.voltas_completadas >= 3:
            self.finalizar_volta()
        
        self.master.after(100, self.update_ui)

    def ligar_carro(self):
        self.status_label.config(text=self.meu_carro.ligar())
    
    def desligar_carro(self):
        self.status_label.config(text=self.meu_carro.desligar())

    def abastecer_carro(self):
        if self.meu_carro.combustivel < 100:
            self.pausas_abastecimento += 1
        resultado = self.meu_carro.abastecer()
        self.status_label.config(text=resultado)

    def acelerar_carro(self, nivel_aceleracao):
        velocidade_adicionada = 0
        consumo = 0
        metros_a_percorrer = 0
        
        if nivel_aceleracao == 1:
            velocidade_adicionada = 5
            consumo = 8
            metros_a_percorrer = 50
        elif nivel_aceleracao == 2:
            velocidade_adicionada = 10
            consumo = 12
            metros_a_percorrer = 100
        elif nivel_aceleracao == 3:
            velocidade_adicionada = 15
            consumo = 18
            metros_a_percorrer = 150
        
        resultado = self.meu_carro.acelerar(velocidade_adicionada, consumo)
        self.status_label.config(text=resultado)
        
        # A distância só é adicionada se o carro conseguiu acelerar
        if "Acelerando" in resultado or "Velocidade máxima" in resultado:
            self.metros_percorridos += metros_a_percorrer
            self.check_lap_completion()

    def frear_carro(self):
        self.meu_carro.frear(6)
        self.status_label.config(text=f"Freando... Velocidade: {self.meu_carro.velocidade} km/h. É um bom momento para abastecer!")

    def check_lap_completion(self):
        if self.metros_percorridos >= self.metros_por_volta:
            self.voltas_completadas += 1
            self.metros_percorridos = 0
            self.meu_carro.velocidade = 0
            
            if self.voltas_completadas < 3:
                messagebox.showinfo("Volta Concluída!", f"Volta {self.voltas_completadas} completada!")

    def finalizar_volta(self):
        global JOGADOR_ATUAL_INDEX
        
        # 1. Salva o resultado do jogador atual
        JOGADORES_PAUSAS[self.jogador_atual] = self.pausas_abastecimento
        
        # 2. Reseta e passa para o próximo jogador
        if JOGADOR_ATUAL_INDEX == 0:
            JOGADOR_ATUAL_INDEX = 1
            self.master.destroy() # Fecha a janela atual
            
            # Inicia o Player 2
            root = tk.Tk()
            app = CarroApp(root)
            root.mainloop()

        # 3. Se o segundo jogador terminou, exibe o vencedor
        else:
            self.determinar_vencedor()
            self.master.destroy()


    def determinar_vencedor(self):
        pausas_player1 = JOGADORES_PAUSAS['Player 1']
        pausas_player2 = JOGADORES_PAUSAS['Player 2']
        
        if pausas_player1 < pausas_player2:
            vencedor = "Player 1"
        elif pausas_player2 < pausas_player1:
            vencedor = "Player 2"
        else:
            vencedor = "Empate"
            
        resultado_final = (
            f"--- FIM DA CORRIDA ---\n\n"
            f"Resultados:\n"
            f"Player 1 ({CARRO_A.modelo}): {pausas_player1} Pausas\n"
            f"Player 2 ({CARRO_B.modelo}): {pausas_player2} Pausas\n\n"
            f"Vencedor: {vencedor}!"
        )
        messagebox.showinfo("Vencedor!", resultado_final)


# Inicializa a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = CarroApp(root)
    root.mainloop()