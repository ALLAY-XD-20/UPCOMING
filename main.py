import tkinter as tk
from tkinter import filedialog
import os
import time
import threading
import re

# Custom ASCII logo
ASCII_LOGO = """\
    █████╗ ██╗     ██████╗ ██╗  ██╗ █████╗     ██████╗ ███████╗██╗   ██╗
    ██╔══██╗██║     ██╔══██╗██║  ██║██╔══██╗    ██╔══██╗██╔════╝██║   ██║
    ███████║██║     ██████╔╝███████║███████║    ██║  ██║█████╗  ██║   ██║
    ██╔══██║██║     ██╔═══╝ ██╔══██║██╔══██║    ██║  ██║██╔══╝  ╚██╗ ██╔╝
    ██║  ██║███████╗██║     ██║  ██║██║  ██║    ██████╔╝███████╗ ╚████╔╝ 
    ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝ ╚══════╝  ╚═══╝  
"""

# Typing animation
def type_text(widget, text, delay=0.005):
    widget.config(state=tk.NORMAL)
    widget.delete("1.0", tk.END)
    for char in text:
        widget.insert(tk.END, char)
        widget.update()
        time.sleep(delay)
    widget.config(state=tk.DISABLED)

# Green hacker-style
def setup_hacker_style(widget):
    widget.configure(bg="black", fg="lime", insertbackground="lime")
    widget.tag_configure("center", justify='center')
    widget.tag_add("center", "1.0", "end")

# Load combo folder and search
def load_folder_and_search(folder_path, search_term, output_widget):
    results = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    for line in lines:
                        if search_term.lower() in line.lower():
                            if re.match(r"https://appname\/.*", line):
                                results.append(line.strip())
    
    with open("result_app_name.txt", "w", encoding="utf-8") as out_file:
        for result in results:
            out_file.write(result + "\n")
    
    output_widget.config(state=tk.NORMAL)
    output_widget.insert(tk.END, f"\n\n✔️ Found {len(results)} matching lines.\nSaved to 'result_app_name.txt'\n")
    output_widget.config(state=tk.DISABLED)

# Browse folder
def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_path)

# Start search
def start_search():
    folder_path = folder_entry.get()
    search_term = search_entry.get()
    if not folder_path or not search_term:
        return
    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    output_box.config(state=tk.DISABLED)
    threading.Thread(target=load_folder_and_search, args=(folder_path, search_term, output_box)).start()

# Main GUI
root = tk.Tk()
root.title("ALPHA DEV")
root.configure(bg="black")
root.geometry("800x600")
root.resizable(False, False)

# Output box for ASCII and results
output_box = tk.Text(root, height=12, bg="black", fg="lime", font=("Courier", 10), bd=0)
output_box.pack(pady=10, padx=20)
setup_hacker_style(output_box)

# Animate ASCII
threading.Thread(target=type_text, args=(output_box, ASCII_LOGO)).start()

# Folder selector
folder_label = tk.Label(root, text="📂 Select Combo Folder", bg="black", fg="lime")
folder_label.pack()
folder_entry = tk.Entry(root, width=60, bg="black", fg="lime", insertbackground="lime")
folder_entry.pack(pady=5)
folder_button = tk.Button(root, text="Browse", command=browse_folder, bg="lime", fg="black")
folder_button.pack()

# Search input
search_label = tk.Label(root, text="🔍 Paste You Searching (appname etc.)", bg="black", fg="lime")
search_label.pack(pady=10)
search_entry = tk.Entry(root, width=40, bg="black", fg="lime", insertbackground="lime")
search_entry.pack(pady=5)

# Search button
search_button = tk.Button(root, text="Start Search", command=start_search, bg="lime", fg="black", width=20)
search_button.pack(pady=10)

# Result display
output_box2 = tk.Text(root, height=10, bg="black", fg="lime", font=("Courier", 10), bd=0)
output_box2.pack(pady=10, padx=20)
output_box2.config(state=tk.DISABLED)

root.mainloop()
