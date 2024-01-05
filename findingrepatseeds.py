import time
import random
import webbrowser
import tkinter as tk
from tkinter import ttk
from threading import Thread
import pyperclip
from tkinter import filedialog

class SeedGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Repeating Seeds Generator")

        # Modern Style
        self.root.option_add("*TButton*highlightBackground", "#4CAF50")
        self.root.option_add("*TButton*highlightColor", "#4CAF50")
        self.root.option_add("*TButton*background", "#4CAF50")
        self.root.option_add("*TButton*foreground", "white")
        self.root.option_add("*TLabel*foreground", "#333333")
        self.root.option_add("*TFrame*Background", "#f2f2f2")

        style = ttk.Style()
        style.configure("TButton", padding=(6, 3), relief="flat")
        style.configure("TLabel", padding=(0, 5), font=('Helvetica', 10), anchor="w")
        style.configure("TProgressbar", thickness=10)

        # Structure Selection
        self.structure_frame = ttk.Frame(root)
        self.structure_frame.pack(pady=10)

        self.structure_label = ttk.Label(self.structure_frame, text="Choose a structure:")
        self.structure_label.grid(row=0, column=0, sticky="w")

        self.structure_var = tk.StringVar()
        self.structure_options = {
            1: "Repeating World [Bedrock]",
            2: "Mineshafts [Bedrock]",
            3: "Repeating World [Java]",
            4: "Repeating World 2 [Java]"
        }

        self.structure_combobox = ttk.Combobox(self.structure_frame, textvariable=self.structure_var, values=list(self.structure_options.values()))
        self.structure_combobox.grid(row=0, column=1, padx=10)

        # Seed Count Entry
        self.seed_count_frame = ttk.Frame(root)
        self.seed_count_frame.pack(pady=10)

        self.seed_count_label = ttk.Label(self.seed_count_frame, text="Enter the number of seeds to generate:")
        self.seed_count_label.grid(row=0, column=0, sticky="w")

        self.seed_count_var = tk.StringVar()
        self.seed_count_entry = ttk.Entry(self.seed_count_frame, textvariable=self.seed_count_var)
        self.seed_count_entry.grid(row=0, column=1, padx=10)

        # Generate Seeds Button
        self.generate_button = ttk.Button(root, text="Generate Seeds", command=self.generate_seeds)
        self.generate_button.pack(pady=10)

        # Save All Seeds Button
        self.save_button = ttk.Button(root, text="Save All Seeds", command=self.save_all_seeds)
        self.save_button.pack(pady=5)

        # Clear Results Button
        self.clear_button = ttk.Button(root, text="Clear Results", command=self.clear_results)
        self.clear_button.pack(pady=5)

        # Result Display with Vertical Scrollbar
        self.result_text_frame = ttk.Frame(root)
        self.result_text_frame.pack()

        self.result_text = tk.Text(self.result_text_frame, height=10, width=50, wrap=tk.WORD)
        self.result_text.grid(row=0, column=0, sticky="w", padx=(0, 10))

        scrollbar = ttk.Scrollbar(self.result_text_frame, command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.result_text.config(yscrollcommand=scrollbar.set)

        # MADE BY MZEEN
        self.made_by_label = ttk.Label(root, text="MADE BY MZEEN", foreground="#666666")
        self.made_by_label.pack(pady=5)

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(root, variable=self.progress_var, maximum=100, mode='indeterminate', length=200)
        self.progress_bar.pack(fill="x", pady=5)

    def get_seed(self, n, structure):
        if structure == "Repeating World [Bedrock]":
            seed = int(bin(n * 3) + '01100011011111111100111100100100', 2)
            return seed
        elif structure == "Mineshafts [Bedrock]":
            return int(bin(n * 4) + '111011101001010100010100101110', 2)
        elif structure == "Repeating World [Java]":
            return int(bin(n * 4) + '11000010101100111010000101010101100110011000100', 2)
        elif structure == "Repeating World 2 [Java]":
            return int(bin(n * 2) + '100101010111000010110010101100011100011011111010', 2)
        else:
            raise ValueError("Invalid structure type")

    def generate_seeds(self):
        structure_choice = self.structure_var.get()
        seed_count = int(self.seed_count_var.get())

        # Start a new thread for generating seeds
        Thread(target=self.generate_seeds_threaded, args=(structure_choice, seed_count)).start()

    def generate_seeds_threaded(self, structure, seed_count):
        start_time = time.time()
        seeds = self.generate_seeds_helper(structure, seed_count)
        end_time = time.time()

        self.display_seeds(seeds)
        self.result_text.insert(tk.END, f"\nTime taken: {end_time - start_time:.4f} seconds")

    def generate_seeds_helper(self, structure, seed_count):
        if structure in ["Repeating World [Java]", "Repeating World 2 [Java]"]:
            lower_limit = 1
            upper_limit = 10000
        else:
            lower_limit = 1
            upper_limit = min(seed_count, 1000000)  # Adjust as needed
        unique_seeds = random.choices(range(lower_limit, upper_limit + 1), k=min(seed_count, upper_limit - lower_limit + 1))

        seeds = [self.get_seed(seed, structure) for seed in unique_seeds]
        return seeds

    def display_seeds(self, seeds):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Generated Seeds:\n")

        # Progress Bar Update
        self.progress_var.set(0)
        self.root.update()

        for index, seed in enumerate(seeds, start=1):
            seed_str = f"{index}. {seed}"
            self.result_text.insert(tk.END, seed_str + "\n")

            # Add a "Copy" button
            copy_button = ttk.Button(self.root, text="Copy", command=lambda s=seed: self.copy_to_clipboard(s))
            self.result_text.window_create(tk.END, window=copy_button)
            self.result_text.insert(tk.END, "\n")

            # Add an "Open in Chunkbase" button
            chunkbase_button = ttk.Button(self.root, text="Open in Chunkbase", command=lambda s=seed: self.open_chunkbase(s))
            self.result_text.window_create(tk.END, window=chunkbase_button)
            self.result_text.insert(tk.END, "\n\n")

            # Progress Bar Update
            progress_value = (index / len(seeds)) * 100
            self.progress_var.set(progress_value)
            self.root.update()

        # MADE BY MZEEN
        self.made_by_label.pack()

    def save_all_seeds(self):
        seeds_text = self.result_text.get("1.0", tk.END)
        if seeds_text.strip() == "Generated Seeds:":
            return  # No seeds to save

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(seeds_text)
            self.result_text.insert(tk.END, f"\nSeeds saved to {file_path}")

    def clear_results(self):
        # Clear the result text
        self.result_text.delete(1.0, tk.END)

    def copy_to_clipboard(self, seed):
        # Copy the seed to the clipboard
        pyperclip.copy(str(seed))

        # Display "Seed copied to clipboard" message below the seed for 3.5 seconds
        self.result_text.insert(tk.END, "Seed copied to clipboard.\n")
        self.root.after(3500, self.clear_message)

    def clear_message(self):
        # Clear the "Seed copied to clipboard" message after 3.5 seconds
        self.result_text.delete(tk.END-2, tk.END)

    def open_chunkbase(self, seed):
        # Open Chunkbase with the selected seed
        chunkbase_url = f"https://www.chunkbase.com/apps/seed-map#{seed}"
        webbrowser.open(chunkbase_url)

if __name__ == "__main__":
    root = tk.Tk()
    app = SeedGeneratorApp(root)
    app.root.mainloop()