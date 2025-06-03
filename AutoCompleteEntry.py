# -*- coding: gbk -*-

import tkinter as tk
from tkinter import simpledialog, Listbox, END

class AutoCompleteEntry(tk.Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.history = []  # 存储历史输入
        self.suggestions = []

        self.var = tk.StringVar()
        self.config(textvariable=self.var)

        self.var.trace_add("write", self.on_input)

        self.popup = None
        self.bind("<Escape>", lambda e: self.hide_suggestions())
        self.bind("<Down>", self.focus_first_suggestion)

    def set_history(self, history):
        self.history = history

    def handle_enter_key(self, event):
        # 按下 Enter 键时，隐藏补全菜单
        print("Enter key pressed!")  # 调试信息
        self.hide_suggestions()

    def on_input(self, *args):
        input_text = self.var.get().lower()
        self.suggestions = [item for item in self.history if input_text in item.lower()]

        if self.suggestions:
            self.show_suggestions()
        else:
            self.hide_suggestions()

    def focus_first_suggestion(self, event):
        if self.popup and self.popup.winfo_exists():
            listbox = self.popup.winfo_children()[0]  # 假设只有一个 Listbox
            listbox.selection_set(0)  # 选中第一项
            listbox.focus_set()  # 将焦点移到 Listbox 上

    def show_suggestions(self):
        if self.popup is not None:
            self.popup.destroy()

        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()

        self.popup = tk.Toplevel(self)
        self.popup.overrideredirect(True)
        self.popup.geometry(f"+{x}+{y}")

        # 绑定 ESC 键
        self.popup.bind("<Escape>", lambda e: self.hide_suggestions())

        listbox = Listbox(
            self.popup,
            width=30,
            height=10,
            bg="#ffffff",
            fg="black",
            font=("Arial", 10),
            relief="solid",
            bd=1
        )
        listbox.pack()

        for suggestion in self.suggestions:
            listbox.insert(END, suggestion)

        listbox.bind("<Double-Button-1>", self.select_suggestion)
        listbox.bind("<Return>", self.select_suggestion)

    def select_suggestion(self, event):
        listbox = event.widget
        selected = listbox.get(listbox.curselection())
        self.var.set(selected)
        self.history.append(selected)
        self.hide_suggestions()

    def hide_suggestions(self):
        if self.popup is not None:
            self.popup.destroy()
            self.popup = None


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("带历史提示的文件匹配工具")
        self.geometry("400x300")

        self.entry = AutoCompleteEntry(self, font=("Arial", 12))
        self.entry.pack(pady=20)

        self.submit_btn = tk.Button(self, text="提交", command=self.submit)
        self.submit_btn.pack(pady=10)

    def submit(self):
        user_input = self.entry.get()
        self.entry.history.append(user_input)
        print("用户输入:", user_input)


if __name__ == "__main__":
    app = App()
    app.mainloop()
