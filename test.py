# test_logger.py
from logger import logger, Level
import time
import os
import shutil

def test_basic_logging():
    print("\n1. Probando niveles básicos de logging:")
    logger.info("Este es un mensaje de información")
    logger.warn("Este es un mensaje de advertencia")
    logger.error("Este es un mensaje de error")
    logger.critical("Este es un mensaje crítico")

def test_file_creation():
    print("\n2. Verificando creación de archivos de log:")
    logger.info("Mensaje de prueba para verificar archivo")
    
    # Verificar que se creó el archivo más reciente
    log_files = [f for f in os.listdir(logger.logs_folder) if f.endswith('.log')]
    if log_files:
        latest_file = max(log_files, key=lambda x: os.path.getctime(os.path.join(logger.logs_folder, x)))
        log_file = os.path.join(logger.logs_folder, latest_file)
        print(f"✅ Archivo de log creado exitosamente en: {log_file}")
        with open(log_file, 'r') as f:
            content = f.read().strip()
            print(f"Contenido del log: {content}")
    else:
        print("❌ Error: No se creó el archivo de log")

def test_aws_cloudwatch():
    print("\n3. Probando integración con AWS CloudWatch:")
    aws_config = {
        'log_group_name': 'test-logs',
        'log_stream_name': 'test-stream'
    }
    
    logger._setup_cloudwatch(aws_config)
    
    if logger.cloudwatch:
        print("✅ Conexión con CloudWatch establecida")
        logger.info("Test mensaje para CloudWatch")
    else:
        print("❌ No se pudo conectar con CloudWatch (verifica credenciales)")

def test_discord_webhook():
    print("\n4. Probando integración con Discord:")
    webhook_url = "TU_WEBHOOK_URL"
    logger.discord_webhook = webhook_url
    
    print("Enviando mensaje de error a Discord...")
    logger.error("Test mensaje de error para Discord")
    logger.critical("Test mensaje crítico para Discord")
    print("Verifica en tu canal de Discord si llegaron los mensajes")

def test_different_files():
    print("\n6. Probando logs desde diferentes archivos:")
    logger.info("Mensaje desde test_logger.py")
    
    # Crear un archivo temporal para probar
    with open("temp_test.py", "w") as f:
        f.write("""
from logger import logger

def test_function():
    logger.info("Mensaje desde temp_test.py")

test_function()
""")
    
    try:
        import temp_test
        os.remove("temp_test.py")
        if os.path.exists("__pycache__"):
            shutil.rmtree("__pycache__")
    except Exception as e:
        print(f"Error en prueba de diferentes archivos: {e}")

def test_multiple_logs():
    print("\n7. Probando múltiples logs consecutivos:")
    for i in range(3):
        logger.info(f"Mensaje de prueba {i+1}")
        time.sleep(1)  # Esperar 1 segundo entre logs
    
    print("\nArchivos generados:")
    log_files = sorted([f for f in os.listdir(logger.logs_folder) if f.endswith('.log')])
    for file in log_files[-3:]:
        print(f"\nArchivo: {file}")
        with open(os.path.join(logger.logs_folder, file), 'r') as f:
            content = f.read().strip()
            print(f"Contenido: {content}")

if __name__ == "__main__":
    # Limpiar la carpeta logs para pruebas frescas
    if os.path.exists(logger.logs_folder):
        shutil.rmtree(logger.logs_folder)
        print("Carpeta logs eliminada para pruebas")
    
    print("🧪 Iniciando pruebas del logger...")
    
    # Ejecutar todas las pruebas
    test_basic_logging()
    test_file_creation()
    test_aws_cloudwatch()
    test_discord_webhook()
    test_different_files()
    test_multiple_logs()
    
    print("\n✨ Pruebas completadas!")