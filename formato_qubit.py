def formatear_componente(valor):
    if abs(valor) < 1e-9:
        return "0.000"
    valor_redondeado = round(valor, 3)
    if abs(valor_redondeado) < 1e-9:
        return "0.000"
    return f"{valor_redondeado:.3f}"


def formatear_amplitud(valor):
    parte_real = valor.real
    parte_imaginaria = valor.imag

    if abs(parte_real) < 1e-9 and abs(parte_imaginaria) < 1e-9:
        return "0.000"

    if abs(parte_imaginaria) < 1e-9:
        return formatear_componente(parte_real)

    if abs(parte_real) < 1e-9:
        texto_imaginario = formatear_componente(abs(parte_imaginaria))
        if parte_imaginaria >= 0:
            return f"{texto_imaginario}i"
        return f"-{texto_imaginario}i"

    texto_real = formatear_componente(parte_real)
    texto_imaginario = formatear_componente(abs(parte_imaginaria))
    if parte_imaginaria >= 0:
        return f"({texto_real} + {texto_imaginario}i)"
    return f"({texto_real} - {texto_imaginario}i)"


def formatear_estado(amplitud_0, amplitud_1):
    termino_0 = formatear_amplitud(amplitud_0)
    termino_1 = formatear_amplitud(amplitud_1)

    signo_1 = "+" if amplitud_1.real >= 0 and amplitud_1.imag >= 0 else "-"
    termino_1_sin_signo = termino_1.lstrip("-")

    if signo_1 == "+":
        return f"{termino_0} |0> + {termino_1_sin_signo} |1>"
    return f"{termino_0} |0> - {termino_1_sin_signo} |1>"
