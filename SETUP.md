# Guía de Configuración del Proyecto

Esta guía explica cómo configurar el proyecto desde cero después de clonarlo desde Git.

## Paso 1: Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd metins
```

## Paso 2: Configurar el Entorno Virtual de Python

### Windows (PowerShell)
```bash
# Crear entorno virtual
python -m venv venv

# Activar el entorno virtual
.\venv\Scripts\Activate.ps1

# Si tienes problemas con la política de ejecución, ejecuta primero:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Windows (CMD)
```bash
# Crear entorno virtual
python -m venv venv

# Activar el entorno virtual
venv\Scripts\activate.bat
```

### Linux/Mac
```bash
# Crear entorno virtual
python3 -m venv venv

# Activar el entorno virtual
source venv/bin/activate
```

## Paso 3: Instalar Dependencias de Python

Una vez activado el entorno virtual (deberías ver `(venv)` al inicio de tu línea de comando):

```bash
# Actualizar pip (recomendado)
python -m pip install --upgrade pip

# Instalar todas las dependencias
pip install -r requirements.txt
```

Esto instalará:
- `pytesseract`
- `pillow`
- `opencv-python`
- `numpy`
- `pyautogui`
- `pygetwindow`

## Paso 4: Instalar Tesseract OCR

### Opción A: Instalación Global (Recomendado)

1. **Descargar Tesseract:**
   - Ve a: https://github.com/UB-Mannheim/tesseract/wiki
   - Descarga el instalador para Windows (ej: `tesseract-ocr-w64-setup-5.x.x.exe`)

2. **Instalar:**
   - Ejecuta el instalador
   - **Importante:** Instálalo en la ruta predeterminada: `C:\Program Files\Tesseract-OCR\`
   - O anota la ruta donde lo instales

3. **Actualizar la ruta en `detect_metin.py`:**
   - Abre `detect_metin.py`
   - Busca la línea: `pytesseract.pytesseract.tesseract_cmd = r'C:\Pablo\Programacion\metin2\metins\tesseract\tesseract.exe'`
   - Cámbiala por: `pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'`
   - O la ruta donde lo hayas instalado

### Opción B: Instalación Local en el Proyecto

1. **Descargar Tesseract:**
   - Ve a: https://github.com/UB-Mannheim/tesseract/wiki
   - Descarga el instalador portable o extrae los binarios

2. **Extraer en el proyecto:**
   - Crea una carpeta `tesseract` en la raíz del proyecto
   - Extrae todos los archivos de Tesseract ahí
   - Asegúrate de que `tesseract.exe` esté en `tesseract/tesseract.exe`

3. **Verificar la ruta:**
   - La ruta en `detect_metin.py` ya debería apuntar a `tesseract/tesseract.exe`
   - Si el proyecto está en otra ubicación, actualiza la ruta absoluta

## Paso 5: Compilar el Proyecto C#

### Windows
```bash
# Navegar a la carpeta del proyecto C#
cd MetinClicker

# Compilar el proyecto
dotnet build

# El ejecutable se generará en:
# MetinClicker/bin/Debug/net8.0/MetinClicker.exe
```

**Nota:** Asegúrate de tener .NET SDK 8.0 instalado. Si no lo tienes:
- Descárgalo desde: https://dotnet.microsoft.com/download/dotnet/8.0

### Verificar la ruta del ejecutable
- Abre `detect_metin.py`
- Busca: `metin_clicker_exe = r'C:\Pablo\Programacion\metin2\metins\MetinClicker\bin\Debug\net8.0\MetinClicker.exe'`
- Cambia la ruta absoluta por la ruta correcta en tu sistema

## Paso 6: Verificar que Todo Funciona

1. **Verificar Python:**
```bash
python --version
# Debería mostrar Python 3.x
```

2. **Verificar dependencias:**
```bash
pip list
# Deberías ver pytesseract, pillow, opencv-python, etc.
```

3. **Verificar Tesseract:**
```bash
# Si Tesseract está en el PATH:
tesseract --version

# O verifica que el archivo existe en la ruta configurada en detect_metin.py
```

4. **Verificar MetinClicker:**
```bash
# Verifica que el ejecutable existe:
# MetinClicker\bin\Debug\net8.0\MetinClicker.exe
```

## Resumen de Cambios Necesarios en `detect_metin.py`

Después de clonar el proyecto, necesitarás actualizar estas dos rutas en `detect_metin.py`:

1. **Ruta de Tesseract** (línea ~11):
   ```python
   # Cambiar de:
   pytesseract.pytesseract.tesseract_cmd = r'C:\Pablo\Programacion\metin2\metins\tesseract\tesseract.exe'
   
   # A tu ruta local, por ejemplo:
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   # O si lo pusiste en el proyecto:
   pytesseract.pytesseract.tesseract_cmd = r'C:\ruta\a\tu\proyecto\tesseract\tesseract.exe'
   ```

2. **Ruta de MetinClicker** (línea ~14):
   ```python
   # Cambiar de:
   metin_clicker_exe = r'C:\Pablo\Programacion\metin2\metins\MetinClicker\bin\Debug\net8.0\MetinClicker.exe'
   
   # A tu ruta local, por ejemplo:
   metin_clicker_exe = r'C:\ruta\a\tu\proyecto\MetinClicker\bin\Debug\net8.0\MetinClicker.exe'
   ```

## Troubleshooting

### Error: "Tesseract no encontrado"
- Verifica que Tesseract esté instalado
- Verifica que la ruta en `detect_metin.py` sea correcta
- Prueba ejecutar `tesseract --version` en la terminal

### Error: "No module named 'pytesseract'"
- Asegúrate de que el entorno virtual esté activado
- Ejecuta: `pip install -r requirements.txt`

### Error: "MetinClicker.exe no encontrado"
- Compila el proyecto C#: `cd MetinClicker && dotnet build`
- Verifica que la ruta en `detect_metin.py` sea correcta

### El entorno virtual no se activa
- Windows PowerShell: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Verifica que Python esté instalado correctamente
- Usa la ruta completa: `.\venv\Scripts\Activate.ps1`

## Notas Importantes

- **Nunca subas `venv/` o `tesseract/` a Git** - están en `.gitignore` por una razón
- Cada desarrollador debe configurar su propio entorno virtual
- Las rutas absolutas en `detect_metin.py` deben ajustarse en cada máquina
- Considera usar rutas relativas o variables de entorno en el futuro para hacer el código más portátil

