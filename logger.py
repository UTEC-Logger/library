from enum import Enum

from connection import Connection
from utils import *

db = Connection()


class Level(Enum):
    INFO = (1, '\033[94m')
    WARNING = (2, '\033[93m')
    ERROR = (3, '\033[91m')
    CRITICAL = (4, '\033[95m')

    def __init__(self, value, color):
        self._value_ = value
        self.color = color

    @property
    def reset_color(self):
        return '\033[0m'


def log(level: Level, message: str):
    frame = get_current_frame()

    file_name = get_file_name(frame)
    line_number = get_line_number(frame)

    print(f"{level.color}{get_time_now()} | {level.name} | {file_name}:{line_number} | {message}{level.reset_color}")


def info(message: str):
    log(Level.INFO, message)


def warn(message: str):
    log(Level.WARNING, message)


def error(message: str):
    log(Level.ERROR, message)


def critical(message: str):
    log(Level.CRITICAL, message)
