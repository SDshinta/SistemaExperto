# backward_motor.py

HECHOS = {
    'no_enciende': '¿El computador no enciende?',
    'ventilador_no_gira': '¿El ventilador no gira?',
    'pantalla_negra': '¿La pantalla está negra?',
    'sonido_pitido': '¿Se escucha un sonido de pitido?',
    'parpadea_luz': '¿Parpadea la luz?',
    'se_apaga_solo': '¿El equipo se apaga solo?',
    'calienta_demasiado': '¿El equipo calienta demasiado?',
    'puertos_usb_no_funcionan': '¿Los puertos USB no funcionan?',
    'teclado_no_responde': '¿El teclado no responde?',
    'windows_no_arranca': '¿Windows no arranca?',
    'arranque_lento': '¿El arranque es lento?',
}

REGLAS = [
    {'condicion': 'no_enciende', 'conclusion': 'Fallo en fuente de poder', 'explicacion': 'El equipo no enciende, puede ser la fuente de poder.'},
    {'condicion': 'ventilador_no_gira', 'conclusion': 'Fallo en sistema de ventilación', 'explicacion': 'El ventilador no gira, posible fallo en el sistema de ventilación.'},
    {'condicion': 'pantalla_negra', 'conclusion': 'Problema en tarjeta gráfica', 'explicacion': 'La pantalla está negra, puede ser la tarjeta gráfica.'},
    {'condicion': 'sonido_pitido', 'conclusion': 'Memoria RAM defectuosa', 'explicacion': 'Se escucha pitido, posible problema en la memoria RAM.'},
    {'condicion': 'parpadea_luz', 'conclusion': 'Fallo en fuente de poder', 'explicacion': 'La luz parpadea, puede ser un fallo en la fuente de poder.'},
    {'condicion': 'se_apaga_solo', 'conclusion': 'Fallo en fuente de poder', 'explicacion': 'El equipo se apaga solo, posible problema en la fuente de poder.'},
    {'condicion': 'calienta_demasiado', 'conclusion': 'Fallo en sistema de ventilación', 'explicacion': 'El equipo calienta mucho, fallo probable en ventilación.'},
    {'condicion': 'puertos_usb_no_funcionan', 'conclusion': 'Controlador USB dañado', 'explicacion': 'Los puertos USB no funcionan, controlador USB dañado.'},
    {'condicion': 'teclado_no_responde', 'conclusion': 'Conector del teclado dañado', 'explicacion': 'El teclado no responde, conector dañado.'},
    {'condicion': 'windows_no_arranca', 'conclusion': 'Sistema operativo dañado', 'explicacion': 'Windows no arranca, sistema operativo dañado.'},
    {'condicion': 'arranque_lento', 'conclusion': 'Disco duro viejo', 'explicacion': 'Arranque lento, disco duro posiblemente viejo.'},
]

def backward_chaining(conclusion_objetivo, respuestas_usuario):
    # Busca todas las reglas que tengan esa conclusion
    reglas_relacionadas = [r for r in REGLAS if r['conclusion'] == conclusion_objetivo]
    if not reglas_relacionadas:
        return False, "No existen reglas para esa conclusión."

    for regla in reglas_relacionadas:
        hecho = regla['condicion']
        # Pregunta si la respuesta del usuario para este hecho es 'si'
        if respuestas_usuario.get(hecho) == 'si':
            return True, regla['explicacion']

    return False, "No se pudo confirmar la conclusión."
