import logging
from typing import Any, Optional

class Logger:
    """
    A logger class supporting two call styles and automatic class name prefixing.

    Features:
    - Configure once via `setup()`.
    - Logging methods (`debug`, `info`, `warning`, `error`, `critical`, `exception`)
      can be called in two ways:
        1. `Logger.info(obj, msg, *args, **kwargs)` – if the first argument is not a string,
           it is treated as an object and the message gets a `ClassName: ` prefix.
        2. `Logger.info(msg, *args, **kwargs)` – if the first argument is a string,
           it is treated as the message, no prefix added.
    - All extra positional and keyword arguments are passed to the underlying logging method,
      allowing formatting (% style) and parameters like `exc_info`, `extra`, etc.

    Examples:
        # Configure the logger
        Logger.setup(name='my_app', log_file='app.log', level=logging.DEBUG)

        # Logging with an object
        class MyClass:
            def process(self):
                Logger.info(self, 'Processing started')
                # ...
                Logger.error(self, 'Error: %s', err_msg)

        # Logging without an object
        Logger.info('Application started')
        Logger.debug('Result: %d', 42)

        # Passing extra parameters (e.g., exc_info)
        try:
            risky_operation()
        except Exception:
            Logger.exception('Critical failure', exc_info=True)
    """

    CRITICAL = logging.CRITICAL
    FATAL    = logging.FATAL
    ERROR    = logging.ERROR
    WARNING  = logging.WARNING
    WARN     = logging.WARN
    INFO     = logging.INFO
    DEBUG    = logging.DEBUG
    NOTSET   = logging.NOTSET

    __logger          : Optional[logging.Logger] = None
    __name            : str                      = "default_logger"
    __log_file        : str                      = ""
    __level           : int                      = INFO
    __format          : str                      = "[%(asctime)s.%(msecs)03d] [%(levelname)-8s] %(message)s"
    __datefmt         : str                      = '%Y-%m-%d %H:%M:%S'
    __handlers        : list[logging.Handler]    = []
    __console_enabled : bool                     = True

    @classmethod
    def setup(cls,
              name     : str = "default_logger",
              log_file : str = "",
              level    : int = INFO,
              format   : str = "[%(asctime)s] [%(levelname)-8s] %(message)s",
              datefmt  : str = '%Y-%m-%d %H:%M:%S') -> None:
        """
        Configure logger parameters.

        Args:
            name: Logger name (default "default_logger").
            log_file: Path to log file. If empty, logs go only to console.
            level: Logging level (e.g., logging.DEBUG, logging.INFO,... or Logger.DEBUG, Logger.INFO,...).
            format: Log message format (see logging.Formatter documentation).
            datefmt: Date/time format (see time.strftime documentation).
        """
        cls.__name     = name
        cls.__log_file = log_file
        cls.__level    = level
        cls.__format   = format
        cls.__datefmt  = datefmt
        cls.__logger   = None

    @classmethod
    def console_enable(cls, enable: bool) -> None:
        """Enable/disable console logging."""
        cls.__console_enabled = enable

    @classmethod
    def add_handler(cls, handler: logging.Handler) -> None:
        """Add a handler to the logger."""
        try:
            if not (handler in cls.__handlers):
                cls.__handlers.append(handler)
        finally:
            if cls.__logger:
                cls.__logger.addHandler(handler)

    @classmethod
    def remove_handler(cls, handler: logging.Handler) -> None:
        """Remove a handler from the logger."""
        try:
            if handler in cls.__handlers:
                cls.__handlers.remove(handler)
        finally:
            if cls.__logger:
                cls.__logger.removeHandler(handler)

    @classmethod
    def __init_logger(cls) -> None:
        """Initialize the underlying logger (create handlers, set formatter)."""
        if cls.__logger is None:
            cls.__logger = logging.getLogger(cls.__name)
            cls.__logger.setLevel(cls.__level)

            for handler in cls.__logger.handlers[:]:
                cls.__logger.removeHandler(handler)

            formatter : logging.Formatter = logging.Formatter(fmt=cls.__format, datefmt=cls.__datefmt)

            if cls.__console_enabled:
                console_handler : logging.StreamHandler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                cls.__logger.addHandler(console_handler)

            if cls.__log_file:
                file_handler : logging.FileHandler = logging.FileHandler(cls.__log_file, encoding="utf-8")
                file_handler.setFormatter(formatter)
                cls.__logger.addHandler(file_handler)

            for handler in cls.__handlers:
                cls.__logger.addHandler(handler)

    @classmethod
    def __log(cls, level: str, *args: Any, **kwargs: Any) -> None:
        """
        Common implementation for all logging methods.

        Args:
            level: Logging level ('debug', 'info', ...).
            *args: Positional arguments. Interpreted as follows:
                - If first argument is a string, it is the message.
                - Otherwise, first argument is an object, second (if present) is the message.
                All remaining arguments are passed as formatting parameters.
            **kwargs: Keyword arguments passed to the logger method (e.g., exc_info).
        """
        if not args:
            return

        cls.__init_logger()

        if isinstance(args[0], str):
            msg      : str       = args[0]
            log_args : list[Any] = args[1:]
            getattr(cls.__logger, level)(msg, *log_args, **kwargs)
        else:
            obj      : object    = args[0]
            msg      : str       = ""
            log_args : list[Any] = []
            if len(args) >= 2:
                msg      = args[1]
                log_args = args[2:]
            getattr(cls.__logger, level)(f"{obj.__class__.__name__}: {msg}" if obj else msg, *log_args, **kwargs)

    @classmethod
    def debug(cls, *args: Any, **kwargs: Any) -> None:
        """
        Log a DEBUG message.

        Supports two call styles:
            - With object: `Logger.debug(obj, msg, *args, **kwargs)`
            - Without object: `Logger.debug(msg, *args, **kwargs)`

        Args:
            *args: Positional arguments (see __log description).
            **kwargs: Keyword arguments passed to logging.debug.
        """
        cls.__log('debug', *args, **kwargs)

    @classmethod
    def info(cls, *args: Any, **kwargs: Any) -> None:
        """
        Log an INFO message.

        Supports two call styles:
            - With object: `Logger.info(obj, msg, *args, **kwargs)`
            - Without object: `Logger.info(msg, *args, **kwargs)`

        Args:
            *args: Positional arguments (see __log description).
            **kwargs: Keyword arguments passed to logging.info.
        """
        cls.__log('info', *args, **kwargs)

    @classmethod
    def warning(cls, *args: Any, **kwargs: Any) -> None:
        """
        Log a WARNING message.

        Supports two call styles:
            - With object: `Logger.warning(obj, msg, *args, **kwargs)`
            - Without object: `Logger.warning(msg, *args, **kwargs)`

        Args:
            *args: Positional arguments (see __log description).
            **kwargs: Keyword arguments passed to logging.warning.
        """
        cls.__log('warning', *args, **kwargs)

    @classmethod
    def error(cls, *args: Any, **kwargs: Any) -> None:
        """
        Log an ERROR message.

        Supports two call styles:
            - With object: `Logger.error(obj, msg, *args, **kwargs)`
            - Without object: `Logger.error(msg, *args, **kwargs)`

        Args:
            *args: Positional arguments (see __log description).
            **kwargs: Keyword arguments passed to logging.error.
        """
        cls.__log('error', *args, **kwargs)

    @classmethod
    def critical(cls, *args: Any, **kwargs: Any) -> None:
        """
        Log a CRITICAL message.

        Supports two call styles:
            - With object: `Logger.critical(obj, msg, *args, **kwargs)`
            - Without object: `Logger.critical(msg, *args, **kwargs)`

        Args:
            *args: Positional arguments (see __log description).
            **kwargs: Keyword arguments passed to logging.critical.
        """
        cls.__log('critical', *args, **kwargs)

    @classmethod
    def exception(cls, *args: Any, **kwargs: Any) -> None:
        """
        Log an ERROR message with exception info (like logging.exception).

        Supports two call styles:
            - With object: `Logger.exception(obj, msg, *args, **kwargs)`
            - Without object: `Logger.exception(msg, *args, **kwargs)`

        Args:
            *args: Positional arguments (see __log description).
            **kwargs: Keyword arguments passed to logging.exception.
        """
        cls.__log('exception', *args, **kwargs)
