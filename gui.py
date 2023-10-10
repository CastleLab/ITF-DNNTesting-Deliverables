import tkinter as tk
from api import DNNTest
from pages.network_analysis import NetworkAnalysisPage
from pages.image_mutation import ImageMutationPage
from pages.image_detection import ImageDetectionPage
from pages.model_training import ModelTrainingPage
from pages.model_evaluation import ModelEvaluationPage
from pages.model_repairing import ModelRepairingPage


dnnTest = DNNTest("DNNTesting")


class AutoTestUnreliableInferenceGUI:
    def __init__(self, master):
        self.master = master
        master.title("AutoTestUnreliableInference")
        self.master.geometry("600x400")
        self.network_analysis_page = None
        self.image_mutation_page = None
        self.image_detection_page = None
        self.model_training_page = None
        self.model_evaluation_page = None
        self.model_repairing_page = None

        button_frame = tk.Frame(self.master)
        button_frame.pack()
        # Creating the buttons on the main page
        self.network_analysis_button = tk.Button(button_frame, text="Network Analysis",
                                                 command=self.show_network_analysis_page)
        self.network_analysis_button.pack()

        self.image_mutation_button = tk.Button(button_frame, text="Image Mutation",
                                               command=self.show_image_mutation_page)
        self.image_mutation_button.pack()

        self.image_detection_button = tk.Button(button_frame, text="Image Detection",
                                                command=self.show_image_detection_page)
        self.image_detection_button.pack()

        self.model_train_button = tk.Button(button_frame, text="Model Training", command=self.show_model_training_page)
        self.model_train_button.pack()

        self.model_evaluation_button = tk.Button(button_frame, text="Model Evaluation",
                                                 command=self.show_model_evaluation_page)
        self.model_evaluation_button.pack()

        self.model_repair_button = tk.Button(button_frame, text="Model Repairing",
                                             command=self.show_model_repairing_page)
        self.model_repair_button.pack()

        # Add more buttons here for your other pages...

    def show_network_analysis_page(self):
        self.network_analysis_page = NetworkAnalysisPage(self.master)
        self.network_analysis_page.tkraise()

    def show_image_mutation_page(self):
        self.image_mutation_page = ImageMutationPage(self.master)
        self.image_mutation_page.tkraise()

    def show_image_detection_page(self):
        self.image_detection_page = ImageDetectionPage(self.master)
        self.image_detection_page.tkraise()

    def show_model_training_page(self):
        self.model_training_page = ModelTrainingPage(self.master)
        self.model_training_page.tkraise()

    def show_model_evaluation_page(self):
        self.model_evaluation_page = ModelEvaluationPage(self.master)
        self.model_evaluation_page.tkraise()

    def show_model_repairing_page(self):
        self.model_repairing_page = ModelRepairingPage(self.master)
        self.model_repairing_page.tkraise()

def run_gui():
    root = tk.Tk()
    # AutoTestUnreliableInferenceGUI(root).show_model_training_page()
    AutoTestUnreliableInferenceGUI(root).show_model_evaluation_page()
    # AutoTestUnreliableInferenceGUI(root).show_image_mutation_page()
    root.mainloop()


if __name__ == "__main__":
    run_gui()
