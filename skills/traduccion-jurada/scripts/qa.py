#!/usr/bin/env python3
"""
Verificacion previa a la entrega de una traduccion jurada.

    python3 qa.py "20260825 - Traduccion X (EN).docx"

Sale 1 si hay hallazgos ERROR. Los AVISO son para revisar a ojo.
Lo que este script NO puede ver: que el contenido corresponda al documento correcto,
que los nombres esten bien escritos, y que las etiquetas del encabezado (mes, cuenta,
titular) correspondan a los datos del cuerpo. Eso es revision humana.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from docx import Document
from docx.enum.text import WD_TAB_LEADER
from docx.shared import Inches, Pt

FUENTE, TAMANO, INTER = "Arial", 10.0, 1.5
MARGENES = {"left": 1.18, "right": 1.32, "bottom": 2.25}
TAB = 6.0

# (patron, flags, nivel, mensaje). La regla de [Sic] va sin re.I a proposito:
# con re.I atrapaba tambien el "[Sic]" bien escrito y ninguna traduccion que lo
# usara podia pasar el QA.
MACHOTE_VIEJO = [
    (r"may\s+deemed", re.I, 'ERROR', '"may deemed" -> "may deem convenient"'),
    (r"into\s+their\s+main\s+part", re.I, 'ERROR',
     '"into their main part" -> "in its/their main part"'),
    (r"\[(?!Sic\])[Ss][Ii][Cc]\]", 0, 'ERROR', '"[Sic]" mal escrito (unica forma: [Sic])'),
    (r"Tax\s+Over\s+Rent", re.I, 'AVISO', '"Tax Over Rent" -> "Income Tax"'),
    (r"\[(Sello|Stamp)[^\]]*(que lee|that reads)", re.I, 'AVISO',
     'forma obsoleta "[Sello que lee: ...]" -> "[Sello]" + la traduccion afuera'),
]

hallazgos = []


def falla(nivel, msg):
    hallazgos.append((nivel, msg))


def texto_completo(doc):
    partes = [p.text for p in doc.paragraphs]
    for t in doc.tables:
        for fila in t.rows:
            for celda in fila.cells:
                partes.append(celda.text)
    return "\n".join(partes)


def revisar_formato(doc):
    sec = doc.sections[0]
    for nombre, esperado in MARGENES.items():
        real = round(getattr(sec, f"{nombre}_margin").inches, 3)
        if abs(real - esperado) > 0.02:
            falla("ERROR", f'margen {nombre}: {real}" (esperado {esperado}")')

    # valores por defecto del estilo Normal: es de donde heredan los runs sin
    # formato directo, asi que un documento mal basado se detecta aqui.
    normal = doc.styles["Normal"]
    if normal.font.name and normal.font.name != FUENTE:
        falla("ERROR", f"el estilo Normal usa {normal.font.name}, no Arial")
    if normal.font.size and round(normal.font.size.pt, 1) != TAMANO:
        falla("ERROR", f"el estilo Normal usa {normal.font.size.pt} pt, no 10")
    ls_normal = normal.paragraph_format.line_spacing
    if ls_normal and round(float(ls_normal), 2) != INTER:
        falla("ERROR", f"el estilo Normal usa interlineado {ls_normal}, no 1.5")

    fuentes, tamanos, interlineados, sin_tab = set(), set(), set(), 0
    for p in doc.paragraphs:
        if not p.text.strip():
            continue
        for r in p.runs:
            if r.font.name:
                fuentes.add(r.font.name)
            if r.font.size:
                tamanos.add(round(r.font.size.pt, 1))
        if p.paragraph_format.line_spacing:
            interlineados.add(round(float(p.paragraph_format.line_spacing), 2))
        tabs = [t for t in p.paragraph_format.tab_stops
                if t.leader == WD_TAB_LEADER.DASHES]
        if not tabs:
            sin_tab += 1
        elif not any(abs(t.position.inches - TAB) < 0.02 for t in tabs):
            falla("AVISO", f'tabulador de guiones fuera de 6.0": {p.text[:40]!r}')
        if not p.text.endswith("\t"):
            falla("AVISO", f"parrafo sin tabulacion final, quedaria sin guiones: "
                           f"{p.text[:50]!r}")

    otras = fuentes - {FUENTE}
    if otras:
        falla("ERROR", f"fuentes distintas de Arial: {sorted(otras)}")
    raros = tamanos - {TAMANO}
    if raros:
        falla("ERROR", f"tamanos distintos de 10 pt: {sorted(raros)}")
    if interlineados - {INTER}:
        falla("ERROR", f"interlineados distintos de 1.5: {sorted(interlineados)}")
    if sin_tab:
        falla("ERROR", f"{sin_tab} parrafos sin tabulador de guiones definido")

    pie = doc.sections[0].footer
    xml = pie._element.xml if pie is not None else ""
    if "PAGE" not in xml:
        falla("ERROR", "el pie de pagina no tiene campo PAGE")


def revisar_corchetes(texto):
    profundidad, linea_abierta = 0, None
    for n, linea in enumerate(texto.split("\n"), 1):
        for ch in linea:
            if ch == "[":
                profundidad += 1
                linea_abierta = linea_abierta or n
            elif ch == "]":
                profundidad -= 1
                if profundidad < 0:
                    falla("ERROR", f"corchete de cierre sin apertura, linea {n}")
                    profundidad = 0
        if profundidad == 0:
            linea_abierta = None
    if profundidad > 0:
        falla("ERROR", f"corchete sin cerrar, abre en linea {linea_abierta}")


def revisar_formulas(texto):
    for patron, flags, nivel, msg in MACHOTE_VIEJO:
        if re.search(patron, texto, flags):
            falla(nivel, msg)

    es = "EN FE DE LO CUAL" in texto
    en = "IN WITNESS WHEREOF" in texto
    if not (es or en):
        falla("ERROR", "no aparece la formula de cierre")
    if es and en:
        falla("ERROR", "aparecen las dos formulas de cierre")
    if not re.search(r"(Traductora Jurada|sworn translator)", texto):
        falla("ERROR", "no aparece el acta de apertura")
    if "346-DDEGN-2018" not in texto:
        falla("ERROR", "falta el numero de resolucion en las credenciales")

    # concordancia singular/plural entre enumeracion y formula
    romanos = re.findall(r"\b(i{1,3}|iv|v)\)", texto[:1500], re.I)
    n = len(set(r.lower() for r in romanos))
    if n:
        plural_es = "los cuales se leen" in texto
        plural_en = "in their main part" in texto
        if n == 1 and (plural_es or plural_en):
            falla("ERROR", "un solo documento enumerado pero la formula esta en plural")
        if n > 1 and (("el cual se lee" in texto) or ("in its main part" in texto)):
            falla("ERROR", f"{n} documentos enumerados pero la formula esta en singular")


def revisar_hojas(ruta, texto):
    m = re.search(r"contenida en (\d+|N) hojas? de papel bond", texto)
    if not m:
        m = re.search(r"translation in (\d+|N) bond pages?", texto)
    if not m:
        falla("ERROR", "el cierre no declara el numero de hojas")
        return
    if m.group(1) == "N":
        falla("ERROR", "el cierre todavia tiene el marcador N en vez del numero de hojas")
        return
    declaradas = int(m.group(1))

    paginas = contar_paginas(ruta)
    if paginas is None:
        falla("AVISO", f"declara {declaradas} hojas; no se pudo contar paginas reales")
    elif paginas != declaradas:
        falla("ERROR", f"declara {declaradas} hojas pero el documento tiene {paginas}")


def contar_paginas(ruta):
    with tempfile.TemporaryDirectory() as tmp:
        try:
            subprocess.run(
                ["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, str(ruta)],
                capture_output=True, timeout=180, check=True,
            )
        except Exception:
            return None
        pdfs = list(Path(tmp).glob("*.pdf"))
        if not pdfs:
            return None
        try:
            salida = subprocess.run(["pdfinfo", str(pdfs[0])],
                                    capture_output=True, text=True, check=True).stdout
        except Exception:
            return None
        m = re.search(r"Pages:\s+(\d+)", salida)
        return int(m.group(1)) if m else None


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    ruta = Path(sys.argv[1])
    doc = Document(ruta)
    texto = texto_completo(doc)

    revisar_formato(doc)
    revisar_corchetes(texto)
    revisar_formulas(texto)
    revisar_hojas(ruta, texto)

    errores = [h for h in hallazgos if h[0] == "ERROR"]
    if not hallazgos:
        print("QA limpio.")
    for nivel, msg in hallazgos:
        print(f"{nivel}: {msg}")
    print(f"\n{len(errores)} error(es), {len(hallazgos) - len(errores)} aviso(s).")
    print("Falta revision humana: contenido correcto, nombres propios, y que los rotulos "
          "del encabezado correspondan al cuerpo.")
    sys.exit(1 if errores else 0)


if __name__ == "__main__":
    main()
