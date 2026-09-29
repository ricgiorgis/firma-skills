# firma-skills

Las skills que solo se usan en la firma. Este repo es privado y sirve de respaldo.

- `traduccion-jurada`: traducciones juradas de Guatemala, de español a inglés y de inglés a español. Genera el esqueleto en Word con el formato de la casa y corre el QA antes de entregar.
- `cotizacion-firma`: cotizaciones de traducción jurada, notariado y legal ops en la plantilla de la casa. Pregunta el correlativo y el IVA en lugar de suponerlos.

## Cómo está armado

Igual que el repo Skills. `skills/` es la versión de Claude y la única que se edita. `chatgpt/` y `CATALOGO.md` salen del script:

```bash
python3 scripts/build_chatgpt.py      # regenera chatgpt/ y CATALOGO.md
python3 scripts/package.py            # deja los zips en dist/
```

Si agregás una skill, dale su entrada en `catalog.json` antes de correr el build.

## Instalar

- En Claude (app o web), subí el zip de `dist/claude/` en la sección de Skills de Configuración.
- En Claude Code, `/plugin marketplace add ricgiorgis/firma-skills` y después `/plugin install firma-skills@firma-skills`. Como el repo es privado, esa máquina tiene que tener acceso a GitHub con tu cuenta.
- En ChatGPT, subí el zip de `dist/chatgpt/` en Skills.

`traduccion-jurada` necesita Python 3 con `python-docx` para generar el esqueleto y correr el QA.
