import subprocess
from ctypes import WinDLL, wintypes
import ctypes
import time
import sys
import os

user32 = WinDLL("user32.dll")


def get_all_wiz_handles():
    target_class = "Wizard Graphical Client"

    handles = []

    def callback(handle, _):
        class_name = ctypes.create_unicode_buffer(len(target_class))
        user32.GetClassNameW(handle, class_name, len(target_class) + 1)
        if target_class == class_name.value:
            handles.append(handle)

        # iterate all windows
        return True

    enumwindows_func_type = ctypes.WINFUNCTYPE(
        ctypes.c_bool,  # return type
        ctypes.c_int,  # arg1 type
        ctypes.POINTER(ctypes.c_int),  # arg2 type
    )
    callback = enumwindows_func_type(callback)
    user32.EnumWindows(callback, 0)

    return handles


def open_wiz():
    command = 'cd "C:\ProgramData\KingsIsle Entertainment\Wizard101\Bin" && start WizardGraphicalClient.exe -L login.us.wizard101.com 12000'
    return subprocess.Popen(command, shell=True)


def wiz_login(window_handle: int, username: str, password: str):
    def send_chars(chars: str):
        for char in chars:
            user32.PostMessageW(window_handle, 0x102, ord(char), 0)

    send_chars(username)
    # tab
    user32.PostMessageW(window_handle, 0x102, 9, 0)
    send_chars(password)
    # enter
    user32.PostMessageW(window_handle, 0x102, 13, 0)

    # Set title
    user32.SetWindowTextW(window_handle, f"[{username[0]}] Wizard101")


if len(sys.argv) > 1:
    accounts_array = [line.strip().split(":") for line in sys.argv[1:]]
else:
    try:
        with open("accounts.txt") as my_file:
            accounts_array = [
                line.strip().split(":") for line in my_file.read().split("\n")
            ]
    except FileNotFoundError:
        print("Incorrect formatting")
        os.pause()
        exit(1)


target = len(accounts_array)
initial_handles = set(get_all_wiz_handles())
initial_handles_l = len(initial_handles)

for i in range(target):
    open_wiz()

# Wait a little
time.sleep(2)

handles = get_all_wiz_handles()
while len(handles) != target + initial_handles_l:
    handles = get_all_wiz_handles()
    time.sleep(0.5)

new_handles = set(handles).difference(initial_handles)
for i, handle in enumerate(new_handles):
    wiz_login(handle, accounts_array[i][0], accounts_array[i][1])

