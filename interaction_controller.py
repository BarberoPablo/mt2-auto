import pytesseract
from PIL import ImageGrab
import pygetwindow as gw
import pyautogui
import subprocess
import time
from pathlib import Path

# === CONFIG ===
pytesseract.pytesseract.tesseract_cmd = r'C:\Pablo\Programacion\metin2\metins\tesseract\tesseract.exe'
clicker_exe = r'C:\Pablo\Programacion\metin2\metins\Interactions\bin\Release\net8.0\Interactions.exe'
default_window = 'Elveron'

# === Funciones genéricas ===
def run_clicker(*args):
    exe = Path(clicker_exe)
    if not exe.exists():
        print(f"❌ No encontré el exe: {exe}")
        return False
    result = subprocess.run([str(exe), *map(str, args)], capture_output=True, text=True, shell=False)
    if result.stdout: print("stdout:", result.stdout.strip())
    if result.stderr: print("stderr:", result.stderr.strip())
    return result.returncode == 0

def focus_window(title=default_window):
    print(f"[+] Focuseando ventana '{title}'...")
    run_clicker("focus", title)

def click_at(x, y, title=None):
    args = ["click", x, y]
    if title: args.append(title)
    run_clicker(*args)

def click_mouse():
    run_clicker("click")  # llama a click en la posición actual

def find_and_click_metin(title=default_window):
    print("[+] Buscando 'metin'...")
    windows = gw.getWindowsWithTitle(title)
    if not windows:
        print(f"❌ Ventana '{title}' no encontrada")
        return
    win = windows[0]
    bbox = (win.left, win.top, win.right, win.bottom)
    screenshot = ImageGrab.grab(bbox=bbox)
    data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
    for i, word in enumerate(data['text']):
        if 'metin' in word.lower():
            x = win.left + data['left'][i] + data['width'][i]//2 + 30
            y = win.top + data['top'][i] + data['height'][i] + 30
            pyautogui.moveTo(x, y, duration=0.1)
            print(f"[+] 'Metin' encontrado en ({x},{y})")
            click_at(x, y, title)
            return
    print("❌ No se encontró 'metin'.")

def move_mouse_to(x, y, duration=0.12):
    pyautogui.moveTo(x, y, duration=duration)
    time.sleep(0.08)

def osk_click_mouse():
    """Hace click usando la lógica del OSK (position actual del mouse)."""
    print("[+] Ejecutando OSK click...")
    success = run_clicker("osk_click")
    if success:
        print("[+] Click OSK enviado correctamente.")
    else:
        print("❌ Error enviando click OSK.")


# === MAIN EJEMPLO ===
if __name__ == "__main__":
    time.sleep(2)
    focus_window()

    time.sleep(0.3)
    find_and_click_metin()
    time.sleep(2)

    move_mouse_to(960, 920)
    osk_click_mouse()
