from pyuac import isUserAdmin, runAsAdmin
from src.app import App

if __name__ == "__main__":
    if not isUserAdmin():
        runAsAdmin()
    else:
        app = App()
        app.mainloop()
