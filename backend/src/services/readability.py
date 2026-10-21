import re

VOWELS = frozenset("aeiouáéíóúü")
OPEN_VOWELS = frozenset("aeoáéó")
ACCENTED_CLOSED_VOWELS = frozenset("íú")
WORD_PATTERN = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+")
SILENT_U_PATTERN = re.compile(r"(?<=[qg])u(?=[eéií])")


def count_syllables(word: str) -> int:
    normalized = SILENT_U_PATTERN.sub("", word.lower())
    vowel_groups = 0
    previous_vowel: str | None = None

    for character in normalized:
        if character not in VOWELS:
            previous_vowel = None
            continue

        hiatus = previous_vowel is not None and (
            (previous_vowel in OPEN_VOWELS and character in OPEN_VOWELS)
            or previous_vowel in ACCENTED_CLOSED_VOWELS
            or character in ACCENTED_CLOSED_VOWELS
        )
        if previous_vowel is None or hiatus:
            vowel_groups += 1
        previous_vowel = character

    return max(vowel_groups, 1)


def readability_label(score: float) -> str:
    if score < 40:
        return "muy difícil"
    if score < 55:
        return "algo difícil"
    if score < 65:
        return "normal"
    if score < 80:
        return "bastante fácil"
    return "muy fácil"


def calculate_readability(text: str) -> dict[str, float | str]:
    words = WORD_PATTERN.findall(text)
    if not words:
        score = 0.0
    else:
        syllables = sum(count_syllables(word) for word in words)
        sentence_count = max(len(re.findall(r"[.!?]+", text)), 1)
        score = 206.835 - 62.3 * (syllables / len(words)) - (len(words) / sentence_count)

    rounded_score = round(score, 2)
    return {"score": rounded_score, "label": readability_label(rounded_score)}
