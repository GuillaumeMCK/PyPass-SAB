import subprocess as sp
from datetime import datetime
from hashlib import sha1
from os import path, remove
from re import search
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

from psutil import process_iter, NoSuchProcess, AccessDenied

from src.datas import PATCHES_REPOSITORY
from src.datas.patches_repository import create_patch_repo, HKEY_TRIAL_REMINDER
from src.models import Patch, FileInfo
from src.regedit import Regedit as reg
from src.widgets.event_viewer import EventViewer


def _get_file_name(path: str) -> str:
    return path.split("/")[-1]


class Patcher(object):
    _file_path = "C:/Program Files/StartAllBack/StartAllBackX64.dll"
    _backup_file_path = None
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
        self.ev.add_banner("Checkup")
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
            self._file_path = self._select_file()
            if self._file_path != "":
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

    def reset_trail_reminder(self) -> None:
        """
        Reset the registry
        :return: None
        """
        regex = r"\{[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{11}\}"

        self.ev.add_banner("Reset trial reminder")
        self.ev.event("Deleting registry keys... ")
        try:
            sub_keys = reg.get_sub_keys_in_key(reg.get_key(HKEY_TRIAL_REMINDER))
            keys_uid = (search(regex, sub_key)[0] for sub_key in sub_keys if
                        search(regex, sub_key) is not None)

            if len(list(keys_uid)) > 0:
                for uid in keys_uid:
                    reg.delete_key(HKEY_TRIAL_REMINDER + uid)

        except FileNotFoundError:
            pass

        except Exception as e:
            self.ev.event_error("Error")
            self.ev.event_error(str(e))
            return
        self.ev.event_warning("Not found")

    @staticmethod
    def get_patches(version: str) -> list[Patch]:
        """
        Get the patches for a specific version
        :param version: Version of the patch
        :return: List of Patch objects
        """
        for infos in PATCHES_REPOSITORY:
            if infos['version'] == version:
                for patch in infos['patches']:
                    yield Patch(offset=patch['offset'], bytes=patch['bytes'])
        return []

    def _create_backup(self) -> None:
        """
        Create a backup of the file.
        :return: None
        """
        self.ev.event("Creating backup... ")
        self._backup_file_path = self._file_path + f".{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.bak"
        self._write_file(self._backup_file_path, self._read_file(self._file_path))

    def _kill_process(self, *process_names: str) -> None:
        """
        Kill a process
        :param process_name: Name of the process
        :return: None
        """
        self.ev.event(f"Killing [{', '.join(process_names)}]... ")
        sp.run(f"taskkill /f /im {' /im '.join(process_names)}", shell=True, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
        # wait for the process to stop
        for proc in process_iter():
            try:
                if proc.name() in process_names:
                    proc.wait()
            except (AccessDenied, NoSuchProcess):
                pass
        self.ev.event_done("Done")

    def patch(self) -> None:
        """
        Patch the file
        :return None
        """
        self.ev.add_banner("Patching")
        if self.checkup_is_valid:
            if self._do_backup_func():
                self._create_backup()
            _original_file = self._read_file(self._file_path)
            _patched_file = _original_file
            self._kill_process("explorer.exe", "StartAllBackCfg.exe")
            self.ev.event("Patching... ")
            try:
                for patch in self.get_patches(self.check_file_result.version):
                    _patched_file = _patched_file[:patch.offset] + patch.bytes + \
                                    _patched_file[patch.offset + len(patch.bytes):]
            except Exception as e:
                self.ev.event(f"Error: {e}", color="red")
                self.restore()
                return
            if self._write_file(self._file_path, _patched_file):
                self._check_hash()
            else:
                self.ev.event_error("Failed")
            self._start_explorer()
        else:
            self.ev.event_error("Checkup not valid")

    def _check_hash(self):
        self.ev.event("Checking hash... ")
        if self._get_hash(self._file_path) == self.check_file_result.patched_hash:
            self.ev.event_done("Patched")
        elif not self._bypass_hash_not_match:
            self.ev.event_error("Not matching")
            self.restore()
        else:
            self.ev.event_warning("Not matching (bypassed)")
            self.ev.event(f"Backup directory: {self._backup_file_path}")

    def restore(self) -> None:
        """
        Restore the backup of the file
        :return: None
        """
        self.ev.add_banner("Restore backup")
        new_path = None
        if self._backup_file_path is None:
            while True:
                new_path = self._select_file()
                if new_path is None:
                    return
                elif self._get_hash(new_path) == self.check_file_result.original_hash:
                    break
                else:
                    self.ev.event_error("Invalid file")

        self._kill_process("explorer.exe", "StartAllBackCfg.exe")
        self.ev.event("Restoring backup... ")
        self._write_file(self._file_path, self._read_file(
            self._backup_file_path if self._backup_file_path is not None else new_path))
        self._start_explorer()

    def _start_explorer(self):
        sp.run("start explorer.exe", shell=True, stdout=sp.DEVNULL, stderr=sp.DEVNULL)

    def _select_file(self) -> str or None:
        """
        Select a file
        :return: Path of the file
        """
        self.ev.event("Selecting file... ")
        file_path = askopenfilename(title="Select file", filetypes=[("Executable", "*.dll"), ("Executable", "*.bak")],
                                    initialdir="C:/Program Files/")
        if file_path == '':
            self.ev.event_error("Cancelled")
            return None
        self.ev.event_done("Done")
        return file_path

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
            self.ev.event_done("Done")
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
