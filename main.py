import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from fpdf import FPDF

class FileConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Type Converter")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # UI Elements
        self.label = tk.Label(root, text="Select a File to Convert", font=("Arial", 14))
        self.label.pack(pady=20)

        self.select_button = tk.Button(root, text="Choose File", command=self.choose_file, font=("Arial", 12), bg="#0078D7", fg="white")
        self.select_button.pack(pady=10)

        self.convert_button = tk.Button(root, text="Convert", command=self.convert_file, font=("Arial", 12), bg="#28A745", fg="white", state=tk.DISABLED)
        self.convert_button.pack(pady=10)

        self.quit_button = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 12), bg="#DC3545", fg="white")
        self.quit_button.pack(pady=20)

        self.selected_file = None

    def choose_file(self):
        self.selected_file = filedialog.askopenfilename(title="Select a File",
                                                        filetypes=[
                                                            ("All Files", "*.*"),
                                                            ("Images", "*.jpg;*.jpeg;*.png;*.bmp;*.gif"),
                                                            ("PDF", "*.pdf"),
                                                            ("Text", "*.txt")
                                                        ])
        if self.selected_file:
            self.label.config(text=f"Selected: {os.path.basename(self.selected_file)}")
            self.convert_button.config(state=tk.NORMAL)

    def convert_file(self):
        if not self.selected_file:
            messagebox.showerror("Error", "No file selected!")
            return

        file_ext = os.path.splitext(self.selected_file)[1].lower()
        output_dir = os.path.join(os.path.dirname(self.selected_file), "Converted_Files")
        os.makedirs(output_dir, exist_ok=True)

        try:
            if file_ext in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]:
                self.convert_image(output_dir)
            elif file_ext == ".txt":
                self.convert_text_to_pdf(output_dir)
            else:
                messagebox.showinfo("Unsupported", f"Conversion for {file_ext} is not supported yet.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def convert_image(self, output_dir):
        try:
            with Image.open(self.selected_file) as img:
                output_path = os.path.join(output_dir, "converted_image.pdf")
                img.convert("RGB").save(output_path, "PDF")
                messagebox.showinfo("Success", f"Image converted to PDF: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert image: {str(e)}")

    def convert_text_to_pdf(self, output_dir):
        try:
            with open(self.selected_file, "r") as file:
                text_content = file.readlines()

            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            for line in text_content:
                pdf.cell(200, 10, txt=line, ln=True, align="L")

            output_path = os.path.join(output_dir, "converted_text.pdf")
            pdf.output(output_path)
            messagebox.showinfo("Success", f"Text file converted to PDF: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert text file: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileConverterApp(root)
    root.mainloop()
