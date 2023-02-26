import PyInstaller.__main__ as pyi

# Définition des options pour PyInstaller
pyinstaller_options = [
    "--name=PyPass-SAB",
    "--noconfirm",
    "--onefile",
    "--windowed",
    "--noconsole",
    "--uac-admin",
    "--icon=src/assets/icon.ico",
    f"--add-data=./env/Lib/site-packages/customtkinter;customtkinter/",
    "--add-data=./src/assets;/assets/",
    "--exclude-module=PyInstaller"
]

# Définition des chemins d'entrée et de sortie pour PyInstaller
input_path = "main.py"

# Appel de PyInstaller avec les options et les chemins définis
pyi.run(pyi_args=pyinstaller_options + [str(input_path)])
