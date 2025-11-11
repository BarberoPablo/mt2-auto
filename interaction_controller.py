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

# === Global Variables ===
game_keys = {
    "1": [875, 1022],
    "2": [910, 1022],
    "3": [940, 1022],
    "4": [972, 1022],
    "f1": [1018, 1022],
    "f2": [1048, 1022],
    "f3": [1081, 1022],
    "f4": [1114, 1022],
}

osk_keys = {
    "q": [1401, 994],
    "w": [1401 + 22, 994],
    "e": [1401 + 22 * 2, 994],
    "r": [1401 + 22 * 3, 994],
    "t": [1401 + 22 * 4, 994],
    "y": [1401 + 22 * 5, 994],
    "u": [1401 + 22 * 6, 994],
    "i": [1401 + 22 * 7, 994],
    "o": [1401 + 22 * 8, 994],
    "p": [1401 + 22 * 9, 994],
    "a": [1413, 1016],
    "s": [1413 + 22, 1016],
    "d": [1413 + 22 * 2, 1016],
    "f": [1413 + 22 * 3, 1016],
    "g": [1413 + 22 * 4, 1016],
    "h": [1413 + 22 * 5, 1016],
    "j": [1413 + 22 * 6, 1016],
    "k": [1413 + 22 * 7, 1016],
    "l": [1413 + 22 * 8, 1016],
    "z": [1424 + 22, 1038],
    "x": [1424 + 22 * 2, 1038],
    "c": [1424 + 22 * 3, 1038],
    "v": [1424 + 22 * 4, 1038],
    "b": [1424 + 22 * 5, 1038],
    "n": [1424 + 22 * 6, 1038],
    "m": [1424 + 22 * 7, 1038],
}


# === Generic Functions ===
def run_clicker(
    *args,
):  # clicker decides wheter to click on the client or in the OSK, based on args
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


def get_key_coords(key, keys):
    return keys[key.lower()]


def use_hotbar(key, title=default_window):
    x, y = get_key_coords(key, game_keys)
    move_mouse_to(x, y)
    right_click_at(x, y, title)


def check_timer(timer, keys, lapse):
    now = time.time()
    elapsed = now - timer
    if elapsed / lapse >= 0.9:
        print(f"[+] Triggering keys: {keys}")
        for key in keys:
            # unmount
            use_hotbar(key)
            time.sleep(4)
            # mount
        timer = now  # reset chronometer


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
        check_timer(skill_timer, skills, 15)
        time.sleep(5.03)
