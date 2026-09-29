---
name: "cotizacion-firma"
description: "Cotizaciones de la firma (traducción jurada, notariado, legal ops) en la plantilla de la casa, con correlativo, términos del servicio y montos verificados."
---

> **Nota de plataforma (ChatGPT).** Esta skill se escribió para Claude y se adaptó automáticamente.
> `<SKILL_DIR>` es la carpeta donde está instalada esta skill. Donde el texto mencione herramientas
> que no existan aquí (sub-agentes, navegador, archivos locales, `CLAUDE.md`), usá el equivalente
> disponible o avisá al usuario qué falta, en lugar de simularlo.
>
> Herramientas de Claude que menciona el texto y qué hacer en su lugar:
> - `SendUserFile`: entregar el archivo al usuario como descarga.

# Cotización de la firma

Se usa cuando Rik pide cotizar un servicio de la firma: traducción jurada, servicios notariales, consultoría legal o legal ops, o paquetes combinados. Las cotizaciones salen a nombre de Sofía Estela Rodríguez Farfán salvo que Rik indique otra cosa.

## Antes de producir: datos que no se suponen

Si falta alguno de estos datos en la conversación, se pregunta antes de generar el documento. Nunca se inventan.

1. **Correlativo.** Es el último número emitido más uno. Han existido al menos dos series (la #2093-2094 en mayo de 2026 y la #067-068 en agosto de 2026): preguntá cuál aplica y cuál fue el último número. Nunca estimes el número.
2. **Cliente.** Nombre de la persona o entidad y a quién va dirigida.
3. **Servicio y alcance.** Qué se cotiza exactamente.
4. **IVA.** Si el monto es "más IVA" o "IVA incluido". Esta diferencia cambia el ingreso neto de forma material; si Rik no lo dice, preguntá.
5. **Idioma.** Español para clientes locales ("Cotización # NNN"), inglés para clientes que lo requieran ("Quotation # NNN"). Todo el documento va en un solo idioma.

## Calidad en que firma Sofía

- Traducción jurada: Traductora Jurada.
- Notariado y consultoría legal: Abogada y Notaria.
El bloque de firma cambia según el servicio. No mezclar calidades en una misma cotización salvo que sea un paquete combinado.

## Reglas por línea de servicio

**Traducción jurada**
- Tarifa base: Q200.00 por página. Incluye la entrega (mensajería en la capital, Forza para el interior).
- Las páginas se cuentan sobre el documento real (conteo de páginas del PDF o imágenes recibidas), sumando cada documento del lote: documento principal, legalización, apostilla. Si no hay archivo, se cotiza sobre el número de páginas que diga Rik y se indica "sujeto a verificación del documento".
- Pedidos solo digitales: se imprime, firma, sella y escanea; se entrega en PDF.

**Notariado**
- Honorarios y gastos van separados. Los gastos (aranceles, timbres, papel de protocolo, habilitación de libros, reproducciones) se manejan con fondo de gastos contra liquidación, no embebidos en el precio.
- Incluir siempre la sección "No incluye" con las exclusiones del trámite.

**Consultoría legal y legal ops**
- Por entregables. Cuando el cliente pide desembolsos por fase, se muestran porcentajes por entregable; los montos por fase solo si Rik los pide.

## Estructura del documento

1. Encabezado: "Cotización # NNN" o "Quotation # NNN" y la fecha a la derecha.
2. Datos del cliente.
3. Detalle de la cotización: tabla con descripción, cantidad, precio unitario y total, más la fila de total general.
4. Condiciones del servicio (Terms of Service): tiempo de entrega, formato de entrega, vigencia de la cotización, forma de pago. En notariado, además, "No incluye".
5. Bloque de firma de Sofía con la calidad que corresponda.

## Diseño

Se replica la plantilla de la casa, no se diseña una nueva: fondo crema, color de marca verde azulado, encabezado de tabla durazno con línea terracota inferior, banda durazno de cierre con el bloque de firma, tipografía Lora y Poppins. Para los colores exactos, se toma la última cotización que Rik adjunte; si no adjunta ninguna, pedila antes de maquetar.

## Verificación

- Toda la aritmética (páginas por tarifa, subtotales, IVA, porcentajes por fase, total) se calcula con código antes de escribirla en el documento.
- La forma de pago del bloque de condiciones debe coincidir con lo que muestra la tabla.
- Renderizá el documento a imagen y revisalo una vez antes de entregar.

## Entrega

- Formato por defecto: .docx para revisar; PDF cuando Rik diga que ya se envía.
- Nombre de archivo: `Cotizacion NNN - <Servicio> - <Cliente>.docx`.
- Se entrega con SendUserFile y una línea de contexto. Al final, enumerar solo los datos que quedaron con hueco o que hay que confirmar (correlativo, IVA, número de colegiada si falta).