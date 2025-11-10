import pytesseract
from PIL import ImageGrab
import pygetwindow as gw
import subprocess
import sys
import pyautogui
import time

# Finding tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Pablo\Programacion\metin2\metins\tesseract\tesseract.exe'

# Client clicker on C#
metin_clicker_exe = r'C:\Pablo\Programacion\metin2\metins\MetinClicker\bin\Debug\net8.0\MetinClicker.exe'

# Finding window of the game
window_title = 'Elveron'  # Change this if your window has another name
windows = gw.getWindowsWithTitle(window_title)
if not windows:
    print(f"❌ Window '{window_title}' not found")
    sys.exit()
win = windows[0]

# Capture only the window of the game
bbox = (win.left, win.top, win.right, win.bottom)
screenshot = ImageGrab.grab(bbox=bbox)

# Get data of each detected word
data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

click_sent = False

# Iterate through detected words and search for "metin"
for i, word in enumerate(data['text']):
    if 'metin' in word.lower():
        # Coordinates inside the screenshot
        x = data['left'][i] + data['width'][i] // 2 + 30
        y = data['top'][i] + data['height'][i] + 30  # un poco debajo del texto

        # Convert relative coordinates to screen
        screen_x = win.left + x
        screen_y = win.top + y

        print(f"'Metin' encontrado en: x={screen_x}, y={screen_y}")
        click_sent = True

        # Move the cursor to the detected coordinates
        print(f"Moviendo cursor a: x={screen_x}, y={screen_y}")
        pyautogui.moveTo(screen_x, screen_y, duration=0.1)
        
        # Small pause to ensure the cursor has moved
        time.sleep(0.05)

        # Execute MetinClicker with the coordinates and the window title
        # The .exe will now click in the position where the cursor is (that we just moved)
        try:
            result = subprocess.run(
                [metin_clicker_exe, str(screen_x), str(screen_y), window_title],
                capture_output=True,
                text=True,
                shell=False
            )
            print("stdout:", result.stdout)
            if result.stderr:
                print("stderr:", result.stderr)
        except Exception as e:
            print(f"Error executing MetinClicker: {e}")

        break  # Just one click, exit the loop

if not click_sent:
    print("❌ No 'Metin' found in the window.")