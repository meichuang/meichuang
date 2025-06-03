# -*- coding: gbk -*-

import os
import fnmatch
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import json
from AutoCompleteEntry  import AutoCompleteEntry

CONFIG_FILE = 'fileconfig.json'

def load_config():
    """
    从配置文件中加载上次选择的目录
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get('last_directory', ''), config.get('history', [])

    return '', []

def save_config(directory, history):
    """
    将当前选择的目录保存到配置文件
    """
    pattern_entry.set_history(history)

    config = {'last_directory': directory, 'history': history}
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)
def find_files(directory, pattern):
    """
    在指定目录及其子目录中查找匹配模式的文件。

    :param directory: 要搜索的目录路径
    :param pattern: 文件名匹配模式（支持通配符）
    :return: 匹配的文件列表
    """
    matches = []


    for root, dirs, files in os.walk(directory):
        for basename in files:
            if match_all_pattern(basename, pattern):
                filename = os.path.join(root, basename)
                matches.append(filename)
    return matches

def match_all_pattern(basename, pattern):
    pattern_list = pattern.split()
    for pt in pattern_list:
        if not pt.lower() in basename.lower():
            return False

    return True
def browse_directory():
    """
    打开文件对话框选择目录
    """
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)
        save_config(directory, history)  # 保存当前选择的目录

def search_files(event=None):
    """
    搜索文件并更新结果列表
    """
    global history  # 声明 history 为全局变量
    directory = directory_entry.get()
    pattern = pattern_entry.get().upper()
    pattern_entry.hide_suggestions()
    pattern_new = pattern.replace(" ",'_')
    pattern_new = "*" + pattern_new + ".txt"
    print(pattern_new)

    if not directory or not pattern:
        messagebox.showwarning("输入错误", "请填写目录和匹配模式")
        return

    matches = find_files(directory, pattern + " .txt")
    result_list.delete(0, tk.END)
    for match in matches:
        relative_path = os.path.relpath(match, directory)
        result_list.insert(tk.END, relative_path)

    # 添加到历史记录
    if pattern not in history:
        history.append(pattern)

    # 去重并排序
    history = sorted(set(history), key=history.index)

    history_list.delete(0, tk.END)
    for item in history:
        history_list.insert(tk.END, item)

    save_config(directory, history)  # 保存历史记录
def open_file(event):
    """
    双击结果列表中的文件以打开文件
    """
    selection = result_list.curselection()
    if selection:
        relative_path = result_list.get(selection[0])
        directory = directory_entry.get()
        file_path = os.path.join(directory, relative_path)

        try:
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # macOS and Linux
                subprocess.run(['open', file_path])
            else:
                messagebox.showerror("错误", "不支持的操作系统")
        except Exception as e:
            messagebox.showerror("错误", f"无法打开文件: {e}")

def re_search(event):
    """
    双击历史记录中的文件名重新进行查找
    """
    selection = history_list.curselection()
    if selection:
        pattern = history_list.get(selection[0])
        pattern_entry.delete(0, tk.END)
        pattern_entry.insert(0, pattern)
        search_files()

# 绑定 Delete 键事件
def delete_history(event):
    last_directory,_  = load_config()
    selected_index = history_list.curselection()
    if selected_index:
        history_list.delete(selected_index)
        del history[selected_index[0]]
        save_config(last_directory, history)  # 保存历史记录
def initWindow():
    global history, directory_entry, pattern_entry, history_list, result_list
    # 加载上次选择的目录
    last_directory, history = load_config()
    # 设置目录
    directory_label = tk.Label(root, text="目录:")
    directory_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    directory_entry = tk.Entry(root, width=70)
    directory_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    directory_entry.insert(0, last_directory)  # 插入上次选择的目录
    browse_button = tk.Button(root, text="浏览", command=browse_directory)
    browse_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

    # 设置匹配模式
    pattern_label = tk.Label(root, text="匹配模式:")
    pattern_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    #pattern_entry = tk.Entry(root, width=70)
    pattern_entry = AutoCompleteEntry(root, width=70)
    pattern_entry.set_history(history)

    pattern_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
    search_button = tk.Button(root, text="搜索", command=search_files)
    search_button.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
    # 绑定回车键事件
    pattern_entry.bind("<Return>", search_files)
    # 历史记录列表
    history_label = tk.Label(root, text="历史记录:")
    history_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    history_list = tk.Listbox(root, height=40, width=25)
    history_list.grid(row=3, column=0, padx=5, pady=5, sticky=tk.N + tk.S)
    # 绑定双击事件
    history_list.bind("<Double-1>", re_search)
    # 绑定 Delete 键事件
    history_list.bind("<Delete>", delete_history)

    # 初始化历史记录列表
    for item in history:
        history_list.insert(tk.END, item)
    # 结果列表
    result_label = tk.Label(root, text="搜索结果:")
    result_label.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
    result_list = tk.Listbox(root, height=25, width=100)
    result_list.grid(row=3, column=1, columnspan=2,padx=5, pady=5, sticky=tk.N + tk.S)
    # 绑定双击事件
    result_list.bind("<Double-1>", open_file)

# 创建主窗口
root = tk.Tk()
root.title("文件查找工具")
root.geometry()  # 设置窗口大小

initWindow()

# 运行主循环
root.mainloop()
