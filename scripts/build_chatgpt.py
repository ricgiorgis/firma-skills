#!/usr/bin/env python3
"""Genera chatgpt/<skill>/ a partir de skills/<skill>/.

skills/ es la unica fuente de verdad. Se edita ahi y se corre:

    python3 scripts/build_chatgpt.py            # regenera todo chatgpt/
    python3 scripts/build_chatgpt.py efemerides # solo una skill

Que hace por cada skill:
  - copia la carpeta completa (scripts, references, assets, licencias);
  - deja en el frontmatter de SKILL.md solo name y description, que es lo
    que ChatGPT lee;
  - cambia las rutas de instalacion de Claude (~/.claude/skills/<skill>/,
    /mnt/skills/.../<skill>/) por <SKILL_DIR>/ en la documentacion;
  - agrega una nota de plataforma que explica las herramientas de Claude
    que menciona el texto y que hacer en su lugar. El texto no se reescribe:
    reescribir a mitad de frase rompe la gramatica, sobre todo en espanol;
  - escribe agents/openai.yaml con nombre visible y descripcion corta;
  - regenera CATALOGO.md.

Los archivos de codigo (scripts) se copian sin tocar para no romperlos.

Solo usa la biblioteca estandar de Python 3.8+.
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "skills"
DST = ROOT / "chatgpt"
CATALOG = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))

DOC_EXT = {".md", ".txt"}

# Herramientas de Claude que pueden aparecer en el texto, con su equivalente.
# "Artifact" no va aqui porque en Fabric significa otra cosa.
TOOLS = [
    ("AskUserQuestion", "hacerle al usuario una pregunta con opciones"),
    ("SendUserFile", "entregar el archivo al usuario como descarga"),
    ("SendUserMessage", "enviarle un mensaje al usuario"),
    ("TodoWrite", "llevar una lista de tareas"),
    ("TaskCreate", "llevar una lista de tareas"),
    ("WebFetch", "abrir la página con navegación web"),
    ("WebSearch", "búsqueda web"),
    ("subagent_type", "el rol del sub-agente, si hay sub-agentes disponibles"),
]

PATH_RES = [
    re.compile(r"~/\.claude/skills/([A-Za-z0-9_-]+)/"),
    re.compile(r"(?<![~\w])\.claude/skills/([A-Za-z0-9_-]+)/"),
    re.compile(r"/mnt/skills/(?:user|public|examples|private|organization)/([A-Za-z0-9_-]+)/"),
]

NOTE = (
    "> **Nota de plataforma (ChatGPT).** Esta skill se escribió para Claude y se adaptó automáticamente.\n"
    "> `<SKILL_DIR>` es la carpeta donde está instalada esta skill. Donde el texto mencione herramientas\n"
    "> que no existan aquí (sub-agentes, navegador, archivos locales, `CLAUDE.md`), usá el equivalente\n"
    "> disponible o avisá al usuario qué falta, en lugar de simularlo."
)


def split_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        raise ValueError("SKILL.md sin frontmatter")
    return m.group(1), m.group(2)


def keep_name_description(fm):
    """Conserva solo name y description, respetando descripciones multilinea."""
    out, keep = [], False
    for line in fm.split("\n"):
        top = re.match(r"^([A-Za-z_][\w-]*):", line)
        if top:
            keep = top.group(1) in ("name", "description")
        if keep:
            out.append(line)
    return "\n".join(out)


def fix_paths(text, own):
    changed = False
    for pat in PATH_RES:
        text, n = pat.subn(lambda m: "<SKILL_DIR>/" if m.group(1) == own else m.group(0), text)
        changed |= n > 0
    return text, changed


def tools_in(text):
    return [(t, eq) for t, eq in TOOLS if re.search(r"\b" + t + r"\b", text)]


def note_for(tools):
    lines = [NOTE]
    if tools:
        lines.append(">")
        lines.append("> Herramientas de Claude que menciona el texto y qué hacer en su lugar:")
        lines += [f"> - `{t}`: {eq}." for t, eq in tools]
    return "\n".join(lines) + "\n\n"


def yaml_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def build(name):
    src, dst = SRC / name, DST / name
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))

    any_change = False
    all_text = ""
    for f in dst.rglob("*"):
        # Solo documentacion: el codigo no se toca para no romperlo.
        if f.is_file() and f.suffix.lower() in DOC_EXT and f.name != "SKILL.md":
            try:
                t = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            t2, ch = fix_paths(t, name)
            all_text += t2
            if ch:
                f.write_text(t2, encoding="utf-8")
                any_change = True

    skill = dst / "SKILL.md"
    fm, body = split_frontmatter(skill.read_text(encoding="utf-8"))
    body, ch = fix_paths(body, name)
    any_change |= ch
    tools = tools_in(body + all_text)
    if any_change or tools or re.search(r"\bClaude\b|CLAUDE\.md", body):
        body = note_for(tools) + body.lstrip("\n")
    skill.write_text("---\n" + keep_name_description(fm) + "\n---\n\n" + body.lstrip("\n"), encoding="utf-8")

    meta = CATALOG["skills"][name]
    agents = dst / "agents"
    agents.mkdir(exist_ok=True)
    (agents / "openai.yaml").write_text(
        "interface:\n"
        f"  display_name: {yaml_str(meta['display'])}\n"
        f"  short_description: {yaml_str(meta['short'])}\n"
        "policy:\n"
        f"  allow_implicit_invocation: {'false' if meta.get('explicit') else 'true'}\n",
        encoding="utf-8",
    )


def write_catalog():
    """Regenera CATALOGO.md desde catalog.json."""
    lines = ["# Catálogo", "", "Generado por `scripts/build_chatgpt.py` desde `catalog.json`. No se edita a mano.", ""]
    for cat in CATALOG["categories"]:
        items = [(n, m) for n, m in CATALOG["skills"].items() if m["category"] == cat]
        if not items:
            continue
        lines += [f"## {cat} ({len(items)})", "", "| Skill | Para qué |", "|---|---|"]
        for n, m in sorted(items):
            flag = " (solo si se invoca)" if m.get("explicit") else ""
            lines.append(f"| [`{n}`](skills/{n}/SKILL.md) | {m['short']}{flag} |")
        lines.append("")
    lines.append(f"Total: {len(CATALOG['skills'])} skills.")
    (ROOT / "CATALOGO.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    names = sys.argv[1:] or sorted(p.name for p in SRC.iterdir() if (p / "SKILL.md").is_file())
    missing = [n for n in names if n not in CATALOG["skills"]]
    if missing:
        sys.exit("Faltan en catalog.json: " + ", ".join(missing))
    if not sys.argv[1:] and DST.exists():
        for p in DST.iterdir():
            if p.is_dir() and p.name not in names:
                shutil.rmtree(p)
    for n in names:
        build(n)
    write_catalog()
    print(f"{len(names)} skills generadas en {DST.relative_to(ROOT)}/ y CATALOGO.md actualizado")


if __name__ == "__main__":
    main()
