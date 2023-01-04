import ctypes

import pefile
import psutil
import win32file
import win32security
from psutil import AccessDenied


def get_sid_and_username(process):
    params = {}
    try:
        params['username'] = process.username()
        user_info = win32security.LookupAccountName(None, params['username'])
        params['sid'] = win32security.ConvertSidToStringSid(user_info[0])
    except AccessDenied:
        params['username'] = "Н\д"
        params['sid'] = "Н\д"
    return params


def get_dll(process):
    dll_list = []
    try:
        for dll in process.memory_maps():
            dll_list.append(dll.path)
        return dll_list
    except AccessDenied:
        return ''


def get_main_info(process):
    params = {
        'pid': process.pid,
        'name': process.name(),
        'status': process.status(),
        'parents': get_parents(process),
        'exe': get_exe(process),
        'dll': get_dll(process),
        'owner': get_sid_and_username(process),
        'bin': get_bin(get_exe(process)),
        'aslr': get_aslr(get_exe(process)),
        'dep': get_dep(process.pid),
    }
    return params


def get_parents(process):
    parents = [(proc.pid, proc.name()) for proc in process.parents()]
    s = ''
    for (pid, name) in parents:
        s += f"{pid}--{name}, "
    return s


def get_exe(process):
    try:
        return process.exe()
    except AccessDenied:
        return "Н\д"


def get_all_process():
    return psutil.process_iter()


def get_aslr(path):
    try:
        pe = pefile.PE(path)
        return "IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE" in pe.dump_dict()['DllCharacteristics']
    except:
        return "Н\д"


def get_bin(exe):
    try:
        type = win32file.GetBinaryType(exe)
        if type == win32file.SCS_32BIT_BINARY:
            return 32
        return 64
    except:
        return "Н\д"


def get_dep(pid):
    if ctypes.CDLL("./lib.so").getDEP(pid) == 1:
        return 'True'
    else:
        return 'Н\д'

