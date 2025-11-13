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

# === CONFIG ===
pytesseract.pytesseract.tesseract_cmd = r"C:\Pablo\Programacion\metin2\metins\tesseract\tesseract.exe"
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
    "alt": [1368 + 22 * 3, 1060],
}


# === Click Functions ===
def run_clicker(
    *args,
):  # clicker decides wheter to click on the client or in the OSK, based on args
    exe = Path(clicker_exe)
    if not exe.exists():
        print(f".exe not found: {exe}")
        return False
    result = subprocess.run([str(exe), *map(str, args)], capture_output=True, text=True, shell=False)
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
    duration = (angle / 360.0) * 3.99  # It takes around 4 seconds to perform a 360° rotation
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
            x = win.left + data["left"][i] + data["width"][i] // 2 + 30
            y = win.top + data["top"][i] + data["height"][i] // 2 + 30
            if 880 < x < 920 and 80 < y < 95:
                metin_ui_detected = True
                break
    if metin_ui_detected:
        print("[attacking] Metin UI detected")
        return "attacking"

    if not first_cicle and not idle:
        osk_tap_keyboard("z")
        match step:
            case 0:
                print("Case 0, moving top left")
                x, y = 450, 70
                pyautogui.moveTo(x, y, duration=0.05)
                click_at(x, y)
                time.sleep(3)
            case 1:
                print("Case 1, moving right")
                x, y = 1800, 550
                pyautogui.moveTo(x, y, duration=0.05)
                click_at(x, y)
                time.sleep(3)
            case 2:
                print("Case 2, moving top left")
                x, y = 660, 50
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
        print(f"[found] Nearest Metin found at ({x}, {y}). Distance: {min_distance}")
        pyautogui.moveTo(x, y, duration=0.05)
        click_at(x, y)
        time.sleep(2)  # Give time to start attacking metin
        return "found"

    print("[idle] No metin found.")
    return "idle"


def get_closest_metin(win, data):
    player_x, player_y = 960, 530  # Screen center
    closest_metin = None
    min_distance = float("inf")

    for i, word in enumerate(data["text"]):
        if "metin" in word.lower():
            x = win.left + data["left"][i] + data["width"][i] // 2 + 30
            y = win.top + data["top"][i] + data["height"][i] + 30
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
    not_working_timer = time.time()  # For when the character is idle or attacking for too long

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
        consumables_timer, first_consumables = check_timer(consumables_timer, consumables, 60 * 3, 0.5, False, first_consumables)
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
                """ If is not idle it means that it is the first loop as idle -> reset not working timer
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
