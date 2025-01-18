import logging

logging.basicConfig(level=logging.DEBUG)

info_logger = logging.getLogger("info_logger")
info_logger.setLevel(logging.INFO)

info_handler = logging.FileHandler("app_info.log")
info_handler.setLevel(logging.INFO)

info_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
info_handler.setFormatter(info_formatter)

info_logger.addHandler(info_handler)


logging.basicConfig(
    filename="error.log",  # Файл для записи логов
    level=logging.ERROR,  # Уровень логирования (ERROR и выше)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат записи
)

error_logger = logging.getLogger("error_logger")
error_logger.setLevel(logging.ERROR)

error_handler = logging.FileHandler("app_errors.log")
error_handler.setLevel(logging.ERROR)

error_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
error_handler.setFormatter(error_formatter)

error_logger.addHandler(error_handler)