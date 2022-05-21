
# toolstr
`toolstr` makes it easy to create precise `str` representations of many different datatypes

`toolstr` has functionality for:
- formatting: convert numbers, timestamps, and bytecounts to str
- charting: create data charts using Unicode and other character sets
- tables: create highly-configurable table representations

`toolstr` uses many Unicode characters, but can also fallback to ascii when needed.


## Install
```bash
pip install toolstr
```

## Contents
- [Formatting Examples](#formatting)
- [Charting Examples](#charting)
- [Tables Examples](#tables)
- [FAQ](#faq)

## Formatting

## Charting

## Tables

Each of the parameters shown below can be mixed and matched to achieve a particular style.

By default numbers in tables are converted to `str` using `toolstr.format_number()`.

There are also some options visible in a terminal but not visible on github, including:
- color cells by column or by value
- separate color control of inner border vs outer border vs header border
- other [rich](https://github.com/Textualize/rich) styles including: bold, italic, and hyperlinks

### Table Examples

`toolstr.print_tables`

#### `{'add_row_index': True}`

```
     │      Name  │                     Era  │            Age  
─────┼────────────┼──────────────────────────┼─────────────────
  1  │  Vaalbara  │   Eoarchean-Mesoarchean  │  3,636,000,000  
  2  │  Gondwana  │      Ediacaran-Jurassic  │    550,000,000  
  3  │    Pangea  │  Carboniferous-Jurassic  │    336,000,000  
```


#### `{'border': 'thick'}`

```
      Name  ┃                     Era  ┃            Age  
━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━
  Vaalbara  ┃   Eoarchean-Mesoarchean  ┃  3,636,000,000  
  Gondwana  ┃      Ediacaran-Jurassic  ┃    550,000,000  
    Pangea  ┃  Carboniferous-Jurassic  ┃    336,000,000  
```


#### `{'border': 'double'}`

```
      Name  ║                     Era  ║            Age  
════════════╬══════════════════════════╬═════════════════
  Vaalbara  ║   Eoarchean-Mesoarchean  ║  3,636,000,000  
  Gondwana  ║      Ediacaran-Jurassic  ║    550,000,000  
    Pangea  ║  Carboniferous-Jurassic  ║    336,000,000  
```


#### `{'border': 'ascii'}`

```
      Name  |                     Era  |            Age  
------------+--------------------------+-----------------
  Vaalbara  |   Eoarchean-Mesoarchean  |  3,636,000,000  
  Gondwana  |      Ediacaran-Jurassic  |    550,000,000  
    Pangea  |  Carboniferous-Jurassic  |    336,000,000  
```


#### `{'outer_border': True}`

```
┌────────────┬──────────────────────────┬─────────────────┐
│      Name  │                     Era  │            Age  │
├────────────┼──────────────────────────┼─────────────────┤
│  Vaalbara  │   Eoarchean-Mesoarchean  │  3,636,000,000  │
│  Gondwana  │      Ediacaran-Jurassic  │    550,000,000  │
│    Pangea  │  Carboniferous-Jurassic  │    336,000,000  │
└────────────┴──────────────────────────┴─────────────────┘
```


#### `{'outer_border': 'thick'}`

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃      Name  │                     Era  │            Age  ┃
┃────────────┼──────────────────────────┼─────────────────┃
┃  Vaalbara  │   Eoarchean-Mesoarchean  │  3,636,000,000  ┃
┃  Gondwana  │      Ediacaran-Jurassic  │    550,000,000  ┃
┃    Pangea  │  Carboniferous-Jurassic  │    336,000,000  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```


#### `{'header_location': 'bottom'}`

```
  Vaalbara  │   Eoarchean-Mesoarchean  │  3,636,000,000  
  Gondwana  │      Ediacaran-Jurassic  │    550,000,000  
    Pangea  │  Carboniferous-Jurassic  │    336,000,000  
────────────┼──────────────────────────┼─────────────────
      Name  │                     Era  │            Age  
```


#### `{'header_location': []}`

```
  Vaalbara  │   Eoarchean-Mesoarchean  │  3,636,000,000  
  Gondwana  │      Ediacaran-Jurassic  │    550,000,000  
    Pangea  │  Carboniferous-Jurassic  │    336,000,000  
```


#### `{'header_location': ['top', 'bottom']}`

```
      Name  │                     Era  │            Age  
────────────┼──────────────────────────┼─────────────────
  Vaalbara  │   Eoarchean-Mesoarchean  │  3,636,000,000  
  Gondwana  │      Ediacaran-Jurassic  │    550,000,000  
    Pangea  │  Carboniferous-Jurassic  │    336,000,000  
────────────┼──────────────────────────┼─────────────────
      Name  │                     Era  │            Age  
```


#### `{'separate_all_rows': True}`

```
      Name  │                     Era  │            Age  
────────────┼──────────────────────────┼─────────────────
  Vaalbara  │   Eoarchean-Mesoarchean  │  3,636,000,000  
────────────┼──────────────────────────┼─────────────────
  Gondwana  │      Ediacaran-Jurassic  │    550,000,000  
────────────┼──────────────────────────┼─────────────────
    Pangea  │  Carboniferous-Jurassic  │    336,000,000  
```


#### `{'compact': True}`

```
    Name                    Era           Age
─────────────────────────────────────────────
Vaalbara  Eoarchean-Mesoarchean 3,636,000,000
Gondwana     Ediacaran-Jurassic   550,000,000
  Pangea Carboniferous-Jurassic   336,000,000
```


#### `{'header_border': 'thick'}`

```
      Name  ┃                     Era  ┃            Age  
━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━
  Vaalbara  │   Eoarchean-Mesoarchean  │  3,636,000,000  
  Gondwana  │      Ediacaran-Jurassic  │    550,000,000  
    Pangea  │  Carboniferous-Jurassic  │    336,000,000  
```


#### `{'header_style': 'bold'}`

```
      Name  │                     Era  │            Age  
────────────┼──────────────────────────┼─────────────────
  Vaalbara  │   Eoarchean-Mesoarchean  │  3,636,000,000  
  Gondwana  │      Ediacaran-Jurassic  │    550,000,000  
    Pangea  │  Carboniferous-Jurassic  │    336,000,000  
```

## FAQ
