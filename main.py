from pyuac import isUserAdmin, runAsAdmin

from idlelib.idle_test.test_configdialog import root
from src import App
import requests
import os
import subprocess
import tkinter as tk
import webbrowser
from tkinter import messagebox


def get_remote_version(url):
    """
    Fetches the version from a remote URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Error fetching version: {e}")
        return None

def is_update_available(current_version, version_url):
    """
    Checks if an update is available.
    """
    remote_version = get_remote_version(version_url)
    if not remote_version:
        return False

    return remote_version != current_version

def prompt_for_update_with_msgbox(update_url):
    """
    Prompts the user for update using a VBScript MsgBox.
    """
    vbscript_content = f"""
    Dim result
    result = MsgBox("An update is available. Do you want to update?", vbYesNo + vbQuestion, "Update Available")
    If result = vbYes Then
        WScript.Echo "yes"
    Else
        WScript.Echo "no"
    End If
    """
    # Create a temporary VBScript file
    vbs_file = "sap_prompt_update.vbs"
    with open(vbs_file, "w") as file:
        file.write(vbscript_content)

    # Execute the VBScript and capture the response
    try:
        result = subprocess.check_output(["cscript", "//NoLogo", vbs_file], text=True).strip()
        if result.lower() == "yes":
            webbrowser.open(update_url)
            return True
    finally:
        os.remove(vbs_file)  # Clean up the VBScript file
    return False

if __name__ == "__main__":
    CURRENT_VERSION = "0.8.3"
    VERSION_URL = "https://raw.githubusercontent.com/danbenba/StartAllPatch/refs/heads/project/version"
    UPDATE_URL = "https://github.com/danbenba/StartAllPatch"

    if not isUserAdmin():
        runAsAdmin()
    else:
        if is_update_available(CURRENT_VERSION, VERSION_URL):
            if prompt_for_update_with_msgbox(UPDATE_URL):
                exit()  # Exits the program after redirecting
        messagebox.showinfo(
            "Note",
            "This is a beta version of StartAllPatch.\n\n"
            "If you encounter any issues, please report them at:\n\n"
            "https://github.com/danbenba/startallpatch/issues"
        )
        app = App()
        app.mainloop()
