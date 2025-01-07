import tkinter as tk
from tkinter import Button, Label, Toplevel, messagebox, Scrollbar, Listbox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import pygame


class TheMealApp:
    # initialize the pygame mixer for button sound
    pygame.mixer.init()

    def play_click_sound(self):
        # play button sound
        pygame.mixer.music.load('buttons.mp3')
        pygame.mixer.music.play()

    def __init__(self, root):
        # initializing main window
        self.root = root
        self.root.title("TheMeal")

        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # setting up background image
        self.bg_image = Image.open("background.jpeg")
        self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(self.root, image=self.bg_image_tk)
        self.bg_label.place(relwidth=1, relheight=1)

        # adding application heading
        self.heading = tk.Label(self.root, text="TheMeal", font=("Arial", 50, "bold"), fg="gold", bg="black")
        self.heading.place(relx=0.5, rely=0.3, anchor="center")

        # first button of the app to start things.
        self.login_button = Button(self.root, text="Login", font=("Arial", 20), fg="gold", bg="black",
                                   command=self.show_second_frame, bd=2)

        self.login_button.place(relx=0.5, rely=0.5, anchor="center")
        self.play_click_sound()

    def show_second_frame(self):
        # in order to navigate to second frame
        for widget in self.root.winfo_children():
            widget.destroy()

        self.play_click_sound()

        self.bg_label = tk.Label(self.root, image=self.bg_image_tk)
        self.bg_label.place(relwidth=1, relheight=1)

        # displaying second frames options as buttons
        Button(self.root, text="Let's Cook", font=("Arial", 20), fg="gold", bg="black", bd=2,
               command=self.show_lets_cook_frame).place(relx=0.5, rely=0.3, anchor="center")
        Button(self.root, text="Instructions", font=("Arial", 20), fg="gold", bg="black", bd=2,
               command=self.show_instructions_frame).place(relx=0.5, rely=0.45, anchor="center")
        Button(self.root, text="Feedback", font=("Arial", 20), fg="gold", bg="black", bd=2,
               command=self.show_feedback_frame).place(relx=0.5, rely=0.6, anchor="center")

    def show_lets_cook_frame(self):
        # navigating to lets cook frame, allowing user to explore meals

        for widget in self.root.winfo_children():
            widget.destroy()

            self.play_click_sound()

        self.bg_label = tk.Label(self.root, image=self.bg_image_tk)
        self.bg_label.place(relwidth=1, relheight=1)

        # options available for users to choose their meals and recipes
        Button(self.root, text="All Categories", font=("Arial", 20), fg="gold", bg="black", bd=2,
               command=self.show_all_categories).place(relx=0.5, rely=0.3, anchor="center")
        Button(self.root, text="Random Meal", font=("Arial", 20), fg="gold", bg="black", bd=2,
               command=self.show_random_meal).place(relx=0.5, rely=0.45, anchor="center")
        Button(self.root, text="Search Meal", font=("Arial", 20), fg="gold", bg="black", bd=2,
               command=self.show_search_meal_frame).place(relx=0.5, rely=0.6, anchor="center")
        Button(self.root, text="Back to Menu", font=("Arial", 20), fg="gold", bg="black", bd=2,
               command=self.show_second_frame).place(relx=0.5, rely=0.75, anchor="center")

    def show_all_categories(self):
        # creating a category to display all the present meals in the application

        for widget in self.root.winfo_children():
            widget.destroy()

            self.play_click_sound()

        # fetch and display all meal from an API
        response = requests.get("https://www.themealdb.com/api/json/v1/1/categories.php")
        categories = response.json().get("categories", [])

        self.bg_label = tk.Label(self.root, image=self.bg_image_tk)
        self.bg_label.place(relwidth=1, relheight=1)

        Label(self.root, text="Meal Categories", font=("Arial", 30, "bold"), fg="gold", bg="black").pack(pady=20)

        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        canvas = tk.Canvas(frame, bg="black")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adding scrollbar, so all the content is visible on screen.
        scrollbar = Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))

        listbox_frame = tk.Frame(canvas, bg="black")
        canvas.create_window((0, 0), window=listbox_frame, anchor="nw")

        category_listbox = Listbox(listbox_frame, font=("Arial", 15), bg="black", fg="gold", selectbackground="gold",
                                   height=15)
        category_listbox.pack(fill=tk.BOTH, expand=True)

        for category in categories:
            category_listbox.insert(tk.END, category["strCategory"])

        def on_category_select(event):
            selected_category = category_listbox.get(category_listbox.curselection())
            self.show_meals_in_category(selected_category)

            self.play_click_sound()

        category_listbox.bind("<<ListboxSelect>>", on_category_select)

        Button(self.root, text="Back to Menu", font=("Arial", 20), fg="gold", bg="black", bd=2,
               command=self.show_lets_cook_frame).pack(pady=20)

    def show_meals_in_category(self, category_name):
        # Code to fetch meal from a chosen category, from an API

        for widget in self.root.winfo_children():
            widget.destroy()

            self.play_click_sound()

        response = requests.get(f"https://www.themealdb.com/api/json/v1/1/filter.php?c={category_name}")
        meals = response.json().get("meals", [])

        self.bg_label = tk.Label(self.root, image=self.bg_image_tk)
        self.bg_label.place(relwidth=1, relheight=1)

        Label(self.root, text=f"Meals in {category_name}", font=("Arial", 30, "bold"), fg="gold", bg="black").pack(
            pady=20)

        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        canvas = tk.Canvas(frame, bg="black")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))

        listbox_frame = tk.Frame(canvas, bg="black")
        canvas.create_window((0, 0), window=listbox_frame, anchor="nw")

        category_listbox = Listbox(listbox_frame, font=("Arial", 15), bg="black", fg="gold", selectbackground="gold",
                                   height=15)
        category_listbox.pack(fill=tk.BOTH, expand=True)

        for meal in meals:
            category_listbox.insert(tk.END, meal["strMeal"])

        def on_meal_select(event):
            selected_meal = category_listbox.get(category_listbox.curselection())
            self.show_meal_details(selected_meal)

        category_listbox.bind("<<ListboxSelect>>", on_meal_select)

        Button(self.root, text="Back to Categories", font=("Arial", 20), fg="gold", bg="black", bd=2,
               command=self.show_all_categories).pack(pady=20)

    def show_meal_details(self, meal_name):
        # code to display all the details of the meal, which include recipe images and description.

        response = requests.get(f"https://www.themealdb.com/api/json/v1/1/search.php?s={meal_name}")
        meal = response.json().get("meals", [])[0]

        self.play_click_sound()

        meal_window = Toplevel(self.root)
        meal_window.geometry("800x600")
        meal_window.title(meal_name)

        canvas = tk.Canvas(meal_window, bg="black", highlightthickness=0)
        scrollbar = Scrollbar(meal_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="black")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        content_frame = tk.Frame(scrollable_frame, bg="black")
        content_frame.pack(pady=20, padx=20, expand=True)

        Label(content_frame, text=meal["strMeal"], font=("Arial", 30, "bold"), fg="gold", bg="black").pack(pady=10)
        Label(content_frame, text=f"Category: {meal['strCategory']}", font=("Arial", 20), fg="gold", bg="black").pack(
            pady=10)
        Label(content_frame, text=f"Area: {meal['strArea']}", font=("Arial", 20), fg="gold", bg="black").pack(pady=10)
        Label(content_frame, text=f"Recipe:\n{meal['strInstructions']}", font=("Arial", 15), fg="gold", bg="black",
              wraplength=600, justify="left").pack(pady=10)

        img_response = requests.get(meal["strMealThumb"])
        img_data = Image.open(BytesIO(img_response.content))
        img_data = img_data.resize((200, 200))
        img = ImageTk.PhotoImage(img_data)
        img_label = Label(content_frame, image=img, bg="black")
        img_label.image = img
        img_label.pack(pady=10)

        Button(content_frame, text="Close", font=("Arial", 20), fg="gold", bg="black", bd=2,
               command=meal_window.destroy).pack(pady=20)

    def show_random_meal(self):
        # Fetches  a random meal from the API
        response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php")
        meal = response.json().get("meals", [])[0]

        self.play_click_sound()

        # Creating a Toplevel window for displaying the random meal
        random_meal_window = Toplevel(self.root)
        random_meal_window.geometry("800x600")
        random_meal_window.title("Random Meal")

        # Add canvas and scrollbar for more user-friendly scrollable interface
        canvas = tk.Canvas(random_meal_window, bg="black", highlightthickness=0)
        scrollbar = Scrollbar(random_meal_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="black")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        content_frame = tk.Frame(scrollable_frame, bg="black")
        content_frame.pack(pady=20, padx=20, expand=True)

        # adding meal details
        Label(content_frame, text=meal["strMeal"], font=("Arial", 30, "bold"), fg="gold", bg="black").pack(pady=10)
        Label(content_frame, text=f"Category: {meal['strCategory']}", font=("Arial", 20), fg="gold", bg="black").pack(
            pady=10)
        Label(content_frame, text=f"Area: {meal['strArea']}", font=("Arial", 20), fg="gold", bg="black").pack(pady=10)
        Label(content_frame, text=f"Recipe:\n{meal['strInstructions']}", font=("Arial", 15), fg="gold", bg="black",
              wraplength=600, justify="left").pack(pady=10)

        # fetching images of meal from an API
        img_response = requests.get(meal["strMealThumb"])
        img_data = Image.open(BytesIO(img_response.content))
        img_data = img_data.resize((200, 200))
        img = ImageTk.PhotoImage(img_data)
        img_label = Label(content_frame, image=img, bg="black")
        img_label.image = img
        img_label.pack(pady=10)

        Button(content_frame, text="Close", font=("Arial", 20), fg="gold", bg="black", bd=2,
               command=random_meal_window.destroy).pack(pady=20)

    def show_search_meal_frame(self):
        # code used to search a meal by name.

        for widget in self.root.winfo_children():
            widget.destroy()

        self.play_click_sound()

        search_window = Toplevel(self.root)
        search_window.geometry("800x600")
        search_window.title("Search Meal")

        canvas = tk.Canvas(search_window, bg="black", highlightthickness=0)
        scrollbar = Scrollbar(search_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="black")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        content_frame = tk.Frame(scrollable_frame, bg="black")
        content_frame.pack(pady=20, padx=20, expand=True)

        Label(content_frame, text="Search for a Meal", font=("Arial", 25, "bold"), fg="gold", bg="black").pack(pady=10)
        search_entry = tk.Entry(content_frame, font=("Arial", 15), width=30, bg="black", fg="gold")
        search_entry.pack(pady=10)

        def search_meals():
            query = search_entry.get().strip()

            self.play_click_sound()

            if query:

                response = requests.get(f"https://www.themealdb.com/api/json/v1/1/search.php?s={query}")
                meals = response.json().get("meals", [])

                for widget in result_frame.winfo_children():
                    widget.destroy()

                if meals:
                    for meal in meals:
                        meal_button = Button(result_frame, text=meal["strMeal"], font=("Arial", 18), fg="gold",
                                             bg="black", width=25,
                                             command=lambda meal_name=meal["strMeal"]: self.show_meal_details(
                                                 meal_name))
                        meal_button.pack(pady=10)

                else:
                    Label(result_frame, text="No meals found. Please try another search.", font=("Arial", 18),
                          fg="gold", bg="black").pack(pady=20)

        search_button = Button(content_frame, text="Search", font=("Arial", 20), fg="gold", bg="black",
                               command=search_meals)
        search_button.pack(pady=20)

        result_frame = tk.Frame(scrollable_frame, bg="black")
        result_frame.pack(pady=20)

        Button(content_frame, text="Back", font=("Arial", 20), fg="gold", bg="black",
               command=self.show_lets_cook_frame).pack(pady=20)

    def show_instructions_frame(self):
        # this code shows instructions on screen on telling user how to use the application

        for widget in self.root.winfo_children():
            widget.destroy()

        self.play_click_sound()

        self.bg_label = tk.Label(self.root, image=self.bg_image_tk)
        self.bg_label.place(relwidth=1, relheight=1)

        instructions = (
            "Welcome to TheMeal App!\n\n"
            "- Use 'Let's Cook' to explore various meals and categories.\n"
            "- Select a category to view meals within that category.\n"
            "- Click on a meal to get more details, including the recipe and image.\n"
            "- Use the 'Random Meal' feature to discover a random meal.\n"
            "- Search for a meal by name using the 'Search Meal' feature.\n"
            "- You can also provide feedback using the 'Feedback' button.\n\n"
            "Enjoy discovering new meals and recipes!")
        Label(self.root, text=instructions, font=("Arial", 14), fg="gold", bg="black", justify="center",
              wraplength=600).place(relx=0.5, rely=0.4, anchor="center")
        Button(self.root, text="Back to Menu", font=("Arial", 20), fg="gold", bg="black", bd=2,
               command=self.show_second_frame).place(relx=0.5, rely=0.75, anchor="center")

    def show_feedback_frame(self):
        # allows user to give feedback about the app

        feedback_window = Toplevel(self.root)
        feedback_window.geometry("400x300")
        feedback_window.title("Feedback")

        self.play_click_sound()

        bg_label = tk.Label(feedback_window, image=self.bg_image_tk)
        bg_label.place(relwidth=1, relheight=1)

        Label(feedback_window, text="Your Feedback:", font=("Arial", 20), fg="gold", bg="black").pack(pady=20)
        feedback_entry = tk.Entry(feedback_window, font=("Arial", 15), width=30)
        feedback_entry.pack(pady=10)

        def submit_feedback():
            feedback = feedback_entry.get()
            if feedback.strip():
                messagebox.showinfo("Thank You", "Thank you for your feedback!")
                feedback_window.destroy()

        self.play_click_sound()

        Button(feedback_window, text="Submit", font=("Arial", 20), fg="gold", bg="black", bd=2,
               command=submit_feedback).pack(pady=20)


# initialize and run the app.
root = tk.Tk()
app = TheMealApp(root)
root.mainloop()
