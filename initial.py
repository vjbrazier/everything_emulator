# Imports
import customtkinter as ctk

# Initial setup
ctk.set_appearance_mode("system")
root = ctk.CTk()
root.geometry("600x600")
root.title("Everything Emulator")

# Grid layout
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Search Bar
search = ctk.CTkEntry(root)
search.grid(sticky="nsew", row=0, column=0, columnspan=2, padx=10, pady=10)

# Button class (to make them the same)
class CustomButton(ctk.CTkButton):
    def __init__(self, master, text, row, column):
        super().__init__(master, text=text, width=100, height=100)
        self.grid(row=row, column=column, sticky="ew", padx=10, pady=10)

# Buttons
CustomButton(root, "SNES", 1, 0)
CustomButton(root, "Wii",  1, 1)

# # Buttons arranged in a grid
# btn1 = ctk.CTkButton(root, text="Button 1")
# btn1.grid(row=0, column=0, padx=10, pady=10)

# btn2 = ctk.CTkButton(root, text="Button 2")
# btn2.grid(row=0, column=1, padx=10, pady=10)

# btn3 = ctk.CTkButton(root, text="Button 3")
# btn3.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")  # Spans 2 columns


root.mainloop()
