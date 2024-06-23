# version 0.1.1
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import hashlib

# Initialize CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class ChecksumVerificationApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("File Encryption Verification Tool")
        self.geometry("600x400")

        # File Loader
        self.file_frame = ctk.CTkFrame(self)
        self.file_frame.pack(pady=20, padx=20, fill="x")

        self.file_label = ctk.CTkLabel(self.file_frame, text="No file loaded", anchor="w")
        self.file_label.pack(side="left", padx=10, fill="x", expand=True)

        self.load_button = ctk.CTkButton(self.file_frame, text="Load File", command=self.load_file)
        self.load_button.pack(side="right", padx=10)

        # Checksum Verification Comparator
        self.checksum_frame = ctk.CTkFrame(self)
        self.checksum_frame.pack(pady=20, padx=20, fill="x")

        self.checksum_label = ctk.CTkLabel(self.checksum_frame, text="Expected Checksum:", anchor="w")
        self.checksum_label.pack(side="left", padx=10, fill="x", expand=True)

        self.checksum_entry = ctk.CTkEntry(self.checksum_frame, width=200)
        self.checksum_entry.pack(side="right", padx=10)

        # Algorithm Selection
        self.algorithm_frame = ctk.CTkFrame(self)
        self.algorithm_frame.pack(pady=20, padx=20, fill="x")

        self.algorithm_label = ctk.CTkLabel(self.algorithm_frame, text="Select Algorithm:", anchor="w")
        self.algorithm_label.pack(side="left", padx=10, fill="x", expand=True)

        self.algorithm_var = tk.StringVar(value="SHA256")
        self.algorithm_menu = ctk.CTkOptionMenu(self.algorithm_frame, variable=self.algorithm_var, values=["SHA256", "MD5", "SHA1", "BLAKE2"])
        self.algorithm_menu.pack(side="right", padx=10)

        # Verification Indicator
        self.verify_button = ctk.CTkButton(self, text="Verify Checksum", command=self.verify_checksum)
        self.verify_button.pack(pady=20)

        self.result_label = ctk.CTkLabel(self, text="", font=("Helvetica", 18))
        self.result_label.pack(pady=10)

        # Signatures in Comparison
        self.result_label1 = ctk.CTkLabel(self, text="", font=("Helvetica", 10))
        self.result_label1.pack(pady=10)
        self.result_label2 = ctk.CTkLabel(self, text="", font=("Helvetica", 10))
        self.result_label2.pack(pady=10)
    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_label.configure(text=file_path)
            self.file_path = file_path

    def verify_checksum(self):
        if not hasattr(self, 'file_path'):
            messagebox.showerror("Error", "No file loaded")
            return

        expected_checksum = self.checksum_entry.get()
        if not expected_checksum:
            messagebox.showerror("Error", "Expected checksum not provided")
            return

        algorithm = self.algorithm_var.get()
        calculated_checksum = self.calculate_checksum(self.file_path, algorithm)
        self.update_result(calculated_checksum, expected_checksum)

    def calculate_checksum(self, file_path, algorithm):
        hash_func = getattr(hashlib, algorithm.lower())()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    def update_result(self, calculated_checksum, expected_checksum):
        if calculated_checksum == expected_checksum:
            self.result_label.configure(text="Checksum Matched!", text_color="green")
            self.result_label1.configure(text={calculated_checksum}, text_color="white")
            self.result_label2.configure(text={calculated_checksum}, text_color="white")
        else:
            self.result_label.configure(text="Checksum Mismatched!", text_color="red")

if __name__ == "__main__":
    app = ChecksumVerificationApp()
    app.mainloop()
