import tkinter as tk
from tkinter import ttk
import pickle
from tkinter import messagebox
from contexts import create_context

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Home Page")
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Manage Contexts", command=lambda: controller.show_frame("Contexts"))
        button1.pack()

        button2 = tk.Button(self, text="Manage Elemtents", command=lambda: controller.show_frame("Elements"))
        button2.pack()

        button3 = tk.Button(self, text="Rate", command=lambda: controller.show_frame("Rating"))
        button3.pack()


class Contexts(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Contexts")
        label.pack(pady=10, padx=10)

        self.entry = tk.Entry(self, width=30)
        self.entry.pack(pady=5)

        # Create a button to trigger the command
        self.button = tk.Button(self, text="Create Context", command=self.create_context_command)
        self.button.pack(pady=5)

        self.back_button = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage"))
        self.back_button.pack()

    def create_context_command(self):
        context_text = self.entry.get()
        if context_text:
            context_id = create_context(context_text)  # Assuming create_context function is accessible here
            messagebox.showinfo("Context Created", f"Context created with ID: {context_id}")
        else:
            messagebox.showerror("Error", "Please enter a context text.")


class Elements(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Elements")
        label.pack(pady=10, padx=10)

        self.back_button = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage"))
        self.back_button.pack()



class Rating(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Rating")
        label.pack(pady=10, padx=10)

        self.back_button = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage"))
        self.back_button.pack()




class Voting(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Rating")
        label.pack(pady=10, padx=10)




class SinglePageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FodboldTur")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        self.create_frames()

        self.show_frame("HomePage")

    def create_frames(self):
        # Define all frames/pages here
        pages = [HomePage, Contexts, Elements, Rating, Voting]

        for F in pages:
            frame = F(self.container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        # Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = SinglePageApp()
    app.mainloop()