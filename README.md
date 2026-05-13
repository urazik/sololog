# BLog

A flexible Python logger class that automatically prefixes messages with the class name when an object is provided, while supporting both object-oriented and simple string logging with full compatibility with the standard `logging` module's formatting and extra arguments.

## Features

- **Two call styles**:
  - `Logger.info(obj, msg, *args, **kwargs)` – prefixes the message with `ClassName: `.
  - `Logger.info(msg, *args, **kwargs)` – logs the message as is.
- **Drop‑in replacement** for standard `logging` methods – supports `%`‑formatting, `exc_info`, `extra`, and all other keyword arguments.
- **Singleton‑like configuration** – set up once with `setup()`, then use anywhere.
- **Console and file output** – configurable log file, format, and date format.

## Installation

You can either copy the `Logger` class directly into your project or build a distributable wheel.

### Direct use

Copy the `Logger` class from this repository into your own Python file. It requires only the standard library.

### Build a wheel

1. Create a `setup.py` file (see example below).
2. Run `python setup.py bdist_wheel` to generate a `.whl` file in the `dist/` directory.
3. Install the wheel with `pip install dist/BLog-0.2.0-py3-none-any.whl`.

## Usage

### 1. Configure the logger (once)

```python
from BLog import Logger

Logger.setup(
    name='my_app',
    log_file='app.log',          # omit or use '' for console only
    level=Logger.DEBUG,
    format='[%(asctime)s] [%(levelname)-8s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
```

## 2. Log messages

### With an object (adds class name)

```python
class MyClass:
    def do_something(self):
        Logger.info(self, 'Processing started')
        try:
            result = 42 / 0
        except Exception:
            Logger.exception(self, 'An error occurred')

obj = MyClass()
obj.do_something()
# Output:
# [2025-03-01 12:34:56] [INFO    ] MyClass: Processing started
# [2025-03-01 12:34:56] [ERROR   ] MyClass: An error occurred
# (with traceback)
```

### Without an object

```python
Logger.debug('Application initialised')
Logger.info(f'User {username} logged in')
Logger.warning('Disk space low: %.2f GB', free_space)
Logger.error('Failed to connect to %s', host, exc_info=True)
Logger.critical('Shutting down')
```

## API Reference

### `setup(name, log_file, level, format, datefmt)`

Configure the logger. Can be called only once; subsequent calls reset the logger.

| Parameter  | Type  | Default                                         | Description                                             |
| ---------- | ----- | ----------------------------------------------- | ------------------------------------------------------- |
| `name`     | `str` | `"default_logger"`                              | Logger name                                             |
| `log_file` | `str` | `""`                                            | Path to log file (empty = console only)                 |
| `level`    | `int` | `Logger.INFO`                                   | Logging level (e.g., `Logger.DEBUG` or `logging.DEBUG`) |
| `format`   | `str` | `"[%(asctime)s] [%(levelname)-8s] %(message)s"` | Log message format                                      |
| `datefmt`  | `str` | `'%Y-%m-%d %H:%M:%S'`                           | Date/time format                                        |

### Logging methods

All methods support the two call styles described above and accept any `*args` and `**kwargs` that the corresponding `logging` method does.

- `debug(*args, **kwargs)`
- `info(*args, **kwargs)`
- `warning(*args, **kwargs)`
- `error(*args, **kwargs)`
- `critical(*args, **kwargs)`
- `exception(*args, **kwargs)`

## Building a Package

Then run:

```bash
python setup.py bdist_wheel
```

The wheel file will be created in the `dist/BLog-0.2.1-py3-none-any.whl` folder. Install it with:

```bash
python -m pip install --force-reinstall dist/BLog-0.2.1-py3-none-any.whl
```

## Dependencies

- Python 3.8 or higher
- No external dependencies – uses only the standard library.

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.