# Quality Control Viewer for iPSCI Rating

## Overview

The Quality Control Viewer for iPSCI Rating is a graphical user interface (GUI) application designed to facilitate quality control of pavement images. This tool allows users to load images and their corresponding ratings from a CSV file, view the images, and update their ratings as necessary. The tool provides buttons to navigate through the images and assign a rating from 1 to 10.

This application is built using Python and the PyQt5 library to provide a simple and effective interface for pavement image quality assessment.

## Features
- **Load Images:** Allows the user to select a folder containing images to be reviewed.
- **Load CSV:** Allows the user to select a CSV file containing image ratings and confidence values.
- **Image Rating Buttons:** Provides 10 rating buttons, color-coded, to rate the current image from 1 to 10.
- **Navigation:** Allows navigation between images using "Next" and "Previous" buttons.
- **Display Ratings and Confidence:** Displays the current rating and confidence percentage for each image.

## Requirements
- Python 3.x
- PyQt5
- Pandas

## Installation

1. **Create a virtual environment (optional but recommended)**
   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

2. **Install dependencies**
   ```sh
   pip install PyQt5 pandas
   ```

3. **Clone the repository**
   ```sh
   git clone <repository-url>
   cd <repository-folder>
   ```

4. **Run the application**
   ```sh
   python pavement_rating_app.py
   ```

## Usage

1. **Load Images:** Click the "Load Images" button to select a folder containing images that need to be reviewed. The supported image formats are `.jpg`, `.jpeg`, and `.png`.

2. **Load CSV File:** Click the "Load CSV" button to load a CSV file containing information about the images. The CSV file must contain the following columns: `Image Name`, `Prediction 1`, `Probability 1`.

3. **Rate Images:** Use the rating buttons (1-10) to rate the image. The buttons are color-coded as follows:
   - **Red (1-4):** Poor condition
   - **Orange (5-6):** Moderate condition
   - **Blue (7-8):** Good condition
   - **Green (9-10):** Excellent condition

4. **Navigate Images:** Use the "Next" and "Previous" buttons to move between images.

5. **Task Completion:** When all images have been analyzed, a completion message will be displayed.

## Code Structure

- **PavementRatingApp Class**: Main class for the application. It provides methods to load images, load CSV data, navigate images, rate images, and display them.
  - **initUI()**: Initializes the UI components, layouts, and buttons.
  - **loadImages()**: Opens a file dialog to select an image folder and loads valid image files.
  - **loadCSV()**: Opens a file dialog to select a CSV file and loads the ratings for the images.
  - **nextImage()**: Navigates to the next image.
  - **prevImage()**: Navigates to the previous image.
  - **rateImage()**: Updates the rating for the current image and moves to the next one.
  - **displayImage()**: Displays the current image along with its rating and confidence.
  - **getButtonStyle()**: Provides the style for rating buttons based on the rating value.

## CSV File Format
The CSV file must contain the following columns:
- **Image Name**: The filename of the image.
- **Prediction 1**: The initial rating prediction for the image.
- **Probability 1**: The confidence percentage of the rating.

Example CSV:
```
Image Name,Prediction 1,Probability 1
image1.jpg,7,0.85
image2.jpg,4,0.65
image3.jpg,9,0.95
```

## Notes
- The program requires images and CSV data to be in the correct format.
- If the CSV file does not contain the expected columns, an error will be shown.
- Only images present in both the CSV and the loaded folder will be shown in the viewer.

## License
This project is licensed under the MIT License.

## Author
- **Waqar Shahid Qureshi** - [Pavement Management Systems (PMS)](https://pms.ie)

## Acknowledgements
- **PyQt5** for GUI development.
- **Pandas** for CSV handling.

