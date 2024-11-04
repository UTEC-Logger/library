# utils.py
import inspect
from os.path import basename
from time import time, strftime, localtime

def get_time_now():
    current_time = time()
    s = int(current_time)
    ms = int((current_time - s) * 1000)
    formatted_time = strftime('%Y-%m-%d %H:%M:%S', localtime(s))
    return f"{formatted_time}.{ms:03d}"

def get_current_frame():
    """
    Obtiene el frame donde se llamó originalmente al logger
    subiendo en la pila de llamadas hasta encontrar el archivo original
    """
    frame = inspect.currentframe()
    
    # Subir en la pila hasta encontrar el frame correcto
    while frame:
        caller_frame = frame.f_back
        if not caller_frame:
            break
            
        caller_name = basename(caller_frame.f_code.co_filename)
        current_name = basename(frame.f_code.co_filename)
        
        if current_name == 'logger.py' and caller_name not in ['logger.py', 'utils.py']:
            return caller_frame
            
        frame = caller_frame
        
    return frame

def get_file_name(frame):
    if frame:
        return basename(frame.f_code.co_filename)
    return "unknown.py"

def get_line_number(frame):
    if frame:
        return frame.f_lineno
    return 0