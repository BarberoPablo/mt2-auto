import pytesseract
from PIL import ImageGrab
import pygetwindow as gw
import pyautogui
import subprocess
import time
from pathlib import Path
import random
import keyboard
import math
import sys


# === CONFIG ===
DEVICE = "notebook"  # "pc 1920x1080" or "notebook 1360x768"
BASE_DIR = None
# Detects if it is executing from packaging (PyInstaller) or in development
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)  # PyInstaller
else:
    BASE_DIR = Path(__file__).resolve().parent  # Development (actual script path)


# === Files Routes ===
pytesseract.pytesseract.tesseract_cmd = str(BASE_DIR / "tesseract" / "tesseract.exe")
clicker_exe = str(BASE_DIR / "Interactions" / "publish" / "Interactions.exe")
default_window = "Elveron"


# === Global Variables ===
osk_keys_pc = {
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
    "alt": [1368 + 22 * 3, 1060],
}
osk_keys_notebook = {
    "1": [860, 660],
    "2": [860 + 22, 660],
    "3": [860 + 22 * 2, 660],
    "4": [860 + 22 * 3, 660],
    "q": [850, 682],
    "w": [850 + 22, 682],
    "e": [850 + 22 * 2, 682],
    "r": [850 + 22 * 3, 682],
    "t": [850 + 22 * 4, 682],
    "y": [850 + 22 * 5, 682],
    "u": [850 + 22 * 6, 682],
    "i": [850 + 22 * 7, 682],
    "o": [850 + 22 * 8, 682],
    "p": [850 + 22 * 9, 682],
    "a": [860, 705],
    "s": [860 + 22, 705],
    "d": [860 + 22 * 2, 705],
    "f": [860 + 22 * 3, 705],
    "g": [860 + 22 * 4, 705],
    "h": [860 + 22 * 5, 705],
    "j": [860 + 22 * 6, 705],
    "k": [860 + 22 * 7, 705],
    "l": [860 + 22 * 8, 705],
    "z": [872, 728],
    "x": [872 + 22, 728],
    "c": [872 + 22 * 2, 728],
    "v": [872 + 22 * 3, 728],
    "b": [872 + 22 * 4, 728],
    "n": [872 + 22 * 5, 728],
    "m": [872 + 22 * 6, 728],
    "fn": [816, 750],
    "ctrl": [816 + 22, 750],
    "alt": [816 + 22 * 3, 750],
}
osk_keys = osk_keys_pc if DEVICE == "pc" else osk_keys_notebook

gautama_370_330_coords = {
    "pc": {
        0: (450, 70),
        1: (1800, 550),
        2: (660, 50),
    },
    "notebook": {
        0: (485, 60),
        1: (1340, 370),
        2: (400, 60),
    },
}

metin_ui_coords = {
    "pc": {
        "min_x": 850,
        "max_x": 890,
        "min_y": 45,
        "max_y": 65,
    },
    "notebook": {
        "min_x": 579,
        "max_x": 660,
        "min_y": 45,
        "max_y": 70,
    },
}

sell_items_coords = {
    "pc": {
        "x": 1820,
        "y": 860,
    },
    "notebook": {
        "x": 1060,
        "y": 342,
    },
}


# === Click Functions ===
def run_clicker(
    *args,
):  # clicker decides wheter to click on the client or in the OSK, based on args
    exe = Path(clicker_exe)
    if not exe.exists():
        print(f".exe not found: {exe}")
        return False
    result = subprocess.run(
        [str(exe), *map(str, args)], capture_output=True, text=True, shell=False
    )
    if result.stdout:
        print("stdout:", result.stdout.strip())
    if result.stderr:
        print("stderr:", result.stderr.strip())
    return result.returncode == 0


def focus_window():
    print(f"Focusing window '{default_window}'...")
    run_clicker("focus", default_window)


def click_at(
    x,
    y,
):
    run_clicker("click", x, y, default_window)


def right_click_at(
    x,
    y,
):
    args = ["click_right", x, y]
    args.append(default_window)
    run_clicker(*args)


def osk_click_mouse():
    success = run_clicker("osk_click")
    if not success:
        print("[-] Error sending OSK click.")


def osk_hold_click_mouse(duration):
    success = run_clicker("osk_hold_click", duration)
    time.sleep(duration)
    if not success:
        print("[-] Error sending OSK click.")


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


# === Generic Functions ===
def move_mouse_to(x, y, duration=0.05):
    pyautogui.moveTo(x, y, duration=duration)
    time.sleep(0.05)


def sell_items(timer, lapse):
    now = time.time()
    elapsed = now - timer
    if elapsed / lapse >= 0.9:
        osk_tap_keyboard("f4")
        time.sleep(1)
        print("[+] Items sold.")
        x, y = sell_items_coords[DEVICE]["x"], sell_items_coords[DEVICE]["y"]
        pyautogui.moveTo(x, y, 0.05)
        click_at(x, y)
        time.sleep(round(random.uniform(0.05, 0.1), 2))
        click_at(x, y)
        osk_tap_keyboard("f4")
        osk_tap_keyboard("i")
        timer = now

    return timer


def check_timer(
    timer,
    keys,
    lapse,
    delay,
    is_skill=False,
    first_run=False,
):
    now = time.time()
    elapsed = now - timer
    if (elapsed / lapse >= 0.9) | first_run:
        print(f"[+]Timer elapsed, Triggering keys: {keys}")
        first_run = False
        if is_skill:
            horse_interaction()
        for key in keys:
            # unmount
            osk_tap_keyboard(key)
            time.sleep(delay)
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


def grab_items():
    osk_tap_keyboard("z")
    time.sleep(0.05)


def rotate_camera(angle):
    duration = (
        angle / 360.0
    ) * 3.99  # It takes around 4 seconds to perform a 360° rotation
    print(f"[+] Rotating camera, angle={angle} => duration={duration:.2f}s")
    osk_hold_keyboard("q", duration)


def move_forward(duration):
    print(f"[+] Moving forward: duration={duration:.2f}s")
    osk_hold_keyboard("w", duration)


def move_backward(duration):
    print(f"[+] Moving backward: duration={duration:.2f}s")
    osk_hold_keyboard("s", duration)


# === METIN PATHS ===
def gautama_370_330(step, first_cicle, idle):
    windows = gw.getWindowsWithTitle(default_window)
    if not windows:
        print(f"[Error] Window not found: '{default_window}'")
        return "error"

    win = windows[0]
    bbox = (win.left, win.top, win.right, win.bottom)

    screenshot = ImageGrab.grab(bbox=bbox)
    data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

    # Detect Metin UI
    metin_ui_detected = False
    for i, word in enumerate(data["text"]):
        if "metin" in word.lower():
            x = win.left + data["left"][i] + data["width"][i] // 2
            y = win.top + data["top"][i] + data["height"][i] // 2
            ui = metin_ui_coords[DEVICE]
            if ui["min_x"] < x < ui["max_x"] and ui["min_y"] < y < ui["max_y"]:
                metin_ui_detected = True
                break

    if metin_ui_detected:
        print("[attacking] Healthbar UI detected at ({x}, {y})")
        return "attacking"

    if not first_cicle and not idle:
        osk_tap_keyboard("z")
        match step:
            case 0 | 1 | 2:
                x, y = gautama_370_330_coords[DEVICE][step]
                print(f"Case {step}, moving to {x},{y}")
                pyautogui.moveTo(x, y, duration=0.05)
                click_at(x, y)
                time.sleep(3)
            case 3:
                print("Case 3, going back")
                move_backward(2.5)

    # Recalculate image for new metins
    screenshot = ImageGrab.grab(bbox=bbox)
    data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

    closest_metin, min_distance = get_closest_metin(win, data)

    if closest_metin:
        x, y = closest_metin
        space = 30
        print(f"[found] Nearest objective found at ({x}, {y}). Distance: {min_distance}")
        pyautogui.moveTo(x, y + space, duration=0.05)
        click_at(x, y + space)
        time.sleep(2)  # Give time to start attacking metin
        return "found"

    print("[idle] No objective found.")
    return "idle"


def get_closest_metin(win, data):
    player_x, player_y = 960, 530  # Screen center
    closest_metin = None
    min_distance = float("inf")

    for i, word in enumerate(data["text"]):
        if "metin" in word.lower():
            x = win.left + data["left"][i] + data["width"][i] // 2
            y = win.top + data["top"][i] + data["height"][i] // 2
            dist = math.sqrt((x - player_x) ** 2 + (y - player_y) ** 2)
            if dist < min_distance:
                min_distance = dist
                closest_metin = [x, y]

    return closest_metin, min_distance


def is_player_bugged(timer, max_time):
    now = time.time()
    elapsed = now - timer
    if elapsed > max_time:
        print("Player is bugged.")
        return True
    return False


def reset_player():
    print("Using teleport item")
    osk_tap_keyboard("alt")
    osk_tap_keyboard("1")
    first_metin = True
    path_step = 0
    first_cicle = True
    is_idle = False
    is_bugged = False
    time.sleep(10)
    print("Player teleported")
    timer = time.time()
    return first_metin, path_step, first_cicle, is_idle, is_bugged, timer


# === MAIN ===
if __name__ == "__main__":
    # Character must be at (130, 480), camera full top view
    first_skills = True
    first_metin = True
    first_consumables = True
    time.sleep(2)
    focus_window()

    skills = ["f1", "f2"]
    consumables = ["1", "2", "3", "4", "f3"]
    path_step = 0
    first_cicle = True
    is_idle = False
    is_bugged = False

    # Chronometers
    skill_timer = time.time()
    sell_timer = time.time()
    consumables_timer = time.time()
    not_working_timer = (
        time.time()
    )  # For when the character is idle or attacking for too long

    while True:
        print("=== While loop ===")
        skill_timer, first_skills = check_timer(
            skill_timer,
            skills,
            60 * 19,
            3,
            True,
            first_skills,
        )
        consumables_timer, first_consumables = check_timer(
            consumables_timer, consumables, 60 * 3, 0.5, False, first_consumables
        )
        result = gautama_370_330(path_step, first_cicle, is_idle)

        # Solo avanzar de paso si hubo movimiento efectivo
        match result:
            case "found":
                is_idle = False
                if not first_cicle:
                    path_step = (path_step + 1) % 4
                first_cicle = False
                not_working_timer = time.time()
            case "idle":
                """If is not idle it means that it is the first loop as idle -> reset not working timer
                Player found a metin -> "attacking" was returned multiple times and not_working_timer was acumulating time ->
                    Pleyer moved and did not found metin -> "idle" starts with previous not_working_timer time. This should be reseted.
                "idle" time should is not being added to "attacking" time on not_working_timer. Configure is_bugged on "idle" and "attacking" for changes.
                """
                if not is_idle:
                    not_working_timer = time.time()

                is_idle = True
                is_bugged = is_player_bugged(not_working_timer, 60)
                if is_bugged:
                    (
                        first_metin,
                        path_step,
                        first_cicle,
                        is_idle,
                        is_bugged,
                        not_working_timer,
                    ) = reset_player()
            case "attacking":
                is_idle = False
                is_bugged = is_player_bugged(not_working_timer, 60)
                if is_bugged:
                    (
                        first_metin,
                        path_step,
                        first_cicle,
                        is_idle,
                        is_bugged,
                        not_working_timer,
                    ) = reset_player()
            case "error":
                is_idle = False
                not_working_timer = time.time()
                print("Error")

        sell_timer = sell_items(sell_timer, 60 * 3)
        time.sleep(3.03)
