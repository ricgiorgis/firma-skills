# Convenciones de contenido

## Inventario de corchetes

Consolidado de las traducciones emitidas. Usar estos, no inventar variantes.

### Elementos gráficos
| Español | Inglés |
|---|---|
| `[Logo]` / `[Logo: RENAP [por sus siglas en español]]` | `[Logo]` / `[Logo: RENAP [By its acronym in Spanish]]` |
| `[Emblema]` | `[Emblem]` |
| `[Escudo de Belice]` | `[Coat of Arms of Ecuador]` |
| `[Código QR]` | `[QR Code]` |
| `[Código de barras]` | `[Bar code]` |
| `[Fotografía]` | `[Photograph]` |
| `[Fotografía no disponible]` | `[Photograph not available]` |
| `[Casilla de fotografía vacía]` | `[Empty Photograph Box]` |
| `[Logos de redes sociales]` | `[Social Media Logos]` |

### Firmas y sellos

**Regla.** El corchete declara **el elemento**; el texto del elemento va traducido **después
del corchete**, como texto normal. Solo cuando no se puede leer, el corchete absorbe la
declaración de ilegibilidad y no hay nada que traducir. Aplica igual en ambas direcciones.

```
[Sello] Cámara de Comercio Indo Latinoamericana, Nueva Delhi, 22/08/2025
[Stamp] Guatemalan Institute of Migration, Foreign Nationals Sub-Directorate
[Firma] Govind Ram, Subsecretario
[Signature] Ruby Santizo de Hernández, General Secretary
```

Ilegible:

```
[Sello ilegible]        [Illegible Stamp]
[Firma ilegible]        [Illegible signature]
```

Parcialmente legible — se traduce lo que se lee y se declara lo que no:

```
[Sello] Registro Civil de las Personas de Guatemala, Oficina No. 195 [resto ilegible]
```

| Español | Inglés |
|---|---|
| `[Firma]` + traducción | `[Signature]` + traducción |
| `[Firma ilegible]` | `[Illegible signature]` |
| `[Sello]` + traducción | `[Stamp]` + traducción |
| `[Sello ilegible]` | `[Illegible Stamp]` |
| `[Sello redondo]` + traducción | `[Round Stamp]` + traducción |
| `[Sello con emblema]` + traducción | `[Stamp with emblem]` + traducción |
| `[Firma y sello del notario]` | `[Signature and Stamp of the Notary]` |
| `[Sello en relieve]` | `[Embossed Seal]` |

> La forma `[Sello que lee: ...]` / `[Stamp that reads: ...]` aparece en traducciones
> anteriores y mete el texto **dentro** del corchete. Queda obsoleta: el contenido del sello
> es contenido traducido del documento, no una acotación del traductor, y meterlo dentro del
> corchete lo disfraza de acotación. Forma única de aquí en adelante: `[Sello]` seguido de la
> traducción.

### Estructura del documento
| Español | Inglés |
|---|---|
| `[Membrete del documento]` | `[Document letterhead]` |
| `[Encabezado de página presente en todas las páginas del documento]` | `[Page header present on every page of the document]` |
| `[PÁGINA 2]` | `[PAGE 2]` |
| `[Reverso del título]` | `[REVERSE OF THE DEGREE]` |
| `[El resto de la página en blanco]` | `[Remainder of the page left blank]` |
| `[En blanco]` | `[Blank]` |
| `[Sin información]` | `[No information]` |
| `[Línea en blanco]` | `[Blank Line]` |
| `[Zona de lectura mecánica (MRZ)]` | `[Machine Readable Zone (MRZ)]` |

### Contenido no traducible
| Español | Inglés |
|---|---|
| `[Sello no se traduce al no tener texto en inglés]` | — |
| `[sin información en idioma inglés]` | — |
| `[Nombre manuscrito ilegible]` | `[Illegible handwritten name]` |
| `[Secuencia numérica]` | `[Numeric sequence]` |
| `[serie de medidas]` | `[series of measurements]` |

### Glosa de siglas
Forma única, siempre entre corchetes junto a la sigla:
- Al inglés: `Personal Identification Document [DPI by its acronym in Spanish]`
- Al español: `Ley Federal de Arbitraje [FAA por sus siglas en inglés]`

## Tratamiento por tipo de documento

**Partidas RENAP (nacimiento, matrimonio, defunción).** Encabezado con Correlativo,
VERIFICADOR e ID. Fechas en letras. Bloques de datos del inscrito, la madre y el padre, cada
uno con su casilla de fotografía declarada. Pie con código QR, hash, correo del solicitante y
"Página 1 de 2". Si trae legalización de RENAP, va como documento aparte enumerado. Verificar
que el nombre del inscrito corresponda al documento — es donde más se ha equivocado el
histórico.

**Apostillas.** Los diez campos numerados de la Convención de La Haya se conservan numerados
y en orden. El encabezado "(Convention de La Haye du 5 octobre 1961)" se mantiene en francés
si así viene en el original. La leyenda de descargo de responsabilidad del ministerio emisor
se traduce completa.

**Estados de cuenta bancarios.** Tabla completa, todas las transacciones, sin resumir. Las
descripciones de comercio son nombres propios: no se traducen ni llevan [Sic]. Los rótulos
del encabezado —mes, número de cuenta, titular, saldo anterior— se leen **del documento que
se está traduciendo**, nunca se heredan del mes anterior. Verificar que el saldo anterior
declarado sea el saldo final del mes previo y que la primera fecha de la tabla caiga dentro
del mes rotulado.

**Títulos y certificaciones universitarias.** Nota mínima de aprobación, promedio, número de
registro, tomo y folio: son los datos que revisa un evaluador de credenciales extranjero.
Contrastar contra el resto del lote cuando hay varios documentos de la misma universidad; en
el histórico hay un número de registro que difiere en un dígito entre dos traducciones del
mismo asiento.

**Pasaportes.** Se recorre por páginas declaradas (`[PÁGINA 1]`, `[PÁGINAS 4 Y 5]`). La MRZ
se copia literal. Un mismo sello migratorio debe traducirse **igual** todas las veces que
aparezca; fijar la forma antes de empezar y repetirla.

**Cartas laborales y de ingresos.** Cantidades en cifras y letras como vengan. Pie de página
institucional completo, incluidos códigos internos y SWIFT (alfanuméricos, llevan [Sic]).

**Laudos y resoluciones.** Notas al pie del original se conservan como notas al pie. Citas
textuales entre comillas. `----LAST LINE----` para la línea de cierre del original, en esa
forma.

## Glosario recurrente

| Español | Inglés |
|---|---|
| Registro Nacional de las Personas (RENAP) | National Registry of Persons |
| Registro Civil de las Personas | Civil Registry of Persons |
| Registrador Civil de las Personas | Civil Registrar of Persons |
| Documento Personal de Identificación (DPI) | Personal Identification Document |
| Código Único de Identificación (CUI) | Unique Identification Code |
| Doy fe | I Attest |
| Partida de nacimiento | Birth Certificate |
| Capitulaciones matrimoniales | Marriage capitulations |
| Régimen económico: comunidad de gananciales | Economic Regime: Community Property |
| Escritura pública número | Public Deed number |
| Colegiado No. | Collegiate No. |
| Aviso notarial de traspaso | Notarial Notice of Transfer |
| Timbre fiscal | Fiscal Stamp Tax |
| Instituto Guatemalteco de Migración (IGM) | Guatemalan Institute of Migration |
| Residencia permanente | Permanent Residency |
| Considerando | Whereas |
| Por tanto | Therefore |
| Bono incentivo | Incentive Bonus |
| Instituto Guatemalteco de Seguridad Social (IGSS) | Guatemalan Social Security Institute |
| Impuesto Sobre la Renta (ISR) | Income Tax |
| Quetzales (Q) | Quetzals |
| Superintendencia de Administración Tributaria (SAT) | Superintendency of Tax Administration |
| Contraloría General de Cuentas | Comptroller General of Accounts |
| Secretario General | General Secretary |
| Certificado de libre venta | Free Sale Certificate |
| Laudo final parcial | Partial Final Award |

> "Impuesto Sobre la Renta" es **Income Tax**. En el histórico aparece como "Tax Over Rent",
> que es traducción literal errada de la sigla.
