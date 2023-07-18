import tkinter
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import os
from api import DNNTest
import threading

dnnTest = DNNTest("DNNTesting")
import threading

# Define a custom Thread class that can return a result
class ThreadWithResult(threading.Thread):
    def __init__(self, target, args=()):
        super(ThreadWithResult, self).__init__()
        self.target = target
        self.args = args
        self.result = None

    def run(self):
        self.result = self.target(*self.args)


class AutoTestUnreliableInferenceGUI:
    def __init__(self, master):
        self.master = master
        master.title("AutoTestUnreliableInference")

        # Creating the buttons on the main page
        self.network_analysis_button = tk.Button(master, text="Network Analysis", command=self.network_analysis_page)
        self.network_analysis_button.pack()

        self.image_mutation_button = tk.Button(master, text="Image Mutation", command=self.image_mutation_page)
        self.image_mutation_button.pack()

        self.model_train_button = tk.Button(master, text="Model Training", command=self.model_train_page)
        self.model_train_button.pack()

        self.model_evaluation_button = tk.Button(master, text="Model Evaluation", command=self.model_evaluation_page)
        self.model_evaluation_button.pack()

        self.model_repair_button = tk.Button(master, text="Model Repairing", command=self.model_repair_page)
        self.model_repair_button.pack()

        # Add more buttons here for your other pages...

    def network_analysis_page(self):
        # Creating a new Tkinter window
        self.new_window = tk.Toplevel(self.master)
        self.new_window.title("Detecting Numerical Bugs in Neural Networks")

        # Creating the "Creating a Network" section
        create_network_frame = tk.Frame(self.new_window)
        create_network_frame.pack(side="left")

        create_network_label = tk.Label(create_network_frame, text="Creating a Network")
        create_network_label.pack()

        self.network_code_entry = tk.Text(create_network_frame, height=20, width=50)
        self.network_code_entry.insert("1.0", "Write your TensorFlow program to create a customized neural network")
        self.network_code_entry.pack()

        save_network_button = tk.Button(create_network_frame, text="Save Network", command=self.save_network)
        save_network_button.pack()

        # Creating the "Network Analyzer" section
        network_analyzer_frame = tk.Frame(self.new_window)
        network_analyzer_frame.pack(side="left")

        network_analyzer_label = tk.Label(network_analyzer_frame, text="Network Analyzer")
        network_analyzer_label.pack(side="top")

        self.model_var = tk.StringVar()
        network_list = self._load_network()
        self.model_var.set(network_list[0])  # default value

        model_menu = tk.OptionMenu(network_analyzer_frame, self.model_var, *network_list)
        model_menu.pack()

        start_analysis_button = tk.Button(network_analyzer_frame, text="Start Analysis", command=self.start_analysis)
        start_analysis_button.pack()

        # tedtbox_status: readonly
        self.analysis_output_textbox = scrolledtext.ScrolledText(network_analyzer_frame, height=20, width=50, state=tk.DISABLED)
        self.analysis_output_textbox.pack()

        # Creating the "Network Display" section
        network_display_frame = tk.Frame(self.new_window)
        network_display_frame.pack(side="right")

        network_display_label = tk.Label(network_display_frame, text="Network Display")
        network_display_label.pack()
        # tedtbox_status: readonly
        self.network_display_textbox = scrolledtext.ScrolledText(network_display_frame, height=20, width=50, state=tk.DISABLED)
        self.network_display_textbox.pack()

    @staticmethod
    def _save_network(dest_dir="./DEBAR/computation_graphs_and_TP_list/computation_graphs"):
        print(f"Successfully save the model to pbtxt format to directory: {dest_dir}")

    @staticmethod
    def _load_network(dest_dir="./DEBAR/computation_graphs_and_TP_list/computation_graphs"):
        network_list = []
        for filename in os.listdir(dest_dir):
            if filename.endswith(".pbtxt"):
                network_list.append(os.path.splitext(filename)[0])
        return network_list

    def save_network(self):
        # Add your 'foo' function here
        code = self.network_code_entry.get("1.0", "end-1c")
        try:
            self._save_network(code)
            message = "Network has been successfully saved"
            messagebox.showinfo("Successful", message)
        except Exception as e:
            message = "Network cannot be correctly saved, please check if your code is correct"
            messagebox.showerror("Error", message)

    @staticmethod
    def _update_readonly_textbox(textbox: tkinter.Text, content: str) -> None:
        textbox.configure(state=tk.NORMAL)
        textbox.delete('1.0', 'end')
        textbox.insert('end', content)
        textbox.configure(state=tk.DISABLED)

    def start_analysis(self, dest_dir="./DEBAR/computation_graphs_and_TP_list/computation_graphs"):
        # Add your 'hoo' function here
        model = self.model_var.get()
        model_name = f"{model}.pbtxt"

        def thread_func(name: str) -> str:
            try:
                res = dnnTest.numerical_analysis(name)
                self._update_readonly_textbox(self.analysis_output_textbox, "Analysis complete for network: " + model + "\n" + res.decode('utf-8'))
            except Exception as e:
                res = "Error", str(e)
            return res

        # Create a ThreadWithResult object to call the function
        t = ThreadWithResult(target=thread_func, args=(model_name, ))
        t.start()
        with open(os.path.join(dest_dir, model_name), "r") as file:
            content = file.read()
        self._update_readonly_textbox(self.network_display_textbox, f"The architecture of model is:\n {content}")
        self._update_readonly_textbox(self.analysis_output_textbox, f"Analyzing network: {model} ...")


    def image_mutation_page(self):
        # Creating a new Tkinter window
        self.new_window = tk.Toplevel(self.master)
        self.new_window.title("Detecting Numerical Bugs in Neural Networks")

        # Creating the "Creating a Network" section
        create_network_frame = tk.Frame(self.new_window)
        create_network_frame.pack(side="left")

    def model_train_page(self):
        # Creating a new Tkinter window
        self.new_window = tk.Toplevel(self.master)
        self.new_window.title("Detecting Numerical Bugs in Neural Networks")

        # Creating the "Creating a Network" section
        create_network_frame = tk.Frame(self.new_window)
        create_network_frame.pack(side="left")

    def model_evaluation_page(self):
        # Creating a new Tkinter window
        self.new_window = tk.Toplevel(self.master)
        self.new_window.title("Detecting Numerical Bugs in Neural Networks")

        # Creating the "Creating a Network" section
        create_network_frame = tk.Frame(self.new_window)
        create_network_frame.pack(side="left")

    def model_repair_page(self):
        # Creating a new Tkinter window
        self.new_window = tk.Toplevel(self.master)
        self.new_window.title("Detecting Numerical Bugs in Neural Networks")

        # Creating the "Creating a Network" section
        create_network_frame = tk.Frame(self.new_window)
        create_network_frame.pack(side="left")

def run_gui():
    root = tk.Tk()
    gui = AutoTestUnreliableInferenceGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()

