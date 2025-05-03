# test.py

import os

from logger import logger


def test_logger_info():
    print("Testing info log...")
    logger.info("This is an info message.")


def test_logger_warning():
    print("Testing warning log...")
    logger.warning("This is a warning message.")


def test_logger_error():
    print("Testing error log...")
    logger.error("This is an error message.")


def test_logger_critical():
    print("Testing critical log...")
    logger.critical("This is a critical message.")


def test_log_file_written():
    print("Testing if log file was created and message written...")
    today = logger.today
    log_path = os.path.join(logger.logs_folder, f"log-{today}.log")

    assert os.path.exists(log_path), "Log file was not created."

    with open(log_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        assert any("This is an info message." in line for line in lines), "Info message not found in log file."


if __name__ == "__main__":
    test_logger_info()
    test_logger_warning()
    test_logger_error()
    test_logger_critical()
    test_log_file_written()

    print("All tests ran. Check 'logs/' directory for output.")
