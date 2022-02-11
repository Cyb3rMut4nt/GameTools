from __future__ import print_function
import time
import win32api, win32con
import re
import os
import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
if is_admin():
    reg_root = win32con.HKEY_LOCAL_MACHINE
    reg_path = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Steam"
    reg_flags = win32con.WRITE_OWNER | win32con.KEY_WOW64_64KEY | win32con.KEY_ALL_ACCESS
    # 遍历枚举子键
    key = win32api.RegOpenKeyEx(reg_root, reg_path, 0, reg_flags)
    i = 0
    while 1:
        try:
            item = win32api.RegEnumValue(key,i)
            print(item)
            i+=1
            if re.findall(r'uninstall', item[1]):
                tmp = item[1]
                dir = tmp[0:tmp.rfind('\\')]
                print('success')
                print(dir)
                break
        except Exception as e:
            print('can not find steam')
            break
    # 关闭键
    win32api.RegCloseKey(key)
else:
    if sys.version_info[0] == 3:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:#in python2.x
        ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)

with open('steam.txt','r',encoding='utf-8') as f:
    while 1:
        time.sleep(1)
        game = f.readline()
        if game:
            if re.findall('^steam:\/\/.*? ',game):
                cmd = re.findall('^steam:\/\/.*? ',game)
                cmd = dir + '\steam ' + str(cmd).replace("['",'').replace("']",'')
            elif re.findall('^steam:\/\/.*[0-9]',game):
                cmd = re.findall('^steam:\/\/.*[0-9]',game)
                cmd = dir + '\steam ' + str(cmd).replace("['",'').replace("']",'')
            else:
                print('not success for: ' + game)
            print(cmd)
            os.system(cmd)
        else:
            break