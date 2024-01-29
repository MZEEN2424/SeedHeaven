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
from datetime import datetime

class SeedGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SeedHeaven")
        
         # Set color scheme
        self.background_color = "#FFFFFF"
        self.primary_color = "#2E7D32"  # Bolder green
        self.secondary_color = "#F57C00"  # Complementary orange
        self.text_color = "#333333"
        
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use a theme for a modern look

        # Configure colors
        self.style.configure("TButton", padding=(15, 10), relief="flat", font=("Roboto", 9), foreground="white", borderwidth=2, borderradius=30)
        self.style.map("TButton", background=[("", self.primary_color)])
        self.style.configure("TLabel", foreground=self.text_color, font=("Roboto", 10), background=self.background_color)
        self.style.configure("TFrame", background=self.background_color)
        self.style.configure("TProgressbar", thickness=20, troughcolor=self.background_color, background=self.secondary_color)
        self.style.configure("TRadiobutton", background=self.secondary_color, foreground="white", padding=(8, 4), font=("Roboto", 8), borderwidth=2, relief="solid")
        self.style.map("TRadiobutton", background=[("selected", self.secondary_color)])
        # Structure Selection
        self.structure_frame = ttk.Frame(root)
        self.structure_frame.pack(pady=10)

        self.structure_label = ttk.Label(self.structure_frame, text="Choose a structure:")
        self.structure_label.grid(row=0, column=0, sticky="w")

        self.structure_var = tk.StringVar()
        self.structure_options = {
            1: "Repeating World [Bedrock]",
            2: "Mineshafts [Bedrock]",
            3: "Repeating Mineshafts [Java]",
            4: "Repeating Mineshafts 2 [Java]",
            5: "12 Eye End Portal [Bedrock]",
            6: "Repeating Ravines [Java]"
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
        self.menu_bar.add_cascade(label="Sister Seeds Finding", menu=self.find_sister_seeds_menu)
        self.find_sister_seeds_menu.add_command(label="Find Sister Seeds", command=self.find_sister_seeds)
        self.result_text_frame = ttk.Frame(root)
        self.result_text_frame.pack(pady=10)

        self.result_text = tk.Text(self.result_text_frame, height=10, width=50, wrap=tk.WORD, font=("Arial", 10))
        self.result_text.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 5))

        scrollbar = ttk.Scrollbar(self.result_text_frame, command=self.result_text.yview, style="Vertical.TScrollbar")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.result_text.config(yscrollcommand=scrollbar.set)

       
        self.result_text.tag_configure("result", background="#2E7D32", foreground="white", font=("Arial", 10))

        self.style = ttk.Style()
        self.style.configure("Vertical.TScrollbar", troughcolor="#F57C00", slidercolor="white", bordercolor="#F57C00", arrowcolor="white")

        # MADE BY MZEEN
        self.made_by_label = ttk.Label(root, text="MADE BY MZEEN\nTool For Minecraft Seeds\nVersion: 1.4", foreground="#666666")
        self.made_by_label.pack(pady=5)

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(root, variable=self.progress_var, maximum=100, mode='indeterminate', length=500)
        self.progress_bar.pack(fill="x", pady=5)    

        # Structure Seed Button
        self.seed_check_button = ttk.Button(root, text="Structure Seed", command=self.seed_check)
        self.seed_check_button.pack(pady=5)

        # Seed To Bits Button
        self.seed_to_bits_button = ttk.Button(root, text="Seed To Bits", command=self.seed_to_bits)
        self.seed_to_bits_button.pack(pady=5)
        
        self.seed_to_text_button = ttk.Button(root, text="Seed To Text(32 Bit Seeds Only)", command=self.seed_to_text)
        self.seed_to_text_button.pack(pady=5)
        
        self.seed_convert_button = ttk.Button(root, text="Bit Info (Only Positive Seeds)", command=self.convert_and_display)
        self.seed_convert_button.pack(pady=5)

        # Existing Result Textbox
        self.result_text.delete(1.0, tk.END) 
        self.result_text.insert(tk.END, "Generated Seeds:\n")
        
        self.status_animation_interval = 80
        self.target_color = "#4CAF50" 

        self.current_color = "#f0f0f0" 
        self.animate_status_bar()
        self.style = ttk.Style()
        self.style.configure("TButton", padding=(15, 10), relief="flat", font=("Roboto", 9), background=self.primary_color)
        self.style.map("TButton", background=[("active", self.secondary_color)])
        
    def convert_and_display(self):
        # Get Decimal Seed from the user
        decimal_seed = tkinter.simpledialog.askstring("Binary Splitter", "Enter Seed:")
        
        if decimal_seed is None:
            return 

        try:
            decimal_seed_int = int(decimal_seed)
            binary_seed = self.get_binary_representation(decimal_seed_int)

            lower_32_bits, upper_32_bits = self.split_bits(binary_seed, 32)
            lower_48_bits, upper_48_bits = self.split_bits(binary_seed, 48)

            result_str = (
            f"\nConverted Seed: {decimal_seed_int}\n"
            f"Lower 32 Bits (Binary): {lower_32_bits}\n"
            f"Upper 32 Bits (Binary): {upper_32_bits}\n"
            f"Lower 32 Bits (Text): {self.binary_to_text(lower_32_bits)}\n"
            f"Upper 32 Bits (Text): {self.binary_to_text(upper_32_bits)}\n"
            f"Lower 32 Bits (Hex): {hex(int(lower_32_bits, 2))}\n"
            f"Upper 32 Bits (Hex): {hex(int(upper_32_bits, 2))}\n"
            f"Lower 32 Bits (Decimal): {int(lower_32_bits, 2)}\n"
            f"Upper 32 Bits (Decimal): {int(upper_32_bits, 2)}\n"
            f"\nLower 48 Bits (Binary): {lower_48_bits}\n"
            f"Upper 48 Bits (Binary): {upper_48_bits}\n"
            f"Lower 48 Bits (Text): {self.binary_to_text(lower_48_bits)}\n"
            f"Upper 48 Bits (Text): {self.binary_to_text(upper_48_bits)}\n"
            f"Lower 48 Bits (Hex): {hex(int(lower_48_bits, 2))}\n"
            f"Upper 48 Bits (Hex): {hex(int(upper_48_bits, 2))}\n"
            f"Lower 48 Bits (Decimal): {int(lower_48_bits, 2)}\n"
            f"Upper 48 Bits (Decimal): {int(upper_48_bits, 2)}\n"
        )
            self.result_text.insert(tk.END, result_str)
        except ValueError:
            self.result_text.insert(tk.END, "\nInvalid input. Please enter a valid decimal seed.")
    
    def binary_to_text(self, binary_str):
    # Convert binary string to text (assuming ASCII encoding)
        text = ''.join([chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8)])
        return text
            

    def get_binary_representation(self, decimal_seed):
        # Convert decimal seed to binary
        binary_seed = bin(decimal_seed)[2:]

        # If the binary representation is longer than 64 bits, truncate the excess bits
        if len(binary_seed) > 64:
            binary_seed = binary_seed[-64:]

        # If the binary representation is shorter than 64 bits, pad with zeros
        binary_seed = binary_seed.zfill(64)

        return binary_seed

    def split_bits(self, binary_seed, num_bits):
        lower_bits = binary_seed[-num_bits:]
        upper_bits = binary_seed[:-num_bits]
        return lower_bits, upper_bits

    
    def convert_seeds(self, lower_bits, upper_bits):
        try:
            lower_bits_int = int(lower_bits, 2)
            upper_bits_int = int(upper_bits, 2)
            
            # Combine lower and upper bits to get the seed
            seed = (upper_bits_int << 48) | lower_bits_int

            # Display the result
            result_str = f"\nConverted Seed: {seed}\n"
            self.result_text.insert(tk.END, result_str)
        except ValueError:
            self.result_text.insert(tk.END, "\nInvalid input. Please enter valid binary representations of lower and upper bits.")


    def combine_bits(self, lower_bits, upper_bits):
        seed = (int(upper_bits) << 16) | int(lower_bits)
        return seed
        
    def seed_to_bits(self):
      seed_input = tkinter.simpledialog.askstring("Seed To Bits", "Enter seed:")
      if seed_input is not None:
        try:
            seed = int(seed_input)
            lower_48_bits = self.get_lower_bits(seed)
            upper_48_bits = self.get_upper_bits(seed, 48)
            lower_32_bits = self.get_lower_bits(seed, 32)
            upper_32_bits = self.get_upper_bits(seed)
            

            result_str = (
                f"\nLower 48 bits: {hex(lower_48_bits)}\n"
                f"Upper 48 bits: {hex(upper_48_bits)}\n"
                f"Lower 32 bits: {hex(lower_32_bits)}\n"
                f"Upper 32 bits: {hex(upper_32_bits)}\n"
            )
            self.result_text.insert(tk.END, result_str)

            # Convert lower bits to decimal and display
            decimal_lower_48_bits = self.bits_to_decimal(lower_48_bits)
            decimal_upper_48_bits = self.bits_to_decimal(upper_48_bits)
            decimal_lower_32_bits = self.bits_to_decimal(lower_32_bits)
            decimal_upper_32_bits = self.bits_to_decimal(upper_32_bits)
            

            result_str = (
                f"\nDecimal representation of Lower 48 bits: {decimal_lower_48_bits}\n"
                f"Decimal representation of Upper 48 bits: {decimal_upper_48_bits}\n"
                f"Decimal representation of Lower 32 bits: {decimal_lower_32_bits}\n"
                f"Decimal representation of Upper 32 bits: {decimal_upper_32_bits}\n"
            )
            self.result_text.insert(tk.END, result_str)

        except ValueError:
                self.result_text.insert(tk.END, "\nInvalid input. Please enter a valid integer seed.")
                
    def animate_status_bar(self):
        target_rgb = [int(self.target_color[i:i+2], 16) for i in (1, 3, 5)]
        current_rgb = [int(self.current_color[i:i+2], 16) for i in (1, 3, 5)]

        step = [(target_rgb[i] - current_rgb[i]) / 100 for i in range(3)]

       
        current_rgb = [round(current_rgb[i] + step[i]) for i in range(3)]
        self.current_color = f"#{current_rgb[0]:02X}{current_rgb[1]:02X}{current_rgb[2]:02X}"

       
        self.status_bar.configure(background=self.current_color)
        self.root.after(self.status_animation_interval, self.animate_status_bar)
        
        
    def hex_to_decimal(self, hex_value):
        try:
            decimal_value = int(hex_value, 16)
            return decimal_value
        except ValueError:
            return None
     
    def find_sister_seeds(self):
        top = tk.Toplevel(self.root) 
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
     
    def seed_to_text(self):
        
        seed_input = tkinter.simpledialog.askstring("Seed To Text", "Enter seed:")
        if seed_input is not None:
            try:
                seed = int(seed_input)
                seed_count = int(tkinter.simpledialog.askstring("Seed To Text", "Enter seed count:"))
                result = self.search(seed, "<", seed_count)
                self.result_text.delete(1.0, tk.END)
                random.shuffle(result)
                self.result_text.insert(tk.END, "Seed results:\n")
                for item in result:
                    self.result_text.insert(tk.END, f"{item}\n")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid integer values.")
                
    
    def search(self, seed, start, amount):
        res = []
        base = ""
        while len(res) < amount:
            base += start
            dist = seed - self.java_hashcode(base)
            while dist < 0:
                dist += 1 << 32
            while 31**len(base) > dist:
                nxt = ""
                tmp = dist
                for char in base:
                    c = ord(char) + tmp % 31
                    tmp //= 31
                    nxt = chr(c) + nxt
                res.append(nxt)
                if len(res) >= amount:
                    return res
                dist += 1 << 32
        return res

    def java_hashcode(self, s):
        h = 0
        for c in s:
            h = (31 * h + ord(c)) & 0xFFFFFFFF
        return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000
    
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
        progress_batch_size = 100  # Adjust as needed
        for i in range(0, 65536, progress_batch_size):
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
        elif structure == "Repeating Mineshafts [Java]":
            return int(bin(n * 4) + '11000010101100111010000101010101100110011000100', 2)
        elif structure == "Repeating Mineshafts 2 [Java]":
            return int(bin(n * 2) + '100101010111000010110010101100011100011011111010', 2)
        elif structure == "12 Eye End Portal [Bedrock]":
            return int(bin(n * 4) + '00111101010101010001111001011000', 2)
        elif structure == "Repeating Ravines [Java]":
            return int(bin(n * 2) + '11000010101100111010000101010101100110011000010', 2)
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
        if structure in ["Repeating World [Java]", "Repeating World 2 [Java]", "Repeating Ravines [Java]"]:
            lower_limit = 1
            upper_limit = 10000
        else:
            lower_limit = 1
            upper_limit = 10000000  # Adjust as needed
        unique_seeds = set()

        while len(unique_seeds) < seed_count:
         seed = self.get_seed(random.randint(lower_limit, upper_limit), structure)
         unique_seeds.add(seed)

        seeds = list(unique_seeds)
        return seeds

    def display_seeds(self, seeds):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Generated Seeds:\n")
        self.display_coordinates()
        # Progress Bar Update
        self.progress_var.set(0)
        self.root.update()
        
        progress_batch_size = 100

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
            
            
         # Update progress bar
        if index % progress_batch_size == 0 or index == len(seeds):
            progress_value = (index / len(seeds)) * 100
            self.progress_var.set(progress_value)
            self.root.update()

        # MADE BY MZEEN
        self.made_by_label.pack()
    
    def display_coordinates(self):
        structure_type = self.structure_var.get()
        if "12 Eye End Portal [Bedrock]" in structure_type:
            coords_str = "Coords: X: 308 Z: 1284"
        else:
            coords_str = ""

        self.result_text.insert(tk.END, coords_str + "\n")
    
    def seed_check(self):
        seed_input = tkinter.simpledialog.askstring("Structure Seed", "Enter seed:")
        if seed_input is not None:
         try:
              seed = int(seed_input)

            # Convert world seed to structure seeds
              structure_seed_48_bit = self.to_structure_seed(seed)
              structure_seed_32_bit = self.to_structure_seed(seed, num_bits=32)

              result_str = (
                f"48-bit Structure Seed: {structure_seed_48_bit}\n"
                f"32-bit Structure Seed: {structure_seed_32_bit}\n"
              )

              self.result_text.insert(tk.END, result_str)

         except ValueError:
            self.result_text.insert(tk.END, "\nInvalid input. Please enter a valid integer seed.")

    def is_32bit_int(n):
     return n.bit_length() <= 32

    def to_structure_seed(self, world_seed, num_bits=48):
        if world_seed.bit_length() <= num_bits:
            return world_seed
        else:
            return world_seed & ((1 << num_bits) - 1)
    
    def save_all_seeds(self):
        seeds_text = self.result_text.get("1.0", tk.END)
        if seeds_text.strip() == "Generated Seeds:":
            return  # No seeds to save

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(seeds_text)
            self.result_text.insert(tk.END, f"\nSeeds saved to {file_path}")

    def reset_progress_bar(self):
        self.progress_var.set(0)
        self.root.update()
    

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
       
        all_text = self.result_text.get("1.0", tk.END)
        pyperclip.copy(all_text)

        
        self.result_text.insert(tk.END, "All text copied to clipboard.\n")
        self.root.after(3500, self.clear_message)
    
if __name__ == "__main__":
    root = tk.Tk()
    app = SeedGeneratorApp(root)
    app.root.mainloop()
    root.mainloop()
