import tkinter as tk
from tkinter import filedialog, messagebox
import pyfiglet

# Generate ASCII Header
ASCII_HEADER = pyfiglet.figlet_format("ALPHA DEV")

class AlphaDevApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ALPHA DEV")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        # Text widget for animated ASCII output
        self.ascii_text = tk.Text(root, height=10, bg="black", fg="lime", font=("Courier", 10), borderwidth=0)
        self.ascii_text.pack()
        self.ascii_text.configure(state="disabled")

        # Typing animation
        self.ascii_chars = list(ASCII_HEADER)
        self.char_index = 0
        self.animate_ascii()

        # Load Combo Button
        self.load_button = tk.Button(root, text="🔍 Load Combo File", command=self.load_file,
                                     bg="black", fg="lime", activebackground="lime", activeforeground="black",
                                     font=("Courier", 12, "bold"), borderwidth=2)
        self.load_button.pack(pady=10)

        # Search Input
        self.search_label = tk.Label(root, text="📎 PASTE YOU SEARCHING (App Name):", fg="lime",
                                     bg="black", font=("Courier", 10))
        self.search_label.pack()
        self.search_entry = tk.Entry(root, width=40, bg="black", fg="lime", insertbackground="lime",
                                     font=("Courier", 12), borderwidth=2, highlightbackground="lime", highlightcolor="lime")
        self.search_entry.pack(pady=5)

        # Search & Save Button
        self.search_button = tk.Button(root, text="✅ SEARCH & SAVE", command=self.search_and_save,
                                       bg="black", fg="lime", activebackground="lime", activeforeground="black",
                                       font=("Courier", 12, "bold"), borderwidth=2)
        self.search_button.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(root, text="", fg="lime", bg="black", font=("Courier", 10))
        self.status_label.pack()

        self.file_data = []

    def animate_ascii(self):
        if self.char_index < len(self.ascii_chars):
            self.ascii_text.configure(state="normal")
            self.ascii_text.insert("end", self.ascii_chars[self.char_index])
            self.ascii_text.configure(state="disabled")
            self.char_index += 1
            self.root.after(5, self.animate_ascii)  # 5ms per character for fast animation

    def load_file(self):
        file_path = filedialog.askopenfilename(title="Select Combo File")
        if file_path:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                self.file_data = f.readlines()
            self.status_label.config(text=f"✔ Loaded {len(self.file_data)} lines from file.")

    def search_and_save(self):
        keyword = self.search_entry.get().strip()
        if not self.file_data:
            messagebox.showerror("Error", "⚠ Please load a file first.")
            return
        if not keyword:
            messagebox.showerror("Error", "⚠ Please enter an app name to search.")
            return

        results = [line for line in self.file_data if keyword.lower() in line.lower()]
        if results:
            output_filename = f"result_{keyword}.txt"
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.writelines(results)
            self.status_label.config(text=f"✅ Found {len(results)} results. Saved to {output_filename}.")
            messagebox.showinfo("Done", f"✅ Found {len(results)} results.\nSaved to: {output_filename}")
        else:
            self.status_label.config(text="❌ No results found.")
            messagebox.showinfo("No Match", "❌ No matching lines found.")

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = AlphaDevApp(root)
    root.mainloop()
