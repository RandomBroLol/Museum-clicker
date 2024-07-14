import tkinter as tk
from tkinter import ttk, messagebox
import json

class InjectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Museum Clicker Cheat Panel")
        self.root.geometry("500x350")
        self.root.configure(bg='#1e272e')

        # Alert message
        messagebox.showwarning("Important", "Please save your clicks in the Clicker Museum before changing values here.")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#1e272e')
        style.configure('TLabel', background='#1e272e', foreground='white', font=("Helvetica", 16))
        style.configure('TButton', padding=10, relief="flat", background='#ff6b6b', foreground='white', font=("Helvetica", 14, "bold"))
        style.map('TButton', background=[('active', '#ff4757'), ('pressed', '#ff6348')])
        style.configure('TEntry', fieldbackground='#2f3542', foreground='white', font=("Helvetica", 14))

        self.frame = ttk.Frame(root, padding=(20, 20), style='TFrame')
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Title
        self.title_label = ttk.Label(self.frame, text="Clicker Injector", style='TLabel', font=("Helvetica", 24, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Box Clicks
        self.box_label = ttk.Label(self.frame, text="Box Clicks:", style='TLabel')
        self.box_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        self.box_entry = ttk.Entry(self.frame, style='TEntry')
        self.box_entry.grid(row=1, column=1, padx=10, pady=10)

        # Spacebar Clicks
        self.space_label = ttk.Label(self.frame, text="Spacebar Clicks:", style='TLabel')
        self.space_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
        self.space_entry = ttk.Entry(self.frame, style='TEntry')
        self.space_entry.grid(row=2, column=1, padx=10, pady=10)

        # Change Values Button
        self.change_button = ttk.Button(self.frame, text="Change Values", style='TButton', command=self.change_values)
        self.change_button.grid(row=3, column=0, columnspan=2, pady=20)

        # Hover Effects
        self.change_button.bind("<Enter>", self.on_enter)
        self.change_button.bind("<Leave>", self.on_leave)

    def change_values(self):
        box_clicks = self.box_entry.get()
        space_clicks = self.space_entry.get()

        try:
            if box_clicks:
                box_clicks = int(box_clicks)
                with open("BoxLVLdata.json", "w") as f:
                    json.dump({'clicks': box_clicks}, f)

            if space_clicks:
                space_clicks = int(space_clicks)
                with open("SpaceLVLdat.json", "w") as f:
                    json.dump({'clicks': space_clicks}, f)

            messagebox.showinfo("Success", "Values changed successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integer values.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def on_enter(self, e):
        self.change_button.config(style='Hover.TButton')

    def on_leave(self, e):
        self.change_button.config(style='TButton')

if __name__ == "__main__":
    root = tk.Tk()
    app = InjectorApp(root)
    root.mainloop()
