def extraer_proposiciones(enunciado):
    try:
        # Eliminar espacios y dividir en partes clave
        partes = enunciado.lower().replace("si", "").split("entonces")
        antecedente = partes[0].strip().capitalize()
        consecuente = partes[1].strip().capitalize()
        return antecedente, consecuente
    except:
        print("Error: Formato inválido. Usa 'Si [antecedente] entonces [consecuente]'")
        return None, None

def es_implicacion_valida(premisa):
    premisa = premisa.lower().strip()
    if "si " in premisa and "entonces" in premisa:
        partes = premisa.split("entonces")
        return len(partes) == 2 and bool(partes[0].replace("si", "").strip())
    return False


def es_negacion(frase1, frase2):
    # Verifica si frase1 es la negación de frase2 (flexible)
    frase1_clean = frase1.lower().replace("no ", "").replace("nunca ", "").replace("ningún ", "").strip()
    frase2_clean = frase2.lower().replace("no ", "").replace("nunca ", "").replace("ningún ", "").strip()
    return (("no " in frase1.lower()) or ("nunca " in frase1.lower()) or ("ningún " in frase1.lower())) != \
           (("no " in frase2.lower()) or ("nunca " in frase2.lower()) or ("ningún " in frase2.lower())) and \
           frase1_clean == frase2_clean

def aplicar_modus_ponens(antecedente, consecuente):
    print(f"\nPremisa 1: Si {antecedente} entonces {consecuente}")
    print(f"Premisa 2: {antecedente}")
    print(f"Conclusión: Por lo tanto, {consecuente} (MP)")

def negar_enunciado(frase):
    palabras = frase.split()
    if len(palabras) > 1:
        # Insertar negación después del sujeto (mejor para español)
        if palabras[0].lower() in ["el", "la", "los", "las"]:
            palabras.insert(2, "no")
        else:
            palabras.insert(1, "no")
        return " ".join(palabras)
    else:
        return "No " + frase

def aplicar_modus_tollens(antecedente, consecuente):
    neg_consecuente = negar_enunciado(consecuente)
    neg_antecedente = negar_enunciado(antecedente)
    print(f"\nPremisa 1: Si {antecedente} entonces {consecuente}")
    print(f"Premisa 2: {neg_consecuente}")
    print(f"Conclusión: Por lo tanto, {neg_antecedente} (MT)")

def detectar_regla(antecedente, consecuente, premisa2):
    # Normalización para comparación flexible
    premisa2_norm = premisa2.lower().strip()
    antecedente_norm = antecedente.lower().strip()
    consecuente_norm = consecuente.lower().strip()
    
    # Caso Modus Ponens (Premisa2 == Antecedente)
    if premisa2_norm == antecedente_norm:
        return "MP"
    
    # Caso Modus Tollens (Premisa2 == Negación del Consecuente)
    neg_consecuente = negar_enunciado(consecuente).lower().strip()
    if premisa2_norm == neg_consecuente or es_negacion(premisa2, consecuente):
        return "MT"
    
    # Detectar negación del antecedente (para inferencia inversa)
    neg_antecedente = negar_enunciado(antecedente).lower().strip()
    if premisa2_norm == neg_antecedente:
        print("\n⚠ Nota: Esto sería una inferencia inversa (no es MP/MT estándar)")
        print(f"Si {antecedente} entonces {consecuente}")
        print(f"Pero: {neg_antecedente.capitalize()}")
        print("Esto no permite concluir nada sobre el consecuente directamente")
        return "INV"
    
    return None

