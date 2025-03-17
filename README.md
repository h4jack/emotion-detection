# Face Recognition System with **Emotion Detection**

This is a Python-based Face Recognition System that uses DeepFace for emotion detection. It captures a live webcam feed, detects faces, and analyzes emotions such as happiness, sadness, anger, and others, displaying the results in a GUI built using Tkinter. The system also shows detailed information on dominant emotions and other detected emotions with their respective percentages.

## Features

- **Face Detection**: Uses OpenCV's pre-trained Haar Cascade for face detection.
- **Emotion Recognition**: Uses DeepFace library to analyze emotions (e.g., happy, sad, angry, etc.).
- **Live Video Feed**: Displays a live video feed from the webcam with detected faces highlighted.
- **Real-time Updates**: Continuously updates the detected emotion on the GUI in real-time.
- **Dynamic GUI**: Displays the main dominant emotion and the full emotion breakdown on a Tkinter window.

## Requirements

Before running the program, you need to install the following dependencies.

### Python 3.12.x

- `tkinter` (for creating the GUI)
- `opencv-python` (for handling video capture and face detection)
- `numpy` (for numerical operations)
- `Pillow` (for image processing in Tkinter)
- `deepface` (for emotion analysis using deep learning)

### Install dependencies using pip:

```bash
pip install opencv-python numpy Pillow deepface
```
##### OR
```bash
pip install -r requirements.txt
```
## Installation
1. Clone or download the repository:
   - Clone the repository using Git:
        ```bash
        git clone https://github.com/h4jack/emotion-detection.git
        ```
    - Or download the zip file and extract it.
2. Install the dependencies: Install the required Python libraries using pip as shown in the "Requirements" section.

## Usage
1. Run the script by executing:
    ```bash
    python ed.py
    ```
2. The program will open a window displaying a live webcam feed. Detected faces will be highlighted with rectangles, and the main emotion will be displayed at the top of the window. Additionally, all detected emotions with their percentages will be shown below.
3.  emotion labels will be updated in real-time as the face detection and emotion analysis continue.

## How it works
- The program opens the webcam and captures the video stream frame by frame.
- For each frame, it detects any faces using OpenCV's Haar Cascade Classifier.
- The DeepFace library is used to analyze emotions from the face in the frame.
- The program continuously updates the GUI, showing the main emotion and the percentage of each detected emotion (like happy, sad, angry, etc.).

## GUI Layout:
- **Main Emotion**: Displays the dominant emotion from the detected face in uppercase letters.
- **All Emotions**: Shows all the emotions detected, sorted by their percentage, with the values aligned for easy reading.

## Frame Resizing:
- The captured frame is resized to fit the Tkinter canvas, while maintaining the aspect ratio to avoid distortion of the image.
- If the canvas size is not valid yet (e.g., when the window is resizing), it uses a default size of 800x600 for the frame.

## Troubleshooting
- **No webcam detected**: Ensure your webcam is properly connected and not being used by any other application.
- **DeepFace errors**: If the DeepFace model fails, ensure you have the required models installed and the system is correctly set up. You can try using a different backend (like VGG-Face or Facenet) if needed.
- **GUI layout issues**: Ensure you have the required dependencies installed and that the Tkinter window is properly sized.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/h4jack/emotion-detection/putlicense) file for details.

## Acknowledgments
- **OpenCV**: For face detection using Haar cascades.
- **DeepFace**: For emotion detection and analysis.
- **Tkinter**: For creating the graphical user interface.
- **Pillow**: For image processing and handling in Tkinter.
> If you have any questions or suggestions, feel free to open an issue or contribute to the project!


### Explanation of Sections:

- **Project Title and Description**: Provides an overview of what the project does.
- **Features**: Describes the main functionality of the program.
- **Requirements**: Lists the necessary libraries and dependencies for the project.
- **Installation**: Step-by-step instructions for setting up the project locally.
- **Usage**: Explains how to run the program and what the user can expect.
- **How it Works**: A breakdown of the program's core functionality and behavior.
- **Troubleshooting**: Addresses potential issues users might encounter and solutions.
- **License**: Information about licensing for the project (if applicable).
- **Acknowledgments**: Credits any libraries or tools used in the project.

This `README.md` file gives users all the necessary information to set up, run, and troubleshoot your face recognition and emotion detection system.
