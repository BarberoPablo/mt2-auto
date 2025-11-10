import pytesseract
from PIL import ImageGrab
import pygetwindow as gw
import subprocess
import sys
import pyautogui
import time

# === CONFIGURACIÓN ===
pytesseract.pytesseract.tesseract_cmd = r'C:\Pablo\Programacion\metin2\metins\tesseract\tesseract.exe'
metin_clicker_exe = r'C:\Pablo\Programacion\metin2\metins\MetinClicker\bin\Debug\net8.0\MetinClicker.exe'
window_title = 'Elveron'


# === FUNCIONES BASE ===

def run_metin_clicker(*args):
    """Ejecuta el .exe MetinClicker con los argumentos dados."""
    try:
        result = subprocess.run(
            [metin_clicker_exe, *map(str, args)],
            capture_output=True,
            text=True,
            shell=False
        )
        if result.stdout.strip():
            print("stdout:", result.stdout.strip())
        if result.stderr.strip():
            print("stderr:", result.stderr.strip())
    except Exception as e:
        print(f"⚠️ Error ejecutando MetinClicker: {e}")


def focus_window():
    """Hace foco en la ventana del juego."""
    print(f"→ Haciendo foco en la ventana '{window_title}'...")
    run_metin_clicker("focus", window_title)


def click_metin():
    """Detecta la palabra 'metin' en la ventana del juego y hace click en ella."""
    print("→ Buscando ventana del juego...")
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        print(f"❌ Ventana '{window_title}' no encontrada")
        return

    win = windows[0]

    # Capturamos la zona visible del juego
    bbox = (win.left, win.top, win.right, win.bottom)
    screenshot = ImageGrab.grab(bbox=bbox)

    # OCR con pytesseract
    data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

    for i, word in enumerate(data['text']):
        if 'metin' in word.lower():
            # Calculamos coordenadas relativas y absolutas
            x = data['left'][i] + data['width'][i] // 2 + 30
            y = data['top'][i] + data['height'][i] + 30
            screen_x = win.left + x
            screen_y = win.top + y

            print(f"✅ 'Metin' encontrado en: x={screen_x}, y={screen_y}")

            # Mover el cursor
            pyautogui.moveTo(screen_x, screen_y, duration=0.1)
            time.sleep(0.05)

            # Ejecutar click mediante el .exe
            run_metin_clicker("click", screen_x, screen_y, window_title)
            return

    print("❌ No se encontró ningún 'Metin' en la ventana.")


# === MAIN ===

def main():
    """Ejecución principal: foco + click una sola vez."""
    print("Iniciando búsqueda y click de Metin...\n")

    focus_window()
    time.sleep(0.3)  # pequeño delay para asegurar el foco
    click_metin()

    print("\nEjecución terminada (loop simple).")


if __name__ == "__main__":
    main()