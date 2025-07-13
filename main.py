import tkinter as tk
from tkinter import filedialog
import os
import time
import threading
import re

ASCII_LOGO = """\
    █████╗ ██╗     ██████╗ ██╗  ██╗ █████╗     ██████╗ ███████╗██╗   ██╗
    ██╔══██╗██║     ██╔══██╗██║  ██║██╔══██╗    ██╔══██╗██╔════╝██║   ██║
    ███████║██║     ██████╔╝███████║███████║    ██║  ██║█████╗  ██║   ██║
    ██╔══██║██║     ██╔═══╝ ██╔══██║██╔══██║    ██║  ██║██╔══╝  ╚██╗ ██╔╝
    ██║  ██║███████╗██║     ██║  ██║██║  ██║    ██████╔╝███████╗ ╚████╔╝ 
    ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝ ╚══════╝  ╚═══╝  
"""

selected_paths = []

def type_text(widget, text, delay=0.005):
    widget.config(state=tk.NORMAL)
    widget.delete("1.0", tk.END)
    for char in text:
        widget.insert(tk.END, char)
        widget.update()
        time.sleep(delay)
    widget.config(state=tk.DISABLED)

def setup_hacker_style(widget):
    widget.configure(bg="black", fg="lime", insertbackground="lime")
    widget.tag_configure("center", justify='center')
    widget.tag_add("center", "1.0", "end")

def load_and_search(paths, search_term, output_widget):
    search_term_lower = search_term.lower()
    pattern = re.compile(rf"(https?://[^\s]*{search_term_lower}[^\s]*)|([^\s]*{search_term_lower}\.[a-z]{{2,6}}[^\s]*)", re.IGNORECASE)

    results = []

    for path in paths:
        if os.path.isfile(path):
            files_to_check = [path]
        elif os.path.isdir(path):
            files_to_check = []
            for root, _, files in os.walk(path):
                for file in files:
                    files_to_check.append(os.path.join(root, file))
        else:
            continue

        for file_path in files_to_check:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        if pattern.search(line):
                            results.append(line.strip())
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    output_file = f"result_{search_term.upper()}.txt"
    with open(output_file, "w", encoding="utf-8") as out:
        out.write('\n'.join(results))

    output_widget.config(state=tk.NORMAL)
    output_widget.insert(tk.END, f"\n✔️ Found {len(results)} matching lines.\n✔️ Saved to '{output_file}'\n")
    output_widget.config(state=tk.DISABLED)

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        selected_paths.clear()
        selected_paths.append(folder_path)
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_path)

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt *.json *.log"), ("All Files", "*.*")])
    if file_path:
        selected_paths.clear()
        selected_paths.append(file_path)
        path_entry.delete(0, tk.END)
        path_entry.insert(0, file_path)

def start_search():
    search_term = search_entry.get().strip()
    if not selected_paths or not search_term:
        return
    output_box2.config(state=tk.NORMAL)
    output_box2.delete("1.0", tk.END)
    output_box2.config(state=tk.DISABLED)
    threading.Thread(target=load_and_search, args=(selected_paths[:], search_term, output_box2)).start()

# GUI Setup
root = tk.Tk()
root.title("ALPHA DEV")
root.configure(bg="black")
root.geometry("800x600")
root.resizable(False, False)

# ASCII Display
output_box = tk.Text(root, height=12, bg="black", fg="lime", font=("Courier", 10), bd=0)
output_box.pack(pady=10, padx=20)
setup_hacker_style(output_box)
threading.Thread(target=type_text, args=(output_box, ASCII_LOGO)).start()

# Path Selection Area
tk.Label(root, text="📂 Combo Folder or File Path", bg="black", fg="lime").pack()
path_entry = tk.Entry(root, width=60, bg="black", fg="lime", insertbackground="lime")
path_entry.pack(pady=5)

button_frame = tk.Frame(root, bg="black")
button_frame.pack()

tk.Button(button_frame, text="Load Folder", command=browse_folder, bg="lime", fg="black", width=15).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Load File", command=browse_file, bg="lime", fg="black", width=15).pack(side=tk.LEFT, padx=5)

# App Name Input
tk.Label(root, text="🔍 Enter App Name (Example: microsoft)", bg="black", fg="lime").pack(pady=10)
search_entry = tk.Entry(root, width=40, bg="black", fg="lime", insertbackground="lime")
search_entry.pack(pady=5)

# Start Button
tk.Button(root, text="Start Search", command=start_search, bg="lime", fg="black", width=20).pack(pady=10)

# Results Output Box
output_box2 = tk.Text(root, height=10, bg="black", fg="lime", font=("Courier", 10), bd=0)
output_box2.pack(pady=10, padx=20)
output_box2.config(state=tk.DISABLED)

root.mainloop()
