import tkinter as tk
from tkinter import filedialog
import os
import time
import threading
import re

# Custom ASCII Logo
ASCII_LOGO = """\
    █████╗ ██╗     ██████╗ ██╗  ██╗ █████╗     ██████╗ ███████╗██╗   ██╗
    ██╔══██╗██║     ██╔══██╗██║  ██║██╔══██╗    ██╔══██╗██╔════╝██║   ██║
    ███████║██║     ██████╔╝███████║███████║    ██║  ██║█████╗  ██║   ██║
    ██╔══██║██║     ██╔═══╝ ██╔══██║██╔══██║    ██║  ██║██╔══╝  ╚██╗ ██╔╝
    ██║  ██║███████╗██║     ██║  ██║██║  ██║    ██████╔╝███████╗ ╚████╔╝ 
    ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝ ╚══════╝  ╚═══╝  
"""

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

def load_folder_and_search(folder_path, search_term, output_widget):
    search_term_lower = search_term.lower()
    # Regex for http/https and domain with app name
    pattern = re.compile(rf"(https?://[^\s]*{search_term_lower}[^\s]*)|([^\s]*{search_term_lower}\.[a-z]{{2,6}}[^\s]*)", re.IGNORECASE)

    results = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    for line in lines:
                        if pattern.search(line):
                            results.append(line.strip())
            except Exception as e:
                print(f"Error reading {file}: {e}")

    output_file = f"result_{search_term.upper()}.txt"
    with open(output_file, "w", encoding="utf-8") as out:
        out.write('\n'.join(results))

    output_widget.config(state=tk.NORMAL)
    output_widget.insert(tk.END, f"\n✔️ Found {len(results)} matching lines.\n✔️ Saved to '{output_file}'\n")
    output_widget.config(state=tk.DISABLED)

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_path)

def start_search():
    folder_path = folder_entry.get()
    search_term = search_entry.get()
    if not folder_path or not search_term:
        return
    output_box2.config(state=tk.NORMAL)
    output_box2.delete("1.0", tk.END)
    output_box2.config(state=tk.DISABLED)
    threading.Thread(target=load_folder_and_search, args=(folder_path, search_term, output_box2)).start()

# GUI Setup
root = tk.Tk()
root.title("ALPHA DEV")
root.configure(bg="black")
root.geometry("800x600")
root.resizable(False, False)

# ASCII Logo Area
output_box = tk.Text(root, height=12, bg="black", fg="lime", font=("Courier", 10), bd=0)
output_box.pack(pady=10, padx=20)
setup_hacker_style(output_box)
threading.Thread(target=type_text, args=(output_box, ASCII_LOGO)).start()

# Folder Input
folder_label = tk.Label(root, text="📂 Select Combo Folder", bg="black", fg="lime")
folder_label.pack()
folder_entry = tk.Entry(root, width=60, bg="black", fg="lime", insertbackground="lime")
folder_entry.pack(pady=5)
folder_button = tk.Button(root, text="Browse", command=browse_folder, bg="lime", fg="black")
folder_button.pack()

# Search Term
search_label = tk.Label(root, text="🔍 Enter App Name (Example: microsoft)", bg="black", fg="lime")
search_label.pack(pady=10)
search_entry = tk.Entry(root, width=40, bg="black", fg="lime", insertbackground="lime")
search_entry.pack(pady=5)

# Start Button
search_button = tk.Button(root, text="Start Search", command=start_search, bg="lime", fg="black", width=20)
search_button.pack(pady=10)

# Results Box
output_box2 = tk.Text(root, height=10, bg="black", fg="lime", font=("Courier", 10), bd=0)
output_box2.pack(pady=10, padx=20)
output_box2.config(state=tk.DISABLED)

root.mainloop()
