"""Genera la PPT de la Semana 13 a partir de la plantilla del curso.

Uso (desde la raíz del repositorio):
    python presentacion/build_ppt.py
    python presentacion/build_ppt.py --github https://github.com/USUARIO/escape-room-bec
    python presentacion/build_ppt.py --github https://github.com/USUARIO/escape-room-bec --resultados resultados.csv

Sin --resultados, la tabla queda con "__" para llenarla después.
Con --resultados, calcula todo con analisis.py y llena la diapositiva de experimentación.
Requiere: pip install python-pptx pandas scipy
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.opc.packuri import PackURI
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
sys.path.insert(0, str(RAIZ))

OR = RGBColor(0xFF, 0x3A, 0x00)
SOFT = RGBColor(0xFF, 0xE3, 0xD9)
INK = RGBColor(0x1A, 0x1A, 0x1A)
GREY = RGBColor(0x6B, 0x6B, 0x6B)
CARD = RGBColor(0xF2, 0xF2, 0xF2)
LINE = RGBColor(0xD0, 0xD0, 0xD0)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0, 0, 0)
FONT = "Verdana"
VACIO = "__"


# ---------------------------------------------------------------- formato
def num(x: float | None, nd: int = 2) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return VACIO
    return f"{x:.{nd}f}".replace(".", ",")


def pval(p: float | None) -> str:
    if p is None or (isinstance(p, float) and math.isnan(p)):
        return f"p = {VACIO}"
    return "p < 0,001" if p < 0.001 else f"p = {num(p, 3)}"


# ---------------------------------------------------------------- helpers
class Builder:
    def __init__(self, plantilla: Path):
        self.prs = Presentation(str(plantilla))
        self.lst = self.prs.slides._sldIdLst

    def renumber(self) -> None:
        sl = list(self.prs.slides)
        for i, x in enumerate(sl):
            x.part.partname = PackURI(f"/ppt/slides/tmp{i + 1}.xml")
        for i, x in enumerate(sl):
            x.part.partname = PackURI(f"/ppt/slides/slide{i + 1}.xml")

    def drop(self, index: int) -> None:
        sid = list(self.lst)[index]
        self.prs.part.drop_rel(sid.rId)
        self.lst.remove(sid)

    def new_slide(self, title: str):
        self.renumber()
        layout = next(l for l in self.prs.slide_layouts if l.name == "TITLE_ONLY")
        s = self.prs.slides.add_slide(layout)
        for ph in list(s.placeholders):
            ph._element.getparent().remove(ph._element)
        t = tb(s, 0.45, 0.3, 8.8, 0.45)
        run(t.paragraphs[0], title, 18, OR, True)
        return s


def run(p, t, size, color=INK, bold=False, italic=False):
    r = p.add_run()
    r.text = t
    r.font.name, r.font.size, r.font.bold, r.font.italic = FONT, Pt(size), bold, italic
    r.font.color.rgb = color
    return r


def tb(s, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    t = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
    t.word_wrap = True
    t.vertical_anchor = anchor
    t.margin_left = t.margin_right = Inches(0.03)
    t.margin_top = t.margin_bottom = Inches(0)
    return t


def shp(s, kind, x, y, w, h, fill=None, line=None, adj=None):
    sh = s.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    if adj is not None:
        sh.adjustments[0] = adj
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(1)
    sh.shadow.inherit = False
    return sh


def set_text(sh, paragraphs):
    """paragraphs: lista de párrafos; cada párrafo = lista de (texto, tamaño, color, negrita)."""
    tf = sh.text_frame
    for p in list(tf.paragraphs)[1:]:
        p._p.getparent().remove(p._p)
    p0 = tf.paragraphs[0]
    for r in list(p0.runs):
        r._r.getparent().remove(r._r)
    for i, para in enumerate(paragraphs):
        p = p0 if i == 0 else tf.add_paragraph()
        for t, size, color, bold in para:
            run(p, t, size, color, bold)


def table(s, x, y, colw, rows, row_h, size, header_fill=OR, center_from=None):
    gs = s.shapes.add_table(len(rows), len(colw), Inches(x), Inches(y), Inches(sum(colw)), Inches(row_h * len(rows)))
    tbl = gs.table
    tblPr = tbl._tbl.tblPr
    tblPr.set("bandRow", "0")
    tblPr.set("firstRow", "0")
    sid = tblPr.find(qn("a:tableStyleId"))
    if sid is not None:
        sid.text = "{5940675A-B579-460E-94D1-54222C63F5DA}"
    for j, w in enumerate(colw):
        tbl.columns[j].width = Inches(w)
    for i, r in enumerate(rows):
        tbl.rows[i].height = Inches(row_h)
        for j, v in enumerate(r):
            c = tbl.cell(i, j)
            c.fill.solid()
            c.fill.fore_color.rgb = header_fill if i == 0 else WHITE
            c.margin_top = c.margin_bottom = Inches(0.02)
            c.margin_left = c.margin_right = Inches(0.07)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            para = c.text_frame.paragraphs[0]
            if center_from is not None and j >= center_from:
                para.alignment = PP_ALIGN.CENTER
            run(para, v, size, WHITE if i == 0 else INK, i == 0 or j == 0)
            tcPr = c._tc.get_or_add_tcPr()
            for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
                ln = etree.SubElement(tcPr, qn(tag), w="6350")
                sf = etree.SubElement(ln, qn("a:solidFill"))
                etree.SubElement(sf, qn("a:srgbClr"), val="D0D0D0")
            fill = tcPr.find(qn("a:solidFill"))
            tcPr.remove(fill)
            tcPr.append(fill)
    return tbl


# ---------------------------------------------------------------- slides
def portada(b: Builder, capturas: Path) -> None:
    cover = b.prs.slides[0]
    for sh in list(cover.shapes):
        txt = sh.text_frame.text if sh.has_text_frame else ""
        if txt.startswith("Título del artículo"):
            set_text(sh, [[("Effectiveness of a competence- and game-based learning environment using a digital "
                            "educational escape room for promoting cybersecurity competence in apprentices", 15, WHITE, True)]])
            sh.top, sh.height = Inches(0.95), Inches(1.15)
        elif txt.startswith("(Autores"):
            set_text(sh, [[("Thomas Keller · University of Hohenheim", 10, WHITE, False)]])
            sh.left, sh.top, sh.width = Inches(2.9), Inches(2.18), Inches(4.4)
            sh.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        elif txt.startswith("Revista"):
            set_text(sh, [[("Revista: ", 9, OR, True), ("Computers & Security, 171", 9, WHITE, False)],
                          [("Año de publicación: ", 9, OR, True), ("2026", 9, WHITE, False)],
                          [("Cuartil: ", 9, OR, True), ("Q1 (SJR)", 9, WHITE, False)],
                          [("DOI: ", 9, OR, True), ("10.1016/j.cose.2026.105120", 9, WHITE, False)]])
            sh.left, sh.top, sh.width, sh.height = Inches(4.75), Inches(2.6), Inches(4.2), Inches(0.9)
            sh.text_frame.word_wrap = True
            for para in sh.text_frame.paragraphs:
                pPr = para._p.get_or_add_pPr()
                for old in pPr.findall(qn("a:buChar")) + pPr.findall(qn("a:buAutoNum")):
                    pPr.remove(old)
                etree.SubElement(pPr, qn("a:buNone"))
                pPr.set("marL", "0")
                pPr.set("indent", "0")
        elif txt.startswith("Nombre del alumno"):
            set_text(sh, [[("Apaza Raymundo Renato Marcelino", 10.5, WHITE, True)]])
            sh.left, sh.top, sh.width = Inches(4.75), Inches(3.65), Inches(4.2)
            sh.text_frame.paragraphs[0].alignment = PP_ALIGN.LEFT
        elif txt.startswith("Si desean"):
            sh._element.getparent().remove(sh._element)
    pic = cover.shapes.add_picture(str(capturas / "ss_intro.png"), Inches(0.55), Inches(2.55), width=Inches(3.0))
    pic.line.color.rgb = OR
    pic.line.width = Pt(1)


def workflow(b: Builder) -> None:
    s = b.new_slide("Workflow de la investigación")
    steps = [
        ("1", "Selección", "Keller (2026), Computers & Security, Q1"),
        ("2", "Adaptación al BEC", "Escape room de ingeniería social → 5 misiones con correos BEC"),
        ("3", "Instrumento", "Test situacional de 7 dimensiones (0-14 pts), formas A y B"),
        ("4", "Prototipo", "Web HTML/JS en GitHub Pages: coach, pistas, feedback e insignias"),
        ("5", "Experimento", "Asignación al azar: grupo juego vs. grupo control, test antes y después"),
        ("6", "Análisis", "Ganancias, Mann-Whitney, g de Hedges y ANCOVA; comparación con Keller"),
    ]
    W, G, Y = 1.42, 0.12, 0.95
    for i, (n, h, d) in enumerate(steps):
        x = 0.45 + i * (W + G)
        shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, Y, W, 1.95, CARD, adj=0.08)
        c = shp(s, MSO_SHAPE.OVAL, x + 0.12, Y + 0.12, 0.42, 0.42, OR)
        ct = c.text_frame
        ct.margin_left = ct.margin_right = Inches(0)
        ct.paragraphs[0].alignment = PP_ALIGN.CENTER
        run(ct.paragraphs[0], n, 12, WHITE, True)
        t = tb(s, x + 0.12, Y + 0.65, W - 0.22, 1.25)
        p = t.paragraphs[0]
        p.space_after = Pt(3)
        run(p, h, 10, INK, True)
        run(t.add_paragraph(), d, 8, INK)
        if i < len(steps) - 1:
            shp(s, MSO_SHAPE.CHEVRON, x + W + 0.015, Y + 0.85, 0.09, 0.2, OR)

    t = tb(s, 0.45, 3.1, 9, 0.3)
    run(t.paragraphs[0], "¿Qué se mantiene y qué cambia respecto al artículo original?", 10.5, INK, True)
    table(s, 0.45, 3.42, [1.5, 3.75, 3.85], [
        ["", "Keller (2026)", "Esta réplica"],
        ["Tema del juego", "Ingeniería social, contraseñas y datos", "Fraude BEC (falso gerente y proveedor)"],
        ["Participantes", "154 aprendices, 2 escuelas (Alemania)", "Compañeros de clase (piloto)"],
        ["Diseño", "Aleatorizado por aulas, con grupo de control", "Aleatorizado por persona, con grupo de control"],
        ["Mediciones", "Antes, 1 semana después y 8 semanas después", "Antes y después, en la misma sesión"],
        ["Análisis", "Modelo de cambio latente", "Ganancias, Mann-Whitney, ANCOVA"],
    ], row_h=0.26, size=8)


def experimentacion(b: Builder, capturas: Path, github: str, res: dict | None) -> None:
    s = b.new_slide("Experimentación: prototipo y resultados")
    h = 2.6 * 620 / 760
    for k, name in enumerate(("ss_m1.png", "ss_badge.png")):
        pic = s.shapes.add_picture(str(capturas / name), Inches(0.45), Inches(0.9 + k * (h + 0.08)), width=Inches(2.6))
        pic.line.color.rgb = LINE
    t = tb(s, 0.45, 5.25, 2.8, 0.2)
    run(t.paragraphs[0], "Misión 1 con pista de la coach · insignia + reflexión", 7, GREY, italic=True)

    g = (res or {}).get("grupos", {})
    J, C = g.get("Juego", {}), g.get("Control", {})
    n_total = str(res["n_total"]) if res else VACIO

    X0 = 3.45
    t = tb(s, X0, 0.9, 3.0, 0.3)
    run(t.paragraphs[0], "Diseño del experimento", 11, INK, True)

    def pill(x, y, w, text, fill, color=INK, bold=False, h=0.36):
        bx = shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill, adj=0.3)
        tf = bx.text_frame
        tf.margin_left = tf.margin_right = Inches(0.04)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        run(tf.paragraphs[0], text, 8, color, bold)

    pill(X0, 1.3, 2.95, f"Participantes (n = {n_total}) · asignación al azar", BLACK, WHITE, True)
    pill(X0, 1.85, 1.4, "Grupo juego", OR, WHITE, True)
    pill(X0 + 1.55, 1.85, 1.4, "Grupo control", CARD, INK, True)
    for k, (a, c2) in enumerate([("Test A (antes)", "Test A (antes)"), ("Escape room ~10 min", "—"),
                                 ("Test B (después)", "Test B (después)")]):
        y = 2.35 + k * 0.45
        pill(X0, y, 1.4, a, WHITE if k != 1 else SOFT, INK)
        pill(X0 + 1.55, y, 1.4, c2, WHITE, GREY)
    for x in (X0, X0 + 1.55):
        shp(s, MSO_SHAPE.RECTANGLE, x, 2.33, 1.4, 1.36, None, LINE)
    t = tb(s, X0, 3.8, 2.95, 1.2)
    p = t.paragraphs[0]
    p.space_after = Pt(3)
    run(p, "Variable medida: ", 8, INK, True)
    run(p, "competencia ante un BEC (test de 7 dimensiones, 0-14 pts).", 8, INK)
    p = t.add_paragraph()
    p.space_after = Pt(3)
    run(p, "Hipótesis (H1 de Keller): ", 8, INK, True)
    run(p, "el grupo juego mejora más que el control.", 8, INK)
    p = t.add_paragraph()
    run(p, "Código y datos: ", 8, INK, True)
    run(p, github.replace("https://", "").replace("http://", ""), 8, OR, True)

    X1 = 6.6
    t = tb(s, X1, 0.9, 3.0, 0.3)
    run(t.paragraphs[0], "Resultados del piloto", 11, INK, True)
    table(s, X1, 1.3, [1.35, 0.8, 0.8], [
        ["", "Juego", "Control"],
        ["n", str(J.get("n", VACIO)), str(C.get("n", VACIO))],
        ["Test antes (0-14)", num(J.get("pre")), num(C.get("pre"))],
        ["Test después (0-14)", num(J.get("post")), num(C.get("post"))],
        ["Ganancia media", num(J.get("ganancia")), num(C.get("ganancia"))],
    ], row_h=0.3, size=8.5, center_from=1)

    mw = (res or {}).get("mann_whitney", {})
    an = (res or {}).get("ancova", {}).get("juego", {})
    t = tb(s, X1, 3.3, 2.95, 0.6)
    p = t.paragraphs[0]
    p.space_after = Pt(3)
    run(p, f"Mann-Whitney: {pval(mw.get('p'))} · g de Hedges = {num((res or {}).get('hedges_g'))}", 8.5, INK, True)
    run(t.add_paragraph(), f"ANCOVA (efecto del grupo, controlando el test inicial): b = {num(an.get('b'))}, {pval(an.get('p'))}", 8, INK)

    k = shp(s, MSO_SHAPE.ROUNDED_RECTANGLE, X1, 3.98, 2.95, 1.12, BLACK, adj=0.08)
    tf = k.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.15)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    run(p, "Original: ", 8.5, OR, True)
    run(p, "el grupo que jugó mejoró bastante más que el control (b = 1,97; p < 0,001) "
           "y la ventaja se mantuvo a las 8 semanas.", 8, WHITE)
    p = tf.add_paragraph()
    p.alignment = PP_ALIGN.LEFT
    run(p, "Réplica: ", 8.5, OR, True)
    run(p, frase_replica(res), 8, WHITE)


def frase_replica(res: dict | None) -> str:
    if not res or "mann_whitney" not in res:
        return VACIO
    d, p = res["dif_ganancia"], res["mann_whitney"]["p"]
    if d > 0 and p < 0.05:
        return f"el grupo que jugó mejoró {num(d, 1)} puntos más que el control ({pval(p)}), como en el corto plazo de Keller."
    if d > 0:
        return (f"el grupo que jugó mejoró {num(d, 1)} puntos más que el control, pero con una muestra "
                f"tan pequeña la diferencia no es significativa ({pval(p)}).")
    return f"el grupo que jugó no mejoró más que el control (diferencia = {num(d, 1)} puntos; {pval(p)})."


# ---------------------------------------------------------------- main
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--github", default="github.com/TU-USUARIO/escape-room-bec")
    ap.add_argument("--resultados", help="CSV con los códigos de resultados del piloto")
    ap.add_argument("--plantilla", default=str(AQUI / "plantilla_semana13.pptx"))
    ap.add_argument("--salida", default=str(AQUI / "PI_2026-2_Semana13_RenatoApaza.pptx"))
    a = ap.parse_args()

    res = None
    if a.resultados:
        import analisis
        res = analisis.calcular(analisis.cargar(a.resultados))

    capturas = AQUI / "capturas"
    b = Builder(Path(a.plantilla))
    for _ in range(len(b.prs.slides) - 1):
        b.drop(1)
    portada(b, capturas)
    workflow(b)
    experimentacion(b, capturas, a.github, res)
    b.renumber()
    b.prs.save(a.salida)
    print(f"PPT guardada en {a.salida}" + (f" con los resultados de {a.resultados}" if res else " (resultados en blanco: __)"))


if __name__ == "__main__":
    main()
