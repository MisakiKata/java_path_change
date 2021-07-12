# -*- coding: utf-8 -*-
# @Time    : 2021/7/9 10:40
# @Author  : misakikata
# @File    : main.py
# Software : PyCharm


from __future__ import print_function
import ctypes
from tkinter import *
from tkinter.ttk import *
import subprocess
from tkinter import filedialog, messagebox
import os
import yaml
from lib import setpath


class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name
        self.top = None

    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("Java环境切换")           #窗口名
        self.init_window_name.geometry('400x230+400+300')

        #标签
        self.init_data_label = Label(self.init_window_name, text="已有环境")
        self.init_data_label.grid(row=0, column=1)

        #文本框
        self.init_data_Text = Listbox(self.init_window_name, width=56, height=8)  #处理结果展示
        for i in self.read_conf():
            self.init_data_Text.insert(1, i)
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)

        self.start_env = Label(self.init_window_name, text="已设置环境："+self.java_envs())
        self.start_env.grid(row=80, column=1, rowspan=1, columnspan=1)

        #按钮
        self.str_trans_to_conf_button = Button(self.init_window_name, text="添加环境", width=10, command=lambda: self.set_path())
        self.str_trans_to_delete_button = Button(self.init_window_name, text="删除环境", width=10, command=lambda: self.del_path(self.init_data_Text.get(ANCHOR)))
        self.str_trans_to_start_button = Button(self.init_window_name, text="启用环境", width=10, command=lambda: self.start_path(self.init_data_Text.get(ANCHOR)))

        self.str_trans_to_conf_button.place(x=50, y=200)
        self.str_trans_to_delete_button.place(x=150, y=200)
        self.str_trans_to_start_button.place(x=250, y=200)

    def read_conf(self):
        config = yaml.safe_load(open("./conf/conf.yml", 'r', encoding="utf-8").read())
        return config.keys()

    def write_conf(self, data_key, data_val, key=None):
        json_data = {data_key: data_val}
        with open('./conf/conf.yml', 'a', encoding="utf-8") as f:
            yaml.safe_dump(json_data, f)

        if key == 'set':
            self.init_data_Text.insert(1, data_key)

        if self.top:
            self.top.destroy()

    def set_path(self):
        file = filedialog.askdirectory(initialdir=os.path.dirname(__file__))
        confirm = messagebox.askyesno("添加成功","是否需要添加备注？", default=messagebox.YES)
        if confirm:
            self.top = Tk()
            self.top.title('修改备注')
            self.top.geometry("300x50+450+300")

            lbl = Label(self.top, text="备注: ")
            lbl.grid(column=0, row=0)
            set_text_val = Entry(self.top, width=20)
            set_text_val.grid(column=1, row=0)
            btn = Button(self.top, text="确认", width=10, command=lambda: self.write_conf(set_text_val.get(), file, 'set'))
            btn.grid(column=2, row=0)

        else:
            self.write_conf(file, file)
            self.init_data_Text.insert(1, file)


    def del_path(self, data_text):
        config = yaml.safe_load(open("./conf/conf.yml", 'r', encoding="utf-8").read())
        del config[data_text]
        with open('./conf/conf.yml', 'w', encoding="utf-8") as f:
            yaml.safe_dump(config, f)
        self.init_data_Text.delete(ANCHOR)
        messagebox.showinfo("删除成功",data_text)


    def start_path(self, data_text):
        config = yaml.safe_load(open("./conf/conf.yml", 'r', encoding="utf-8").read())
        path = config[data_text]
        envs = setpath.EnvironmentVariables(path)
        envs.on()
        messagebox.showinfo("设置环境",data_text)
        print(self.java_envs())
        self.start_env['text'] = "已设置环境：" + self.java_envs()


    def java_envs(self):
        envs = setpath.Environmentiter()
        env_path = envs.iterenv()
        javapath = str(env_path) + "\\bin\\java.exe"
        if os.path.exists(javapath):
            p = subprocess.Popen([javapath, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if p.poll() == None:
                return bytes.decode(p.communicate()[1]).split('\r\n')[0]
            else:
                return "配置失败，请检查报错"
        else:
            return "配置失败，请检查目录"


def main():
    init_window = Tk()
    ZMJ_PORTAL = MY_GUI(init_window)
    ZMJ_PORTAL.set_init_window()
    init_window.mainloop()


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == '__main__':
    if is_admin():
        main()
    else:
        if sys.version_info[0] == 3:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    # main()