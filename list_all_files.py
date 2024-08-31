import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, Button
import os

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        combine_python_files(directory)

def combine_python_files(directory):
    python_files = [file for file in os.listdir(directory) if file.endswith('.py')]
    combined_content = ""
    for file_name in python_files:
        with open(os.path.join(directory, file_name), 'r') as file:
            combined_content += f"\n# File: {file_name}\n" + file.read() + "\n"
    text_area.delete('1.0', tk.END)  # Clear previous content
    text_area.insert(tk.END, combined_content)  # Display combined content

def save_combined_files():
    save_path = filedialog.asksaveasfilename(filetypes=[("Text files", "*.txt")], defaultextension=".txt")
    if save_path:
        with open(save_path, 'w') as file:
            file.write(text_area.get("1.0", tk.END))  # Write text area content to file
        messagebox.showinfo("Success", "All Python files have been combined and saved!")

def main():
    root = tk.Tk()
    root.title("Towel Code Combiner")
    root.geometry("600x400")

    global text_area
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Browse Directory Button
    browse_button = Button(root, text="Browse Directory", command=browse_directory)
    browse_button.pack(pady=5)

    # Save Files Button
    save_button = Button(root, text="Save Combined Files", command=save_combined_files)
    save_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
