"""Análisis del piloto: replicación a pequeña escala de Keller (2026).

Uso:
    pip install pandas scipy
    python analisis.py resultados.csv

El CSV sale del panel del responsable (index.html?admin=1 → "Descargar CSV")
o se arma pegando los códigos de resultados debajo de la cabecera de
resultados_plantilla.csv.
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd
from scipy import stats

DIMS = [
    "Conciencia de la amenaza", "Identificación de la amenaza", "Evaluación del impacto",
    "Elección de la táctica", "Justificación de la táctica", "Ejecución de la táctica",
    "Revisión y seguimiento",
]


def cargar(path: str) -> pd.DataFrame:
    df = pd.read_csv(path).drop_duplicates(subset="id", keep="first")
    df["grupo"] = df["grupo"].map({"J": "Juego", "C": "Control"})
    if df["grupo"].isna().any():
        raise ValueError("La columna 'grupo' solo puede tener J o C.")
    return df


def hedges_g(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return float("nan")
    sp = np.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2))
    if sp == 0:
        return float("nan")
    d = (a.mean() - b.mean()) / sp
    return float(d * (1 - 3 / (4 * (na + nb) - 9)))


def ancova(df: pd.DataFrame) -> dict:
    """post = b0 + b1*pre + b2*juego, por mínimos cuadrados ordinarios."""
    y = df["post"].to_numpy(float)
    X = np.column_stack([np.ones(len(df)), df["pre"].to_numpy(float), (df["grupo"] == "Juego").to_numpy(float)])
    dof = len(y) - X.shape[1]
    if dof < 1:
        return {}
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    sigma2 = resid @ resid / dof
    se = np.sqrt(np.diag(sigma2 * np.linalg.inv(X.T @ X)))
    out = {}
    for name, b, s in zip(["intercepto", "pre", "juego"], beta, se):
        t = b / s if s > 0 else float("nan")
        out[name] = {"b": float(b), "ee": float(s), "t": float(t), "p": float(2 * stats.t.sf(abs(t), dof))}
    return out


def calcular(df: pd.DataFrame) -> dict:
    j, c = df[df.grupo == "Juego"], df[df.grupo == "Control"]
    res = {"n_total": len(df), "grupos": {}}
    for name, g in (("Juego", j), ("Control", c)):
        res["grupos"][name] = {
            "n": len(g),
            "pre": float(g.pre.mean()) if len(g) else float("nan"),
            "post": float(g.post.mean()) if len(g) else float("nan"),
            "ganancia": float(g.ganancia.mean()) if len(g) else float("nan"),
            "de_ganancia": float(g.ganancia.std(ddof=1)) if len(g) > 1 else float("nan"),
        }
    res["dif_ganancia"] = res["grupos"]["Juego"]["ganancia"] - res["grupos"]["Control"]["ganancia"]
    if len(j) and len(c):
        u = stats.mannwhitneyu(j.ganancia, c.ganancia, alternative="greater")
        res["mann_whitney"] = {"U": float(u.statistic), "p": float(u.pvalue)}
    if len(j) > 1 and len(c) > 1:
        t = stats.ttest_ind(j.ganancia, c.ganancia, equal_var=False, alternative="greater")
        res["welch"] = {"t": float(t.statistic), "p": float(t.pvalue)}
    res["hedges_g"] = hedges_g(j.ganancia.to_numpy(float), c.ganancia.to_numpy(float))
    res["ancova"] = ancova(df)
    res["wilcoxon"] = {}
    for name, g in (("Juego", j), ("Control", c)):
        if len(g) > 1 and (g.post - g.pre).abs().sum() > 0:
            w = stats.wilcoxon(g.post, g.pre)
            res["wilcoxon"][name] = {"W": float(w.statistic), "p": float(w.pvalue)}
    res["dimensiones"] = [
        {"dimension": dim,
         "Juego": float((j[f"post_d{k}"] - j[f"pre_d{k}"]).mean()) if len(j) else float("nan"),
         "Control": float((c[f"post_d{k}"] - c[f"pre_d{k}"]).mean()) if len(c) else float("nan")}
        for k, dim in enumerate(DIMS, start=1)
    ]
    return res


def imprimir(df: pd.DataFrame, res: dict) -> None:
    print("== Descriptivos (puntaje 0-14) ==")
    print(df.groupby("grupo")[["pre", "post", "ganancia"]].agg(["count", "mean", "std"]).round(2), "\n")

    print("== H1: ¿el grupo que jugó mejora más que el control? ==")
    if "mann_whitney" in res:
        print(f"Mann-Whitney U = {res['mann_whitney']['U']:.1f}, p = {res['mann_whitney']['p']:.4f} (unilateral)")
    if "welch" in res:
        print(f"t de Welch = {res['welch']['t']:.2f}, p = {res['welch']['p']:.4f} (unilateral)")
    print(f"Diferencia de ganancias (juego - control) = {res['dif_ganancia']:.2f} puntos")
    print(f"g de Hedges (ganancias) = {res['hedges_g']:.2f}\n")

    print("== ANCOVA: post ~ pre + grupo (controla el punto de partida) ==")
    for name, label in (("intercepto", "Intercepto"), ("pre", "Test inicial"), ("juego", "Grupo juego")):
        if name in res["ancova"]:
            r = res["ancova"][name]
            print(f"{label:<13} b = {r['b']:6.2f}  EE = {r['ee']:5.2f}  t = {r['t']:6.2f}  p = {r['p']:.4f}")
    print()

    print("== Cambio dentro de cada grupo (Wilcoxon pre vs. post) ==")
    for name in ("Juego", "Control"):
        w = res["wilcoxon"].get(name)
        print(f"{name}: W = {w['W']:.1f}, p = {w['p']:.4f}" if w else f"{name}: sin cambios suficientes para la prueba")
    print()

    print("== Ganancia media por dimensión (0-2 puntos cada una) ==")
    print(pd.DataFrame(res["dimensiones"]).round(2).to_string(index=False), "\n")

    j = df[df.grupo == "Juego"]
    if len(j):
        print("== Datos del juego ==")
        print(j[["puntos", "pistas", "errores", "t_juego_s"]].describe().round(1))


def main(path: str) -> None:
    df = cargar(path)
    imprimir(df, calcular(df))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "resultados.csv")
