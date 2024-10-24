from logger import log, Level

for i in range(10):
    l = int(input())

    if l == 1:
        log(Level.CRITICAL, f"Message {i}")

    elif l == 2:
        log(Level.ERROR, f"Message {i}")

    elif l == 3:
        log(Level.WARNING, f"Message {i}")

    elif l == 4:
        log(Level.INFO, f"Message {i}")
