import pytesseract
from PIL import ImageGrab
import pygetwindow as gw
import pyautogui
import subprocess
import time
from pathlib import Path
import random
import keyboard

# === CONFIG ===
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Pablo\Programacion\metin2\metins\tesseract\tesseract.exe"
)
clicker_exe = r"C:\Pablo\Programacion\metin2\metins\Interactions\bin\Release\net8.0\Interactions.exe"
default_window = "Elveron"

# === Global Variables ===
osk_keys = {
    "1": [1412, 971],
    "2": [1412 + 22, 971],
    "3": [1412 + 22 * 2, 971],
    "4": [1412 + 22 * 3, 971],
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
    "z": [1424, 1038],
    "x": [1424 + 22, 1038],
    "c": [1424 + 22 * 2, 1038],
    "v": [1424 + 22 * 3, 1038],
    "b": [1424 + 22 * 4, 1038],
    "n": [1424 + 22 * 5, 1038],
    "m": [1424 + 22 * 6, 1038],
    "fn": [1368, 1060],
    "ctrl": [1368 + 22, 1060],
}


# === Click Functions ===
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


def click_at(x, y, title=default_window):
    args = ["click", x, y]
    if title:
        args.append(title)
    run_clicker(*args)


def right_click_at(x, y, title=default_window):
    args = ["click_right", x, y]
    if title:
        args.append(title)
    run_clicker(*args)


def osk_click_mouse():
    success = run_clicker("osk_click")
    if not success:
        print("❌ Error enviando click OSK.")


def osk_hold_click_mouse(duration):
    success = run_clicker("osk_hold_click", duration)
    time.sleep(duration)
    if not success:
        print("❌ Error enviando click OSK.")


# === Generic Functions ===
def find_and_click_metin(title=default_window):
    max_attempts = 4
    print("[+] Buscando 'metin'...")

    windows = gw.getWindowsWithTitle(title)
    if not windows:
        print(f"❌ Ventana '{title}' no encontrada")
        return False

    win = windows[0]
    bbox = (win.left, win.top, win.right, win.bottom)
    check_forward = True

    for attempt in range(max_attempts):
        screenshot = ImageGrab.grab(bbox=bbox)
        data = pytesseract.image_to_data(
            screenshot, output_type=pytesseract.Output.DICT
        )

        # --- 1️⃣ Buscar si ya hay un metin en zona de UI ---
        metin_ui_detected = False
        for i, word in enumerate(data["text"]):
            if "metin" in word.lower():
                x = win.left + data["left"][i] + data["width"][i] // 2 + 30
                y = win.top + data["top"][i] + data["height"][i] // 2 + 30
                if 880 < x < 920 and 80 < y < 95:
                    metin_ui_detected = True
                    break  # no hace falta seguir buscando

        if metin_ui_detected:
            print("⚠️ Ya estás destruyendo un metin (detectado en la UI).")
            return True  # salimos sin buscar más

        # --- 2️⃣ Si no hay metin en UI, buscar en el entorno ---
        for i, word in enumerate(data["text"]):
            if "metin" in word.lower():
                x = win.left + data["left"][i] + data["width"][i] // 2 + 30
                y = win.top + data["top"][i] + data["height"][i] + 30
                print(f"[+] 'Metin' encontrado en ({x}, {y})")
                osk_tap_keyboard("z")
                pyautogui.moveTo(x, y, duration=0.05)
                click_at(x, y)
                return True

        # --- 3️⃣ Si no encontró nada, rotar y reintentar ---
        print(f"[{attempt+1}/{max_attempts}] No se encontró metin. Rotando cámara...")
        if check_forward:
            osk_tap_keyboard("z")
            check_forward = not check_forward
            move_forward(1)
        else:
            osk_tap_keyboard("z")
            check_forward = not check_forward
            move_backward(1)

    print(f"❌ No se encontró ningún 'metin' tras {max_attempts} intentos.")
    return False


def move_mouse_to(x, y, duration=0.05):
    pyautogui.moveTo(x, y, duration=duration)
    time.sleep(0.05)


def sell_items(timer, lapse):
    now = time.time()
    elapsed = now - timer
    if elapsed / lapse >= 0.9:
        osk_tap_keyboard("f4")
        time.sleep(1)
        print("[+] Selling items...")
        pyautogui.moveTo(1820, 885, 0.05)  # Sell items
        # pyautogui.moveTo(1820, 860, 0.05)  # Select items
        click_at(1820, 860)
        time.sleep(round(random.uniform(0.05, 0.1), 2))
        # pyautogui.moveTo(1820, 885, 0.05)  # Sell items
        click_at(1820, 860)
        osk_tap_keyboard("f4")
        osk_tap_keyboard("i")
        timer = now

    return timer


def get_key_coords(key, keys):
    return keys[key.lower()]


def osk_tap_keyboard(key):
    print(f"[+] Tapping '{key}'...")
    if key in ["f1", "f2", "f3", "f4"]:
        fn_x, fn_y = get_key_coords("fn", osk_keys)
        move_mouse_to(fn_x, fn_y)
        osk_click_mouse()
        time.sleep(0.02)
        key_x, key_y = get_key_coords(key[-1], osk_keys)
        move_mouse_to(key_x, key_y)
        osk_click_mouse()
        time.sleep(0.02)
    else:
        x, y = get_key_coords(key, osk_keys)
        move_mouse_to(x, y)
        osk_click_mouse()
        time.sleep(0.02)


def osk_hold_keyboard(key, duration):
    x, y = get_key_coords(key, osk_keys)
    move_mouse_to(x, y)
    osk_hold_click_mouse(duration)


def check_timer(timer, keys, lapse, is_skill=False, first_run=False):
    now = time.time()
    elapsed = now - timer
    if (elapsed / lapse >= 0.9) | first_run:
        print(f"check_timer, elapsed: {elapsed} lapse: {lapse} first_run: {first_run}")
        first_run = False
        print(f"[+] Triggering keys: {keys}")
        if is_skill:
            horse_interaction()
        for key in keys:
            # unmount
            osk_tap_keyboard(key)
            time.sleep(3)
            # mount
        if is_skill:
            horse_interaction()
        timer = now  # reset chronometer

    return timer, first_run


def horse_interaction():
    osk_tap_keyboard("ctrl")
    time.sleep(0.1)
    osk_tap_keyboard("g")
    time.sleep(0.1)


def check_metin_timer(timer, lapse, first_run=False):
    now = time.time()
    elapsed = now - timer
    grab_items()  # Grab in every loop just in case mobs droped something
    if (elapsed / lapse >= 1) | first_run:
        first_run = False
        find_and_click_metin()
        timer = now

    return timer, first_run


def grab_items():
    osk_tap_keyboard("z")
    time.sleep(0.05)


def rotate_camera(angle):
    duration = (angle / 360.0) * 3.99  # It takes 4 seconds to perform a 360° rotation
    print(f"[+] rotate_camera: angle={angle} => duration={duration:.2f}s")
    osk_hold_keyboard("q", duration)


def move_forward(duration):
    print(f"[+] move_forward: duration={duration:.2f}s")
    osk_hold_keyboard("w", duration)


def move_backward(duration):
    print(f"[+] move_backward: duration={duration:.2f}s")
    osk_hold_keyboard("s", duration)


# === MAIN ===
if __name__ == "__main__":
    first_skills = True
    first_metin = True
    time.sleep(2)
    focus_window()

    skills = ["f1", "f2"]

    # Chronometers
    skill_timer = time.time()
    sell_timer = time.time()

    while True:
        print("=== While loop X ===")
        skill_timer, first_skills = check_timer(
            skill_timer, skills, 60 * 19, True, first_skills
        )
        find_and_click_metin()
        time.sleep(0.5)

        sell_timer = sell_items(sell_timer, 60 * 3)

        time.sleep(5.03)
