import tkinter as tk
from tkinter import Canvas, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
from deepface import DeepFace
import random
import json

# Create a Tkinter window
root = tk.Tk()
root.title("Expression Detection")
root.geometry("800x600")  # Start with a window size of 800x600

# Create a canvas to display the video feed
canvas = Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)

# Create a label for displaying face details (Expression, Gender, Age, Race)
d_label_main = tk.Label(root, 
                        text="Main Expression",
                        font=('Arial', 18),
                        bg='#d3d3d3',
                        fg='#203040',
                        anchor="center",  # Center the text both horizontally and vertically
                        bd=2,  # Set border width
                        highlightbackground="blue",  # Set border color
                        highlightthickness=2)  # Set thickness of the border
d_label_main.place(x=20, y=50, width=200, height=50)

d_label_all = tk.Label(root, 
                        text="All Expressions",
                        font=('Arial', 15), 
                        bg='#d3d3d3', 
                        fg='#203040', 
                        anchor="nw", 
                        justify="left",
                        bd=2,  # Set border width
                        highlightbackground="green",  # Set border color
                        highlightthickness=2)  # Set thickness of the border
d_label_all.place(x=20, y=110, width=200, height=200)

# Input field and button to get user name
name_label = tk.Label(root,
                    text="Enter your name:",
                    font=('Arial', 14))
name_label.place(x=250, y=50)

name_entry = tk.Entry(root,
                    font=('Arial', 14))
name_entry.place(x=250, y=90)

# Button to start the game
start_button = tk.Button(root,
                    text="Start",
                    font=('Arial', 14),
                    command=lambda: start_game())
start_button.place(x=250, y=130)

# Button to stop the game and record the score
stop_button = tk.Button(root,
                    text="Stop",
                    font=('Arial', 14),
                    command=lambda: stop_game(),
                    state=tk.DISABLED)
stop_button.place(x=260, y=130)

# Leaderboard label and list
lboard_label = tk.Label(root,
                    text="Leaderboard",
                    font=('Arial', 16, 'bold'))
lboard_label.place(x=500, y=50)

lboard_list = tk.Listbox(root,
                    font=('Arial', 12),
                    height=10, width=30)
lboard_list.place(x=500, y=90)

# Expression mapping and user info
user_score = 0
current_expression = None
game_started = False
lboard = []

# Open the webcam
cap = cv2.VideoCapture(0)

# 16:9 Aspect Ratio
ASPECT_RATIO = 16 / 9

# File to store leaderboard data
LEADERBOARD_FILE = "leaderboard.json"

import json

def save_leaderboard():
    """Save the leaderboard to the JSON file."""
    # Convert any NumPy data types to native Python types
    for i in range(len(lboard)):
        name, expression, score = lboard[i]
        lboard[i] = (name, expression, float(score))  # Convert score to float
    
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(lboard, f, indent=4)

def load_leaderboard():
    """Load the leaderboard from the JSON file."""
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            leaderboard = json.load(f)
            # Convert any NumPy data types to native Python types when loading
            for i in range(len(leaderboard)):
                name, expression, score = leaderboard[i]
                leaderboard[i] = (name, expression, float(score))  # Convert score to float
            return leaderboard
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is corrupted, return an empty leaderboard
        return []

def show_leaderboard():
    """Load the leaderboard from the JSON file and display it on the GUI."""
    global lboard
    # Load the leaderboard from the file
    lboard = load_leaderboard()

    # Clear the current leaderboard list in the listbox
    lboard_list.delete(0, tk.END)

    # Display the top 10 leaderboard entries
    for i, (name, expression, score) in enumerate(lboard[:10]):
        lboard_list.insert(tk.END, f"{i+1}. {name} - {expression} - {score:.2f}%")

def resize_frame(frame, max_width, max_height):
    """Resize the frame to fit the window's width and height while maintaining aspect ratio."""
    frame_height, frame_width = frame.shape[:2]
    frame_aspect_ratio = frame_width / frame_height

    # Determine the limiting factor (width or height) based on the aspect ratio
    if frame_aspect_ratio > ASPECT_RATIO:
        # Width is the limiting factor
        new_width = max_width
        new_height = int(new_width / frame_aspect_ratio)
    else:
        # Height is the limiting factor
        new_height = max_height
        new_width = int(new_height * frame_aspect_ratio)
    
    # Resize the frame to fit within the max dimensions
    return cv2.resize(frame, (new_width, new_height))

def update_details(main_expression, expression_data):
    """Update the details label with the given information including Expression percentages and main Expression."""
    # Update the main Expression label with uppercase text
    global game_started, user_score, current_expression
    d_label_main.config(text=main_expression.upper(), font=('Arial', 20), bg='#d3d3d3', fg='#203040')

    # Prepare the sorted Expression data with percentages
    sorted_expressions = sorted(expression_data.items(), key=lambda x: x[1], reverse=True)

    if(game_started):
        score = (expression_data[current_expression])
        user_score = max(score, user_score)
        # it is for setting cap on the score of leaderboard.
        # if(user_score > 70):
        #     user_score = user_score - 30 + ((random.random()*20)-2);
        
    # Format the Expressions and percentages for display
    expressions_text = "All Expressions\n"
    for expression, percentage in sorted_expressions:
        # Format each Expression and percentage with a tab for alignment
        expressions_text += f"{expression.capitalize()}\t{percentage:.2f}%\n"

    # Update the second label with all Expressions
    d_label_all.config(text=expressions_text)

def update_leaderboard_position():
    """Update the leaderboard label position once the window is rendered."""
    window_width = root.winfo_width()  # Get the width of the window after it's rendered
    window_height = root.winfo_height()  # Get the height of the window after it's rendered
    label_width = lboard_label.winfo_reqwidth()  # Get the width of the label
    list_width = lboard_list.winfo_reqwidth()  # Get the width of the listbox

    # Position the leaderboard label 50 pixels from the right side
    lboard_label.place(x=window_width - 20 - label_width, y=20)

    # Position the leaderboard list 50 pixels from the right side
    lboard_list.place(x=window_width - 20 - list_width, y=60)

    # Position the start and stop buttons from the bottom and right
    st_btn_width = start_button.winfo_reqwidth()
    sp_btn_width = stop_button.winfo_reqwidth()

    # Calculate vertical position from the bottom
    bottom_margin = 20  # Adjust this to change the distance from the bottom edge
    y_position = window_height - bottom_margin - max(st_btn_width, sp_btn_width)  # Ensure buttons don't overlap

    name_l_width = name_label.winfo_reqwidth()
    name_e_width = name_entry.winfo_reqwidth()

    # Position the input label (name_label) and entry field (name_entry)
    # Place the input fields just above the buttons
    input_margin = 10  # Adjust this to change the distance between the buttons and the input fields
    input_y_position = y_position - input_margin - 60  # Adjust to place the input field just above the buttons

    name_label.place(x=window_width - 20 - name_e_width, y=input_y_position)
    name_entry.place(x=window_width - 20 - name_e_width, y=input_y_position + 40)  # Adjust Y for entry

    # Position the start button
    start_button.place(x=window_width - 20 - name_e_width, y=y_position)

    # Position the stop button next to the start button, maintaining right alignment
    stop_button.place(x=(window_width - 20 - name_e_width) + st_btn_width + 20, y=y_position)

def update_frame():
    """Fetches a frame from the webcam and updates the Tkinter canvas"""
    ret, frame = cap.read()
    if not ret:
        return   # If frame reading fails, return early
    
    try:
        # Use a faster backend like 'VGG-Face' or 'Facenet'
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        expressions = analysis[0]['emotion']
        d_expression = analysis[0]['dominant_emotion']
        print(f"\rExpression : {d_expression}         ", end='', flush=True)

        # Get the face region from the analysis
        dominant_face_region = analysis[0]['region']
        x, y, w, h = dominant_face_region['x'], dominant_face_region['y'], dominant_face_region['w'], dominant_face_region['h']
        
        # Draw a rectangle around the dominant face (Green)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green rectangle for dominant face
    except Exception as e:
        print(f"❌ DeepFace Error: {e}")
        expressions = "Natural"

    # Update the details next to the face box
    update_details(d_expression, expressions)

    # Ensure canvas dimensions are available and valid
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    
    # Wait for canvas size to be valid before resizing the frame
    if canvas_width > 0 and canvas_height > 0:
        # Resize the frame to fit the canvas while maintaining aspect ratio
        frame_resized = resize_frame(frame, canvas_width, canvas_height)
    else:
        # Use default size if canvas size is invalid or zero
        frame_resized = cv2.resize(frame, (800, 600))
    
    # Convert the frame to RGB (Tkinter needs RGB format)
    frame_resized = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    
    # Convert the frame to a format Tkinter can display
    img = Image.fromarray(frame_resized)
    imgtk = ImageTk.PhotoImage(image=img)
    
    # Calculate the position to center the image
    x_offset = (canvas_width - frame_resized.shape[1]) // 2
    y_offset = (canvas_height - frame_resized.shape[0]) // 2
    
    # Update the canvas with the resized and centered image
    canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=imgtk)
    canvas.imgtk = imgtk  # Keep a reference to avoid garbage collection

    # Update the position of the leaderboard lebel. so it will align to the left.
    update_leaderboard_position()
    
    # Update the frame every 10 ms
    canvas.after(10, update_frame)

def start_game():
    """Start the game by taking the user's name and randomly selecting an Expression."""
    global current_expression, game_started
    user_name = name_entry.get()
    if user_name == "":
        messagebox.showwarning("Input Error", "Please enter your name.")
        return

    # Randomly choose an Expression from the list
    expressions_list = ["angry", "happy", "sad", "surprise"]
    current_expression = random.choice(expressions_list)

    game_started = True
    name_label.config(text=f"Do the {current_expression} Face")

    # Disable the start button and enable the stop button
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

def stop_game():
    """Stop the game and calculate the user's score."""
    global user_score, current_expression, game_started

    if current_expression is None:
        messagebox.showwarning("Game Error", "No Expression has been chosen yet.")
        return

    game_started = False

    # Add the score to the Leaderboard
    lboard.append((name_entry.get(), current_expression, user_score))
    lboard.sort(key=lambda x: x[2], reverse=True)

    save_leaderboard()

    user_score = 0

    # Update the Leaderboard (show top 10 scores)
    lboard_list.delete(0, tk.END)
    for i, (name, expression, score) in enumerate(lboard[:10]):
        lboard_list.insert(tk.END, f"{i+1}. {name} - {expression} - {score:.2f}%")
    
    name_label.config(text=f"Enter Your Name:")

    # Disable the start button and enable the stop button
    stop_button.config(state=tk.DISABLED)
    start_button.config(state=tk.NORMAL)

print() # Print new line to the console.
show_leaderboard()
# Start the video feed after a short delay to ensure canvas size is available
root.after(100, update_frame)

# Run the Tkinter main loop
root.mainloop()

print("\nProgram Terminated...")
