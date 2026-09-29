---
name: traduccion-jurada
description: >
  Producir traducciones juradas de Guatemala firmadas por la Traductora Jurada Sofía Estela
  Rodríguez Farfán (Resolución 346-DDEGN-2018, registro 004-2018), en ambas direcciones
  español↔inglés. Cubre el acta de apertura bajo juramento, el cuerpo literal con
  convenciones de corchetes, el cierre "EN FE DE LO CUAL" / "IN WITNESS WHEREOF" con
  declaración de hojas de papel bond, y el formato Word exacto (Arial 10, interlineado 1.5,
  relleno de línea con guiones). Aplica a partidas de nacimiento, matrimonio y defunción de
  RENAP, apostillas, títulos y certificaciones universitarias, cartas laborales y de
  ingresos, estados de cuenta bancarios, pasaportes, resoluciones de migración, avisos
  notariales, laudos arbitrales, certificados de libre venta y dispositivos médicos,
  reglamentos corporativos y reportes de buró de crédito. Usar siempre que se pida traducir,
  revisar o armar una traducción jurada, sworn translation, o cualquier documento que deba
  llevar fe pública de traductor jurado guatemalteco.
---

# Traducción jurada — Guatemala

## Antes de empezar: qué es norma y qué es estilo de la casa

No existe en Guatemala un reglamento que regule la **forma** de la traducción jurada. La
figura se rige por el Decreto 251 de 1879 y sus reformas (Decretos 1478 y 1956), y el título
se tramita conforme al Acuerdo Ministerial 1292-2009 ante las Direcciones Departamentales de
Educación. Ninguna de esas normas dice tipografía, márgenes, ni cómo marcar un sello
ilegible.

Lo que sigue es **estilo de la casa**, consolidado de las traducciones ya emitidas. Dos
convenciones sí tienen raíz normativa prestada del Código de Notariado (Decreto 314),
artículo 13: llenar con una línea los espacios en blanco que permitan intercalaciones
(numeral 7) — de ahí el relleno con guiones — y expresar fechas y cantidades con letras
(numeral 4), que es por qué las partidas de RENAP se traducen "May nineteenth, two thousand
twenty-one" y no "05/19/2021".

No citar norma para justificar reglas de forma. No hay.

## Flujo de trabajo

1. **Identificar** cada documento del lote y su idioma destino. Un trabajo puede traer
   varios documentos (documento principal + legalización + apostilla): van todos en una sola
   traducción, enumerados.
2. **Enumerar** los documentos en el acta de apertura con romanos minúsculos: `i)`, `ii)`,
   `iii)`, en negrita y con el nombre real del documento. Nunca el nombre del archivo, ni el
   rango de páginas del lote, ni una etiqueta interna tipo "APOSTILLA 5-6".
3. **Generar el esqueleto** con `scripts/nueva_traduccion.py` (formato ya cargado).
4. **Traducir el cuerpo** literalmente, en el orden del original, aplicando las reglas de
   contenido de abajo y las de `reference/convenciones.md`.
5. **Rotular** cada documento del lote antes de su cuerpo, entre corchetes y en negrita:
   `[Apostilla]`, `[Certificado de Defunción]`, `[Legalización]`.
6. **Contar las hojas reales** y escribir ese número en el cierre. Es lo último que se hace.
7. **Correr `scripts/qa.py`** sobre el archivo final. No se entrega nada sin pasar el QA.

## Formato del documento (no negociable)

| Parámetro | Valor |
|---|---|
| Tipografía | Arial 10 |
| Interlineado | 1.5 |
| Alineación | Justificada |
| Margen izquierdo | 1.18" |
| Margen derecho | 1.32" |
| Margen inferior | 2.25" (espacio para firma y sello) |
| Margen superior | 1.0" |
| Tamaño de página | Carta (8.5 × 11") |
| Relleno de línea | Tabulador **derecho a 6.0"** con guía de **guiones** |
| Numeración | Campo PAGE en el pie de página |

El relleno de guiones **no se teclea**. Cada párrafo termina con un carácter de tabulación y
el tabulador con guía de guiones dibuja la línea hasta el margen. Tecleado a mano se
desalinea al primer cambio de texto.

## Fórmulas fijas

Están literales en `reference/formulas.md` y las inserta el script. Cambian solo en tres
variables: idioma, cantidad de documentos, y número de hojas.

Credenciales invariables, nunca parametrizar: Sofía Estela Rodríguez Farfán, Resolución
346-DDEGN-2018 de la Dirección de Educación Departamental Norte del Ministerio de Educación,
Acuerdo Ministerial 3850-2017 del nueve de julio de dos mil dieciocho, registro 004-2018.

**Correcciones de 2026 al machote histórico.** Las traducciones emitidas hasta esta fecha
arrastran dos errores en las fórmulas en inglés. En el skill van corregidos:

- `for the uses that this party may deem convenient` — no "may deemed".
- `which I translate in its main part as follows` para un documento;
  `in their main part` solo cuando la enumeración trae dos o más.

## Reglas de contenido

**Corchetes.** Todo lo que no es texto traducible se declara entre corchetes describiendo qué
es: `[Logo]`, `[Sello]`, `[Firma ilegible]`, `[Sello redondo que lee: ...]`, `[Fotografía no
disponible]`, `[Código QR]`, `[Membrete del documento]`, `[Zona de lectura mecánica (MRZ)]`,
`[El resto de la página en blanco]`. Inventario completo en `reference/convenciones.md`.

**[Sic].** Marca lo que se **copió textualmente en lugar de traducirse**, por dos causas: es
un dato alfanumérico (`SWIFT: INDLGTGC [Sic]`, `DSDE 99 (2/12) [Sic]`, `1 - 024205 [Sic]`) o
es una palabra mal escrita en el original que se reproduce como está. Siempre con S mayúscula.
Nombres propios, marcas comerciales y direcciones no se traducen y **no llevan [Sic]**: no
traducirlos es lo normal, no una anomalía. Marcar cuarenta comercios en un estado de cuenta
le quita todo el peso a los [Sic] que sí señalan un defecto real del documento fuente.

**Sellos y firmas.** El corchete declara el elemento y la traducción del contenido va
**después**, como texto normal: `[Sello] Cámara de Comercio Indo Latinoamericana`, `[Firma]
Govind Ram`. Cuando no se puede leer, el corchete lo declara y no hay nada que traducir:
`[Sello ilegible]`, `[Firma ilegible]`. Aplica igual al traducir al inglés: `[Stamp] ...`,
`[Signature] ...`. No usar `[Sello que lee: ...]` — el texto del sello es contenido del
documento, no acotación del traductor, y adentro del corchete se confunde con una.

**Manuscritos.** Si es legible, se transcribe como cualquier otro texto. Solo lo ilegible se
declara entre corchetes, describiendo qué es: `[Firma ilegible]`, `[Nombre manuscrito
ilegible]`.

**Alcance parcial.** Cuando no se traduce todo el documento, se declara en el rótulo:
`[Certificado de Exportación de Productos Médicos del cual se traduce únicamente la parte
redactada en inglés]`. En el acta de apertura, la variante correspondiente de la fórmula
("para traducir únicamente en su parte conducente").

**Estructura del original.** Se respeta: si el original numera 1. y 2., la traducción numera
1. y 2., no convierte a viñetas. Las tablas se reproducen como tablas. Los saltos de página
y encabezados repetidos se declaran (`[Encabezado de página presente en todas las páginas del
documento]`, `[PÁGINA 2]`).

**Fechas y cantidades en letras** cuando el original las trae en letras, y en el idioma
destino: "el fourth day of November of two thousand twenty-five".

**Glosa de siglas**, siempre en la misma forma: `Documento Personal de Identificación [DPI by
its acronym in Spanish]`. Al traducir al español: `[por sus siglas en inglés]`.

**Cifras y saldos se copian, nunca se recalculan ni se corrigen.** Si la aritmética del
original no cuadra, se traduce tal cual y punto: el traductor no asume responsabilidad por el
contenido. Lo que sí se verifica es que la traducción no haya alterado un número respecto del
original.

## Nomenclatura de archivos

`yyyymmdd - Traducción <Documento> (ES|EN).docx`

La fecha es la de emisión, la misma del cierre, para que el archivo rastree contra el
documento firmado. `<Documento>` nombra el documento real y a la persona cuando aplica —
"Certificado Nacimiento Tomás Bermúdez", no "Apostilla 5-6". Dos archivos del mismo trabajo
no pueden distinguirse solo por un número al final.

## QA obligatorio

`scripts/qa.py archivo.docx` revisa:

- número de hojas declarado en el cierre contra páginas reales del documento
- corchetes abiertos sin cerrar
- presencia del acta de apertura y del cierre, y que la enumeración concuerde en número con
  la fórmula (`el cual se lee` / `los cuales se leen`, `in its` / `in their main part`)
- las fórmulas erradas del machote histórico ("may deemed", "into their main part")
- [Sic] en minúscula
- formato: fuente, interlineado, márgenes, tabulador de guiones, campo PAGE
- párrafos sin tabulación final (línea que quedaría sin relleno de guiones)

Lo que el QA **no** puede revisar y sigue siendo trabajo humano: que el contenido corresponda
al documento correcto, que los nombres propios estén bien escritos, y que las etiquetas del
encabezado (mes, número de cuenta, titular) correspondan a los datos del cuerpo. Los errores
más caros del histórico fueron de ese tipo — un estado de cuenta de octubre rotulado
"September", partidas de nacimiento con el nombre de otro hermano — y todos vinieron de
guardar un archivo encima de otro. **Nunca partir de una traducción anterior: partir siempre
del esqueleto que genera el script.**

## Archivos de referencia

- `reference/formulas.md` — actas de apertura y cierres, literales, en ambos idiomas
- `reference/convenciones.md` — inventario de corchetes, tratamiento por tipo de documento,
  glosario de términos recurrentes (RENAP, DPI, CUI, IGSS, ISR, apostilla, protocolo)
- `scripts/nueva_traduccion.py` — genera el esqueleto con el formato cargado
- `scripts/qa.py` — verificación previa a la entrega
