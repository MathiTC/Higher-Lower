import tkinter as tk
from tkinter import messagebox
from elements import store_element
from contexts import get_contexts, create_context


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Home Page")
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Manage Contexts", command=lambda: controller.show_frame("Contexts"))
        button1.pack()

        button2 = tk.Button(self, text="Manage Elements", command=lambda: controller.show_frame("Elements"))
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

        # Dropdown menu to choose context
        self.context_var = tk.StringVar()

        # Get the list of contexts
        contexts_list = get_contexts()

        if contexts_list:
            # Set the initial selection to the first context
            initial_context_id, initial_context_text = contexts_list[0]
            self.context_var.set(initial_context_id)  # Set the initial selection to the first context ID

            # Create the OptionMenu with the list of context texts as labels
            self.context_dropdown = tk.OptionMenu(self, self.context_var, *[context_text for context_id, context_text in
                                                                            contexts_list], command=self.display_context)
            self.context_dropdown.pack(pady=5)
        else:
            # If no contexts are available, display a message
            message_label = tk.Label(self, text="No contexts found.")
            message_label.pack(pady=5)

        # Label to display selected context
        self.context_label = tk.Label(self)
        self.context_label.pack(pady=5)

        # Entry field for RGB code
        self.rgb_entry = tk.Entry(self, width=30)
        self.rgb_entry.pack(pady=5)

        # Button to add new element with RGB code
        self.add_button = tk.Button(self, text="Store Element", command=self.store_element_command)
        self.add_button.pack(pady=5)

        self.back_button = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage"))
        self.back_button.pack()

    def display_context(self, *args):
        selected_context_text = self.context_var.get()
        selected_context_id = self.get_context_id(selected_context_text)
        if selected_context_id:
            self.context_label.config(text=f"Selected Context: {selected_context_text} (ID: {selected_context_id})")

    def get_context_id(self, context_text):
        contexts_list = get_contexts()
        for context_id, context in contexts_list:
            if context == context_text:
                return context_id
        return None

    def store_element_command(self):
        selected_context_text = self.context_var.get()
        selected_context_id = self.get_context_id(selected_context_text)
        rgb_code = self.rgb_entry.get()
        if selected_context_id and rgb_code:
            store_element(selected_context_id, rgb_code)
        else:
            print("Please select a context and enter an RGB code.")


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
        self.title("ELO TEST")

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
