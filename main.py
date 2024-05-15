import tkinter as tk
from tkinter import messagebox
import pickle
from elements import store_element, get_elements_rating
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
            context_id = create_context(context_text)
            messagebox.showinfo("Context Created", f"Context created with ID: {context_id}")
        else:
            messagebox.showerror("Error", "Please enter a context text.")


class Elements(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Elements")
        label.pack(pady=10, padx=10)

        self.context_var = tk.StringVar()
        self.context_dropdown = tk.OptionMenu(self, self.context_var, "")
        self.context_dropdown.pack(pady=5)

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

        self.refresh_contexts()

    def refresh_contexts(self):
        # Get the list of contexts
        contexts_list = get_contexts()

        # Clear existing options in the dropdown
        self.context_dropdown["menu"].delete(0, "end")

        if contexts_list:
            for context_id, context_text in contexts_list:
                self.context_dropdown["menu"].add_command(
                    label=context_text,
                    command=lambda value=context_text: self.context_var.set(value)
                )

            self.context_var.set(contexts_list[0][1])  # Set the initial selection to the first context text
            self.display_context()
        else:
            self.context_var.set("")
            self.context_label.config(text="No contexts found.")

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

        # Age input
        age_label = tk.Label(self, text="Age")
        age_label.pack(pady=5)
        self.age_entry = tk.Entry(self, width=30)
        self.age_entry.pack(pady=5)

        # Gender input
        gender_label = tk.Label(self, text="Gender")
        gender_label.pack(pady=5)
        self.gender_entry = tk.Entry(self, width=30)
        self.gender_entry.pack(pady=5)

        # Button to save the data
        self.save_button = tk.Button(self, text="Save", command=self.save_data)
        self.save_button.pack(pady=10)

        self.back_button = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage"))
        self.back_button.pack(pady=10)

    def save_data(self):
        age = self.age_entry.get()
        gender = self.gender_entry.get()
        if age and gender:
            self.controller.age = age
            self.controller.gender = gender
            tk.messagebox.showinfo("Data Saved", "Age and Gender have been saved.")
            self.controller.show_frame("Voting")  # Navigate to the Voting page
        else:
            tk.messagebox.showerror("Input Error", "Please enter both age and gender.")


class Voting(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Voting")
        label.pack(pady=10, padx=10)

        # Dropdown menu to choose context
        self.context_var = tk.StringVar()
        self.context_dropdown = tk.OptionMenu(self, self.context_var, "")
        self.context_dropdown.pack(pady=5)

        self.refresh_contents()

        # Create a frame to hold the color boxes
        self.color_frame = tk.Frame(self)
        self.color_frame.pack(fill="both", expand=True)

        # Create two boxes for RGB colors
        self.box1 = tk.Label(self.color_frame, text="", bg="red", width=20, height=10, relief="raised")
        self.box1.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        self.box1.bind("<Button-1>", self.box1_clicked)

        self.box2 = tk.Label(self.color_frame, text="", bg="blue", width=20, height=10, relief="raised")
        self.box2.pack(side="right", expand=True, fill="both", padx=10, pady=10)
        self.box2.bind("<Button-1>", self.box2_clicked)

        self.back_button = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage"))
        self.back_button.pack(pady=10)

    def refresh_contents(self):
        contexts_list = get_contexts()

        self.context_dropdown["menu"].delete(0, "end")

        if contexts_list:
            for context_id, context_text in contexts_list:
                self.context_dropdown["menu"].add_command(
                    label=context_text,
                    command=lambda value=context_text: self.context_var.set(value)
                )

            self.context_var.set(contexts_list[0][1])  # Set the initial selection to the first context text
        else:
            self.context_var.set("")

    def refresh_boxes(self):
        selected_context_text = self.context_var.get()
        selected_context_id = self.get_context_id(selected_context_text)
        if selected_context_id:
            elements = self.get_elements(selected_context_id)
            if elements:
                rgb_colors = list(elements.values())
                if len(rgb_colors) >= 2:
                    self.box1.config(bg=rgb_colors[0])
                    self.box2.config(bg=rgb_colors[1])

    def get_context_id(self, context_text):
        contexts_list = get_contexts()
        for context_id, context in contexts_list:
            if context == context_text:
                return context_id
        return None

    def get_elements(self, context_id):
        try:
            with open(f"{context_id}.pickle", "rb") as f:
                data = pickle.load(f)
            return data
        except FileNotFoundError:
            print("Context file not found.")
            return {}

    def box1_clicked(self, event):
        self.process_vote(1)

    def box2_clicked(self, event):
        self.process_vote(2)

    def process_vote(self, box_number):
        age = getattr(self.controller, 'age', None)
        gender = getattr(self.controller, 'gender', None)
        if age and gender:
            print(f"Box {box_number} clicked with Age: {age}, Gender: {gender}")
            # Add your logic here
        else:
            tk.messagebox.showerror("Data Missing",
                                    "Age and Gender data are missing. Please enter them in the Rating page.")


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
        frame = self.frames[page_name]
        if page_name in ["Elements", "Voting"]:
            frame.refresh_contents()
        frame.tkraise()


if __name__ == "__main__":
    app = SinglePageApp()
    app.mainloop()
