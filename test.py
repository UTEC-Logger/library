# test_aws_logger.py
from logger import logger, Level
import time
import os

def setup_aws():
    """Configura AWS CloudWatch"""
    aws_config = {
        'log_group_name': 'utec-logger-test',
        'log_stream_name': f'test-stream-{time.strftime("%Y%m%d")}'
    }
    
    logger._setup_cloudwatch(aws_config)
    
    return aws_config

def test_aws_logging():
    print("\n1. Probando conexión con AWS CloudWatch:")
    
    if logger.cloudwatch:
        print("✅ Conexión con CloudWatch establecida")
        
        print("\n2. Enviando logs de prueba a CloudWatch:")
        
        logger.info("Test INFO message para CloudWatch")
        print("✅ Log INFO enviado")
        
        logger.warn("Test WARNING message para CloudWatch")
        print("✅ Log WARNING enviado")
        
        logger.error("Test ERROR message para CloudWatch")
        print("✅ Log ERROR enviado")
        
        logger.critical("Test CRITICAL message para CloudWatch")
        print("✅ Log CRITICAL enviado")
        
        print("\n3. Verificación:")
        print(f"Por favor, verifica en la consola de AWS CloudWatch:")
        print(f"  - Log Group: {logger.log_group_name}")
        print(f"  - Log Stream: {logger.log_stream_name}")
        
    else:
        print("❌ Error: No se pudo conectar con CloudWatch")
        print("Verifica tus credenciales de AWS y la configuración")
        print("Asegúrate de tener configurado:")
        print("  1. AWS_ACCESS_KEY_ID")
        print("  2. AWS_SECRET_ACCESS_KEY")
        print("  3. AWS_DEFAULT_REGION")

def test_aws_and_file():
    print("\n4. Probando logging simultáneo (archivo y AWS):")
    
    test_message = "Test mensaje simultaneo"
    logger.info(test_message)
    logger.warn(test_message)
    logger.error(test_message)
    logger.critical(test_message)
    
    current_date = time.strftime('%Y-%m-%d')
    log_file = os.path.join(logger.logs_folder, f"{current_date}.log")
    
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            last_line = f.readlines()[-1]
            print(f"✅ Mensaje guardado en archivo local: {last_line.strip()}")
    
    if logger.cloudwatch:
        print(f"✅ Mensaje enviado a CloudWatch")
    
    print("\nEl mensaje debería aparecer en:")
    print(f"1. Archivo local: {log_file}")
    print(f"2. CloudWatch grupo: {logger.log_group_name}, stream: {logger.log_stream_name}")

if __name__ == "__main__":
    print("🧪 Iniciando pruebas de AWS CloudWatch Logger...")
    
    aws_config = setup_aws()
    
    test_aws_logging()
    test_aws_and_file()
    
    print("\n✨ Pruebas completadas!")
    print("\nNota: Verifica en la consola de AWS CloudWatch que los logs se hayan registrado correctamente.")