# Metin2 Detection Project

Proyecto para detectar y hacer clic automáticamente en "Metin" en el juego usando OCR (Tesseract).

## 🚀 Configuración Inicial

**¿Acabas de clonar el proyecto?** Consulta [SETUP.md](SETUP.md) para una guía paso a paso de cómo configurar el proyecto desde cero (crear `venv`, instalar Tesseract, compilar C#, etc.).

## Requisitos

### 1. Python Dependencies
Instala las dependencias de Python:
```bash
pip install -r requirements.txt
```

### 2. Tesseract OCR
Tesseract es necesario para el reconocimiento óptico de caracteres (OCR). **NO se incluye en el repositorio** debido a su tamaño.

#### Opción A: Instalación Global (Recomendado)
1. Descarga Tesseract para Windows desde: https://github.com/UB-Mannheim/tesseract/wiki
2. Instálalo en la ubicación predeterminada: `C:\Program Files\Tesseract-OCR\`
3. **Actualiza la ruta en `detect_metin.py`** (línea ~11) para que apunte a: `C:\Program Files\Tesseract-OCR\tesseract.exe`

#### Opción B: Instalación Local
1. Descarga Tesseract y extrae la carpeta `tesseract` en la raíz del proyecto
2. **Actualiza la ruta en `detect_metin.py`** (línea ~11) para que apunte a la ruta correcta de `tesseract.exe` en tu sistema

### 3. MetinClicker (C#)
1. Compila el proyecto C#:
```bash
cd MetinClicker
dotnet build
```

2. El ejecutable se generará en `MetinClicker/bin/Debug/net8.0/MetinClicker.exe`

3. **Actualiza la ruta en `detect_metin.py`** (línea ~14) para que apunte a la ruta correcta del ejecutable en tu sistema

## Configuración

### Ventana del Juego
Por defecto, el script busca la ventana con el título "Elveron". Puedes modificar esto en `detect_metin.py`:
```python
window_title = 'Elveron'  # Cambia esto al título de tu ventana
```

## Uso

1. Asegúrate de que el juego esté abierto y visible
2. Ejecuta el script:
```bash
python detect_metin.py
```

El script:
- Captura la ventana del juego
- Busca la palabra "metin" usando OCR
- Mueve el cursor a la posición detectada
- Ejecuta MetinClicker para hacer clic

## Estructura del Proyecto

```
.
├── detect_metin.py      # Script principal de detección
├── requirements.txt     # Dependencias de Python
├── MetinClicker/       # Proyecto C# (compilado a bin/)
└── README.md           # Este archivo
```

## Configuración de Git

Este proyecto está configurado para excluir archivos pesados del repositorio Git mediante `.gitignore`. Esto es la práctica estándar para proyectos con dependencias grandes.

### Archivos Excluidos
- `tesseract/` - Tesseract OCR (demasiado pesado, ~100MB+)
- `venv/` - Entorno virtual de Python (se regenera con `pip install`)
- `MetinClicker/bin/` y `MetinClicker/obj/` - Archivos de compilación (se regeneran con `dotnet build`)

### Subir el Proyecto a Git

1. **Inicializar Git** (si no está inicializado):
```bash
git init
```

2. **Verificar que `.gitignore` está funcionando**:
```bash
git status
```
Deberías ver que `tesseract/`, `venv/`, y `bin/` NO aparecen en los archivos a agregar.

3. **Agregar archivos al repositorio**:
```bash
git add .
git commit -m "Initial commit"
```

4. **Crear repositorio remoto** (GitHub, GitLab, etc.) y conectar:
```bash
git remote add origin <URL_DEL_REPOSITORIO>
git push -u origin main
```

### ¿Por qué no incluir Tesseract en Git?

- **Tamaño**: Tesseract ocupa ~100MB+, haciendo el repositorio innecesariamente grande
- **Plataforma**: Los binarios son específicos de Windows/Linux/Mac
- **Actualización**: Es mejor que cada usuario instale la versión más reciente
- **Mejores prácticas**: Los binarios y dependencias pesadas no deben estar en Git

### Alternativas para Distribuir Tesseract

Si realmente necesitas distribuir Tesseract con el proyecto, considera:

1. **Git LFS** (Large File Storage): Para archivos grandes, pero tiene límites en repositorios gratuitos
2. **Releases de GitHub**: Subir Tesseract como un archivo ZIP en las releases
3. **Instalador automático**: Script que descarga Tesseract automáticamente durante la instalación
4. **Docker**: Si el proyecto se ejecuta en contenedores

Para este proyecto, **recomendamos la Opción A** (instalación global) como se describe en los requisitos.

## Notas

- Los archivos pesados (Tesseract, `venv/`, `bin/`, `obj/`) están excluidos del repositorio mediante `.gitignore`
- Cada usuario debe instalar Tesseract según sus preferencias
- **Importante:** Después de clonar, debes actualizar las rutas en `detect_metin.py` para que apunten a las ubicaciones correctas en tu sistema
- Consulta [SETUP.md](SETUP.md) para instrucciones detalladas de configuración

## Troubleshooting

### Tesseract no encontrado
- Verifica que Tesseract esté instalado
- Comprueba que la ruta en `detect_metin.py` (línea ~11) sea correcta
- Asegúrate de que el ejecutable tenga permisos de ejecución
- Verifica que la ruta use barras invertidas dobles (`\\`) o una `r` antes de la cadena (raw string)

### Ventana no encontrada
- Verifica el título de la ventana del juego
- Asegúrate de que la ventana esté abierta y visible
- Modifica `window_title` en el script si es necesario

### MetinClicker no encontrado
- Compila el proyecto C# primero: `cd MetinClicker && dotnet build`
- Verifica la ruta en `detect_metin.py` (línea ~14)
- Asegúrate de que el ejecutable exista en la ruta especificada

