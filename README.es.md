# Atlas de Casos de Emprendimiento

[简体中文](README.md) ｜ [English](README.en.md) ｜ [日本語](README.ja.md) ｜ [한국어](README.ko.md) ｜ **Español**

**419 casos estructurados de startups y pequeños negocios, escritos en chino y legibles por máquina.**

Autopsias de fracasos, ingresos reales de fundadores en solitario, y las cuentas reales de comercios de barrio en China: alquiler, personal, margen por unidad y cómo se acabó el efectivo.

---

## Qué es esto

Casi todo lo que se escribe sobre emprendimiento tiene el mismo problema: en las historias de éxito desaparecen los números, y en las de fracaso la causa se reduce a "mala gestión". Este atlas intenta lo contrario. Toma 419 negocios concretos y registra, uno por uno, **cuánto costó, cuánto ingresó, a dónde se fue el dinero y en qué decisión se rompió**.

Cada caso es un archivo Markdown con los mismos 16 campos. Un vendedor de Taobao, una empresa de hardware en Shenzhen y un puesto de fideos en Shanghái comparten el mismo esqueleto, así que se pueden comparar, filtrar y pasar a un modelo sin limpieza previa.

Dos cosas hacen distinta esta colección:

**Incluye negocios que normalmente nadie registra.** Un local de fideos de diez metros cuadrados. Un puesto callejero. Una franquicia de olla caliente que facturó 700.000 yuanes el primer mes y aun así perdió más de 200.000. La economía del pequeño comercio chino aparece aquí al nivel del alquiler y el precio de compra, no del promedio sectorial.

**Documenta de dónde sale cada cifra.** Todos los archivos terminan con una sección de «límites de los hechos» que indica si los datos provienen del propio fundador, de una entrevista periodística, de un expediente judicial o de una estimación, y qué no pudo verificarse. Cuando una cifra está en disputa, la disputa también queda escrita.

## Qué contiene

| Directorio | Casos | Cobertura | Período |
| --- | --- | --- | --- |
| [`cases/01-personal-failure/`](cases/01-personal-failure/) | 4 | Relatos de fracaso escritos por los propios fundadores | 2015–2024 |
| [`cases/02-founder-postmortems/`](cases/02-founder-postmortems/) | 25 | Análisis extensos de fundadores, sobre todo B2B y herramientas | 2006–2016 |
| [`cases/03-failory/`](cases/03-failory/) | 129 | Entrevistas con startups fallidas en más de 20 países | 2020–2023 |
| [`cases/04-indie-hacker/`](cases/04-indie-hacker/) | 156 | Fundadores individuales y equipos pequeños con producto de pago | 2019–2026 |
| [`cases/05-china-interviews/`](cases/05-china-interviews/) | 69 | Negocios físicos chinos: restauración, franquicias, comercios | 2018–2026 |
| [`cases/06-starter-story/`](cases/06-starter-story/) | 36 | Ingresos mensuales, costo inicial y tiempo de lanzamiento | 2019–2024 |
| [`legacy/articles/`](legacy/articles/) | 95 | Archivo de artículos chinos antiguos, en su mayoría con enlaces muertos | 2000–2012 |

**Totales:** 419 casos · ~576.000 caracteres chinos de texto · 95 artículos archivados · 31 países y regiones · 13 sectores · 5 tipos de desenlace · 12 mecanismos de fracaso.

## Cómo usarlo

### Para leer

Empieza por un índice, no por un archivo.

- [Por sector](index/by-industry.md) — restauración, comercio, e-commerce, software, hardware, servicios
- [Por desenlace](index/by-outcome.md) — fracaso, venta, reconversión, en marcha
- [Por mecanismo de fracaso](index/by-mechanism.md) — trampa de franquicia, quiebre de caja, dependencia de plataforma, estructura de costos
- [Por región](index/by-region.md) — China, EE. UU., Reino Unido, India y 27 más
- [Por año](index/by-year.md) — cómo el mismo error se repite durante una década

### Para alimentar un modelo

```
llms.txt             # estructura e índices, ~2 KB, empieza aquí
data/cases.jsonl     # 419 registros, un JSON por línea, todos los campos
llms-full.txt        # todos los cuerpos concatenados, ~1,7 MB
data/cases.csv       # para hoja de cálculo, etiquetas aplanadas
```

`llms.txt` sigue la convención de [llmstxt.org](https://llmstxt.org). Si tu pipeline trocea documentos, apunta a `cases/**/*.md`: cada archivo es autocontenido.

## Esquema

Los 16 campos están definidos en [`docs/schema.md`](docs/schema.md). Resumen:

| Campo | Tipo | Nota |
| --- | --- | --- |
| `id` | string | `G001`–`G736`, los huecos están reservados |
| `title` | string | Titular original en chino, factual, con la cifra clave |
| `title_en` | string | Versión en inglés, 8–14 palabras |
| `type` | string | Tipo de fuente: testimonio, entrevista, reportaje, base de datos |
| `source` | url | Enlace al artículo o entrevista original |
| `era` | string | `idioma · país · año`, según la fuente |
| `source_language` | enum | `zh` \| `en` \| `unknown` |
| `region` | enum | Código de país, o `unknown`; **nunca se adivina** |
| `outcome` | enum | `failure` \| `success` \| `exit` \| `pivoted` \| `ongoing` |
| `industry` | enum | 13 valores |
| `tags` | list | 2–5 mecanismos de una lista cerrada de 12 |
| `key_numbers` | string | Las cifras que sostienen la historia, separadas por `｜` |

El cuerpo tiene tres secciones fijas: `## 故事正文` (relato), `## 可用观点` (ángulos utilizables), `## 事实边界` (límites de los hechos).

## Fuentes y licencia

Es una **obra derivada, no un espejo**. Aquí no hay ni un artículo copiado y pegado: cada caso es una redacción original en chino basada en reportajes publicados, con el enlace a la fuente dentro del propio archivo.

- **Notas de casos** (419 archivos): [CC BY-SA 4.0](LICENSE)
- **Cuatro casos derivados de [`byoungd/up`](https://github.com/byoungd/up)**: el texto de ese proyecto es **CC BY-NC 4.0**, así que esos cuatro casos **no son aptos para uso comercial**. Ver [`ATTRIBUTIONS.md`](ATTRIBUTIONS.md).
- **Artículos archivados** (`legacy/`): los derechos siguen siendo de sus autores y editores originales. Se incluyen solo con fines de investigación e indexación, bajo un mecanismo de notificación y retirada. Ver [`DISCLAIMER.md`](DISCLAIMER.md).

Las licencias upstream se conservan íntegras en [`third-party/`](third-party/).

**Si eres titular de derechos** y quieres que se retire algo, abre un issue o escribe a la dirección de `DISCLAIMER.md`. Se retira sin discusión.

## Contribuir

**Corregir vale más que añadir.** Si una cifra contradice la fuente original, es un bug: repórtalo con el enlace.

Los casos nuevos son bienvenidos si cumplen tres condiciones: enlace de origen que abra, al menos dos cifras concretas, y un mecanismo más específico que "fracasó".

## Una nota

Esto no es asesoramiento de inversión, ni una clasificación de quién es listo. Que un caso aparezca aquí significa que fue documentado, no que fue juzgado. Varios de estos fracasos son personas que hicieron casi todo bien y se quedaron sin tiempo.

---

*Mantenido como conjunto de datos público. Si lo usas en investigación o en un producto, se agradece un enlace, pero no es obligatorio.*
