# -*- coding: utf-8 -*-
# @Time    : 2021/7/9 10:43
# @Author  : misakikata
# @File    : setpath.py
# Software : PyCharm


import winreg
import ctypes


class Registry(object):
    def __init__(self, key_location, key_path):
        self.reg_key = winreg.OpenKey(key_location, key_path, 0, winreg.KEY_ALL_ACCESS)
    def set_key(self, name, value):
        try:
            _, reg_type = winreg.QueryValueEx(self.reg_key, name)
        except WindowsError:
            reg_type = winreg.REG_SZ
        winreg.SetValueEx(self.reg_key, name, 0, reg_type, value)


class EnvironmentVariables(Registry):

    def __init__(self,JAVA_ENV):
        super(EnvironmentVariables, self).__init__(winreg.HKEY_LOCAL_MACHINE,
                                                   r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment')
        self.JAVA_ENV = JAVA_ENV

    def on(self):
        self.set_key('JAVA_HOME', self.JAVA_ENV.replace('/','\\'))
        self.refresh()

    def refresh(self):
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x1A

        SMTO_ABORTIFHUNG = 0x0002

        result = ctypes.c_long()
        SendMessageTimeoutW = ctypes.windll.user32.SendMessageTimeoutW
        SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, u'Environment', SMTO_ABORTIFHUNG, 5000, ctypes.byref(result))


class Environmentiter(Registry):

    def __init__(self):
        super(Environmentiter, self).__init__(winreg.HKEY_LOCAL_MACHINE,
                                                   r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment')

    def iterenv(self):
        countkey = winreg.QueryInfoKey(self.reg_key)[1]
        for i in range(int(countkey)):
            name, value, type = winreg.EnumValue(self.reg_key, i)
            if "JAVA_HOME" in name:
                return value

        winreg.CloseKey(self.reg_key)

