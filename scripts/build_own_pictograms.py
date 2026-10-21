from __future__ import annotations

import json
from pathlib import Path

OUTPUT = Path(__file__).resolve().parents[1] / "backend" / "assets" / "pictograms" / "own"
INK = "#2B2B2B"
SAGE = "#4F7D63"
TERRACOTTA = "#E07A5F"
SKY = "#DCEBF5"
BUTTER = "#FBEFC9"
PEACH = "#FBE1D6"
LILAC = "#E9E3F5"
CREAM = "#FBF7F0"


def person(cx: int, shirt: str, hair: str, skirt: bool = False) -> str:
    lower = (
        f'<path d="M{cx - 24} 174h48l-7 58h-34z" fill="{TERRACOTTA}"/>'
        if skirt
        else f'<path d="M{cx - 23} 173h46l7 62h-20l-10-38-10 38h-20z" fill="{SAGE}"/>'
    )
    return (
        f'<circle cx="{cx}" cy="96" r="30" fill="{PEACH}"/>'
        f'<path d="M{cx - 29} 91q2-35 30-35 27 0 29 32l-14-13-18 7-18-5z" fill="{hair}"/>'
        f'<circle cx="{cx - 10}" cy="98" r="3" fill="{INK}" stroke="none"/>'
        f'<circle cx="{cx + 10}" cy="98" r="3" fill="{INK}" stroke="none"/>'
        f'<path d="M{cx - 8} 113q8 8 16 0" fill="none"/>'
        f'<path d="M{cx - 22} 145q22-16 44 0l12 34h-68z" fill="{shirt}"/>'
        f'<path d="M{cx - 20} 153l-23 33m65-33 23 33" fill="none"/>'
        f"{lower}"
        f'<path d="M{cx - 12} 235v30m24-30v30" fill="none"/>'
        f'<path d="M{cx - 19} 267h16m6 0h16" fill="none"/>'
    )


ICONS: list[tuple[str, list[str], str]] = [
    ("nino", ["niño", "nino", "chico", "alumno"], person(150, SAGE, "#6B4B3E")),
    ("nina", ["niña", "nina", "chica", "alumna"], person(150, LILAC, "#6B4B3E", True)),
    ("profesor", ["profesor", "maestro", "docente"], person(150, SKY, "#3E3A39")),
    ("profesora", ["profesora", "maestra", "docente"], person(150, TERRACOTTA, "#3E3A39", True)),
    (
        "familia",
        ["familia", "familiares"],
        f'<circle cx="150" cy="80" r="95" fill="{BUTTER}" stroke="none"/>'
        + person(105, SAGE, "#6B4B3E")
        + person(195, TERRACOTTA, "#3E3A39", True)
        + f'<circle cx="150" cy="166" r="21" fill="{PEACH}"/>'
        + f'<path d="M124 205q26-30 52 0l7 35h-66z" fill="{LILAC}"/>',
    ),
    (
        "colegio",
        ["colegio", "escuela", "colegios", "escuelas"],
        f'<path d="M45 114 150 45l105 69v132H45z" fill="{SKY}"/>'
        f'<path d="M37 116 150 39l113 77" fill="none"/>'
        f'<rect x="72" y="139" width="42" height="44" rx="6" fill="{BUTTER}"/>'
        f'<rect x="186" y="139" width="42" height="44" rx="6" fill="{BUTTER}"/>'
        f'<path d="M125 246v-68h50v68" fill="{TERRACOTTA}"/>'
        f'<circle cx="161" cy="211" r="3" fill="{INK}" stroke="none"/>',
    ),
    (
        "clase",
        ["clase", "aula", "salón"],
        f'<rect x="39" y="40" width="222" height="119" rx="12" fill="{SAGE}"/>'
        f'<rect x="58" y="58" width="184" height="82" rx="6" fill="{CREAM}"/>'
        f'<path d="M71 103h54m13 0h89" fill="none"/>'
        f'<path d="M54 177h76v18H54zm116 0h76v18h-76z" fill="{BUTTER}"/>'
        f'<path d="M66 195v55m50-55v55m66-55v55m50-55v55" fill="none"/>',
    ),
    (
        "libro",
        ["libro", "libros", "lectura"],
        f'<path d="M45 72q50-18 105 9v158q-52-26-105-8z" fill="{SKY}"/>'
        f'<path d="M255 72q-50-18-105 9v158q52-26 105-8z" fill="{PEACH}"/>'
        f'<path d="M150 81v158m-82-125q28-5 58 8m-58 23q28-5 58 8m26-31q30-13 58-8m-58 31q30-13 58-8" fill="none"/>',
    ),
    (
        "leer",
        ["leer", "leyendo", "lectora", "lector"],
        person(116, LILAC, "#6B4B3E")
        + f'<path d="M166 194q34-19 68 0v52q-34-19-68 0z" fill="{SKY}"/>'
        f'<path d="M166 194v52m13-39 39 0m-39 16 39 0" fill="none"/>',
    ),
    (
        "escribir",
        ["escribir", "escribe", "escribiendo"],
        f'<rect x="35" y="164" width="230" height="25" rx="12" fill="{BUTTER}"/>'
        f'<path d="M70 189v65m160-65v65" fill="none"/>'
        f'<circle cx="115" cy="83" r="29" fill="{PEACH}"/>'
        f'<path d="M85 81q3-37 31-37 26 0 29 34l-20-13-21 7z" fill="#6B4B3E"/>'
        f'<path d="M88 132q27-18 55 0l14 42H74z" fill="{SAGE}"/>'
        f'<path d="m131 150 71 59-12 14-71-59z" fill="{TERRACOTTA}"/>'
        f'<path d="m191 223 12-14 6 23z" fill="{INK}"/>',
    ),
    (
        "lapiz",
        ["lápiz", "lapiz", "lápices"],
        f'<path d="m79 220 30 30L229 130l-30-30z" fill="{TERRACOTTA}"/>'
        f'<path d="m199 100 30 30 18-18-30-30z" fill="{BUTTER}"/>'
        f'<path d="m79 220 30 30-46 16z" fill="{PEACH}"/>'
        f'<path d="m109 250 120-120m-150 120 15-15" fill="none"/>',
    ),
    (
        "cuaderno",
        ["cuaderno", "cuadernos", "libreta"],
        f'<rect x="66" y="38" width="171" height="224" rx="17" fill="{LILAC}"/>'
        f'<path d="M103 39v222" fill="none"/>'
        f'<path d="M124 91h86m-86 35h86m-86 35h86m-86 35h86" fill="none"/>'
        f'<circle cx="84" cy="83" r="5" fill="{CREAM}"/><circle cx="84" cy="133" r="5" fill="{CREAM}"/><circle cx="84" cy="183" r="5" fill="{CREAM}"/>',
    ),
    (
        "mochila",
        ["mochila", "mochilas", "bolsa escolar"],
        f'<path d="M93 94q0-49 57-49t57 49l21 32v113H72V126z" fill="{SAGE}"/>'
        f'<path d="M112 95q0-27 38-27t38 27" fill="none"/>'
        f'<rect x="105" y="152" width="90" height="62" rx="18" fill="{SKY}"/>'
        f'<path d="M150 151v65m-39-30h78" fill="none"/>'
        f'<path d="M72 128q-25 28-18 78m174-78q25 28 18 78" fill="none"/>',
    ),
    (
        "mesa",
        ["mesa", "mesas"],
        f'<rect x="41" y="91" width="218" height="47" rx="13" fill="{TERRACOTTA}"/>'
        f'<path d="M65 139v115m170-115v115" fill="none"/>'
        f'<path d="M79 180h142" fill="none"/>'
        f'<circle cx="148" cy="69" r="17" fill="{BUTTER}"/>',
    ),
    (
        "silla",
        ["silla", "sillas"],
        f'<rect x="88" y="48" width="125" height="112" rx="18" fill="{SKY}"/>'
        f'<rect x="75" y="150" width="151" height="39" rx="12" fill="{SAGE}"/>'
        f'<path d="M91 189v73m118-73v73" fill="none"/>'
        f'<path d="M91 240h-24m142 0h24" fill="none"/>',
    ),
    (
        "pizarra",
        ["pizarra", "pizarras", "encerado"],
        f'<rect x="36" y="45" width="228" height="162" rx="12" fill="{SAGE}"/>'
        f'<rect x="54" y="63" width="192" height="126" rx="5" fill="#EAF1DF"/>'
        f'<path d="M78 106h70m-70 38h127m-82 63v51m52-51v51m-87 0h123" fill="none"/>'
        f'<circle cx="202" cy="95" r="16" fill="{BUTTER}"/>',
    ),
    (
        "ordenador",
        ["ordenador", "computadora", "computador", "pantalla"],
        f'<rect x="36" y="46" width="228" height="153" rx="18" fill="{LILAC}"/>'
        f'<rect x="55" y="64" width="190" height="117" rx="9" fill="{SKY}"/>'
        f'<path d="M150 199v35m-39 0h78" fill="none"/>'
        f'<path d="m84 124 27 24m-27-24 27-24m31 49h44" fill="none"/>',
    ),
    (
        "comer",
        ["comer", "come", "comiendo"],
        f'<ellipse cx="151" cy="182" rx="100" ry="47" fill="{SKY}"/>'
        f'<ellipse cx="151" cy="174" rx="62" ry="27" fill="{CREAM}"/>'
        f'<path d="M64 62v74m-14-74v35m28-35v35m-14 39v61m124-98q25 26 0 53v44" fill="none"/>'
        f'<circle cx="151" cy="169" r="14" fill="{TERRACOTTA}"/>'
        f'<circle cx="181" cy="177" r="10" fill="{BUTTER}"/>',
    ),
    (
        "beber",
        ["beber", "bebe", "bebiendo"],
        f'<path d="M103 82h94l-12 156h-70z" fill="{SKY}"/>'
        f'<path d="M111 149q37 14 78 0" fill="none"/>'
        f'<path d="M197 106h22q34 0 21 39t-47 26" fill="none"/>'
        f'<path d="M140 52q-24 29 0 38m31-47q-24 29 0 38" fill="none"/>',
    ),
    (
        "agua",
        ["agua", "aguas", "gota"],
        f'<path d="M150 38q-73 92-73 139a73 73 0 0 0 146 0q0-47-73-139z" fill="{SKY}"/>'
        f'<path d="M109 180q19 15 39 0t42 0" fill="none"/>'
        f'<path d="M125 216q13 10 26 0t27 0" fill="none"/>',
    ),
    (
        "dormir",
        ["dormir", "duerme", "durmiendo", "sueño"],
        f'<path d="M48 160h204v79H48z" fill="{SKY}"/>'
        f'<path d="M62 160v-38h62q38 0 38 38m-114 79v22m181-22v22" fill="none"/>'
        f'<circle cx="94" cy="143" r="24" fill="{PEACH}"/>'
        f'<path d="M194 54a38 38 0 1 0 49 48 44 44 0 0 1-49-48z" fill="{BUTTER}"/>',
    ),
    (
        "casa",
        ["casa", "casas", "hogar"],
        f'<path d="M42 132 150 43l108 89v118H42z" fill="{PEACH}"/>'
        f'<path d="m30 135 120-99 120 99" fill="none"/>'
        f'<rect x="122" y="174" width="57" height="76" rx="7" fill="{TERRACOTTA}"/>'
        f'<rect x="65" y="157" width="42" height="42" rx="6" fill="{SKY}"/>'
        f'<rect x="194" y="157" width="42" height="42" rx="6" fill="{SKY}"/>',
    ),
    (
        "jugar",
        ["jugar", "juega", "jugando", "juego"],
        person(102, SAGE, "#6B4B3E")
        + f'<circle cx="218" cy="207" r="42" fill="{TERRACOTTA}"/>'
        f'<path d="M180 207h76m-38-42q-20 42 0 84m-30-72 59 60m0-60-59 60" fill="none"/>'
        f'<path d="m131 155 45 25" fill="none"/>',
    ),
    (
        "parque",
        ["parque", "jardín", "jardin"],
        f'<circle cx="103" cy="110" r="49" fill="{SAGE}"/>'
        f'<circle cx="166" cy="86" r="58" fill="#79A67F"/>'
        f'<circle cx="219" cy="122" r="40" fill="{SAGE}"/>'
        f'<path d="M164 137v110m-69-15h131m-112-26h93m-83 0v41m73-41v41" fill="none"/>'
        f'<path d="M63 246h174" fill="none"/>',
    ),
    (
        "patio",
        ["patio", "patios", "exterior"],
        f'<path d="M45 230h210M70 230V84h160v146" fill="none"/>'
        f'<path d="M112 84v91m76-91v91m-76 0q38 52 76 0" fill="none"/>'
        f'<circle cx="150" cy="219" r="26" fill="{TERRACOTTA}"/>'
        f'<path d="M150 193v52m-26-26h52" fill="none"/>',
    ),
    (
        "recreo",
        ["recreo", "descanso", "juego"],
        f'<circle cx="89" cy="93" r="35" fill="{BUTTER}"/>'
        f'<path d="M55 208q42-38 84 0l11 45H44z" fill="{SAGE}"/>'
        f'<circle cx="211" cy="93" r="35" fill="{PEACH}"/>'
        f'<path d="M177 208q42-38 84 0l11 45h-106z" fill="{LILAC}"/>'
        f'<circle cx="151" cy="205" r="25" fill="{TERRACOTTA}"/>'
        f'<path d="M126 205h50m-25-25v50" fill="none"/>',
    ),
    (
        "musica",
        ["música", "musica", "canción", "cancion"],
        f'<path d="M120 63v140q0 29-31 29-28 0-28-23 0-27 59-30m0-116 104-23v140q0 29-31 29-28 0-28-23 0-27 59-30V40" fill="none"/>'
        f'<circle cx="76" cy="209" r="18" fill="{TERRACOTTA}"/>'
        f'<circle cx="181" cy="209" r="18" fill="{LILAC}"/>',
    ),
    (
        "pintar",
        ["pintar", "pinta", "pintando", "pintura"],
        f'<rect x="42" y="45" width="161" height="158" rx="13" fill="{SKY}"/>'
        f'<path d="M71 239 156 82q11-19 30-9t8 29l-91 143z" fill="{TERRACOTTA}"/>'
        f'<path d="m71 239-9 22 28-16" fill="{BUTTER}"/>'
        f'<path d="M224 50q24 22 0 44t-24 44" fill="none"/>',
    ),
    (
        "contar",
        ["contar", "cuenta", "contando"],
        f'<path d="M54 224V87m48 137V66m48 158V97m48 127V73m48 151V111" fill="none"/>'
        f'<circle cx="54" cy="78" r="17" fill="{TERRACOTTA}"/>'
        f'<circle cx="102" cy="56" r="17" fill="{SAGE}"/>'
        f'<circle cx="150" cy="87" r="17" fill="{LILAC}"/>'
        f'<circle cx="198" cy="63" r="17" fill="{BUTTER}"/>'
        f'<circle cx="246" cy="101" r="17" fill="{PEACH}"/>'
        f'<path d="M39 224h222" fill="none"/>',
    ),
    (
        "numeros",
        ["números", "numeros", "número", "numero"],
        f'<rect x="42" y="54" width="92" height="92" rx="17" fill="{SKY}"/>'
        f'<rect x="166" y="54" width="92" height="92" rx="17" fill="{BUTTER}"/>'
        f'<rect x="42" y="170" width="92" height="92" rx="17" fill="{PEACH}"/>'
        f'<rect x="166" y="170" width="92" height="92" rx="17" fill="{LILAC}"/>'
        f'<circle cx="88" cy="100" r="12" fill="{SAGE}"/>'
        f'<circle cx="207" cy="92" r="10" fill="{TERRACOTTA}"/><circle cx="232" cy="112" r="10" fill="{TERRACOTTA}"/>'
        f'<circle cx="75" cy="203" r="9" fill="{SAGE}"/><circle cx="101" cy="203" r="9" fill="{SAGE}"/><circle cx="88" cy="229" r="9" fill="{SAGE}"/>'
        f'<circle cx="190" cy="192" r="8" fill="{TERRACOTTA}"/><circle cx="231" cy="192" r="8" fill="{TERRACOTTA}"/><circle cx="190" cy="234" r="8" fill="{TERRACOTTA}"/><circle cx="231" cy="234" r="8" fill="{TERRACOTTA}"/>',
    ),
    (
        "letras",
        ["letras", "letra", "abecedario"],
        f'<rect x="43" y="82" width="86" height="139" rx="16" fill="{TERRACOTTA}"/>'
        f'<rect x="171" y="82" width="86" height="139" rx="16" fill="{SAGE}"/>'
        f'<path d="M72 180q0-49 27-49 25 0 25 49m-52-17h51m45-29h57m-28 0v59m-29 0h57" fill="none"/>'
        f'<path d="M61 239h177" fill="none"/>',
    ),
    (
        "palabra",
        ["palabra", "palabras", "frase"],
        f'<path d="M44 63q0-19 19-19h174q19 0 19 19v111q0 19-19 19h-71l-48 49v-49H63q-19 0-19-19z" fill="{SKY}"/>'
        f'<circle cx="104" cy="119" r="9" fill="{SAGE}"/><circle cx="150" cy="119" r="9" fill="{TERRACOTTA}"/><circle cx="196" cy="119" r="9" fill="{LILAC}"/>',
    ),
    (
        "pregunta",
        ["pregunta", "preguntar", "preguntas"],
        f'<path d="M44 56q0-18 18-18h140q18 0 18 18v96q0 18-18 18h-44l-38 41v-41H62q-18 0-18-18z" fill="{BUTTER}"/>'
        f'<circle cx="112" cy="102" r="25" fill="{PEACH}"/>'
        f'<path d="M112 88q0-15 15-15 16 0 16 14 0 10-15 19v12m0 18v2" fill="none"/>'
        f'<circle cx="228" cy="221" r="30" fill="{SKY}"/>'
        f'<path d="m211 221 12 12 24-27" fill="none"/>',
    ),
    (
        "escuchar",
        ["escuchar", "escucha", "oyendo"],
        f'<path d="M91 143V119q0-61 59-61t59 61v39q0 31-25 40-16 6-18 27-2 24-27 24-24 0-24-26 0-42 34-56 14-6 14-24v-18q0-14-14-14t-14 14v17" fill="{PEACH}"/>'
        f'<path d="M237 102q26 24 0 48m18-64q42 40 0 80" fill="none"/>',
    ),
    (
        "hablar",
        ["hablar", "habla", "hablando", "decir"],
        person(120, SAGE, "#6B4B3E")
        + f'<path d="M147 52h106v72h-38l-28 28v-28h-40z" fill="{SKY}"/>'
        f'<circle cx="176" cy="88" r="5" fill="{TERRACOTTA}" stroke="none"/>'
        f'<circle cx="201" cy="88" r="5" fill="{TERRACOTTA}" stroke="none"/>'
        f'<circle cx="226" cy="88" r="5" fill="{TERRACOTTA}" stroke="none"/>',
    ),
    (
        "mirar",
        ["mirar", "mira", "mirando", "ver"],
        f'<path d="M31 150q47-73 119-73t119 73q-47 73-119 73T31 150z" fill="{SKY}"/>'
        f'<circle cx="150" cy="150" r="43" fill="{SAGE}"/>'
        f'<circle cx="150" cy="150" r="19" fill="{CREAM}"/>'
        f'<circle cx="150" cy="150" r="8" fill="{INK}" stroke="none"/>',
    ),
    (
        "pensar",
        ["pensar", "piensa", "pensando"],
        f'<circle cx="135" cy="133" r="80" fill="{LILAC}"/>'
        f'<path d="M81 151q0-48 54-48 47 0 47 39 0 34-37 40l-13 26-12-25q-39-5-39-32z" fill="{PEACH}"/>'
        f'<circle cx="220" cy="76" r="26" fill="{SKY}"/>'
        f'<circle cx="255" cy="42" r="12" fill="{BUTTER}"/>'
        f'<path d="M119 148h1m29 0h1m-19 20q9 7 18 0" fill="none"/>',
    ),
    (
        "ayudar",
        ["ayudar", "ayuda", "ayudando", "apoyar"],
        f'<path d="M45 155q30-34 62 0l43 42q12 13-1 26-12 11-25 0l-24-20" fill="{SKY}"/>'
        f'<path d="M255 155q-30-34-62 0l-43 42q-12 13 1 26 12 11 25 0l24-20" fill="{PEACH}"/>'
        f'<path d="M150 197q-31-27-47-6-14 18 4 36l43 38 43-38q18-18 4-36-16-21-47 6z" fill="{TERRACOTTA}"/>',
    ),
    (
        "esperar",
        ["esperar", "espera", "esperando"],
        f'<circle cx="150" cy="128" r="83" fill="{BUTTER}"/>'
        f'<circle cx="150" cy="128" r="59" fill="{CREAM}"/>'
        f'<path d="M150 85v47l33 20" fill="none"/>'
        f'<path d="M92 221q58-35 116 0v32H92z" fill="{SAGE}"/>'
        f'<path d="M113 252v19m74-19v19" fill="none"/>',
    ),
    (
        "terminar",
        ["terminar", "termina", "terminado", "acabar"],
        f'<path d="M67 45v209m0-190q71 30 144 0v88q-73 30-144 0z" fill="{TERRACOTTA}"/>'
        f'<path d="M93 87h82m-82 34h82" fill="none"/>'
        f'<circle cx="67" cy="47" r="14" fill="{SAGE}"/>'
        f'<path d="m176 219 17 17 37-42" fill="none"/>',
    ),
    (
        "empezar",
        ["empezar", "empieza", "comenzar", "inicio"],
        f'<path d="M55 238h190M82 211V90m136 121V90" fill="none"/>'
        f'<path d="M82 90h136l-30 57 30 57H82z" fill="{BUTTER}"/>'
        f'<circle cx="150" cy="119" r="17" fill="{SAGE}"/>'
        f'<path d="M150 139v42m0-42-22 22m22-22 22 22m-22 20-17 23m17-23 17 23" fill="none"/>',
    ),
    (
        "si",
        ["sí", "si", "afirmar", "correcto"],
        f'<circle cx="150" cy="150" r="108" fill="{SAGE}"/>'
        f'<path d="m91 154 39 39 82-88" fill="none" stroke="{CREAM}" stroke-width="18"/>',
    ),
    (
        "no",
        ["no", "negación", "negacion"],
        f'<circle cx="150" cy="150" r="108" fill="{PEACH}"/>'
        f'<circle cx="150" cy="150" r="72" fill="none" stroke="{TERRACOTTA}" stroke-width="17"/>'
        f'<path d="m101 101 98 98" fill="none" stroke="{TERRACOTTA}" stroke-width="17"/>',
    ),
    (
        "contento",
        ["contento", "contenta", "alegre", "feliz"],
        f'<circle cx="150" cy="150" r="108" fill="{BUTTER}"/>'
        f'<circle cx="112" cy="127" r="7" fill="{INK}" stroke="none"/>'
        f'<circle cx="188" cy="127" r="7" fill="{INK}" stroke="none"/>'
        f'<path d="M99 170q51 58 102 0" fill="none"/>',
    ),
    (
        "triste",
        ["triste", "tristeza"],
        f'<circle cx="150" cy="150" r="108" fill="{SKY}"/>'
        f'<circle cx="112" cy="127" r="7" fill="{INK}" stroke="none"/>'
        f'<circle cx="188" cy="127" r="7" fill="{INK}" stroke="none"/>'
        f'<path d="M103 207q47-58 94 0" fill="none"/>'
        f'<path d="M204 148q-19 27-5 42 16-13 5-42z" fill="{SKY}"/>',
    ),
    (
        "enfadado",
        ["enfadado", "enfadada", "enfado", "molesto"],
        f'<circle cx="150" cy="150" r="108" fill="{PEACH}"/>'
        f'<path d="m92 112 38 13m78-13-38 13" fill="none"/>'
        f'<circle cx="119" cy="140" r="7" fill="{INK}" stroke="none"/>'
        f'<circle cx="181" cy="140" r="7" fill="{INK}" stroke="none"/>'
        f'<path d="M112 203q38-52 76 0" fill="none"/>',
    ),
    (
        "cansado",
        ["cansado", "cansada", "cansancio", "agotado"],
        f'<circle cx="150" cy="150" r="108" fill="{LILAC}"/>'
        f'<path d="M93 127h43m28 0h43" fill="none"/>'
        f'<circle cx="116" cy="136" r="6" fill="{INK}" stroke="none"/>'
        f'<circle cx="184" cy="136" r="6" fill="{INK}" stroke="none"/>'
        f'<path d="M119 203q31-25 62 0" fill="none"/>'
        f'<path d="M226 53h28l-20 20h20" fill="none" stroke="{SAGE}"/>',
    ),
    (
        "bano",
        ["baño", "bano", "aseo", "inodoro"],
        f'<path d="M89 58h122v94H89z" fill="{SKY}"/>'
        f'<path d="M63 153h174q-6 73-87 73t-87-73z" fill="{CREAM}"/>'
        f'<path d="M112 228v25m76-25v25m-78 0h80" fill="none"/>'
        f'<circle cx="150" cy="196" r="9" fill="{SAGE}"/>',
    ),
    (
        "lavarse-las-manos",
        ["lavarse las manos", "lavarse", "lavar", "manos", "lavado"],
        f'<path d="M81 167q0-14 13-14 12 0 12 13v-47q0-13 12-13t12 13v38-58q0-13 12-13t12 13v56-39q0-13 12-13t12 13v51q0 60-47 60-33 0-45-28z" fill="{PEACH}"/>'
        f'<path d="M54 57q-18 22 0 43m191-43q18 22 0 43" fill="none" stroke="{SKY}"/>'
        f'<path d="M112 247h78" fill="none"/>'
        f'<rect x="206" y="163" width="39" height="54" rx="8" fill="{SAGE}"/>'
        f'<path d="M216 163v-15h20v15" fill="none"/>',
    ),
    (
        "autobus",
        ["autobús", "autobus", "bus", "autobuses"],
        f'<rect x="36" y="67" width="228" height="152" rx="30" fill="{BUTTER}"/>'
        f'<path d="M51 126h198" fill="none"/>'
        f'<rect x="54" y="85" width="51" height="34" rx="6" fill="{SKY}"/>'
        f'<rect x="124" y="85" width="51" height="34" rx="6" fill="{SKY}"/>'
        f'<rect x="194" y="85" width="51" height="34" rx="6" fill="{SKY}"/>'
        f'<circle cx="82" cy="221" r="24" fill="{INK}"/>'
        f'<circle cx="218" cy="221" r="24" fill="{INK}"/>'
        f'<circle cx="82" cy="221" r="9" fill="{CREAM}" stroke="none"/>'
        f'<circle cx="218" cy="221" r="9" fill="{CREAM}" stroke="none"/>',
    ),
    (
        "sol",
        ["sol", "soleado", "soles"],
        f'<circle cx="150" cy="150" r="62" fill="{BUTTER}"/>'
        f'<path d="M150 27v39m0 168v39M27 150h39m168 0h39M63 63l28 28m118 118 28 28m0-174-28 28M91 209l-28 28" fill="none" stroke="{TERRACOTTA}"/>'
        f'<circle cx="130" cy="145" r="5" fill="{INK}" stroke="none"/>'
        f'<circle cx="170" cy="145" r="5" fill="{INK}" stroke="none"/>'
        f'<path d="M129 173q21 17 42 0" fill="none"/>',
    ),
]


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    index = []
    for pictogram_id, keywords, drawing in ICONS:
        filename = f"{pictogram_id}.svg"
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300" '
            f'fill="none" stroke="{INK}" stroke-width="10" '
            'stroke-linecap="round" stroke-linejoin="round">'
            f'<rect x="12" y="12" width="276" height="276" rx="46" fill="{CREAM}" stroke="none"/>'
            f"{drawing}</svg>\n"
        )
        (OUTPUT / filename).write_text(svg, encoding="utf-8")
        index.append({"id": pictogram_id, "file": filename, "keywords": keywords})
    (OUTPUT / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(index)} own pictograms to {OUTPUT}")


if __name__ == "__main__":
    main()
