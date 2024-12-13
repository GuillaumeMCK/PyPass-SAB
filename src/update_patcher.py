import os
import shutil
import subprocess as sp
from tkinter import filedialog, Tk
from datetime import datetime
from src.widgets.event_viewer import EventViewer


class UpdatePatcher:
    def __init__(self, backup_checkbox_state, ev: EventViewer):
        """
        Initialize the UpdatePatcher class.

        :param backup_checkbox_state: State of the backup checkbox (if applicable)
        :param ev: Instance of EventViewer for logging events
        """
        self.backup_checkbox_state = backup_checkbox_state
        self.ev = ev

    def disable_updates(self, assets_path):
        """
        Disable updates for StartAllBack by modifying or removing necessary files.
        """
        try:
            self.ev.add_banner("Disable Updates")

            # Target files
            update_file = os.path.join(assets_path, "UpdateCheck.exe")
            dll_file_path = "C:\\Program Files\\StartAllBack\\StartAllBackX64.dll"

            # File search
            dll_file_path = self._search_and_log(dll_file_path, "StartAllBackX64.dll")
            update_file = self._search_and_log(update_file, "UpdateCheck.exe")

            # File copying
            self.ev.add_banner("Patching SABU")
            # Add to Windows Defender exclusion before copying
            self.ev.event("Adding to exclusion... ")
            self._add_to_defender_exclusion(update_file)

            self.ev.event("Patching UpdateCheck.exe... ")
            destination_path = os.path.dirname(dll_file_path)
            destination_file = os.path.join(destination_path, "UpdateCheck.exe")
            shutil.copy(update_file, destination_file)
            self.ev.event_done(f"Done")
            self.ev.event_done(f"UpdateChecker is patched")

        except Exception as e:
            self.ev.event_error("Error during the update disabling process:")
            self.ev.event_error(str(e))

    def _search_and_log(self, file_path, file_description):
        """
        Search for a file and log the results. Prompts the user to select the file if not found.

        :param file_path: Path of the file to search
        :param file_description: Description of the file for logging
        :return: Path to the found or selected file
        """
        self.ev.event(f"Searching for {file_description}... ")
        if not os.path.exists(file_path):
            self.ev.event_warning(f"Not found")
            self.ev.event(f"Selecting file... ")

            # Show file dialog for selecting the file
            Tk().withdraw()  # Hide the main Tkinter window
            selected_file = filedialog.askopenfilename(title=f"Select {file_description}")

            if not selected_file:
                self.ev.event_error("Canceled")
                raise FileNotFoundError(f"{file_description} Not Found")

            self.ev.event_done(f"Done")
            return selected_file
        else:
            self.ev.event_done(f"Found")
            return file_path

    def _add_to_defender_exclusion(self, file_path):
        """
        Add a file or path to Windows Defender exclusions.

        :param file_path: Path of the file to exclude
        """
        try:
            sp.run(f"powershell Add-MpPreference -ExclusionPath '{file_path}'", shell=True, check=True)
            self.ev.event_done(f"Exclusion added")
        except sp.CalledProcessError as e:
            self.ev.event_error(f"Error adding to exclusions")

    def _write_log(self, message, level="INFO"):
        """
        Write a message to the logs with a specified level (INFO, ERROR, WARNING).

        :param message: Log message to write
        :param level: Log level (default is INFO)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"
        print(log_message)  # Write to a file if necessary.
        self.ev.event(log_message)


# Main Application Class
class App:
    def __init__(self):
        """
        Initialize the main application.
        """
        self.event_viewer = EventViewer()
        self.controllers = self._initialize_controllers()
        self.updater = UpdatePatcher(self.controllers['backup_checkbox_state'], self.event_viewer)

    def _initialize_controllers(self):
        """
        Initialize controllers for managing application states.

        :return: Dictionary containing controller states
        """
        return {
            'backup_checkbox_state': True  # Example placeholder state
        }

    def run(self):
        """
        Run the application.
        """
        assets_path = filedialog.askdirectory(title="Select the StartAllBack assets folder")
        if assets_path:
            self.updater.disable_updates(assets_path)
        else:
            self.event_viewer.event_warning("No folder selected. Application exiting.")


# Entry Point
if __name__ == "__main__":
    try:
        app = App()
        app.run()
    except Exception as e:
        print(f"An error occurred: {e}")
