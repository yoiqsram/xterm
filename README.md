# xterm

Styled input and output for xterm 

## Getting Started

## Installing

```{bash}
python setup.py install
```

## Usages

```{python}
import xterm
```

### Styled text

```{python}
text = xterm.stylize('Lorem ipsum', font=['bold', 'italic'], color='cyan')
highlighted_text = xterm.stylize(' Mark ', font='invert', color='yellow')
```

```{python}
text1 = text + 'Hello'
text2 = str(text) + 'Hello'

text3 = highlighted_text + text
text4 = text1 + text

text5 = text3 + text4
```

### Query

```{python}
name = xterm.query('name', required=True)
```

```{python}
query_list = [
    {'name': 'name',
     'required': True},

    {'name': 'age',
     'type': int,
     'required': True}

    {'name': 'sex',
     'validate': lambda sex: sex.lower() in {'m', 'f'},
     'transformer': lambda sex: 'Male' if sex == 'm' else 'Female'}
]

query_input = xterm.queries(query_list)
## {'name': ..., 'age': ..., 'sex': ...}
```

### Logger

```{python}
logger = xterm.Logger(__name__, 'debug')  # default: 'info'

logger.info('message')

logger.debug('debug message')
logger.done('done message')
logger.warning('warning message')
logger.error('error message')
```

```{python}
logger.theme.Info.font = 'bold'
logger.theme.Info.color = xterm.Color.Green

logger.info('message')
```

## Progress

```{python}
import time

progress = xterm.Progress()
progress.start('Waiting...')
time.sleep(5)
progress.stop('Done {time:.f}s')
```

## Author

- **Yoiq S Rambadian** - https://github.com/yoiqsram
