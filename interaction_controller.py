import pytesseract
from PIL import ImageGrab
import pygetwindow as gw
import pyautogui
import subprocess
import time
from pathlib import Path
import random

# === CONFIG ===
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Pablo\Programacion\metin2\metins\tesseract\tesseract.exe"
)
clicker_exe = r"C:\Pablo\Programacion\metin2\metins\Interactions\bin\Release\net8.0\Interactions.exe"
default_window = "Elveron"


# === Funciones genéricas ===
def run_clicker(*args):
    exe = Path(clicker_exe)
    if not exe.exists():
        print(f"❌ No encontré el exe: {exe}")
        return False
    result = subprocess.run(
        [str(exe), *map(str, args)], capture_output=True, text=True, shell=False
    )
    if result.stdout:
        print("stdout:", result.stdout.strip())
    if result.stderr:
        print("stderr:", result.stderr.strip())
    return result.returncode == 0

def focus_window(title=default_window):
    print(f"[+] Focuseando ventana '{title}'...")
    run_clicker("focus", title)

def click_at(x, y, title=None):
    args = ["click", x, y]
    if title:
        args.append(title)
    run_clicker(*args)

def right_click_at(x, y, title=None):
    args = ["click_right", x, y]
    if title:
        args.append(title)
    run_clicker(*args)


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
    for i, word in enumerate(data["text"]):
        if "metin" in word.lower():
            x = win.left + data["left"][i] + data["width"][i] // 2 + 30
            y = win.top + data["top"][i] + data["height"][i] + 30
            pyautogui.moveTo(x, y, duration=0.1)
            print(f"[+] 'Metin' encontrado en ({x},{y})")
            click_at(x, y, title)
            return
    print("❌ No se encontró 'metin'.")


def move_mouse_to(x, y, duration=0.12):
    pyautogui.moveTo(x, y, duration=duration)
    time.sleep(0.08)


def osk_click_mouse():
    success = run_clicker("osk_click")
    if not success:
        print("❌ Error enviando click OSK.")


def sell_items(title=default_window):
    print("[+] Selling items...")
    pyautogui.moveTo(1820, 860, duration=0.1)  # Select items
    click_at(1820, 860, title)
    time.sleep(round(random.uniform(0.10, 0.15), 2))
    pyautogui.moveTo(1820, 885, duration=0.1)  # Sell items
    click_at(1820, 860, title)


def get_key_coords(key):
    keys = {
        "1": [875, 1022],
        "2": [910, 1022],
        "3": [940, 1022],
        "4": [972, 1022],
        "f1": [1018, 1022],
        "f2": [1048, 1022],
        "f3": [1081, 1022],
        "f4": [1114, 1022],
    }
    return keys[key.lower()]


def use_hotbar(key, title=default_window):
    x, y = get_key_coords(key)
    move_mouse_to(x, y)
    right_click_at(x, y, title)


# === MAIN ===
if __name__ == "__main__":
    time.sleep(2)
    focus_window()

    # Skills to trigger every 30sec
    skills = ["f1", "f2"]

    # Chronometers
    skill_timer = time.time() 
    sell_timer = time.time()

    while True:
        print("=== While loop X ===")
        now = time.time()
        elapsed_skill = now - skill_timer
        print("Elapsed ?:", elapsed_skill / 30)
        if elapsed_skill / 30 >= 0.9:
            print(f"[+] Trigger de skills: {skills}")
            for key in skills:
                #unmount
                use_hotbar(key)
                time.sleep(4)
                #mount
            skill_timer = now  # reset chronometer
        
        time.sleep(5.03)