# detect_metin.py
import pytesseract
from PIL import ImageGrab
import pygetwindow as gw
import subprocess
import sys
import pyautogui
import time

# Ruta local del tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Pablo\Programacion\metin2\metins\tesseract\tesseract.exe'

# Ruta a tu ejecutable de MetinClicker
metin_clicker_exe = r'C:\Pablo\Programacion\metin2\metins\MetinClicker\bin\Debug\net8.0\MetinClicker.exe'

# Buscar ventana del juego
window_title = 'Elveron'  # Cambia esto si tu ventana tiene otro nombre
windows = gw.getWindowsWithTitle(window_title)
if not windows:
    print(f"❌ Ventana '{window_title}' no encontrada")
    sys.exit()
win = windows[0]

# Captura solo la ventana del juego
bbox = (win.left, win.top, win.right, win.bottom)
screenshot = ImageGrab.grab(bbox=bbox)

# Obtener datos de cada palabra detectada
data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

click_sent = False

# Recorrer palabras detectadas y buscar "metin"
for i, word in enumerate(data['text']):
    if 'metin' in word.lower():
        # Coordenadas dentro del screenshot
        x = data['left'][i] + data['width'][i] // 2 + 30
        y = data['top'][i] + data['height'][i] + 30  # un poco debajo del texto

        # Convertir coordenadas relativas a la pantalla
        screen_x = win.left + x
        screen_y = win.top + y

        print(f"'Metin' encontrado en: x={screen_x}, y={screen_y}")
        click_sent = True

        # Mover el cursor a las coordenadas detectadas
        print(f"Moviendo cursor a: x={screen_x}, y={screen_y}")
        pyautogui.moveTo(screen_x, screen_y, duration=0.1)
        
        # Pequeña pausa para asegurar que el cursor se ha movido
        time.sleep(0.05)

        # Ejecutar MetinClicker con las coordenadas y el título de la ventana
        # El .exe ahora hará click en la posición donde está el cursor (que acabamos de mover)
        try:
            result = subprocess.run(
                [metin_clicker_exe, str(screen_x), str(screen_y), window_title],
                capture_output=True,
                text=True,
                shell=False  # No necesitamos shell=True para ejecutar .exe
            )
            print("stdout:", result.stdout)
            if result.stderr:
                print("stderr:", result.stderr)
        except Exception as e:
            print(f"Error ejecutando MetinClicker: {e}")

        break  # Solo un click, salir del loop

if not click_sent:
    print("❌ No se encontró ningún 'Metin' en la ventana.")


""" 
# detect_metin.py
import pytesseract
from PIL import ImageGrab
import pygetwindow as gw
import subprocess
import sys

# Ruta local del tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Pablo\Programacion\metin2\metins\tesseract\tesseract.exe'

# Ruta a tu ejecutable de MetinClicker
metin_clicker_exe = r'C:\Pablo\Programacion\metin2\metins\MetinClicker\bin\Debug\net8.0\MetinClicker.exe'

# Buscar ventana del juego
windows = gw.getWindowsWithTitle('Elveron')
if not windows:
    print("❌ Ventana no encontrada")
    sys.exit()
win = windows[0]

# Captura solo la ventana del juego
screenshot = ImageGrab.grab()

# Obtener datos de cada palabra detectada
data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

click_sent = False

# Recorrer palabras detectadas y buscar "metin"
for i, word in enumerate(data['text']):
    if 'metin' in word.lower():
        # Coordenadas dentro del screenshot
        x = data['left'][i] + 30
        y = data['top'][i] + 30  # un poco debajo del texto

        print(f"'Metin' encontrado en: x={x}, y={y}")
        click_sent = True

        # Ejecutar MetinClicker
        try:
            result = subprocess.run([metin_clicker_exe, str(x), str(y)])
            print("stdout:", result.stdout)
            print("stderr:", result.stderr)
        except Exception as e:
            print("Error ejecutando MetinClicker:", e)

        break  # Solo un click, salir del loop

if not click_sent:
    print("❌ No se encontró ningún 'Metin' en la ventana.")

 """