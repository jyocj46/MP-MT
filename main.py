from caso1 import AgenteLogico
from caso2y3 import (
    extraer_proposiciones,
    aplicar_modus_ponens,
    aplicar_modus_tollens,
    detectar_regla,
    es_implicacion_valida
)

def analizar_tabla_verdad():
    agente = AgenteLogico()
    premisa2 = input("Premisa 2: ")
    conclusion = input("Conclusión (inicia con 'Por lo tanto'): ")
    
    p1 = agente.traducir_a_logica(global_premisa1)
    p2 = agente.traducir_a_logica(premisa2)
    conc = agente.traducir_a_logica(conclusion)
    
    print("\nTRADUCCIÓN:")
    print(f"Premisa 1: {p1}")
    print(f"Premisa 2: {p2}")
    print(f"Conclusión: {conc}")

    forma_logica = agente.generar_forma_logica([p1, p2], conc)
    print(f"\nFORMA LÓGICA: {forma_logica}")

    tabla = agente.generar_tabla_verdad([p1, p2], conc)
    print("\nTABLA DE VERDAD:")
    agente.mostrar_tabla_consola(tabla)
    
    print(f"\nRESULTADO: {agente.clasificar(tabla)}")

def analizar_mp_mt():
    antecedente, consecuente = extraer_proposiciones(global_premisa1)
    entrada = input("Ingrese (MP/MT) o la Premisa 2: ").strip()
    
    if entrada.upper() in ["MP", "MT"]:
        if entrada.upper() == "MP":
            aplicar_modus_ponens(antecedente, consecuente)
        else:
            aplicar_modus_tollens(antecedente, consecuente)
    else:
        regla = detectar_regla(antecedente, consecuente, entrada)
        if regla == "MP":
            aplicar_modus_ponens(antecedente, consecuente)
        elif regla == "MT":
            aplicar_modus_tollens(antecedente, consecuente)

def main():
    global global_premisa1
    print("=== AGENTE LÓGICO INTELIGENTE ===")
    
    while True:
        global_premisa1 = input("\nPremisa 1 (o 'salir'): ").strip()
        if global_premisa1.lower() == "salir":
            break
            
        if es_implicacion_valida(global_premisa1):
            analizar_mp_mt()
        else:
            analizar_tabla_verdad()

if __name__ == "__main__":
    main()