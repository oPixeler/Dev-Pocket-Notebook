import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import customtkinter as ct
import sqlite3
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x512")
        self.center_window()
        self.title("Dev Pocket Notebook!")

        self.background_image_path = os.path.join("resources", "yolanda.gif")
        self.background_images = self.load_and_resize_gif(self.background_image_path, (500, 500))

        image_path = os.path.join("resources", "PDN_logo.png")
        image = Image.open(image_path)
        image = image.resize((200, 200), resample=Image.LANCZOS)
        self.landing_logo = ImageTk.PhotoImage(image)

        setup_database()  # Initialize the database
        self.landing_page()
        self.update_background(0)

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 530
        window_height = 500
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def load_and_resize_gif(self, path, size):
        original_gif = Image.open(path)
        frames = ImageSequence.Iterator(original_gif)
        resized_frames = [ImageTk.PhotoImage(frame.resize(size, resample=Image.LANCZOS)) for frame in frames]
        return resized_frames

    def landing_page(self):
        for i in self.winfo_children():
            i.destroy()

        self.background_label = tk.Label(self, image=self.background_images[0])
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.logo_show = tk.Label(self, image=self.landing_logo)
        self.logo_show.pack(side="top", pady=30)

        self.button1 = ct.CTkButton(self, text="New Snippet", command=self.new_snippet, 
                                   width=200, height=50, 
                                   corner_radius=10, 
                                   fg_color="#F93E83", 
                                   hover_color="#F9673E",
                                   font=("Lolicandy", 16, "bold"), 
                                   text_color="light blue")
        self.button1.pack(pady=10)
        self.button2 = ct.CTkButton(self, text="Your Saved Snippets", command=self.saved_snippets, 
                                   width=200, height=50, 
                                   corner_radius=10, 
                                   fg_color="#F93E83", 
                                   hover_color="#F9673E",
                                   font=("Lolicandy", 16, "bold"), 
                                   text_color="light blue")
        self.button2.pack(pady=10)

    def update_background(self, frame_index):
        if hasattr(self, 'background_label') and self.background_label.winfo_exists():
            self.background_label.configure(image=self.background_images[frame_index])
            frame_index = (frame_index + 1) % len(self.background_images)
            self.after(50, self.update_background, frame_index)

    def new_snippet(self):
        for i in self.winfo_children():
            i.destroy()

        self.frame2 = tk.Frame(self, width=300, height=300)
        self.frame2.pack(pady=20)

        self.shortcut_name_label = ttk.Label(self.frame2, text="Shortcut Name:")
        self.shortcut_name_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.shortcut_name_entry = ttk.Entry(self.frame2, width=50)
        self.shortcut_name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.description_label = ttk.Label(self.frame2, text="Description:")
        self.description_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.description_entry = ttk.Entry(self.frame2, width=50)
        self.description_entry.grid(row=1, column=1, padx=6, pady=5)

        self.category_button = ct.CTkButton(self.frame2, text="Category", width=100, height=30)
        self.category_button.grid(row=1, column=2, padx=5, pady=5)

        self.snippet_label = ttk.Label(self.frame2, text="Snippet:")
        self.snippet_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.snippet_text = tk.Text(self.frame2, width=45, height=10, padx=5)
        self.snippet_text.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        self.save_button = ct.CTkButton(self.frame2, text="Save to Library", width=70, height=30, command=self.save_snippet)
        self.save_button.grid(row=3, column=1, sticky="e", padx=5, pady=5)
        self.share_button = ct.CTkButton(self.frame2, text="Share/Commit", width=70, height=30)
        self.share_button.grid(row=3, column=2, sticky="w", padx=5, pady=5)

        # Add padding to all widgets
        for child in self.frame2.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def save_snippet(self):
        shortcut_name = self.shortcut_name_entry.get()
        description = self.description_entry.get()
        snippet = self.snippet_text.get("1.0", tk.END).strip()

        if shortcut_name and snippet:  # Ensure required fields are not empty
            save_snippet_to_db(shortcut_name, description, snippet)
            self.landing_page()

    def saved_snippets(self):
        for i in self.winfo_children():
            i.destroy()

        self.frame2 = tk.Frame(self, width=300, height=300)
        self.frame2.pack()

        snippets = load_snippets_from_db()

        if not snippets:
            no_snippets_label = ttk.Label(self.frame2, text="No snippets found.")
            no_snippets_label.pack(pady=10)
        else:
            for snippet in snippets:
                snippet_button = tk.Button(self.frame2, text=snippet[0], command=lambda s=snippet: self.show_snippet_detail(s), relief=tk.FLAT, font=("Helvetica", 10, "underline"), fg="blue", cursor="hand2")
                snippet_button.pack(pady=5, anchor="w")

        self.login_btn = ct.CTkButton(self.frame2, text="Go to Landing Page", command=self.landing_page, 
                                 width=150, height=40, 
                                 corner_radius=10, 
                                 fg_color="#2980b9", 
                                 hover_color="#3498db",
                                 font=("Roboto", 14), 
                                 text_color="white")
        self.login_btn.pack(pady=10)


    def show_snippet_detail(self, snippet):
        for i in self.winfo_children():
            i.destroy()
    
        self.frame2 = tk.Frame(self, width=300, height=300)
        self.frame2.pack(pady=20)
    
    # Display snippet details
        snippet_name = ttk.Label(self.frame2, text=f"Name: {snippet[0]}", font=("Helvetica", 12, "bold"))
        snippet_name.grid(row=0, column=0, sticky="w", padx=5, pady=5)
    
        snippet_description = ttk.Label(self.frame2, text=f"Description: {snippet[1]}")
        snippet_description.grid(row=1, column=0, sticky="w", padx=5, pady=5)
    
        snippet_content = tk.Text(self.frame2, width=50, height=10)
        snippet_content.insert(tk.END, snippet[2])
        snippet_content.config(state=tk.DISABLED)
        snippet_content.grid(row=2, column=0, padx=5, pady=5)
    
    # Add a back button to return to the list of snippets
        back_button = ct.CTkButton(self.frame2, text="Back to List", command=self.saved_snippets, width=100, height=30)
        back_button.grid(row=3, column=0, padx=5, pady=5)

    # Add padding to all widgets
        for child in self.frame2.winfo_children():
            child.grid_configure(padx=5, pady=5)


def setup_database():
    conn = sqlite3.connect("snippets.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS snippets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shortcut_name TEXT NOT NULL,
            description TEXT,
            snippet TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_snippet_to_db(shortcut_name, description, snippet):
    conn = sqlite3.connect("snippets.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO snippets (shortcut_name, description, snippet)
        VALUES (?, ?, ?)
    ''', (shortcut_name, description, snippet))
    conn.commit()
    conn.close()

def load_snippets_from_db():
    conn = sqlite3.connect("snippets.db")
    cursor = conn.cursor()
    cursor.execute('SELECT shortcut_name, description, snippet FROM snippets')
    snippets = cursor.fetchall()
    conn.close()
    return snippets

def is_first_run():
    return not os.path.exists("snippets.db")

def clear_database():
    if os.path.exists("snippets.db"):
        os.remove("snippets.db")
    setup_database()

if __name__ == "__main__":
    if is_first_run():
        clear_database()
    app = App()
    app.mainloop()


