import logging
import sys
from pathlib import Path


def setup_logging(log_level: str = "INFO", log_file: Path = None):
    """
    Настройка логирования для всего проекта

    Args:
        log_level: Уровень логирования (DEBUG, INFO, WARNING, ERROR)
        log_file: Путь к файлу для записи логов (опционально)
    """
    # Создаем форматтер
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Базовый логгер проекта
    logger = logging.getLogger("my_project")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Обработчик для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Обработчик для файла (если указан)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Предотвращаем дублирование логов
    logger.propagate = False

    return logger


# logger.py (продолжение)
def get_logger(name: str):
    """
    Получить логгер для конкретного модуля

    Args:
        name: Имя модуля (обычно __name__)
    """
    # Упрощаем имя для читаемости
    if name == "__main__":
        module_name = "main"
    else:
        # Преобразуем 'package.module' в 'package.module'
        module_name = name.split('.')[-1]

    return logging.getLogger(f"my_project.{module_name}")

# Создаем глобальный логгер по умолчанию
project_logger = setup_logging()