import ctypes
import subprocess as sp
import sys
from ctypes import wintypes
from datetime import datetime
from hashlib import sha1
from os import path, remove
from re import search
from tkinter.filedialog import askopenfilename

from psutil import process_iter, NoSuchProcess, AccessDenied

from src.datas import *
from src.datas.functions_footprint import PATCHED_FUNCS_FOOTPRINTS
from src.datas.patches_repository import create_patch_repo, HKEY_TRIAL_REMINDER
from src.models import Patch, FileInfo
from src.regedit import Regedit as reg
from src.widgets.event_viewer import EventViewer

# Define necessary types
CHAR = ctypes.c_char
DWORD = wintypes.DWORD
HGLOBAL = wintypes.HGLOBAL

# Function prototype
GetSystemFirmwareTable: ctypes.WINFUNCTYPE = ctypes.windll.kernel32.GetSystemFirmwareTable
GetSystemFirmwareTable.restype = DWORD
GetSystemFirmwareTable.argtypes = [DWORD, DWORD, wintypes.LPVOID, DWORD]

GlobalAlloc: ctypes.WINFUNCTYPE = ctypes.windll.kernel32.GlobalAlloc
GlobalAlloc.restype = HGLOBAL
GlobalAlloc.argtypes = [wintypes.UINT, wintypes.SIZE]

# Constants
RSMB: DWORD = DWORD(int.from_bytes(b"RSMB", byteorder="big"))


def _get_file_name(path: str) -> str:
    return path.split("/")[-1]


class Patcher(object):
    _file_path = "C:/Program Files/StartAllBack/StartAllBackX64.dll"
    _backup_file_path = None

    def __init__(self, _do_backup_func: any, ev: EventViewer):
        self.ev = ev
        self.checkup_is_valid = False
        self._do_backup_func = _do_backup_func
        self.check_file_result = FileInfo()
        self.already_patched = False

    def checkup(self):
        """
        Check if the file is patched and if it can be patched
        :return None
        """
        self.already_patched = False
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
            else:
                self.ev.event_warning("Not matching")
                self.ev.add_banner("Check with functions footprint")
                for func_name in self.check_file_result.funcs_offset.keys():
                    self.ev.event(f"Checking {func_name}... ")
                    self.check_file_result.funcs_offset[func_name] = get_offset_from_footprint(
                        self._file_path,
                        FUNCS_FOOTPRINTS[func_name]
                    )
                    if self.check_file_result.funcs_offset[func_name] is None or \
                            self.check_file_result.funcs_offset[func_name] == -1:
                        # Check if the function is already patched
                        already_patched = get_offset_from_footprint(
                            self._file_path,
                            PATCHED_FUNCS_FOOTPRINTS[func_name]
                        )
                        if already_patched == -1:
                            self.ev.event_error("Not found")
                        else:
                            self.ev.event_done("Patched")
                            self.already_patched = True
                    else:
                        self.ev.event_warning("Found")

                if self.check_file_result.haveFuncsOffset():
                    self.ev.event_done("All functions are found")
                    self.checkup_is_valid = True
                elif self.already_patched:
                    self.ev.event_done("All functions are patched")
                else:
                    self.checkup_is_valid = False
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

    def get_remaining_trial_days_key_head(self) -> str:
        """
        Get the head of the remaining trial days key
        :return: Head of the remaining trial days key
        """
        result: str = "00000000-0000"

        firmware_table_size: int = GetSystemFirmwareTable(RSMB, 0, None, 0)

        if firmware_table_size != 0:
            firmware_table_buffer: int = GlobalAlloc(0x40, wintypes.SIZE(firmware_table_size + 8))
            firmware_table_ptr: ctypes.c_void_p = ctypes.c_void_p(firmware_table_buffer)

            GetSystemFirmwareTable(RSMB, 0, firmware_table_ptr, firmware_table_size)

            index = 0
            while index + 1 < firmware_table_size:
                current_index: int = index
                buffer_ptr: ctypes.POINTER(CHAR) = ctypes.cast(
                    firmware_table_ptr.value + 8 + current_index, ctypes.POINTER(CHAR))
                entry: bytes = buffer_ptr.contents.value

                if entry == b'\x01':
                    if current_index != 0:
                        entry_ptr: ctypes.POINTER(ctypes.c_ulonglong) = ctypes.cast(
                            firmware_table_ptr.value + current_index + 8 + 8, ctypes.POINTER(ctypes.c_ulonglong))
                        entry_value: int = entry_ptr.contents.value

                        first_part: int = entry_value & 0xFFFFFFFF
                        second_part: int = (entry_value >> 0x30) & 0xFFFF

                        result = "%08x-%04x" % (first_part, second_part)

                    break

                b_value: CHAR = buffer_ptr[1]

                if b_value == 0:
                    break

                updated_index: int = current_index + int.from_bytes(b_value, byteorder=sys.byteorder)

                while True:
                    current_index = len(ctypes.string_at(firmware_table_ptr.value + 8 + updated_index))
                    if current_index == 0:
                        break
                    updated_index = updated_index + current_index + 1
                index = updated_index + 1
        return result

    def reset_trail_reminder(self) -> None:
        """
        Reset the registry
        :return: None
        """
        key_head = self.get_remaining_trial_days_key_head()
        regex = r"\{" + key_head + r"\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{11}\}"

        self.ev.add_banner("-")
        self.ev.event_info("            StartAllPatch v0.8.3")
        self.ev.event_info("  This Patch is compatible with SAB 3.x.x.")
        self.ev.add_banner("-")
        self.ev.event("\n")
        self.ev.add_banner("Reset trial reminder")
        self.ev.event("Deleting registry keys... ")
        try:
            sub_keys = reg.get_sub_keys_in_key(reg.get_key(HKEY_TRIAL_REMINDER))
            keys_uid = [search(regex, sub_key)[0] for sub_key in sub_keys if
                        search(regex, sub_key) is not None]
            if len(keys_uid) > 0:
                for uid in keys_uid:
                    reg.delete_key(HKEY_TRIAL_REMINDER + uid)
                self.ev.event_done("Done")
                return
        except FileNotFoundError:
            pass
        except Exception as e:
            self.ev.event_error("Error")
            self.ev.event_error(str(e))
            return
        self.ev.event_warning("Not found")

    @staticmethod
    def get_patches(fileInfo: FileInfo) -> list[Patch]:
        """
        Get the patches for a specific version
        :param fileInfo:
        :return: List of Patch objects
        """
        if not fileInfo.haveFuncsOffset:
            for infos in PATCHES_REPOSITORY:
                if infos['version'] == fileInfo.version:
                    for patch in infos['patches']:
                        yield Patch(offset=patch['offset'], bytes=patch['bytes'])
        else:
            for key, value in fileInfo.funcs_offset.items():
                offset = value
                patch = PATCHED_FUNCS_FOOTPRINTS[key]
                if offset == -1 or patch is None:
                    raise Exception("Invalid offset or patch is None\n" +
                                    "offset: " + str(offset) + "\n" +
                                    "patch: " + str(patch) + "\n")
                yield Patch(offset=offset, bytes=patch)
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
        self.ev.event_loading(f"Loading, Please Wait... ")
        if self.checkup_is_valid:
            if self._do_backup_func():
                self._create_backup()
            _original_file = self._read_file(self._file_path)
            _patched_file = _original_file
            self._kill_process("explorer.exe", "StartAllBackCfg.exe")
            self.ev.event("Patching... ")
            try:
                for patch in self.get_patches(self.check_file_result):
                    _patched_file = _patched_file[:patch.offset] + patch.bytes + \
                                    _patched_file[patch.offset + len(patch.bytes):]
            except Exception as e:
                self.ev.event(f"Error: {e}", color="red")
                self.restore()
                return

            if self._write_file(self._file_path, _patched_file):
                if not self.check_file_result.haveFuncsOffset():
                    self._check_hash()
            else:
                self.ev.event_error("Failed")
            self._start_explorer()
        else:
            self.ev.event_error("Checkup not valid (The program is already patched)")

    def _check_hash(self):
        self.ev.event("Checking hash... ")
        if self._get_hash(self._file_path) == self.check_file_result.patched_hash:
            self.ev.event_done("Patched")
        else:
            self.ev.event_error("Not matching")
            self.restore()

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
                break

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