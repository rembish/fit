# fit

Read and write Garmin FIT (Flexible and Interoperable Data Transfer) files from Python.

FIT is a binary format designed for sport, fitness, and health devices. It is compact,
interoperable, and extensible — any FIT-compliant device can interpret a FIT file from
any other FIT-compliant device.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Or use the Makefile:

```bash
make install
```

## Usage

### Reading a FIT file

```python
from fit import FitFile

with FitFile.open("path/to/activity.fit") as f:
    for message in f:
        print(message)
```

### Copying a FIT file

```python
from fit import FitFile

with FitFile.open("path/to/source.fit") as src:
    with FitFile.open("path/to/copy.fit", mode="w") as dst:
        dst.copy(src)
```

### Creating a new FIT file

```python
from fit.files.activity import ActivityFile
from fit.messages.common import FileCreator

fnew = ActivityFile.create("path/to/new.fit")
fnew.append(FileCreator(software_version=100))
fnew.write()
fnew.close()
```

### Reading from a stream

```python
from io import BytesIO
from fit import FitFile

data = open("path/to/activity.fit", "rb").read()
with FitFile.open(BytesIO(data)) as f:
    for message in f:
        print(message)
```

## Development

```bash
make install     # create .venv and install all dev dependencies
make format      # run black
make lint        # run ruff
make typecheck   # run mypy
make test        # run pytest with coverage
make tox         # run tests across Python 3.8, 3.10, 3.12
make clean       # remove build artefacts and the virtualenv
```

## License

BSD 3-Clause — see `LICENSE`.
