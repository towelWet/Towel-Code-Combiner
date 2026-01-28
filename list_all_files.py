import os
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import Button, Checkbutton, IntVar, Toplevel, Label, Entry, Frame, StringVar

from tkinterdnd2 import DND_FILES, TkinterDnD


def parse_drop_data(data: str):
    # tkinterdnd2 returns a Tcl list-like string; splitlist safely handles braces/spaces.
    try:
        return list(root.tk.splitlist(data))
    except Exception:
        return [data]


def safe_int_depth():
    try:
        depth = int(depth_entry.get())
        if depth < 0:
            raise ValueError
        return depth
    except Exception:
        messagebox.showerror("Invalid Input", "Please enter a valid non-negative integer for depth.")
        return None


def get_selected_extensions():
    exts = []

    # Main/common file types (checkboxes on main window)
    if py_var.get(): exts.append(".py")
    if pyw_var.get(): exts.append(".pyw")

    if c_var.get(): exts.append(".c")
    if cpp_var.get(): exts.append(".cpp")
    if h_var.get(): exts.append(".h")
    if hpp_var.get(): exts.append(".hpp")

    if js_var.get(): exts.append(".js")
    if jsx_var.get(): exts.append(".jsx")
    if ts_var.get(): exts.append(".ts")
    if tsx_var.get(): exts.append(".tsx")

    if html_var.get(): exts.append(".html")
    if css_var.get(): exts.append(".css")
    if php_var.get(): exts.append(".php")

    if json_var.get(): exts.append(".json")
    if yml_var.get(): exts.append(".yml")
    if yaml_var.get(): exts.append(".yaml")
    if xml_var.get(): exts.append(".xml")
    if toml_var.get(): exts.append(".toml")
    if md_var.get(): exts.append(".md")
    if sql_var.get(): exts.append(".sql")

    if sh_var.get(): exts.append(".sh")
    if bat_var.get(): exts.append(".bat")
    if ps1_var.get(): exts.append(".ps1")

    # Bonus types (checkboxes in Bonus window)
    for ext, var in bonus_vars.items():
        if var.get():
            exts.append(ext)

    # Deduplicate while preserving order
    seen = set()
    out = []
    for e in exts:
        if e not in seen:
            seen.add(e)
            out.append(e)
    return out


def combine_files_in_directory(directory, depth, supported_extensions):
    combined_content = ""
    matched_files = 0

    for root_dir, dirs, files in os.walk(directory):
        current_depth = root_dir[len(directory):].count(os.sep)
        if current_depth > depth:
            del dirs[:]
            continue

        filtered = [f for f in files if any(f.endswith(ext) for ext in supported_extensions)]
        for file_name in filtered:
            file_path = os.path.join(root_dir, file_name)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    combined_content += f"\n// File: {file_path}\n" + f.read() + "\n"
                matched_files += 1
            except Exception:
                continue

    return combined_content, matched_files


def combine_files_from_file_list(file_paths, supported_extensions):
    combined_content = ""
    matched_files = 0

    for file_path in file_paths:
        if not os.path.isfile(file_path):
            continue
        if not any(file_path.endswith(ext) for ext in supported_extensions):
            continue

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                combined_content += f"\n// File: {file_path}\n" + f.read() + "\n"
            matched_files += 1
        except Exception:
            continue

    return combined_content, matched_files


def load_directory(directory):
    depth = safe_int_depth()
    if depth is None:
        return

    exts = get_selected_extensions()
    if not exts:
        messagebox.showwarning("No file types selected", "Select at least one extension.")
        return

    content, matched = combine_files_in_directory(directory, depth, exts)

    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, content)

    status_var.set(f"Loaded folder: {directory} | Depth: {depth} | Matched files: {matched}")


def load_files(files):
    exts = get_selected_extensions()
    if not exts:
        messagebox.showwarning("No file types selected", "Select at least one extension.")
        return

    content, matched = combine_files_from_file_list(files, exts)

    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, content)

    status_var.set(f"Loaded files: {len(files)} | Matched files: {matched}")


def on_drop(event):
    paths = parse_drop_data(event.data)

    # Prefer folder behavior if any folder is dropped
    if len(paths) == 1 and os.path.isdir(paths[0]):
        load_directory(paths[0])
        return

    for p in paths:
        if os.path.isdir(p):
            load_directory(p)
            return

    load_files(paths)


def save_combined_files():
    from tkinter import filedialog

    save_path = filedialog.asksaveasfilename(
        filetypes=[("Text files", "*.txt")],
        defaultextension=".txt",
    )
    if save_path:
        try:
            with open(save_path, "w", encoding="utf-8", errors="ignore") as f:
                f.write(text_area.get("1.0", tk.END))
            messagebox.showinfo("Success", "Selected files have been combined and saved!")
        except Exception as e:
            messagebox.showerror("Save Failed", str(e))


def raise_frame(frame):
    frame.tkraise()


def show_bonus_options():
    bonus_window = Toplevel(root)
    bonus_window.title("Bonus File Types")
    bonus_window.geometry("340x680")

    page1 = Frame(bonus_window)
    page2 = Frame(bonus_window)
    page3 = Frame(bonus_window)

    for frame in (page1, page2, page3):
        frame.grid(row=0, column=0, sticky="news")

    # Bonus pages (less common / extra formats)
    page1_exts = [
        ".cc", ".cxx", ".hh", ".hxx", ".mm",
        ".java", ".cs", ".go", ".rs", ".swift", ".kt", ".dart",
        ".lua", ".rb", ".pl", ".r",
    ]
    page2_exts = [
        ".v", ".vhd", ".asm", ".s", ".f90", ".ml", ".sc", ".hs",
        ".clj", ".cljc", ".ex", ".exs", ".erl", ".groovy",
    ]
    page3_exts = [
        ".coffee", ".mjs", ".pas", ".prl", ".vbs", ".tex", ".pm", ".rkt",
        ".f", ".jl", ".tsv", ".rhtml", ".vb", ".scala", ".sqlx", ".cmake",
        ".ini",
    ]

    def add_checks(frame, exts):
        for ext in exts:
            if ext not in bonus_vars:
                continue
            Checkbutton(frame, text=ext, variable=bonus_vars[ext]).pack(anchor="w", padx=10, pady=2)

    add_checks(page1, page1_exts)
    add_checks(page2, page2_exts)
    add_checks(page3, page3_exts)

    Button(page1, text="Next Page", command=lambda: raise_frame(page2)).pack(pady=10)
    Button(page2, text="Previous Page", command=lambda: raise_frame(page1)).pack(side="left", padx=10, pady=10)
    Button(page2, text="Next Page", command=lambda: raise_frame(page3)).pack(side="right", padx=10, pady=10)
    Button(page3, text="Previous Page", command=lambda: raise_frame(page2)).pack(pady=10)

    raise_frame(page1)


def main():
    global root, text_area, depth_entry, status_var
    global py_var, pyw_var, c_var, cpp_var, h_var, hpp_var
    global js_var, jsx_var, ts_var, tsx_var, html_var, css_var, php_var
    global json_var, yml_var, yaml_var, xml_var, toml_var, md_var, sql_var
    global sh_var, bat_var, ps1_var
    global bonus_vars

    root = TkinterDnD.Tk()
    root.title("Towel Code Combiner (DnD)")
    root.geometry("760x820")

    status_var = StringVar(value="Drop a folder or files onto the window.")

    # Common code files selected by default
    py_var = IntVar(value=1)
    pyw_var = IntVar(value=1)

    c_var = IntVar(value=1)
    cpp_var = IntVar(value=1)
    h_var = IntVar(value=1)
    hpp_var = IntVar(value=1)

    js_var = IntVar(value=1)
    jsx_var = IntVar(value=1)
    ts_var = IntVar(value=1)
    tsx_var = IntVar(value=1)

    html_var = IntVar(value=1)
    css_var = IntVar(value=1)
    php_var = IntVar(value=1)

    json_var = IntVar(value=1)
    yml_var = IntVar(value=1)
    yaml_var = IntVar(value=1)
    xml_var = IntVar(value=1)
    toml_var = IntVar(value=1)
    md_var = IntVar(value=1)
    sql_var = IntVar(value=1)

    sh_var = IntVar(value=1)
    bat_var = IntVar(value=1)
    ps1_var = IntVar(value=1)

    # Bonus extensions (default OFF; you can flip common ones ON here if you want)
    bonus_ext_list = [
        ".java", ".cc", ".cxx", ".hh", ".hxx", ".mm",
        ".cs", ".tsv", ".sqlx", ".cmake", ".ini",
        ".go", ".rs", ".swift", ".kt", ".dart",
        ".lua", ".rb", ".pl", ".r",
        ".v", ".vhd", ".asm", ".s",
        ".f90", ".ml", ".sc", ".hs",
        ".clj", ".cljc", ".ex", ".exs", ".erl", ".groovy",
        ".coffee", ".mjs", ".pas", ".prl", ".vbs", ".tex", ".pm", ".rkt",
        ".f", ".jl", ".rhtml", ".vb", ".scala",
    ]

    # If you want "common bonus" selected by default, add them to this set:
    common_bonus = {
        ".java", ".cs", ".go", ".rs", ".swift", ".kt", ".dart",
        ".cc", ".cxx", ".hh", ".hxx", ".mm",
        ".asm", ".s",
        ".ini",
    }

    bonus_vars = {ext: IntVar(value=1 if ext in common_bonus else 0) for ext in bonus_ext_list}

    # UI: Common file types
    Label(root, text="Common file types (default selected):").pack(anchor="w", padx=10, pady=(10, 0))

    grid = Frame(root)
    grid.pack(fill=tk.X, padx=10, pady=(5, 0))

    checks = [
        (".py", py_var), (".pyw", pyw_var),
        (".c", c_var), (".cpp", cpp_var),
        (".h", h_var), (".hpp", hpp_var),
        (".js", js_var), (".jsx", jsx_var),
        (".ts", ts_var), (".tsx", tsx_var),
        (".html", html_var), (".css", css_var),
        (".php", php_var), (".json", json_var),
        (".yml", yml_var), (".yaml", yaml_var),
        (".xml", xml_var), (".toml", toml_var),
        (".md", md_var), (".sql", sql_var),
        (".sh", sh_var), (".bat", bat_var),
        (".ps1", ps1_var),
    ]

    cols = 6
    for i, (label, var) in enumerate(checks):
        r = i // cols
        c = i % cols
        Checkbutton(grid, text=label, variable=var).grid(row=r, column=c, sticky="w", padx=6, pady=3)

    # Depth
    Label(root, text="Depth for subdirectories (0 = current folder only):").pack(pady=(10, 0))
    depth_entry = Entry(root)
    depth_entry.insert(0, "0")
    depth_entry.pack(pady=5)

    # Bonus button
    Button(root, text="Bonus", command=show_bonus_options).pack(pady=5)

    # Drop target
    drop_label = Label(
        root,
        text="Drop folder or files here",
        relief="ridge",
        bd=3,
        padx=10,
        pady=10,
    )
    drop_label.pack(fill=tk.X, padx=10, pady=(10, 5))

    # Register DnD
    root.drop_target_register(DND_FILES)
    root.dnd_bind("<<Drop>>", on_drop)
    drop_label.drop_target_register(DND_FILES)
    drop_label.dnd_bind("<<Drop>>", on_drop)

    # Status line
    Label(root, textvariable=status_var, anchor="w").pack(fill=tk.X, padx=10, pady=(0, 10))

    # Output text area
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=26)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Save
    Button(root, text="Save Combined Files", command=save_combined_files).pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
