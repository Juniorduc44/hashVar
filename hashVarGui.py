# Version 0.2.0
# File Checksum Verification Tool with GUI


import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import hashlib
import pyperclip  # For copying results to clipboard

# Initialize CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class ChecksumVerificationApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("File Checksum Verification Tool")
        self.geometry("700x500")
        self.resizable(False, False)  # Fixed size for consistent layout

        # File Loader Section
        self.file_frame = ctk.CTkFrame(self)
        self.file_frame.pack(pady=10, padx=20, fill="x")

        self.file_label = ctk.CTkLabel(self.file_frame, text="No file loaded", anchor="w", wraplength=500)
        self.file_label.pack(side="left", padx=10, fill="x", expand=True)

        self.load_button = ctk.CTkButton(self.file_frame, text="Load File", command=self.load_file)
        self.load_button.pack(side="right", padx=10)

        # Checksum Input Section
        self.checksum_frame = ctk.CTkFrame(self)
        self.checksum_frame.pack(pady=10, padx=20, fill="x")

        self.checksum_label = ctk.CTkLabel(self.checksum_frame, text="Expected Checksum:", anchor="w")
        self.checksum_label.pack(side="left", padx=10)

        self.checksum_entry = ctk.CTkEntry(self.checksum_frame, width=400, placeholder_text="Enter checksum here")
        self.checksum_entry.pack(side="right", padx=10)

        # Algorithm Selection Section
        self.algorithm_frame = ctk.CTkFrame(self)
        self.algorithm_frame.pack(pady=10, padx=20, fill="x")

        self.algorithm_label = ctk.CTkLabel(self.algorithm_frame, text="Select Algorithm:", anchor="w")
        self.algorithm_label.pack(side="left", padx=10)

        self.algorithm_var = tk.StringVar(value="SHA256")
        self.algorithm_menu = ctk.CTkOptionMenu(
            self.algorithm_frame, 
            variable=self.algorithm_var, 
            values=["SHA256", "SHA1", "MD5", "BLAKE2b", "BLAKE2s"]
        )
        self.algorithm_menu.pack(side="right", padx=10)

        # Verify Button
        self.verify_button = ctk.CTkButton(self, text="Verify Checksum", command=self.verify_checksum)
        self.verify_button.pack(pady=20)

        # Results Section
        self.result_frame = ctk.CTkFrame(self)
        self.result_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.result_status = ctk.CTkLabel(self.result_frame, text="", font=("Helvetica", 18, "bold"))
        self.result_status.pack(pady=10)

        # Calculated Checksum with Copy Button
        self.calculated_frame = ctk.CTkFrame(self.result_frame)
        self.calculated_frame.pack(pady=5, fill="x")
        self.calculated_label = ctk.CTkLabel(self.calculated_frame, text="Calculated Checksum: N/A", anchor="w", wraplength=500)
        self.calculated_label.pack(side="left", padx=10, fill="x", expand=True)
        self.copy_calculated_button = ctk.CTkButton(
            self.calculated_frame, text="Copy", command=self.copy_calculated, width=80, state="disabled"
        )
        self.copy_calculated_button.pack(side="right", padx=10)

        # Expected Checksum with Copy Button
        self.expected_frame = ctk.CTkFrame(self.result_frame)
        self.expected_frame.pack(pady=5, fill="x")
        self.expected_label = ctk.CTkLabel(self.expected_frame, text="Expected Checksum: N/A", anchor="w", wraplength=500)
        self.expected_label.pack(side="left", padx=10, fill="x", expand=True)
        self.copy_expected_button = ctk.CTkButton(
            self.expected_frame, text="Copy", command=self.copy_expected, width=80, state="disabled"
        )
        self.copy_expected_button.pack(side="right", padx=10)

    def load_file(self):
        """Load a file and update the file label."""
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path = file_path
            self.file_label.configure(text=file_path)

    def verify_checksum(self):
        """Verify the checksum and update the GUI with results."""
        if not hasattr(self, 'file_path'):
            messagebox.showerror("Error", "Please load a file first.")
            return

        expected_checksum = self.checksum_entry.get().strip()
        if not expected_checksum:
            messagebox.showerror("Error", "Please enter an expected checksum.")
            return

        algorithm = self.algorithm_var.get()
        try:
            calculated_checksum = self.calculate_checksum(self.file_path, algorithm)
            self.update_result(calculated_checksum, expected_checksum)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate checksum: {str(e)}")

    def calculate_checksum(self, file_path, algorithm):
        """
        Calculate the checksum of a file using the specified algorithm.
        
        Args:
            file_path (str): Path to the file
            algorithm (str): Hashing algorithm (e.g., SHA256, MD5)
            
        Returns:
            str: Hexadecimal checksum
        """
        if algorithm == "BLAKE2b":
            hash_func = hashlib.blake2b()
        elif algorithm == "BLAKE2s":
            hash_func = hashlib.blake2s()
        else:
            hash_func = getattr(hashlib, algorithm.lower())()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    def update_result(self, calculated_checksum, expected_checksum):
        """Update the GUI with verification results."""
        # Update status
        if calculated_checksum.lower() == expected_checksum.lower():
            self.result_status.configure(text="Checksum Matched!", text_color="green")
        else:
            self.result_status.configure(text="Checksum Mismatched!", text_color="red")

        # Update checksum labels
        self.calculated_label.configure(text=f"Calculated Checksum: {calculated_checksum}")
        self.expected_label.configure(text=f"Expected Checksum: {expected_checksum}")

        # Enable copy buttons
        self.copy_calculated_button.configure(state="normal")
        self.copy_expected_button.configure(state="normal")
        self.calculated_checksum = calculated_checksum
        self.expected_checksum = expected_checksum

    def copy_calculated(self):
        """Copy the calculated checksum to the clipboard."""
        if hasattr(self, 'calculated_checksum'):
            pyperclip.copy(self.calculated_checksum)
            messagebox.showinfo("Success", "Calculated checksum copied to clipboard!")

    def copy_expected(self):
        """Copy the expected checksum to the clipboard."""
        if hasattr(self, 'expected_checksum'):
            pyperclip.copy(self.expected_checksum)
            messagebox.showinfo("Success", "Expected checksum copied to clipboard!")

if __name__ == "__main__":
    app = ChecksumVerificationApp()
    app.mainloop()