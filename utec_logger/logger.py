from datetime import datetime
from enum import Enum
from inspect import currentframe
from os import getcwd, getenv, makedirs, path
from os.path import basename

from boto3 import Session
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError


class Level(Enum):
    INFO = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    CRITICAL = '\033[97m\033[41m'

    def __init__(self, color):
        self.color = color

    @property
    def reset(self):
        return '\033[0m'


def _get_time_():
    now = datetime.now()
    return now.microsecond // 1000, now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


def _get_current_frame_():
    frame = currentframe()

    while frame:
        caller_frame = frame.f_back

        if not caller_frame:
            break

        caller_name = basename(caller_frame.f_code.co_filename)
        current_name = basename(frame.f_code.co_filename)

        if current_name == 'logger.py' and caller_name not in ['logger.py']:
            return caller_frame

        frame = caller_frame

    return frame


def _get_file_name_(frame):
    if frame:
        return basename(frame.f_code.co_filename)
    return "unknown.py"


def _get_line_number_(frame):
    if frame:
        return frame.f_lineno
    return 0


def _get_where_():
    frame = _get_current_frame_()
    return f'{_get_file_name_(frame)}:{_get_line_number_(frame)}'


class Logger:
    _instance_ = None

    def __new__(cls, *args, **kwargs):
        if cls._instance_ is None:
            cls._instance_ = super().__new__(cls)
        return cls._instance_

    def __init__(self):
        if not hasattr(self, '_init_'):
            self.aws_access_key_id = getenv('AWS_ACCESS_KEY_ID')
            self.aws_secret_access_key = getenv('AWS_SECRET_ACCESS_KEY')
            self.aws_session_token = getenv('AWS_SESSION_TOKEN')
            self.aws_region = getenv('AWS_REGION')

            self.session = None
            self.cloud_watch = None

            self.cloud_watch_group = getenv('CLOUD_WATCH_GROUP')
            self.cloud_watch_stream = getenv('CLOUD_WATCH_STREAM')

            self.today = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

            self.logs_folder = path.join(getcwd(), "logs")

            makedirs(self.logs_folder, exist_ok=True)

            self._init_ = True
            self._init_cloud_watch()

    def _check_aws_credentials(self):
        try:
            self.session = Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                aws_session_token=self.aws_session_token,
                region_name=self.aws_region
            )

            sts_client = self.session.client('sts')
            identity = sts_client.get_caller_identity()

            print(f'AWS Ready: {identity['Account']}')
            return True
        except NoCredentialsError:
            print('AWS is not SET: No credentials')
            return False
        except PartialCredentialsError:
            print('AWS is not SET: Partial credentials')
            return False
        except Exception as e:
            print(f'AWS is not SET: {e}')
            return False

    def _init_cloud_watch(self):
        if not self._check_aws_credentials():
            print('CloudWatch is not SET.')
            return

        try:
            self.cloud_watch = self.session.client('logs')

            try:
                self.cloud_watch.create_log_group(logGroupName=self.cloud_watch_group)
                print(f'CloudWatch Group: {self.cloud_watch_group}')
            except ClientError as e:
                if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
                    print(f'CloudWatch Group: {self.cloud_watch_group}')
                else:
                    raise

            try:
                self.cloud_watch.create_log_stream(
                    logGroupName=self.cloud_watch_group,
                    logStreamName=self.cloud_watch_stream
                )
                print(f'CloudWatch Stream: {self.cloud_watch_stream}')
            except ClientError as e:
                if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
                    print(f'CloudWatch Stream: {self.cloud_watch_stream}')
                else:
                    pass

            print('CloudWatch Ready')
        except Exception as e:
            print(f'CloudWatch is not SET: {e}')

    def _send_to_cloud_watch(self, message: str, timestamp: int, where: str, level: Level = Level.INFO):
        self.cloud_watch.put_log_events(
            logGroupName=self.cloud_watch_group,
            logStreamName=self.cloud_watch_stream,
            logEvents=[
                {
                    'timestamp': timestamp,
                    'level': level.value,
                    'where': where,
                    'message': message,
                }
            ]
        )

    def _write_to_file_(self, message: str):
        location = path.join(self.logs_folder, f'log-{self.today}.log')

        with open(location, 'a', encoding='utf-8') as file:
            file.write(message + '\n')

    def log(self, message: str, level: Level = Level.INFO):
        log_time_ms, log_time_str = _get_time_()
        log_where = _get_where_()

        if self.cloud_watch:
            self._send_to_cloud_watch(message, timestamp=log_time_ms, where=log_where, level=level)

        formatted = f'{log_time_str} | {level.name} | {log_where} | {message}'

        print(f'{level.color}{formatted}{level.reset}')
        self._write_to_file_(formatted)

    def info(self, message: str):
        self.log(message, level=Level.INFO)

    def warning(self, message: str):
        self.log(message, level=Level.WARNING)

    def error(self, message: str):
        self.log(message, level=Level.ERROR)

    def critical(self, message: str):
        self.log(message, level=Level.CRITICAL)


logger = Logger()


def log(level: Level, message: str):
    logger.log(message, level=level)


def info(message: str):
    logger.info(message)


def warning(message: str):
    logger.warning(message)


def error(message: str):
    logger.error(message)


def critical(message: str):
    logger.critical(message)
