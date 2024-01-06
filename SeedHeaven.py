import time
import random
import webbrowser
import tkinter as tk
from tkinter import ttk
from threading import Thread
import pyperclip
from tkinter import filedialog
import tkinter.simpledialog
from tkinter import messagebox

class SeedGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SeedHeaven")

        # Modern Style
        self.root.option_add("*TButton*highlightBackground", "#4CAF50")
        self.root.option_add("*TButton*highlightColor", "#4CAF50")
        self.root.option_add("*TButton*background", "#4CAF50")
        self.root.option_add("*TButton*foreground", "white")
        self.root.option_add("*TLabel*foreground", "#333333")
        self.root.option_add("*TFrame*Background", "#f2f2f2")

        style = ttk.Style()
        style.configure("TButton", padding=(6, 3), relief="flat")
        style.configure("Status.TLabel", background="#f0f0f0", relief="flat", font=("Helvetica", 10))
        style.configure("TProgressbar", thickness=100)

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


        # Copy All Button
        self.copy_all_button = ttk.Button(root, text="Copy All", command=self.copy_all)
        self.copy_all_button.pack(pady=5)

        # Clear Results Button
        self.clear_button = ttk.Button(root, text="Clear Results", command=self.clear_results)
        self.clear_button.pack(pady=5)
        #Staus Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, style="Status.TLabel")
        self.status_bar.pack(side="bottom", fill="x", ipady=4)  # Add padding for better spacing
        # Optional: Add a subtle border for visual separation
        self.status_bar.configure(borderwidth=1, relief="solid")


        ## Add menu bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Add "Find Sister Seeds" menu item
        self.find_sister_seeds_menu = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(label="Sister Seeds", menu=self.find_sister_seeds_menu)
        self.find_sister_seeds_menu.add_command(label="Find Sister Seeds", command=self.find_sister_seeds)

        # Result Display with Vertical Scrollbar
        self.result_text_frame = ttk.Frame(root)
        self.result_text_frame.pack()

        self.result_text = tk.Text(self.result_text_frame, height=10, width=50, wrap=tk.WORD)
        self.result_text.grid(row=0, column=0, sticky="w", padx=(0, 10))

        scrollbar = ttk.Scrollbar(self.result_text_frame, command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.result_text.config(yscrollcommand=scrollbar.set)

        # MADE BY MZEEN
        self.made_by_label = ttk.Label(root, text="MADE BY MZEEN\nTool For Minecraft Seeds\nVersion: 1.1", foreground="#666666")
        self.made_by_label.pack(pady=5)

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(root, variable=self.progress_var, maximum=100, mode='indeterminate', length=200)
        self.progress_bar.pack(fill="x", pady=5)

        # Structure Seed Button
        self.seed_check_button = ttk.Button(root, text="Structure Seed", command=self.seed_check)
        self.seed_check_button.pack(pady=5)

        # Seed To Bits Button
        self.seed_to_bits_button = ttk.Button(root, text="Seed To Bits", command=self.seed_to_bits)
        self.seed_to_bits_button.pack(pady=5)

    def seed_to_bits(self):
      seed_input = tkinter.simpledialog.askstring("Seed To Bits", "Enter seed:")
      if seed_input is not None:
        try:
            seed = int(seed_input)
            lower_48_bits = self.get_lower_bits(seed)
            upper_48_bits = self.get_upper_bits(seed, 48)
            lower_32_bits = self.get_lower_bits(seed, 32)
            upper_32_bits = self.get_upper_bits(seed)
            lower_16_bits = self.get_lower_bits(seed, 16)  # Added for 16 bits
            upper_16_bits = self.get_upper_bits(seed, 16)  # Added for 16 bits

            result_str = (
                f"\nLower 48 bits: {hex(lower_48_bits)}\n"
                f"Upper 48 bits: {hex(upper_48_bits)}\n"
                f"Lower 32 bits: {hex(lower_32_bits)}\n"
                f"Upper 32 bits: {hex(upper_32_bits)}\n"
                f"Lower 16 bits: {hex(lower_16_bits)}\n"  # Added for 16 bits
                f"Upper 16 bits: {hex(upper_16_bits)}\n"  # Added for 16 bits
            )
            self.result_text.insert(tk.END, result_str)

            # Convert lower bits to decimal and display
            decimal_lower_48_bits = self.bits_to_decimal(lower_48_bits)
            decimal_upper_48_bits = self.bits_to_decimal(upper_48_bits)
            decimal_lower_32_bits = self.bits_to_decimal(lower_32_bits)
            decimal_upper_32_bits = self.bits_to_decimal(upper_32_bits)
            decimal_lower_16_bits = self.bits_to_decimal(lower_16_bits)  # Added for 16 bits
            decimal_upper_16_bits = self.bits_to_decimal(upper_16_bits)  # Added for 16 bits

            result_str = (
                f"\nDecimal representation of Lower 48 bits: {decimal_lower_48_bits}\n"
                f"Decimal representation of Upper 48 bits: {decimal_upper_48_bits}\n"
                f"Decimal representation of Lower 32 bits: {decimal_lower_32_bits}\n"
                f"Decimal representation of Upper 32 bits: {decimal_upper_32_bits}\n"
                f"Decimal representation of Lower 16 bits: {decimal_lower_16_bits}\n"  # Added for 16 bits
                f"Decimal representation of Upper 16 bits: {decimal_upper_16_bits}\n"  # Added for 16 bits
            )
            self.result_text.insert(tk.END, result_str)

        except ValueError:
                self.result_text.insert(tk.END, "\nInvalid input. Please enter a valid integer seed.")
    def hex_to_decimal(self, hex_value):
        try:
            decimal_value = int(hex_value, 16)
            return decimal_value
        except ValueError:
            return None
     
    def find_sister_seeds(self):
        top = tk.Toplevel(self.root)  # Yeni bir üst düzey pencere oluştur
        top.title("Find Sister Seeds")


        # Input frame for base seed and search range
        input_frame = ttk.Frame(top)
        input_frame.pack(pady=10)

        base_seed_label = ttk.Label(input_frame, text="Enter base seed:")
        base_seed_label.grid(row=0, column=0, sticky="w")

        self.base_seed_entry = ttk.Entry(input_frame)
        self.base_seed_entry.grid(row=0, column=1, padx=10)

        search_range_label = ttk.Label(input_frame, text="Search range:")
        search_range_label.grid(row=1, column=0, sticky="w")

        self.search_range_var = tk.StringVar(value="2^32")  # Default to 2^32
        search_range_radio_2_16 = ttk.Radiobutton(input_frame, text="2^16 (16-Bit Search)", variable=self.search_range_var, value="2^16")
        search_range_radio_2_16.grid(row=1, column=1)
        search_range_radio_2_32 = ttk.Radiobutton(input_frame, text="2^32 (32-Bit Search)", variable=self.search_range_var, value="2^32")
        search_range_radio_2_32.grid(row=1, column=2)
        search_range_radio_2_48 = ttk.Radiobutton(input_frame, text="2^48 (48-Bit Search)", variable=self.search_range_var, value="2^48")
        search_range_radio_2_48.grid(row=1, column=3)

        # Generate button
        generate_button = ttk.Button(top, text="Find Sister Seeds", command=self.generate_sister_seeds)
        generate_button.pack(pady=5)
        
    def generate_sister_seeds(self):
     base_seed = self.base_seed_entry.get()
     try:
        base_seed = int(base_seed)
     except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid integer seed.")
        return

     search_range = int(self.search_range_var.get().split("^")[1])
     Thread(target=self.generate_sister_seeds_threaded, args=(base_seed, search_range)).start()
    
    
    def generate_sister_seeds_threaded(self, base_seed, search_range):
        self.status_var.set("Searching Seeds...")
        sister_seeds = []
        for i in range(65536):
            sister_seed = (2 ** search_range) * i + base_seed
            sister_seeds.append(sister_seed)

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Sister Seeds:\n")
        for seed in sister_seeds:
            self.result_text.insert(tk.END, f"{seed}\n") 

        # Update progress bar
        progress_value = (i / 65536) * 100
        self.progress_var.set(progress_value)
        self.root.update()

         # Update status bar
        self.status_var.set("Sister seeds generated successfully.")


    def get_lower_bits(self, seed, num_bits=48):
        mask = (1 << num_bits) - 1
        return seed & mask

    def get_upper_bits(self, seed, num_bits=32):
        mask = (1 << (num_bits + 32)) - 1
        return (seed & mask) >> 32

    def bits_to_decimal(self, bits):
        return bits

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
        self.status_var.set("Searching Seeds...")
        start_time = time.time()
        seeds = self.generate_seeds_helper(structure, seed_count)
        end_time = time.time()

        self.display_seeds(seeds)
        self.result_text.insert(tk.END, f"\nTime taken: {end_time - start_time:.4f} seconds")

        # Update status bar
        self.status_var.set("Seeds generated successfully.")

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
        
    def seed_check(self):
     seed_input = tkinter.simpledialog.askstring("Structure Seed", "Enter seed:")
     if seed_input is not None:
        try:
            seed = int(seed_input)

            # Convert world seed to structure seed
            structure_seed = self.to_structure_seed(seed)
            result_str = f"Structure Seed: {structure_seed}\n"

            self.result_text.insert(tk.END, result_str)

        except ValueError:
            self.result_text.insert(tk.END, "\nInvalid input. Please enter a valid integer seed.")

    

    def to_structure_seed(self, world_seed):
        # This is a placeholder for the WorldSeed.toStructureSeed() method
        return world_seed & ((1 << 48) - 1)  # This is just a dummy calculation
    
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

    def copy_all(self):
        # Kullanıcı kutucuktaki tüm metni kopyalayabilir
        all_text = self.result_text.get("1.0", tk.END)
        pyperclip.copy(all_text)

        # Kullanıcıya "All text copied to clipboard" mesajını göster
        self.result_text.insert(tk.END, "All text copied to clipboard.\n")
        self.root.after(3500, self.clear_message)


if __name__ == "__main__":
    root = tk.Tk()
    app = SeedGeneratorApp(root)
    app.root.mainloop()
