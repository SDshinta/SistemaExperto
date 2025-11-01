from .models import Regla

def motor_inferencia(hechos_usuario):
    # Cargar todas las reglas
    reglas = Regla.objects.all()

    # Crear estructura de pesos y explicaciones basada en las reglas
    pesos = {}
    explicaciones_humanas = {}

    for regla in reglas:
        hecho_key = regla.hecho  # es un string que debe coincidir con hecho.descripcion
        conclusion = regla.conclusion
        peso = regla.peso
        explicacion = regla.explicacion_humana or ""

        if hecho_key not in pesos:
            pesos[hecho_key] = {}

        pesos[hecho_key][conclusion] = peso
        if conclusion not in explicaciones_humanas:
            explicaciones_humanas[conclusion] = explicacion

    puntajes = {}
    hechos_por_conclusion = {}

    for hecho_usuario in hechos_usuario:
        if hecho_usuario in pesos:
            for conclusion, peso in pesos[hecho_usuario].items():
                puntajes[conclusion] = puntajes.get(conclusion, 0) + peso
                hechos_por_conclusion.setdefault(conclusion, []).append(hecho_usuario)

    # Ordenar conclusiones por puntaje descendente
    conclusiones_ordenadas = sorted(puntajes.items(), key=lambda x: x[1], reverse=True)

    resultado = []
    for conclusion, puntaje in conclusiones_ordenadas:
        if puntaje > 0:
            explicacion = explicaciones_humanas.get(conclusion, "")
            hechos_relacionados = hechos_por_conclusion.get(conclusion, [])
            resultado.append({
                'conclusion': conclusion,
                'puntaje': puntaje,
                'explicacion': explicacion,
                'hechos': ", ".join(hechos_relacionados)
            })

    return resultado
