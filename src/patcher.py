from datetime import datetime
from hashlib import sha1
from os import path
from os import system, remove
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

from psutil import process_iter, NoSuchProcess, AccessDenied

from src.datas import PATCHES_REPOSITORY
from src.datas.patches_repository import create_patch_repo
from src.models import Patch, FileInfo
from src.widgets.event_viewer import EventViewer


def _get_file_name(path: str) -> str:
    return path.split("/")[-1]


class Patcher(object):
    _file_path = "C:/Program Files/StartAllBack/StartAllBackX64.dll"
    _backup_file_path = ""
    _bypass_hash_not_match = False

    def __init__(self, _do_backup_func: any, ev: EventViewer):
        self.ev = ev
        self.checkup_is_valid = False
        self._do_backup_func = _do_backup_func
        self.check_file_result = FileInfo()

    def checkup(self):
        """
        Check if the file is patched
        :return None
        """
        self.ev.event(f"Searching for {_get_file_name(self._file_path)}... ")
        if path.isfile(self._file_path):
            self.ev.event_done("Found")
            self.ev.event("Checking hash... ")
            self.check_file_result = self._get_file_info(self._file_path, print_hash=True)
            if self.check_file_result.is_original:
                self.ev.event_warning("Not patched")
                self.checkup_is_valid = True
            elif self.check_file_result.is_patched:
                self.ev.event_done("Patched")
            elif self._bypass_hash_not_match:
                self.ev.event_warning("Not matching (bypassed)")
                self.checkup_is_valid = True
            else:
                self.ev.event_error("Not matching")
                if messagebox.askyesno(
                        "File not matching",
                        "The file is not matching the original file. Do you want to patch it anyway ?"):
                    self._bypass_hash_not_match = True
                else:
                    self.checkup_is_valid = False
                    self._file_path = ""
        else:
            self.ev.event_error("Not found")
            self.ev.event("Select the file... ")
            self._file_path = askopenfilename(filetypes=[("DLL", "*.dll")])
            if self._file_path != "":
                self.ev.event_done("Selected")
                self.checkup()
            else:
                self.ev.event_error("Cancelled")
                self.checkup_is_valid = False

    def _get_hash(self, file_path: str, print_hash: bool = False) -> str:
        """
        Get the hash of a file
        :param file_path: Path of the file
        :param print_hash: Print the hash of the file
        :return Hash of the file
        """
        if not path.isfile(file_path):
            return ""
        with open(file_path, 'rb') as f:
            file_hash = sha1(f.read()).hexdigest()
        if print_hash:
            self.ev.event(f"{file_hash} ", color="blue")
        return file_hash

    def _get_file_info(self, file_path: str, print_hash: bool = False) -> FileInfo:
        """
        Get the information of startallback.dll
        :param file_path: Path of the file
        :param print_hash: Print the hash of the file
        :return CheckFileResult object
        """
        _hash = self._get_hash(file_path, print_hash)
        _file_info_result = FileInfo()
        for infos in PATCHES_REPOSITORY:
            _file_info_result.original_hash = infos['original_hash']
            _file_info_result.patched_hash = infos['patched_hash']
            _file_info_result.version = infos['version']
            if _hash == infos['original_hash']:
                _file_info_result.is_original = True
                break
            elif _hash == infos['patched_hash']:
                _file_info_result.is_patched = True
                break
        return _file_info_result

    @staticmethod
    def get_patches(version: str):
        """
        Get the patches for a specific version
        :param version: Version of the patch
        :return: Patches
        """
        for infos in PATCHES_REPOSITORY:
            if infos['version'] == version:
                return infos['patches']
        return []

    def _create_backup(self) -> None:
        """
        Create a backup of the file.
        :return: None
        """
        self.ev.event("Creating backup... ")
        self._backup_file_path = self._file_path + f".{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.bak"
        if self._write_file(self._backup_file_path, self._read_file(self._file_path)):
            self.ev.event_done("Done")

    def _kill_process(self, process_name: str) -> None:
        """
        Kill a process
        :param process_name: Name of the process
        :return: None
        """
        self.ev.event(f"Killing {process_name}... ")
        system(f"taskkill /f /im {process_name}")
        # wait for the process to stop
        for proc in process_iter():
            try:
                if proc.name() == process_name:
                    proc.wait()
            except (NoSuchProcess, AccessDenied):
                pass
        self.ev.event_done("Done")

    def patch(self) -> None:
        """
        Patch the file
        :return None
        """
        self.ev.add_banner("Start patch")
        if self.checkup_is_valid:
            if self._do_backup_func():
                self._create_backup()
            _original_file = self._read_file(self._file_path)
            _patched_file = _original_file
            self._kill_process("explorer.exe")
            self.ev.event("Patching... ")
            try:
                for patch in self.get_patches(self.check_file_result.version):
                    _patched_file = _patched_file[:patch.offset] + patch.bytes + \
                                    _patched_file[patch.offset + len(patch.bytes):]
            except Exception as e:
                self.ev.event_error("Failed")
                self.ev.event(f"Error: {e}", color="red")
                self._restore_backup()
                return
            if self._write_file(self._file_path, _patched_file):
                self.ev.event_done("Done")
                self.ev.event("Checking hash... ")
                if self._get_hash(self._file_path) == self.check_file_result.patched_hash:
                    self.ev.event_done("Patched")
                elif not self._bypass_hash_not_match:
                    self.ev.event_error("Not matching")
                    self.ev.event("Restoring backup... ")
                    self._restore_backup()
                else:
                    self.ev.event_warning("Not matching (bypassed)")
                    self.ev.event(f"Backup directory: {self._backup_file_path}", end="\r")
            else:
                self.ev.event_error("Failed")
            self.ev.event("Start explorer.exe", end="\n")
            system("start explorer.exe")
        else:
            self.ev.event_error("Checkup not valid")
        self.ev.add_banner("End of patch")

    def _restore_backup(self) -> None:
        """
        Restore the backup of the file
        :return: None
        """
        self.ev.event("Restoring backup... ")
        if self._write_file(self._file_path, self._read_file(self._backup_file_path)):
            self.ev.event_done("Done")
        else:
            self.ev.event_error("Failed")

    def _write_file(self, file_path: str, data: bytes) -> bool:
        """
        Write data to a file
        :param file_path: Path to the file
        :param data: Data to write
        :return True if the file was written, False otherwise
        """
        try:
            if path.isfile(file_path):
                remove(file_path)
            with open(file_path, 'wb') as f:
                f.write(data)
            return True
        except IOError as e:
            self.ev.event_error("Error while writing file : " + str(e))
            return False

    def _read_file(self, path: str) -> bytes:
        """
        Read a file
        :param path: Path of the file
        :return Data of the file
        """
        try:
            with open(path, 'rb') as f:
                return f.read()
        except IOError as e:
            self.ev.event_error("Error while reading file : " + str(e))
            raise e

    @staticmethod
    def gen_patches(original_file_path: str, patched_file_path: str, version: str) -> list[Patch]:
        """
        Generate patches from two files
        :param version: Version of the patch
        :param original_file_path: Path of the original file
        :param patched_file_path: Path of the patched file
        :return: List of patches
        """
        rf = lambda f: open(f, 'rb').read()
        hash = lambda f: sha1(rf(f)).hexdigest()
        original_file = rf(original_file_path)
        patched_file = rf(patched_file_path)
        patches = []
        patch_size = 0
        for i in range(len(original_file)):
            if original_file[i] != patched_file[i]:
                patch_size += 1
            elif patch_size > 0:
                patches.append(Patch(offset=i - patch_size, bytes=patched_file[i - patch_size:i]))
                patch_size = 0
        print(create_patch_repo(
            patches=patches,
            original_hash=hash(original_file_path),
            patched_hash=hash(patched_file_path),
            version=version))
        return patches
