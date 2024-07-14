import tkinter as tk
from tkinter import ttk, messagebox
import json
from PIL import Image, ImageTk
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ClickerMuseum:
    def __init__(self, root):
        self.root = root
        self.root.title("Clicker Museum")
        self.root.geometry("800x600")
        self.root.configure(bg='#1e1e1e')

        self.show_warning()

        self.box_clicks = 0
        self.space_clicks = 0
        self.double_click = False

        self.box_label = None
        self.space_label = None

        self.load_clicks_from_files()

        # Styles
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#1e1e1e')
        self.style.configure('TLabel', background='#1e1e1e', foreground='white', font=("Helvetica", 16))
        self.style.configure('TButton', padding=10, relief="flat", background='#616161', foreground='white', font=("Helvetica", 14, "bold"))
        self.style.map('TButton', background=[('active', '#424242'), ('pressed', '#757575')])
        self.style.configure('TEntry', fieldbackground='#424242', foreground='white', font=("Helvetica", 14))

        # Main Frame
        self.main_frame = ttk.Frame(root, padding=(20, 20), style='TFrame')
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Title
        self.title_label = ttk.Label(self.main_frame, text="Clicker Museum", style='TLabel', font=("Helvetica", 24, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Clicker Labels and Buttons
        self.setup_clicker_ui()

        # Save Button
        self.save_button = ttk.Button(self.main_frame, text="Save", style='TButton', command=self.save_clicks_to_files)
        self.save_button.grid(row=3, column=0, columnspan=2, pady=20)

        # Shop Button
        self.shop_button = ttk.Button(self.main_frame, text="Open Shop", style='TButton', command=self.open_shop)
        self.shop_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Watch for JSON file changes
        self.event_handler = ClicksFileHandler(self)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, path='.', recursive=False)
        self.observer.start()

    def show_warning(self):
        result = messagebox.askokcancel("Warning", "This is a parody of Cookie Clicker.\nClick OK to continue.")
        if not result:
            self.root.destroy()

    def setup_clicker_ui(self):
        # Box Clicker
        box_label_frame = ttk.Frame(self.main_frame, style='TFrame')
        box_label_frame.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        box_img = Image.open("Images/box.png").resize((50, 50))
        box_img = ImageTk.PhotoImage(box_img)

        self.box_label = ttk.Label(box_label_frame, image=box_img, text=f"Box Clicker: {self.box_clicks}", compound=tk.LEFT, style='TLabel')
        self.box_label.image = box_img
        self.box_label.pack(side=tk.LEFT, padx=10)

        self.box_button = ttk.Button(self.main_frame, text="Click Me!", style='TButton', command=self.box_click)
        self.box_button.grid(row=1, column=1, padx=10, pady=10)

        # Spacebar Clicker
        space_label_frame = ttk.Frame(self.main_frame, style='TFrame')
        space_label_frame.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        space_img = Image.open("Images/space.jpg").resize((50, 50))
        space_img = ImageTk.PhotoImage(space_img)

        self.space_label = ttk.Label(space_label_frame, image=space_img, text=f"Spacebar Clicker: {self.space_clicks}", compound=tk.LEFT, style='TLabel')
        self.space_label.image = space_img
        self.space_label.pack(side=tk.LEFT, padx=10)

        self.root.bind("<space>", self.space_click)

    def box_click(self):
        self.box_clicks += 10 if self.double_click else 1
        self.update_labels()

    def space_click(self, event=None):
        self.space_clicks += 10 if self.double_click else 1
        self.update_labels()

    def update_labels(self):
        if self.box_label:
            self.box_label.config(text=f"Box Clicker: {self.box_clicks}")
        if self.space_label:
            self.space_label.config(text=f"Spacebar Clicker: {self.space_clicks}")

    def save_clicks_to_files(self):
        with open("BoxLVLdata.json", "w") as f:
            json.dump({'clicks': self.box_clicks}, f)
        with open("SpaceLVLdat.json", "w") as f:
            json.dump({'clicks': self.space_clicks}, f)
        messagebox.showinfo("Success", "Values saved successfully!")

    def load_clicks_from_files(self):
        try:
            with open("BoxLVLdata.json", "r") as f:
                data = json.load(f)
                self.box_clicks = data.get('clicks', 0)
            with open("SpaceLVLdat.json", "r") as f:
                data = json.load(f)
                self.space_clicks = data.get('clicks', 0)
        except FileNotFoundError:
            self.box_clicks = 0
            self.space_clicks = 0
        self.update_labels()

    def open_shop(self):
        shop_window = tk.Toplevel(self.root)
        shop_window.title("Clicker Museum Shop")
        shop_window.geometry("600x400")
        shop_window.configure(bg='#1e1e1e')

        shop_frame = ttk.Frame(shop_window, padding=(20, 20), style='TFrame')
        shop_frame.pack(expand=True, fill=tk.BOTH)

        shop_title_label = ttk.Label(shop_frame, text="Clicker Museum Shop", style='TLabel', font=("Helvetica", 20, "bold"))
        shop_title_label.grid(row=0, column=0, columnspan=2, pady=10)

        shop_items = [
            {"name": "Double Click", "price": 100, "image": "Images/potion.jpg", "effect": "Double click rate"},
            {"name": "+10 Box Clicks", "price": 50, "image": "Images/box_upgrade.jpg", "effect": "Increase box clicks"},
            {"name": "+10 Space Clicks", "price": 50, "image": "Images/space_upgrade.jpg", "effect": "Increase space clicks"},
            {"name": "+10 Clicks in 5s", "price": 150, "image": "Images/potion.jpg", "effect": "Clicks x10 for 5 seconds"},
        ]

        for i, item in enumerate(shop_items):
            item_frame = ttk.Frame(shop_frame, style='TFrame', padding=(10, 10))
            item_frame.grid(row=i+1, column=0, padx=10, pady=10, sticky=tk.W)

            item_img = Image.open(item["image"]).resize((50, 50))
            item_img = ImageTk.PhotoImage(item_img)

            item_label = ttk.Label(item_frame, image=item_img, text=f"{item['name']} ({item['price']} clicks)", compound=tk.LEFT, style='TLabel')
            item_label.image = item_img
            item_label.pack(side=tk.LEFT, padx=10)

            buy_button = ttk.Button(item_frame, text="Buy", style='TButton', command=lambda item=item: self.buy_item(item))
            buy_button.pack(side=tk.RIGHT, padx=10)

        shop_window.transient(self.root)
        shop_window.grab_set()

    def buy_item(self, item):
        if self.box_clicks >= item["price"]:
            self.box_clicks -= item["price"]
            if item["name"] == "Double Click":
                self.double_click = True
            elif item["name"] == "+10 Box Clicks":
                self.box_clicks += 10
            elif item["name"] == "+10 Space Clicks":
                self.space_clicks += 10
            elif item["name"] == "+10 Clicks in 5s":
                self.activate_clicks_in_5s()
            self.update_labels()
        else:
            messagebox.showerror("Error", "Not enough Box Clicks!")

    def activate_clicks_in_5s(self):
        self.root.after(5000, self.deactivate_clicks_in_5s)
        self.box_clicks_per_5s = 10

    def deactivate_clicks_in_5s(self):
        self.box_clicks_per_5s = 0

    def update_from_json(self):
        self.load_clicks_from_files()

class ClicksFileHandler(FileSystemEventHandler):
    def __init__(self, app):
        self.app = app

    def on_modified(self, event):
        if event.src_path.endswith("BoxLVLdata.json") or event.src_path.endswith("SpaceLVLdat.json"):
            self.app.update_from_json()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClickerMuseum(root)
    root.mainloop()
