from pyuac import isUserAdmin, runAsAdmin
from src import App

if __name__ == "__main__":
    if not isUserAdmin():
        runAsAdmin()
    else:
        app = App()
        app.mainloop()
