import re

class AgenteLogico:
    def __init__(self):
        self.connectors = {
            ' y ': ' ∧ ',
            ' o ': ' ∨ ',
            ' o bien ': ' ⊻ ',
            ' entonces ': ' → ',
            ' si y sólo si ': ' ↔ ',
            ' no ': '¬',
            'por lo tanto': ''
        }
        self.proposiciones = {}
        self.variables_disponibles = ['P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.indice_variable = 0

    def obtener_variable(self, texto_proposicion):
        texto_proposicion = texto_proposicion.strip().lower()
        if texto_proposicion not in self.proposiciones:
            if self.indice_variable < len(self.variables_disponibles):
                self.proposiciones[texto_proposicion] = self.variables_disponibles[self.indice_variable]
                self.indice_variable += 1
            else:
                num_extra = self.indice_variable - len(self.variables_disponibles) + 1
                self.proposiciones[texto_proposicion] = f'P{num_extra}'
                self.indice_variable += 1
        return self.proposiciones[texto_proposicion]

    def traducir_a_logica(self, texto):
        texto = texto.replace("Por lo tanto", "").replace(",", "").strip()
        temp_connectors = {
            ' y ': ' _CONJ_ ',
            ' o ': ' _DISY_ ',
            ' o bien ': ' _XDISY_ ',
            ' entonces ': ' _IMPL_ ',
            ' si y sólo si ': ' _EQUIV_ ',
            ' no ': ' _NEG_ '
        }
        for conector, temp in temp_connectors.items():
            texto = texto.replace(conector, temp)
        partes = re.split(r'(_CONJ_|_DISY_|_XDISY_|_IMPL_|_EQUIV_|_NEG_)', texto)
        expr_logica = ""
        for parte in partes:
            parte = parte.strip()
            if not parte:
                continue
            if parte == '_CONJ_':
                expr_logica += ' ∧ '
            elif parte == '_DISY_':
                expr_logica += ' ∨ '
            elif parte == '_XDISY_':
                expr_logica += ' ⊻ '
            elif parte == '_IMPL_':
                expr_logica += ' → '
            elif parte == '_EQUIV_':
                expr_logica += ' ↔ '
            elif parte == '_NEG_':
                expr_logica += '¬'
            else:
                expr_logica += self.obtener_variable(parte)
        return expr_logica.strip()

    def generar_forma_logica(self, premisas, conclusion):
        return f"({premisas[0]} → {premisas[1]}) → {conclusion}"

    def evaluar_expresion(self, expr, valores):
        expr = (expr.replace("∧", " and ")
                     .replace("∨", " or ")
                     .replace("⊻", " != ")
                     .replace("→", " <= ")
                     .replace("↔", " == ")
                     .replace("¬", " not "))
        return eval(expr, {}, valores)

    def generar_tabla_verdad(self, premisas, conclusion):
        variables = sorted(set(self.proposiciones.values()))
        n = len(variables)
        tabla = []
        for i in range(2**n):
            valores = {var: bool((i >> j) & 1) for j, var in enumerate(variables)}
            fila = {var: "V" if valores[var] else "F" for var in variables}
            p1_val = self.evaluar_expresion(premisas[0], valores)
            p2_val = self.evaluar_expresion(premisas[1], valores)
            conc_val = self.evaluar_expresion(conclusion, valores)
            impl_parcial = not p1_val or p2_val
            impl_final = not impl_parcial or conc_val
            fila.update({
                "P∧Q": "V" if p1_val else "F",
                "Q∨R": "V" if p2_val else "F",
                "(P∧Q)→(Q∨R)": "V" if impl_parcial else "F",
                "P∨R": "V" if conc_val else "F",
                "Resultado": "V" if impl_final else "F",
                "Premisa 1": "V" if p1_val else "F",
                "Premisa 2": "V" if p2_val else "F",
                "Conclusión": "V" if conc_val else "F"
            })
            tabla.append(fila)
        return tabla

    def mostrar_tabla_consola(self, tabla):
        variables = sorted([v for v in tabla[0].keys() if v not in ["Premisa 1", "Premisa 2", "Conclusión"]])
        headers = variables + ["Premisa 1", "Premisa 2", "Conclusión"]
        print(" | ".join(headers))
        print("-" * (len(" | ".join(headers))))
        for fila in tabla:
            valores = [fila[var] for var in variables] + [
                fila["Premisa 1"],
                fila["Premisa 2"],
                fila["Conclusión"]
            ]
            print(" | ".join(valores))

    def clasificar(self, tabla):
        es_falacia = any(
            fila["Premisa 1"] == "V" and 
            fila["Premisa 2"] == "V" and 
            fila["Conclusión"] == "F"
            for fila in tabla
        )
        todas_verdad = all(fila["Conclusión"] == "V" for fila in tabla)
        todas_falsa = all(fila["Conclusión"] == "F" for fila in tabla)
        if es_falacia:
            return "Falacia"
        elif todas_verdad:
            return "Tautología"
        elif todas_falsa:
            return "Contradicción"
        else:
            return "Contingencia"

def main():
    print("=== AGENTE LÓGICO UNIFICADO ===")
    print("Instrucciones: Ingrese premisas en lenguaje natural")

    agente = AgenteLogico()

    premisa1 = input("\nPrimera premisa: ")
    expr_logica1 = agente.traducir_a_logica(premisa1)

    if '→' in expr_logica1 or '↔' in expr_logica1:
        opcion = input("¿Deseas ingresar (mp/mt) o una segunda premisa? ").lower()
        if opcion in ["mp", "mt"]:
            segunda = input("Ingrese segunda premisa: ")
            p2 = agente.traducir_a_logica(segunda)
            if opcion == "mp":
                conclusion = input("Conclusión (será generada por modus ponens): ")
                conc = agente.traducir_a_logica(conclusion)
            else:
                conclusion = input("Conclusión (será generada por modus tollens): ")
                conc = agente.traducir_a_logica(conclusion)
        else:
            p2 = agente.traducir_a_logica(opcion)
            conclusion = input("Conclusión (inicia con 'Por lo tanto'): ")
            conc = agente.traducir_a_logica(conclusion)
        print(f"\nPremisa 1: {expr_logica1}")
        print(f"Premisa 2: {p2}")
        print(f"Conclusión: {conc}")
        forma = agente.generar_forma_logica([expr_logica1, p2], conc)
    else:
        premisa2 = input("Segunda premisa: ")
        conclusion = input("Conclusión (inicia con 'Por lo tanto'): ")
        p1 = expr_logica1
        p2 = agente.traducir_a_logica(premisa2)
        conc = agente.traducir_a_logica(conclusion)
        print(f"\nPremisa 1: {p1}")
        print(f"Premisa 2: {p2}")
        print(f"Conclusión: {conc}")
        forma = agente.generar_forma_logica([p1, p2], conc)

    print(f"\nFORMA LÓGICA:\n{forma}")

    tabla = agente.generar_tabla_verdad([p1, p2], conc)
    print("\nTABLA DE VERDAD:")
    agente.mostrar_tabla_consola(tabla)

    resultado = agente.clasificar(tabla)
    print("\nRESULTADO:")
    print(resultado)

if __name__ == "__main__":
    main()
