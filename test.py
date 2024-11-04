# test_logger.py
from logger import logger, Level
import time
import os

def test_basic_logging():
    print("\n1. Probando niveles básicos de logging:")
    logger.info("Este es un mensaje de información")
    logger.warn("Este es un mensaje de advertencia")
    logger.error("Este es un mensaje de error")
    logger.critical("Este es un mensaje crítico")

def test_file_creation():
    print("\n2. Verificando creación de archivo de log:")
    log_file = os.path.join(logger.logs_folder, logger.current_log_file)
    
    logger.info("Mensaje de prueba para verificar archivo")
    
    if os.path.exists(log_file):
        print(f"✅ Archivo de log creado exitosamente en: {log_file}")
        with open(log_file, 'r') as f:
            logs = f.readlines()
            print(f"Contenido del archivo ({len(logs)} líneas):")
            for log in logs:
                print(f"  {log.strip()}")
    else:
        print("❌ Error: No se creó el archivo de log")

def test_multiple_executions():
    print("\n3. Simulando múltiples ejecuciones:")
    # Crear una nueva instancia del logger (simulando nueva ejecución)
    from logger import Logger
    
    logger1 = Logger()
    logger1.info("Log desde primera ejecución")
    
    # Esperar un segundo para asegurar un timestamp diferente
    time.sleep(1)
    
    logger2 = Logger()
    logger2.info("Log desde segunda ejecución")
    
    # Listar todos los archivos de log
    print("\nArchivos de log generados:")
    for file in os.listdir(logger.logs_folder):
        if file.startswith("log_") and file.endswith(".log"):
            print(f"  {file}")

if __name__ == "__main__":
    print("🧪 Iniciando pruebas del logger...")
    print(f"Archivo de log actual: {logger.current_log_file}")
    
    # Ejecutar pruebas
    test_basic_logging()
    test_file_creation()
    test_multiple_executions()
    
    print("\n✨ Pruebas completadas!")