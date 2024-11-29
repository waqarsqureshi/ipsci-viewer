import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QWidget,
    QMessageBox
)
from PyQt5.QtGui import QPixmap, QImage, QColor, QPalette
from PyQt5.QtCore import Qt

class PavementRatingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Initialize the User Interface.
        Sets up the window, layouts, buttons, and other UI components.
        """
        self.setWindowTitle("Quality Control Viewer for iPSCI Rating")
        self.resize(1000, 600)

        # Layouts and Widgets
        mainLayout = QHBoxLayout()  # Main layout to align buttons on the left side
        imageAndRatingLayout = QVBoxLayout()  # Layout for image and rating label
        topButtonLayout = QHBoxLayout()  # Layout for top buttons
        ratingButtonLayout = QVBoxLayout()  # Layout for rating buttons on the left side

        # PMS Logo
        self.logoLabel = QLabel()
        self.logoPixmap = QPixmap("pms.png")
        self.logoLabel.setPixmap(self.logoPixmap.scaled(150, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        topButtonLayout.addWidget(self.logoLabel)

        # Image and Rating Widgets
        self.imageLabel = QLabel("No Image Loaded")
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setFixedSize(720, 560)  # Set fixed size for image display
        self.ratingLabel = QLabel("Rating: 0, Confidence: 0%")
        self.ratingLabel.setAlignment(Qt.AlignCenter)
        self.ratingLabel.setStyleSheet("font-weight: bold; font-size: 30px;")

        # Buttons for navigation and loading
        self.loadImagesButton = QPushButton("Load Images")
        self.loadCSVButton = QPushButton("Load CSV")
        self.nextButton = QPushButton("Next")
        self.prevButton = QPushButton("Previous")

        # Adding buttons to the top button layout
        topButtonLayout.addWidget(self.loadImagesButton)
        topButtonLayout.addWidget(self.loadCSVButton)
        topButtonLayout.addWidget(self.prevButton)
        topButtonLayout.addWidget(self.nextButton)

        # Adding rating buttons to rating button layout
        self.ratingButtons = []
        for i in range(1, 11):
            button = QPushButton(str(i))
            button.setFixedSize(50, 50)
            button.setStyleSheet(self.getButtonStyle(i))
            button.clicked.connect(lambda _, rating=i: self.rateImage(rating))
            ratingButtonLayout.addWidget(button)
            self.ratingButtons.append(button)

        # Adding widgets to the image and rating layout
        imageAndRatingLayout.addLayout(topButtonLayout)
        imageAndRatingLayout.addWidget(self.imageLabel)
        imageAndRatingLayout.addWidget(self.ratingLabel)

        # Adding layouts to the main layout
        mainLayout.addLayout(ratingButtonLayout)
        mainLayout.addLayout(imageAndRatingLayout)

        self.setLayout(mainLayout)

        # Connecting buttons to functions
        self.nextButton.clicked.connect(self.nextImage)
        self.prevButton.clicked.connect(self.prevImage)
        self.loadImagesButton.clicked.connect(self.loadImages)
        self.loadCSVButton.clicked.connect(self.loadCSV)

        # Variables for images and ratings
        self.imagePaths = []
        self.imageRatings = []
        self.currentIndex = 0
        self.imagesFolder = ""
        self.csvFilePath = ""

    def loadImages(self):
        """
        Load images from a selected folder.
        Opens a file dialog to select a folder containing images and gathers all valid image files.
        """
        self.imagesFolder = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if self.imagesFolder:
            # Gather all image paths
            self.imagePaths = []
            for root, _, files in os.walk(self.imagesFolder):
                for file in files:
                    if file.lower().endswith((".jpg", ".jpeg", ".png")):
                        self.imagePaths.append(os.path.join(root, file))
            if self.imagePaths:
                self.currentIndex = 0
                self.displayImage()
                # Initialize image ratings with default value if not loaded from CSV
                self.imageRatings = [(5, 0.0)] * len(self.imagePaths)
            else:
                QMessageBox.warning(self, "Warning", "No images found in the selected folder.")

    def loadCSV(self):
        """
        Load image ratings from a CSV file.
        Opens a file dialog to select a CSV file containing image names, ratings, and confidence values.
        """
        self.csvFilePath = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")[0]
        if self.csvFilePath:
            try:
                self.df = pd.read_csv(self.csvFilePath)

                # Check for the expected columns
                if 'Image Name' not in self.df.columns or 'Prediction 1' not in self.df.columns or 'Probability 1' not in self.df.columns:
                    raise ValueError("CSV file does not contain the required columns 'Image Name', 'Prediction 1', and 'Probability 1'.")

                # Reset image paths and ratings
                self.imagePaths = []
                self.imageRatings = []
                self.imageNames = self.df['Image Name'].tolist()

                for image_name in self.imageNames:
                    # Search for the image in the provided folder and subfolders
                    found_image = False
                    for root, _, files in os.walk(self.imagesFolder):
                        if image_name in files:
                            image_path = os.path.join(root, image_name)
                            self.imagePaths.append(image_path)
                            rating = int(self.df.loc[self.df['Image Name'] == image_name, 'Prediction 1'].values[0])
                            confidence = float(self.df.loc[self.df['Image Name'] == image_name, 'Probability 1'].values[0])
                            self.imageRatings.append((rating, confidence))
                            found_image = True
                            break

                if self.imagePaths:
                    self.currentIndex = 0
                    self.displayImage()
                else:
                    QMessageBox.warning(self, "Warning", "No images from the CSV file could be found in the selected image folder.")

            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not load CSV file: {e}")

    def nextImage(self):
        """
        Display the next image in the sequence.
        Moves to the next image if available, or shows a completion message if at the end.
        """
        if self.imagePaths:
            if self.currentIndex < len(self.imagePaths) - 1:
                self.currentIndex += 1
                self.displayImage()
            else:
                QMessageBox.information(self, "Completed", "Task Completed. All images have been analyzed.")
        else:
            QMessageBox.warning(self, "Warning", "No images loaded to navigate.")

    def prevImage(self):
        """
        Display the previous image in the sequence.
        Moves to the previous image if available.
        """
        if self.currentIndex > 0:
            self.currentIndex -= 1
            self.displayImage()

    def rateImage(self, rating):
        """
        Rate the current image and move to the next one.
        Updates the rating of the current image and moves to the next image automatically.
        
        Parameters:
        - rating: The rating value assigned by the user (1-10).
        """
        if self.imagePaths:
            current_rating, confidence = self.imageRatings[self.currentIndex]
            self.imageRatings[self.currentIndex] = (rating, confidence)
            self.nextImage()

    def displayImage(self):
        """
        Display the current image along with its rating and confidence.
        Shows the image, sets the size, and updates the rating label with current values.
        """
        if self.imagePaths:
            image_path = self.imagePaths[self.currentIndex]
            image = QImage(image_path)
            if not image.isNull():
                # Display the image with specified size (720x560)
                self.imageLabel.setPixmap(QPixmap.fromImage(image).scaled(720, 560, Qt.KeepAspectRatio, Qt.SmoothTransformation))

                if self.currentIndex < len(self.imageRatings):
                    rating, confidence = self.imageRatings[self.currentIndex]
                    self.ratingLabel.setText(f"Rating: {rating}, Confidence: {confidence * 100:.1f}%")
            else:
                self.imageLabel.setText("Failed to load image.")

    def getButtonStyle(self, rating):
        """
        Get the style for the rating buttons.
        Returns a style string based on the rating value (color-coded).
        
        Parameters:
        - rating: The rating value (1-10).
        
        Returns:
        - A stylesheet string with appropriate color for the button.
        """
        if rating >= 9:
            color = "green"
        elif rating >= 7:
            color = "blue"
        elif rating >= 5:
            color = "orange"
        else:
            color = "red"

        return f"background-color: {color}; border-radius: 25px; font-size: 14px; color: white;"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PavementRatingApp()
    window.show()
    sys.exit(app.exec_())
