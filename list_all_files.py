import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, Button, Checkbutton, IntVar, Toplevel, Label, Entry
import os

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        try:
            depth = int(depth_entry.get())  # Get depth from entry field and convert to integer
            if depth < 0:
                raise ValueError("Depth cannot be negative")
            combine_files(directory, depth)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid non-negative integer for depth.")

def combine_files(directory, depth):
    combined_content = ""
    supported_extensions = []

    # Add selected file extensions
    if py_var.get(): supported_extensions.append('.py')
    if cpp_var.get(): supported_extensions.append('.cpp')
    if h_var.get(): supported_extensions.append('.h')
    if html_var.get(): supported_extensions.append('.html')
    if js_var.get(): supported_extensions.append('.js')
    if php_var.get(): supported_extensions.append('.php')
    if css_var.get(): supported_extensions.append('.css')

    # Add bonus file types if selected
    for ext, var in bonus_vars.items():
        if var.get():
            supported_extensions.append(ext)

    # Traverse directories up to the specified depth
    for root, dirs, files in os.walk(directory):
        # Calculate depth of the current directory
        current_depth = root[len(directory):].count(os.sep)
        if current_depth > depth:
            del dirs[:]  # Stop traversing deeper into this directory
            continue
        
        # Filter files by supported extensions
        files = [file for file in files if any(file.endswith(ext) for ext in supported_extensions)]
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                combined_content += f"\n// File: {file_path}\n" + file.read() + "\n"

    text_area.delete('1.0', tk.END)  # Clear previous content
    text_area.insert(tk.END, combined_content)  # Display combined content

def save_combined_files():
    save_path = filedialog.asksaveasfilename(filetypes=[("Text files", "*.txt")], defaultextension=".txt")
    if save_path:
        with open(save_path, 'w') as file:
            file.write(text_area.get("1.0", tk.END))  # Write text area content to file
        messagebox.showinfo("Success", "Selected files have been combined and saved!")

def raise_frame(frame):
    frame.tkraise()

def show_bonus_options():
    bonus_window = Toplevel(root)
    bonus_window.title("Bonus File Types")
    bonus_window.geometry("300x600")

    # Create frames for each page
    page1 = tk.Frame(bonus_window)
    page2 = tk.Frame(bonus_window)
    page3 = tk.Frame(bonus_window)

    for frame in (page1, page2, page3):
        frame.grid(row=0, column=0, sticky='news')

    # Page 1 file types
    page1_vars = {
        '.java': bonus_vars['.java'],
        '.c': bonus_vars['.c'],
        '.cs': bonus_vars['.cs'],
        '.ts': bonus_vars['.ts'],
        '.rb': bonus_vars['.rb'],
        '.css': bonus_vars['.css'],
        '.go': bonus_vars['.go'],
        '.swift': bonus_vars['.swift'],
        '.kt': bonus_vars['.kt'],
        '.rs': bonus_vars['.rs'],
        '.dart': bonus_vars['.dart'],
        '.lua': bonus_vars['.lua'],
        '.pl': bonus_vars['.pl'],
        '.r': bonus_vars['.r'],
        '.sh': bonus_vars['.sh'],
        '.bat': bonus_vars['.bat'],
        '.m': bonus_vars['.m'],
        '.v': bonus_vars['.v'],
    }

    # Page 2 file types
    page2_vars = {
        '.vhd': bonus_vars['.vhd'],
        '.sql': bonus_vars['.sql'],
        '.xml': bonus_vars['.xml'],
        '.asm': bonus_vars['.asm'],
        '.md': bonus_vars['.md'],
        '.groovy': bonus_vars['.groovy'],
        '.erl': bonus_vars['.erl'],
        '.tsx': bonus_vars['.tsx'],
        '.jsx': bonus_vars['.jsx'],
        '.s': bonus_vars['.s'],
        '.f90': bonus_vars['.f90'],
        '.ml': bonus_vars['.ml'],
        '.sc': bonus_vars['.sc'],
        '.hs': bonus_vars['.hs'],
        '.clj': bonus_vars['.clj'],
        '.cljc': bonus_vars['.cljc'],
        '.ex': bonus_vars['.ex'],
        '.exs': bonus_vars['.exs'],
    }

    # Page 3 file types
    page3_vars = {
        '.coffee': bonus_vars['.coffee'],
        '.rbw': bonus_vars['.rbw'],
        '.pas': bonus_vars['.pas'],
        '.mjs': bonus_vars['.mjs'],
        '.pyw': bonus_vars['.pyw'],
        '.prl': bonus_vars['.prl'],
        '.vbs': bonus_vars['.vbs'],
        '.tex': bonus_vars['.tex'],
        '.pm': bonus_vars['.pm'],
        '.rkt': bonus_vars['.rkt'],
        '.f': bonus_vars['.f'],
        '.jl': bonus_vars['.jl'],
        '.tsv': bonus_vars['.tsv'],
        '.rhtml': bonus_vars['.rhtml'],
        '.vb': bonus_vars['.vb'],
        '.scala': bonus_vars['.scala'],
        '.sqlx': bonus_vars['.sqlx'],
        '.cmake': bonus_vars['.cmake'],
    }

    # Add checkboxes for page 1
    for ext in page1_vars.keys():
        Checkbutton(page1, text=ext, variable=bonus_vars[ext]).pack(anchor='w', padx=10, pady=2)

    # Add checkboxes for page 2
    for ext in page2_vars.keys():
        Checkbutton(page2, text=ext, variable=bonus_vars[ext]).pack(anchor='w', padx=10, pady=2)

    # Add checkboxes for page 3
    for ext in page3_vars.keys():
        Checkbutton(page3, text=ext, variable=bonus_vars[ext]).pack(anchor='w', padx=10, pady=2)

    # Add Next/Previous buttons
    Button(page1, text="Next Page", command=lambda: raise_frame(page2)).pack(pady=10)
    Button(page2, text="Previous Page", command=lambda: raise_frame(page1)).pack(side='left', pady=10)
    Button(page2, text="Next Page", command=lambda: raise_frame(page3)).pack(side='right', pady=10)
    Button(page3, text="Previous Page", command=lambda: raise_frame(page2)).pack(pady=10)

    # Start with the first page
    raise_frame(page1)

def main():
    global text_area, py_var, cpp_var, h_var, html_var, js_var, php_var, css_var, bonus_vars, root, depth_entry

    root = tk.Tk()
    root.title("Towel Code Combiner")
    root.geometry("600x650")

    # Default file type checkboxes (auto-selected)
    py_var = IntVar(value=1)
    cpp_var = IntVar(value=1)
    h_var = IntVar(value=1)
    html_var = IntVar(value=1)
    js_var = IntVar(value=1)
    php_var = IntVar(value=1)
    css_var = IntVar(value=1)

    # Initialize the dictionary for bonus file types
    bonus_vars = {
        '.java': IntVar(),
        '.c': IntVar(),
        '.cs': IntVar(),
        '.ts': IntVar(),
        '.rb': IntVar(),
        '.css': IntVar(),
        '.go': IntVar(),
        '.swift': IntVar(),
        '.kt': IntVar(),
        '.rs': IntVar(),
        '.dart': IntVar(),
        '.lua': IntVar(),
        '.pl': IntVar(),
        '.r': IntVar(),
        '.sh': IntVar(),
        '.bat': IntVar(),
        '.m': IntVar(),
        '.v': IntVar(),
        '.vhd': IntVar(),
        '.sql': IntVar(),
        '.xml': IntVar(),
        '.asm': IntVar(),
        '.md': IntVar(),
        '.groovy': IntVar(),
        '.erl': IntVar(),
        '.tsx': IntVar(),
        '.jsx': IntVar(),
        '.s': IntVar(),
        '.f90': IntVar(),
        '.ml': IntVar(),
        '.sc': IntVar(),
        '.hs': IntVar(),
        '.clj': IntVar(),
        '.cljc': IntVar(),
        '.ex': IntVar(),
        '.exs': IntVar(),
        '.coffee': IntVar(),
        '.rbw': IntVar(),
        '.pas': IntVar(),
        '.mjs': IntVar(),
        '.pyw': IntVar(),
        '.prl': IntVar(),
        '.vbs': IntVar(),
        '.tex': IntVar(),
        '.pm': IntVar(),
        '.rkt': IntVar(),
        '.f': IntVar(),
        '.jl': IntVar(),
        '.tsv': IntVar(),
        '.rhtml': IntVar(),
        '.vb': IntVar(),
        '.scala': IntVar(),
        '.sqlx': IntVar(),
        '.cmake': IntVar()
    }

    # Add default checkboxes
    py_checkbox = Checkbutton(root, text=".py", variable=py_var)
    cpp_checkbox = Checkbutton(root, text=".cpp", variable=cpp_var)
    h_checkbox = Checkbutton(root, text=".h", variable=h_var)
    html_checkbox = Checkbutton(root, text=".html", variable=html_var)
    js_checkbox = Checkbutton(root, text=".js", variable=js_var)
    php_checkbox = Checkbutton(root, text=".php", variable=php_var)
    css_checkbox = Checkbutton(root, text=".css", variable=css_var)

    py_checkbox.pack(anchor='w', padx=10, pady=2)
    cpp_checkbox.pack(anchor='w', padx=10, pady=2)
    h_checkbox.pack(anchor='w', padx=10, pady=2)
    html_checkbox.pack(anchor='w', padx=10, pady=2)
    js_checkbox.pack(anchor='w', padx=10, pady=2)
    php_checkbox.pack(anchor='w', padx=10, pady=2)
    css_checkbox.pack(anchor='w', padx=10, pady=2)

    # Entry for depth selection
    depth_label = Label(root, text="Enter Depth for Subdirectories (0 for current folder only):")
    depth_label.pack(pady=5)
    depth_entry = Entry(root)
    depth_entry.insert(0, "0")  # Default depth level 0
    depth_entry.pack(pady=5)

    # Button to show bonus options
    bonus_button = Button(root, text="Bonus", command=show_bonus_options)
    bonus_button.pack(pady=5)

    # Browse Directory Button
    browse_button = Button(root, text="Browse Directory", command=browse_directory)
    browse_button.pack(pady=5)

    # Text area for displaying combined content
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Save Files Button
    save_button = Button(root, text="Save Combined Files", command=save_combined_files)
    save_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
