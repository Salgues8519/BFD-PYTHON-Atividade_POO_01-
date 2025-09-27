from classe_carro import Carro

meu_carro = Carro("Preto", "Fusca", '1986')

voltas_completadas = 0
metros_por_volta = 5000
pausa_abastecimento = 0

print(f"--- Simulação de Corrida: {meu_carro.modelo} ---")

while voltas_completadas < 3:
    print(f"\n--- Volta {voltas_completadas + 1} ---")
    metros_percorridos = 0

    while metros_percorridos < metros_por_volta:
        print(f"\nDistância percorrida na volta: {metros_percorridos}m / {metros_por_volta}m")
        meu_carro.painel()

        if meu_carro.combustivel <= 8:
            print("Combustível insuficiente! Parada obrigatória para abastecer.")
            meu_carro.abastecer()
            meu_carro.ligar()
            pausa_abastecimento += 1

        meu_carro.acelerar()

        metros_percorridos += meu_carro.velocidade * 10

    voltas_completadas += 1
    meu_carro.velocidade = 0
    print(f"\n--- Volta {voltas_completadas} completada! ---")


print("\n--- FIM DA CORRIDA ---")
print(f"O {meu_carro.modelo} completou a corrida com {pausa_abastecimento} pontos de pausa para abastecimento.")