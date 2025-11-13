# Metin2 Clicker – Workflow

## Actiave python env
```bash
source venv/Scripts/activate
```

## Compile C#
```bash
cd MetinClicker
dotnet build -c Release
```

# Generate global .exe inside /publish

## 1. Update C# .exe file
```bash
cd C:\Pablo\Programacion\metin2\metins\Interactions
dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true -o ./publish
```

## 2. Generate .exe for Python + C#
```bash
pyinstaller --noconfirm --onefile --add-data "tesseract;tesseract" --add-data "Interactions\publish;Interactions\publish" --hidden-import pytesseract --hidden-import PIL --hidden-import pygetwindow --name interaction_controller_pc interaction_controller.py
```

## 3. Final result
```bash
dist\interaction_controller.exe
```

# Utils

## Parser
```bash
black <.py file>
```

## To create Program.cs folder
```bash
dotnet new console -n OKSClicker
```

# Resumed information

### Steps to generate global .exe file:
```bash
1- If C# changed (Esto actualiza el Interactions.exe dentro de publish): 
   cd C:\Pablo\Programacion\metin2\metins\Interactions
   dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true -o ./publish
2- Update Python and .exe:
   cd C:\Pablo\Programacion\metin2\metins
   notebook name: pyinstaller --noconfirm --onefile --add-data "tesseract;tesseract" --add-data "Interactions\publish;Interactions\publish" --hidden-import pytesseract --hidden-import PIL --hidden-import pygetwindow --name interaction_controller interaction_controller.py
   pc name: pyinstaller --noconfirm --onefile --add-data "tesseract;tesseract" --add-data "Interactions\publish;Interactions\publish" --hidden-import pytesseract --hidden-import PIL --hidden-import pygetwindow --name interaction_controller_pc interaction_controller.py
3- New .exe generated at dist\interaction_controller.exe
```