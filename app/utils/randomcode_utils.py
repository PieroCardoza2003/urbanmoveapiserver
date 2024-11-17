import random
import string

def generar_codigo_unico() -> str:
    caracteres = string.ascii_uppercase + string.digits
    segmentos = [''.join(random.choices(caracteres, k=4)) for _ in range(3)]
    codigo_unico = '-'.join(segmentos)
    return codigo_unico
