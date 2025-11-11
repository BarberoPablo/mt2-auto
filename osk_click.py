import subprocess
import time
import pyautogui
from pathlib import Path
import sys

# === CONFIG ===
# Ajusta la ruta al exe que compila tu Program.cs (OKSClicker)
osk_clicker_exe = r'C:\Pablo\Programacion\metin2\metins\OKSClicker\bin\Release\net8.0\OKSClicker.exe'


# Coordenada fija donde quieres posicionar el mouse (la del OSK)
TARGET_X = 960
TARGET_Y = 920

# Delay en segundos antes de mover el mouse (te da tiempo para preparar la pantalla)
PREPARE_DELAY = 2.0

# Tiempo para mover el mouse (suavizado)
MOVE_DURATION = 0.12

# Delay pequeño antes de invocar el exe (dar tiempo a que el sistema estabilice el cursor)
POST_MOVE_DELAY = 0.08


def move_mouse_to(x: int, y: int, duration: float = MOVE_DURATION):
    """Mueve el cursor a (x,y) usando pyautogui (visual)."""
    print(f"[+] Moviendo cursor a ({x}, {y}) (duration={duration}s)...")
    pyautogui.moveTo(x, y, duration=duration)
    # pequeña pausa para estabilizar
    time.sleep(POST_MOVE_DELAY)


def call_oks_clicker(exe_path: str):
    """Llama al exe que hace click en la posición actual del mouse."""
    exe = Path(exe_path)
    if not exe.exists():
        print(f"❌ No encontré el exe en: {exe}")
        return False

    print(f"[+] Ejecutando clicker: {exe} (debe ejecutarse con permisos adecuados si es necesario)...")
    try:
        # Llamamos sin argumentos: el exe hará click donde esté el mouse
        # Si tu exe requiere argumentos, ajusta la lista.
        result = subprocess.run([str(exe)], capture_output=True, text=True, shell=False)
        if result.stdout:
            print("stdout:", result.stdout.strip())
        if result.stderr:
            print("stderr:", result.stderr.strip())
        return result.returncode == 0
    except Exception as e:
        print("❌ Error ejecutando el clicker:", e)
        return False


def main_once():
    print("=== OKS click test desde Python ===")
    print(f"Tenés {PREPARE_DELAY}s para dejar el OSK en su sitio...")
    time.sleep(PREPARE_DELAY)

    move_mouse_to(TARGET_X, TARGET_Y, duration=MOVE_DURATION)

    success = call_oks_clicker(osk_clicker_exe)
    if success:
        print("[+] Clicker ejecutado (verificá si OSK reaccionó).")
    else:
        print("[-] El clicker no terminó correctamente. Revisá la ruta o permisos (ejecutar Python/EXE como administrador).")


if __name__ == "__main__":
    main_once()
