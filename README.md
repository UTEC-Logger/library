# utec_logger

Un logger personalizado para Python con salida en consola a color, guardado en archivos locales y soporte opcional para AWS CloudWatch Logs.

## 🚀 Características

- Logs a consola con colores según el nivel (INFO, WARNING, ERROR, CRITICAL)
- Logs persistentes en archivos locales (`logs/log-<file>-<timestamp>.log`)
- Integración opcional con AWS CloudWatch para centralizar logs
- Singleton: mantiene una única instancia del logger

---

## 🧑‍💻 Instalación

Clona o añade este módulo en tu proyecto:

```bash
git clone <repositorio>
```

Importa el logger en tus scripts:

```python
from utec_logger.logger import logger, info, warning, error, critical, Level
```

---

## 📝 Uso

```python
logger.info("Este es un mensaje informativo")
logger.warning("Advertencia")
logger.error("Error")
logger.critical("Crítico")

# O usa funciones directas:
info("Mensaje directo tipo info")
```

---

## 🧾 Salida esperada

En consola (con colores):

```
2025-05-03 12:30:01.123 | INFO | main.py:23 | Este es un mensaje informativo
```

En archivo:

```
logs/log-main-2025-05-03-12-30-01.log
```

---

## ☁️ Integración con AWS CloudWatch (opcional)

Si defines las variables de entorno necesarias, el logger también enviará los eventos a AWS CloudWatch Logs.

### 🔐 Variables necesarias

Debes definir las siguientes variables de entorno antes de ejecutar tu aplicación:

```bash
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token   # Opcional, si usas roles temporales
export AWS_REGION=us-east-1
export CLOUD_WATCH_GROUP=your-log-group-name
export CLOUD_WATCH_STREAM=your-log-stream-name
```

Si prefieres usar un archivo `.env`:

```env
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_SESSION_TOKEN=your-session-token
AWS_REGION=us-east-1
CLOUD_WATCH_GROUP=my-app-logs
CLOUD_WATCH_STREAM=dev-instance
```

Y luego en tu código, carga estas variables con `python-dotenv`:

```python
from dotenv import load_dotenv

load_dotenv()
```

---

## 🧪 Verificación

Al iniciar, el logger mostrará en consola si AWS y CloudWatch han sido correctamente configurados:

```
AWS Ready: 123456789012
CloudWatch Group: my-app-logs
CloudWatch Stream: dev-instance
CloudWatch Ready
```

---

## 📁 Estructura de logs

* Los archivos `.log` se guardan en la carpeta `logs/` dentro del directorio donde se ejecuta el programa.
* Cada archivo de log contiene todos los eventos desde que se inició el script.

---

## ✅ Requisitos

* Python 3.7+
* `boto3`
* (Opcional) `python-dotenv` para cargar `.env`

---

## 📦 Instalación de dependencias

```bash
pip install boto3 python-dotenv
```

---

## 🧊 Ejemplo completo

```python
from utec_logger.logger import logger, info, warning, error, critical

logger.info("Iniciando el sistema")
logger.warning("Este es un warning")
error("Ocurrió un error")
critical("Error crítico")
```

---

## Créditos

Desarrollado con fines educativos para el curso de **Cloud Computing - UTEC**.

- **Geraldo Colchado**
    - *[gcolchado@utec.edu.pe](mailto:gcolchado@utec.edu.pe)*
    - Profesor de Cloud Computing

- **Maykol Morales**
    - *[maykol.morales@utec.edu.pe](mailto:maykol.morales@utec.edu.pe)*
    - ACL de Cloud Computing

- **Gino Daza**
    - *[gino.daza@utec.edu.pe](mailto:gino.daza@utec.edu.pe)*
    - Ex-Alumno de Cloud Computing

- **Ian Condori**
    - *[ian.condori@utec.edu.pe](mailto:ian.condori@utec.edu.pe)*
    - Ex-Alumno de Cloud Computing