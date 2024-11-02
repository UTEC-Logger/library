# logger.py
import os
from enum import Enum
import boto3
import requests
from typing import Optional, Dict
from botocore.exceptions import ClientError
from utils import get_time_now, get_current_frame, get_file_name, get_line_number

class Level(Enum):
    INFO = (1, '\033[92m')
    WARNING = (2, '\033[93m')
    ERROR = (3, '\033[91m')
    CRITICAL = (4, '\033[97m\033[41m')

    def __init__(self, value, color):
        self._value_ = value
        self.color = color

    @property
    def reset_color(self):
        return '\033[0m'


class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, 
                 logs_folder: str = "logs",
                 console_output: bool = True,
                 aws_config: Optional[Dict[str, str]] = None,
                 discord_webhook: Optional[str] = None):
        if not hasattr(self, 'initialized'):
            self.logs_folder = logs_folder
            self.console_output = console_output
            self.discord_webhook = discord_webhook
            self.cloudwatch = None
            self.log_group_name = None
            self.log_stream_name = None

            # Crea el directorio de logs si no existe
            os.makedirs(logs_folder, exist_ok=True)

            # Configurar AWS CloudWatch si se proporcionan credenciales (Falta probarlo aun)
            if aws_config and 'log_group_name' in aws_config and 'log_stream_name' in aws_config:
                self._setup_cloudwatch(aws_config)

            self.initialized = True

    def _setup_cloudwatch(self, aws_config: Dict[str, str]):
        """Configura la conexión con AWS CloudWatch"""
        try:
            self.cloudwatch = boto3.client('logs')
            self.log_group_name = aws_config['log_group_name']
            self.log_stream_name = aws_config['log_stream_name']

            # Crea el grupo de logs si no existe
            try:
                self.cloudwatch.create_log_group(logGroupName=self.log_group_name)
            except ClientError:
                pass

            # Crea el stream de logs si no existe
            try:
                self.cloudwatch.create_log_stream(
                    logGroupName=self.log_group_name,
                    logStreamName=self.log_stream_name
                )
            except ClientError:
                pass

        except Exception as e:
            print(f"Error configurando CloudWatch: {str(e)}")
            self.cloudwatch = None

    def _get_log_info(self):
        """Obtiene información sobre el archivo y línea donde se llamó al logger"""
        frame = get_current_frame()
        return get_file_name(frame), get_line_number(frame)

    def _format_log(self, level: Level, message: str, filename: str, line: int) -> str:
        """Formatea el mensaje de log según las especificaciones"""
        timestamp = get_time_now()
        return f"{timestamp} | {level.name} | {filename}:{line} | {message}"

    def _write_to_file(self, formatted_message: str):
        """Escribe el mensaje en el archivo de log del día"""
        # Extraemos la fecha del timestamp ya formateado (YYYY-MM-DD)
        # Todo esto utilizandos lo hice utilizando el utils.py, no se si es que se debia agregar algo ahi
        date = formatted_message.split()[0]
        log_file = os.path.join(self.logs_folder, f"{date}.log")
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(formatted_message + '\n')

    def _send_to_cloudwatch(self, formatted_message: str):
        """Envía el log a AWS CloudWatch si está configurado"""
        if self.cloudwatch:
            try:
                timestamp = int(float(get_time_now().split('.')[1]) * 1000)
                self.cloudwatch.put_log_events(
                    logGroupName=self.log_group_name,
                    logStreamName=self.log_stream_name,
                    logEvents=[{
                        'timestamp': timestamp,
                        'message': formatted_message
                    }]
                )
            except Exception as e:
                print(f"Error enviando log a CloudWatch: {str(e)}")

    def _send_to_discord(self, level: Level, formatted_message: str):
        """Envía el log a Discord si está configurado y es ERROR o CRITICAL"""
        if self.discord_webhook and level in [Level.ERROR, Level.CRITICAL]:
            try:
                requests.post(self.discord_webhook, 
                            json={'content': f"```{formatted_message}```"})
            except Exception as e:
                print(f"Error enviando log a Discord: {str(e)}")

    def log(self, level: Level, message: str):
        """Método principal para registrar logs"""
        filename, line = self._get_log_info()
        formatted_message = self._format_log(level, message, filename, line)

        # Escribir en archivo
        self._write_to_file(formatted_message)

        # Mostrar en consola si está habilitado
        if self.console_output:
            print(f"{level.color}{formatted_message}{level.reset_color}")

        # Enviar a CloudWatch si está configurado
        self._send_to_cloudwatch(formatted_message)

        # Enviar a Discord si está configurado y es necesario
        self._send_to_discord(level, formatted_message)

    def info(self, message: str):
        self.log(Level.INFO, message)

    def warn(self, message: str):
        self.log(Level.WARNING, message)

    def error(self, message: str):
        self.log(Level.ERROR, message)

    def critical(self, message: str):
        self.log(Level.CRITICAL, message)


# Uso de un singleton para el logger
logger = Logger()

# Para el uso de 2 versiones AKA logger.info() o info() directamente
def log(level: Level, message: str):
    logger.log(level, message)

def info(message: str):
    logger.info(message)

def warn(message: str):
    logger.warn(message)

def error(message: str):
    logger.error(message)

def critical(message: str):
    logger.critical(message)