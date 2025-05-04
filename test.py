from utec_logger import logger


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


if __name__ == "__main__":
    test_logger_info()
    test_logger_warning()
    test_logger_error()
    test_logger_critical()

    print("All tests ran. Check 'logs/' directory for output.")
