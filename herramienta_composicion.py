from src.models.consortium import BioproductSimulator

def main():
    print("Iniciando Simulador de Composición de Bioproductos...\n")
    
    # Perfil típico de residuos de frutas (coronas, cáscaras, pulpa) diluidos
    feedstock_fruta = {
        'azucares_simples': 120.0,   # Glucosa, fructosa, sacarosa
        'celulosa': 40.0,            # Fibra estructural
        'nitrogeno_organico': 15.0,  # Proteínas
        'minerales': 5.0             # K, Ca, Mg
    }
    
    # Escenario 1: Fermentación espontánea (Solo levaduras salvajes)
    consorcio_espontaneo = ['Levadura']
    sim1 = BioproductSimulator(feedstock_fruta, consorcio_espontaneo)
    print("ESCENARIO 1: Fermentación Alcohólica Simple")
    print(sim1.generate_report())
    print("\n")
    
    # Escenario 2: Consorcio Completo (Biol Enriquecido)
    consorcio_completo = ['Levadura', 'Lactobacillus', 'Bacillus']
    sim2 = BioproductSimulator(feedstock_fruta, consorcio_completo)
    print("ESCENARIO 2: Consorcio Completo (Biol Enriquecido)")
    print(sim2.generate_report())

if __name__ == "__main__":
    main()
