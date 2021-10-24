import inspect
import os
import sys
from typing import TypedDict


# Copied from stackOverflow
def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False):  # py2exe, PyInstaller, cx_Freeze
        pth = os.path.abspath(sys.executable)
    else:
        pth = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        pth = os.path.realpath(pth)
    return os.path.dirname(pth)


class ProgramInfo:
    name: str = 'ThermoState'
    version: str = '2.0'
    build: int = 2


class FolderFileName:
    data_folder: str = "Data"
    history: str = f"historyV{ProgramInfo.build}"
    flows: str = f"flowsV{ProgramInfo.build}"
    settings: str = f"settingsV{ProgramInfo.build}"
    unit: str = f"unit_configV{ProgramInfo.build}"
    log: str = "error.log"


class Path:
    script_dir: str = get_script_dir()
    data_dir: str = os.path.join(script_dir, FolderFileName.data_folder)
    history: str = os.path.join(data_dir, FolderFileName.history)
    flows: str = os.path.join(data_dir, FolderFileName.flows)
    settings: str = os.path.join(data_dir, FolderFileName.settings)
    unit: str = os.path.join(data_dir, FolderFileName.unit)
    log: str = os.path.join(data_dir, FolderFileName.log)
    home: str = os.path.expanduser("~")


class ServerInfo:
    register_interval_days: int = 30
    website: str = 'https://thermo-state.github.io/'
    issue_url: str = 'https://github.com/Thermo-State/ThermoState/issues'
    github_url: str = 'http://127.0.0.1:5000/url'
