# Atlas de Casos de Emprendimiento

[中文](README.md) · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · **Español**

![cases](https://img.shields.io/badge/cases-419-D85A30?style=flat-square) ![chars](https://img.shields.io/badge/text-576k_chars-6B7280?style=flat-square) ![license](https://img.shields.io/badge/license-CC_BY--SA_4.0-0F6E56?style=flat-square) ![llms](https://img.shields.io/badge/llms.txt-ready-534AB7?style=flat-square)

**419 negocios, cada uno con sus cuentas: cuánto costó, cuánto ingresó y en qué paso exacto se acabó el dinero.**

**246 de ellos (59 %) murieron de lo mismo**: construyeron algo que nadie quería y se gastaron el dinero averiguándolo.

[Explorar por mecanismo de fracaso](index/by-mechanism.md) · [Por sector](index/by-industry.md) · [Por región](index/by-region.md) · [Descargar los datos](data/cases.jsonl) · [Alimentar un modelo](llms.txt)

<img src="assets/failure-mechanisms.svg" width="780" alt="Distribución de mecanismos de fracaso en 419 casos: desajuste de demanda 246, sobreexpansión 120, estructura de costes 118, dependencia de una sola fuente de tráfico 108, rotura de tesorería 93">

> **Los cuerpos de los casos están en chino.** El esquema, los índices, los datos y este README están en español; los 419 relatos están en chino, porque ese es el hueco que este atlas cubre: los casos de negocio estructurados y con fuentes en chino escasean, los que están en inglés no.

---

## En 30 segundos

| Lo que quieres | Dónde ir |
| --- | --- |
| Leer uno | [`index/by-mechanism.md`](index/by-mechanism.md): empieza por «trampa de franquicia» o «rotura de tesorería» |
| Un corte concreto | [Sector](index/by-industry.md) · [Desenlace](index/by-outcome.md) · [Región](index/by-region.md) · [Año](index/by-year.md) |
| Los datos | [`data/cases.jsonl`](data/cases.jsonl): 419 líneas, un caso por línea, todos los campos |
| Un modelo | Lee primero [`llms.txt`](llms.txt) (1,3 KB) y luego [`llms-full.txt`](llms-full.txt) (1,7 MB) si el contexto lo permite |

```bash
git clone https://github.com/Shooang/startup-case-atlas.git
```

Hay cinco índices. [Por sector](index/by-industry.md): hostelería, comercio, e-commerce, software, hardware, servicios. [Por desenlace](index/by-outcome.md): fracaso, venta, giro, en marcha. [Por mecanismo](index/by-mechanism.md): trampa de franquicia, rotura de tesorería, dependencia de plataforma, estructura de costes. [Por región](index/by-region.md): China, EE. UU., Reino Unido, India y 31 países en total. [Por año](index/by-year.md): cómo el mismo error se repite a lo largo de una década.

## Cómo es un caso

Un bufé de marisco en Qingdao. El dueño vendió su casa para reunir 1,5 millones de RMB; el primer mes facturó entre 600 y 700 mil RMB y al cierre contable perdió más de 200 mil. Cerró al cuarto mes.

```yaml
id: G623
title: 卖房凑150万加盟火锅自助，首月流水70万反而亏20多万，四个月闭店
title_en: Sold his house for 1.5M RMB to join a buffet chain, closed in four months
type: 中文小生意
source: https://cbgc.scol.com.cn/news/7946483
era: 中文·青岛·2025-2026
region: CN
outcome: failure
industry: food-beverage
tags: [franchise, low-price-trap, cashflow-crunch, cost-structure]
key_numbers: 总投入150多万（加盟费十几万＋装修40多万＋备货七八十万）｜首月流水六七十万、净亏20多万｜59.9元引流套餐预售近80万｜4个月闭店、自称损失180多万
```

Todos los archivos comparten el mismo esqueleto: **16 campos fijos + tres secciones de cuerpo**.

- `## 故事正文`: de 600 a 900 caracteres, en orden cronológico, sin saltar a la conclusión
- `## 可用观点`: para qué sirve este caso como argumento, bajado a mecanismo
- `## 事实边界`: qué cifras son palabras del propio fundador, cuáles son entrevista periodística, cuáles son estimaciones y cuáles no se pudieron verificar

La tercera sección es deliberada. El mismo «perdió 700 mil» pesa muy distinto según venga del fundador, de un periodista o de un expediente judicial. Mezclarlos es como se produce un análisis malo.

## Qué contiene

| Directorio | Casos | Cobertura | Periodo |
| --- | --- | --- | --- |
| [`cases/01-personal-failure/`](cases/01-personal-failure/) | 4 | Autopsias escritas por el propio protagonista | 2015–2024 |
| [`cases/02-founder-postmortems/`](cases/02-founder-postmortems/) | 25 | Reflexiones largas de fundadores, sobre todo B2B y herramientas | 2006–2016 |
| [`cases/03-failory/`](cases/03-failory/) | 129 | Entrevistas a startups fracasadas de más de veinte países | 2020–2023 |
| [`cases/04-indie-hacker/`](cases/04-indie-hacker/) | 156 | Productos de pago hechos por una persona o un equipo mínimo | 2019–2026 |
| [`cases/05-china-interviews/`](cases/05-china-interviews/) | 69 | Negocio físico en China: restauración, franquicias, tiendas, servicios | 2018–2026 |
| [`cases/06-starter-story/`](cases/06-starter-story/) | 36 | Pequeños negocios con ingresos, coste inicial y tiempo de arranque | 2019–2024 |
| [`legacy/articles/`](legacy/articles/) | 95 | Archivo de artículos chinos antiguos, en su mayoría con enlaces muertos | 2000–2012 |

**Totales:** 419 casos · unos 576 000 caracteres de relato · 95 artículos archivados · 31 países y regiones · 13 sectores · 5 desenlaces · 12 mecanismos de fracaso.

## Fichas de marco: la capa de juicio

Un caso te dice cómo pasó algo; un marco te dice cómo juzgar lo siguiente. **154 fichas, extraídas de 13 libros y cursos.**

Cada ficha abre con una frase que se puede leer en voz alta, explica qué dice el marco, da tres o cuatro cosas que puedes juzgar con él y termina con **fuentes y límites**: dónde deja de funcionar el método.

[Por libro](index/frameworks-by-book.md) · [Por disciplina](index/frameworks-by-doctrine.md) · [Todas las aperturas](index/frameworks-hooks.md) · [Esquema de la ficha](docs/framework-schema.md)

## Para qué sirve

**Para escribir.** Un caso es el esqueleto de un capítulo: los números ya están, los giros ya están, y a quién mostrárselo está en `angles`. Filtra por mecanismo y tendrás diez casos del mismo tipo para comparar en paralelo.

**Para juzgar un negocio.** Si quieres saber si una franquicia de olla caliente es rentable, aquí hay muestras de Qingdao, Chengdu y Kunshan. Si quieres saber por qué las herramientas para creadores mueren tan fácilmente, hay 129 entrevistas de fracaso para contrastar. El mismo mecanismo reaparece en sectores distintos: esa regularidad vale más que un caso suelto.

**Para alimentar una IA.** El corpus en chino de casos de negocio tiene una cola larguísima casi vacía, sobre todo en negocios pequeños con cuentas concretas. Esta biblioteca está hecha para máquinas: campos cerrados, fuentes rastreables, cada archivo autocontenido. Troceado, cualquier fragmento sigue teniendo sentido.

## Por qué existe

Casi todo lo que se escribe sobre emprendimiento tiene dos defectos: las historias de éxito borran los números y las de fracaso reducen la causa a «mala gestión».

Este atlas intenta lo contrario. Toma 419 negocios concretos y registra, uno por uno, **cuánto costó, cuánto ingresó, a dónde se fue el dinero y en qué decisión se rompió**.

Dos cosas lo diferencian.

**Incluye los negocios que normalmente nadie registra.** Un local de fideos de diez metros cuadrados, un puesto callejero, una franquicia de olla caliente que facturó 700 mil RMB el primer mes y perdió más de 200 mil. La economía del pequeño comercio chino queda anotada al nivel del alquiler y del precio de compra, no en promedios sectoriales.

**Cada cifra lleva su procedencia.** Donde hay disputa, la disputa también está escrita.

## Esquema

Los 16 campos están definidos en [`docs/schema.md`](docs/schema.md). Resumen:

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `id` | string | `G001`–`G736`; los huecos son tramos reservados |
| `title` | string | Título original en chino, con el dato clave |
| `title_en` | string | Título en inglés, de 8 a 14 palabras |
| `type` | string | Tipo de fuente: testimonio, entrevista, reportaje, base de datos |
| `source` | url | Enlace al original o a la entrevista de origen |
| `era` | string | `idioma·país·año`, según lo indique la fuente |
| `source_language` | enum | `zh` \| `en` \| `unknown` |
| `region` | enum | Código de país; si se desconoce, `unknown`, **nunca se adivina** |
| `year` | int | Año en que arranca el caso |
| `outcome` | enum | `failure` \| `success` \| `exit` \| `pivoted` \| `ongoing` |
| `industry` | enum | 13 valores, ver [`docs/taxonomy.md`](docs/taxonomy.md) |
| `tags` | list | De 2 a 5 mecanismos, de un vocabulario cerrado de 12 |
| `key_numbers` | string | Las cifras que sostienen el relato, separadas por `｜` |
| `timeline` | string | Origen → giro → desenlace, una frase cada uno |
| `causal_chain` | string | Una sola línea causal, no una lista de motivos |
| `angles` | string | Para qué se puede usar este caso como argumento |
| `status` | string | Estado editorial; no forma parte de los datos |

## Fuentes y licencia

Esto es una **obra derivada, no un espejo**. No hay ni un solo texto copiado y pegado: cada caso es un relato en chino escrito de nuevo a partir de material publicado, y el enlace al original está dentro del archivo.

- **Cuerpos de los casos** (419): [CC BY-SA 4.0](LICENSE). Se pueden reproducir y adaptar con atribución, y las obras derivadas mantienen la misma licencia.
- **4 de ellos provienen de [`byoungd/up`](https://github.com/byoungd/up)**: el texto de ese proyecto es **CC BY-NC 4.0**, así que esos 4 casos **no admiten uso comercial**. Ver [`ATTRIBUTIONS.md`](ATTRIBUTIONS.md).
- **Artículos archivados** (`legacy/`): los derechos son de sus autores y publicadores originales. Se incluyen solo con fines de estudio e indexación, bajo un mecanismo de notificación y retirada. Ver [`DISCLAIMER.md`](DISCLAIMER.md).

Las licencias de origen se conservan tal cual en [`third-party/`](third-party/). El crédito de cada fuente, la fecha de recogida y qué se usó están en [`ATTRIBUTIONS.md`](ATTRIBUTIONS.md).

**Si eres titular de derechos** y quieres que algo se retire, abre un issue con la etiqueta `takedown`. No discutimos: lo borramos.

## Contribuir

**Corregir vale más que añadir.** Si una cifra de aquí contradice la fuente original, es un bug: repórtalo con el enlace. Ver [`docs/contributing.md`](docs/contributing.md).

Se aceptan casos nuevos si pasan tres condiciones: un enlace original que abra, al menos dos cifras concretas y un mecanismo de fracaso más específico que «mala gestión». Lo que no tiene fuente y se escribió por suposición se rechaza, por buena que sea la historia.

## Una nota

Esto no es asesoramiento de inversión ni un ranking de quién es más listo. Que un caso aparezca aquí significa que fue registrado, no que fue juzgado. Algunos de los que fracasaron hicieron casi todo bien y simplemente no llegaron a tiempo.

---

Si esta biblioteca te ahorró unos días de búsqueda, **una estrella es la forma más directa de devolverlo**, y además hace que la próxima persona que busque este material llegue aquí más fácil.

*Se mantiene como conjunto de datos público. Si lo usas en investigación o en un producto, un enlace de vuelta se agradece, pero no es obligatorio.*
