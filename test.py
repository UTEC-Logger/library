from utec_logger import logger


def test_logger_info():
    logger.info("This is an info message.")


def test_logger_warning():
    logger.warning("This is a warning message.")


def test_logger_error():
    logger.error("This is an error message.")


def test_logger_critical():
    logger.critical("This is a critical message.")


if __name__ == "__main__":
    test_logger_info()
    test_logger_warning()
    test_logger_error()
    test_logger_critical()

    print("All tests ran. Check 'logs/' directory for output.")
