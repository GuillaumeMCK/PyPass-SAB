import PyInstaller.__main__ as pyi

pyinstaller_options = [
    "--name=PyPass-SAB",
    "--noconfirm",
    "--onefile",
    "--windowed",
    "--noconsole",
    "--uac-admin",
    "--icon=src/assets/icon.ico",
    "--add-data=src/assets;/assets/",
    "--add-data=env/Lib/site-packages/customtkinter;customtkinter/",
    "--exclude-module=PyInstaller",
]

script_name = "main.py"

pyi.run(pyi_args=[str(script_name)] + pyinstaller_options)
