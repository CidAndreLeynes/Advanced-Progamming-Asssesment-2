import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
from io import BytesIO

class MealApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Meal Finder")
        self.root.geometry("600x700")
        self.root.config(bg="#ffffff")  # Light background color

        # Add a gradient background using a frame
        self.background = tk.Frame(self.root, bg="#6a11cb")  # Purple gradient color
        self.background.pack(fill="both", expand=True)
        
        # Create a content frame for better layout management
        self.content_frame = tk.Frame(self.background, bg="#ffffff", bd=10, relief="solid", padx=20, pady=20)
        self.content_frame.pack(expand=True, padx=30, pady=30)

        # Title Header
        self.header_label = tk.Label(self.content_frame, text="Meal of the Day", font=("Helvetica", 24, "bold"), bg="#ffffff", fg="#6a11cb")
        self.header_label.pack(pady=15)

        # Button to get a random meal
        self.get_meal_button = ttk.Button(self.content_frame, text="Get Random Meal", command=self.display_random_meal, 
                                           style="TButton")
        self.get_meal_button.pack(pady=20)

        # Label to display the meal name
        self.meal_name_label = tk.Label(self.content_frame, text="", font=("Helvetica", 18), bg="#ffffff", fg="#333333", wraplength=500)
        self.meal_name_label.pack()

        # Label to display the meal image
        self.meal_image_label = tk.Label(self.content_frame, bg="#ffffff")
        self.meal_image_label.pack(pady=20)

        # Style for the buttons (modern look)
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 14, "bold"), padding=10, relief="flat", background="#4CAF50", foreground="white")
        self.style.map("TButton", background=[("active", "#45a049"), ("pressed", "#388e3c")])  # Hover and pressed effect

    def display_random_meal(self):
        # Fetch a random meal from the API
        url = "https://www.themealdb.com/api/json/v1/1/random.php"
        response = requests.get(url)
        meal_data = response.json()

        # Extract the meal's name and image URL
        meal = meal_data['meals'][0]
        meal_name = meal['strMeal']
        meal_image_url = meal['strMealThumb']

        # Set the meal name label
        self.meal_name_label.config(text=meal_name)

        # Fetch and display the meal image
        img_response = requests.get(meal_image_url)
        img_data = img_response.content
        img = Image.open(BytesIO(img_data))

        # Resize image to fit in the window using Resampling.LANCZOS
        img = img.resize((400, 400), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        # Store a reference to the image to prevent garbage collection
        self.meal_image_label.config(image=img_tk)
        self.meal_image_label.image = img_tk  # Keep a reference to the image

# Set up the Tkinter window
root = tk.Tk()
app = MealApp(root)

# Run the application
root.mainloop()
