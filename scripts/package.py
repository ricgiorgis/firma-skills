#!/usr/bin/env python3
"""Empaqueta skills en .zip listos para subir.

    python3 scripts/package.py                  # todas, Claude y ChatGPT
    python3 scripts/package.py efemerides       # solo una
    python3 scripts/package.py --only chatgpt   # solo una plataforma

Salida en dist/claude/<skill>.zip y dist/chatgpt/<skill>.zip (dist/ no se versiona).
Cada zip trae la carpeta de la skill en la raiz, que es lo que piden
claude.ai (Configuracion > Skills) y ChatGPT (Skills > subir).
"""
import argparse
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = {"claude": ROOT / "skills", "chatgpt": ROOT / "chatgpt"}
SKIP = {"__pycache__", ".DS_Store"}


def pack(src_dir, out_zip):
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(src_dir.rglob("*")):
            if f.is_file() and not SKIP.intersection(f.parts) and f.suffix != ".pyc":
                z.write(f, f.relative_to(src_dir.parent))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("skills", nargs="*")
    ap.add_argument("--only", choices=list(SOURCES))
    a = ap.parse_args()
    for plat, base in SOURCES.items():
        if a.only and plat != a.only:
            continue
        names = a.skills or sorted(p.name for p in base.iterdir() if (p / "SKILL.md").is_file())
        for n in names:
            pack(base / n, ROOT / "dist" / plat / f"{n}.zip")
        print(f"{plat}: {len(names)} zip en dist/{plat}/")


if __name__ == "__main__":
    main()
