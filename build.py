import PyInstaller.__main__ as pyi

pyinstaller_options = [
    "--name=PyPass-SAB",
    "--noconfirm",
    "--onefile",
    "--windowed",
    "--noconsole",
    "--uac-admin",
    "--icon=src/assets/icon.ico",
    "--add-data=./env/Lib/site-packages/customtkinter;customtkinter/",
    "--add-data=./src/assets;/assets/",
    "--exclude-module=PyInstaller"
]

input_path = "main.py"

pyi.run(pyi_args=pyinstaller_options + [str(input_path)])
