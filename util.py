import tkinter as tk
import threading
import subprocess


def update_readonly_textbox(textbox: tk.Text, content: str) -> None:
    textbox.configure(state=tk.NORMAL)
    textbox.delete('1.0', 'end')
    textbox.insert('end', content)
    textbox.configure(state=tk.DISABLED)


def string_is_float(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False

# Define a custom Thread class that can return a result
class ThreadWithResult(threading.Thread):
    def __init__(self, target, args=()):
        super(ThreadWithResult, self).__init__()
        self.target = target
        self.args = args
        self.result = None

    def run(self):
        self.result = self.target(*self.args)


def check_docker_exists() -> bool:
    try:
        subprocess.run(["docker", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False


check_docker_exists()
