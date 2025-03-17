import tkinter as tk
from tkinter import Canvas
import cv2
import numpy as np
from PIL import Image, ImageTk
from deepface import DeepFace

# Initialize the face detection model (OpenCV pre-trained Haar cascades or DNN model)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Create a Tkinter window
root = tk.Tk()
root.title("Emotion Detection")
root.geometry("800x600")  # Start with a window size of 800x600

# Create a canvas to display the video feed
canvas = Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)

# Create a label for displaying face details (Emotion, Gender, Age, Race)
d_label_main = tk.Label(root, 
                        text="Main Emotion", 
                        font=('Arial', 18), 
                        bg='#d3d3d3', 
                        fg='#203040', 
                        anchor="center",  # Center the text both horizontally and vertically
                        bd=2,  # Set border width
                        highlightbackground="blue",  # Set border color
                        highlightthickness=2)  # Set thickness of the border
d_label_main.place(x=20, y=50, width=200, height=50)

d_label_all = tk.Label(root, 
                       text="All Emotions",
                       font=('Arial', 15), 
                       bg='#d3d3d3', 
                       fg='#203040', 
                       anchor="nw", 
                       justify="left",
                       bd=2,  # Set border width
                       highlightbackground="green",  # Set border color
                       highlightthickness=2)  # Set thickness of the border
d_label_all.place(x=20, y=110, width=200, height=200)

# Open the webcam
cap = cv2.VideoCapture(0)

# 16:9 Aspect Ratio
ASPECT_RATIO = 16 / 9

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

def update_details(main_emotion, emotion_data):
    """Update the details label with the given information including emotion percentages and main emotion."""

    # Update the main emotion label with uppercase text
    d_label_main.config(text=main_emotion.upper(), font=('Arial', 20), bg='#d3d3d3', fg='#203040')

    # Prepare the sorted emotion data with percentages
    sorted_emotions = sorted(emotion_data.items(), key=lambda x: x[1], reverse=True)

    # Format the emotions and percentages for display
    emotions_text = "All Emotions\n"
    for emotion, percentage in sorted_emotions:
        # Format each emotion and percentage with a tab for alignment
        emotions_text += f"{emotion.capitalize()}\t{percentage:.2f}%\n"

    # Update the second label with all emotions
    d_label_all.config(text=emotions_text)

def update_frame():
    """Fetches a frame from the webcam and updates the Tkinter canvas"""
    ret, frame = cap.read()
    if not ret:
        return   # If frame reading fails, return early
    
    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    # Draw rectangles around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
    try:
        # Use a faster backend like 'VGG-Face' or 'Facenet'
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotions = analysis[0]['emotion']
        d_emotion = analysis[0]['dominant_emotion']
        print(f"\rEmotion : {d_emotion}         ", end='', flush=True)

        # Get the face region from the analysis
        dominant_face_region = analysis[0]['region']
        x, y, w, h = dominant_face_region['x'], dominant_face_region['y'], dominant_face_region['w'], dominant_face_region['h']
        
        # Draw a rectangle around the dominant face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green rectangle for dominant face
    except Exception as e:
        print(f"❌ DeepFace Error: {e}")
        emotions = "Natural"

    # Update the details next to the face box
    update_details(d_emotion, emotions)

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

    # Update the frame every 10 ms
    canvas.after(10, update_frame)

print() # Print new line to the console.
# Start the video feed after a short delay to ensure canvas size is available
root.after(100, update_frame)

# Run the Tkinter main loop
root.mainloop()
