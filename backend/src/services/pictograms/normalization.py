import unicodedata

VERB_FORMS = {
    "aprende": "aprender",
    "aprenden": "aprender",
    "aprendio": "aprender",
    "ayuda": "ayudar",
    "ayudan": "ayudar",
    "bebe": "beber",
    "beben": "beber",
    "busca": "buscar",
    "buscan": "buscar",
    "canta": "cantar",
    "cantan": "cantar",
    "come": "comer",
    "comen": "comer",
    "cuenta": "contar",
    "cuentan": "contar",
    "dibuja": "dibujar",
    "dibujan": "dibujar",
    "duerme": "dormir",
    "duermen": "dormir",
    "empieza": "empezar",
    "empiezan": "empezar",
    "enseña": "enseñar",
    "ensena": "enseñar",
    "enseñan": "enseñar",
    "ensenen": "enseñar",
    "escucha": "escuchar",
    "escuchan": "escuchar",
    "espera": "esperar",
    "esperan": "esperar",
    "escribe": "escribir",
    "escriben": "escribir",
    "habla": "hablar",
    "hablan": "hablar",
    "juega": "jugar",
    "juegan": "jugar",
    "lee": "leer",
    "leen": "leer",
    "limpia": "limpiar",
    "limpian": "limpiar",
    "mira": "mirar",
    "miran": "mirar",
    "piensa": "pensar",
    "piensan": "pensar",
    "pinta": "pintar",
    "pintan": "pintar",
    "pregunta": "preguntar",
    "preguntan": "preguntar",
    "prepara": "preparar",
    "preparan": "preparar",
    "sale": "salir",
    "salen": "salir",
    "salta": "saltar",
    "saltan": "saltar",
    "termina": "terminar",
    "terminan": "terminar",
    "trabaja": "trabajar",
    "trabajan": "trabajar",
    "usa": "usar",
    "usan": "usar",
}


def normalize_word(value: str) -> str:
    decomposed = unicodedata.normalize("NFD", value.lower())
    return "".join(char for char in decomposed if unicodedata.category(char) != "Mn")


def lookup_forms(value: str) -> list[str]:
    normalized = normalize_word(value)
    forms = [normalized]
    if normalized.endswith("es") and len(normalized) > 4:
        forms.append(normalized[:-2])
    if normalized.endswith("s") and len(normalized) > 3:
        forms.append(normalized[:-1])
    infinitive = VERB_FORMS.get(normalized)
    if infinitive:
        forms.append(normalize_word(infinitive))
    return list(dict.fromkeys(forms))
