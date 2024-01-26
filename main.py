from image_backend.image_processing_main import VideoReader
from image_analysis.image_analysis_main import ImageAnalysisMain

import config
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2, sys
import numpy as np
import threading
import _thread

class DivingVisualTracker:
    def __init__(self, id:int=1):
        self.id = id
        
        #Other classes
        self.videoReading = VideoReader("")
        self.videoAnalysis = ImageAnalysisMain()

        self.currentframe = None
        #Display placeholers
        self.reference_frame = None
        self.shape_frame = None

        #Keep track of position in space
        self.current_shape_indexes = {
            "black": 0,
            "white": 0,
            "red": 0,
            "green": 0,
            "blue": 0,
            "light blue": 0,
            "cyan": 0,
            "aqua": 0,
            "pink": 0,
            "magenta": 0,
            "purple": 0,
            "light green": 0,
            "yellow": 0,
            "orange": 0}

        self.currentPicture = None
        self.index = {
            "black": np.array([0, 0, 0]),
            "white": np.array([255, 255, 255]),
            "red": np.array([0, 0, 255]),
            "green": np.array([0, 255, 0]),
            "blue": np.array([255, 0, 0]),
            "light blue": np.array([255, 157, 0]),
            "cyan": np.array([255, 255, 0]),
            "aqua": np.array([190, 255, 0]),
            "pink": np.array([255, 0, 190]),
            "magenta": np.array([255, 0, 255]),
            "purple": np.array([255, 0, 100]),
            "light green": np.array([0, 255, 150]),
            "yellow": np.array([0, 255, 255]),
            "orange": np.array([0, 165, 255])
        }

    def start_shape_detetion(self, first_frame: np.array) -> None:
        self.id = 1
        self.videoAnalysis.read_frame(first_frame)
        if 0 == self.videoAnalysis.start_RGB_shape_detection(False, [], 5, 5, 3):
            self.reference_frame = self.videoAnalysis.reference_frame
            self.shape_frame = self.videoAnalysis.all_colour_frames[1]
            return True
        else:
            return False



    def __str__(self) -> str:
        pass
    
    def process_video(self, path: str) -> list:
        print("Loading... Processing Video File...")
        self.frames = self.videoReading.read_all_video_frames_source
        self.frameCounter = 0
        print("Done")
        return self.frames
    
    def process_picture(self, path: str):
        i = self.videoReading.get_picture__feed_source(path)
        self.currentframe = i
        self.currentPicture = i

        self.current_shape_indexes = {
            "black": 0,
            "white": 0,
            "red": 0,
            "green": 0,
            "blue": 0,
            "light blue": 0,
            "cyan": 0,
            "aqua": 0,
            "pink": 0,
            "magenta": 0,
            "purple": 0,
            "light green": 0,
            "yellow": 0,
            "orange": 0}

        return i

    def __del__(self):
        print("Destroyed visual tracker")

    def select_colour(self, colour):
        if colour == "All Colors":
            self.reference_frame = self.videoAnalysis.reference_frame
            self.shape_frame = self.videoAnalysis.all_colour_frames[1]
        else:
            self.reference_frame = self.videoAnalysis.extract_colour_by_pixel(self.videoAnalysis.reference_frame, colour)
            if len(self.videoAnalysis.shape_dictionary[colour]) != 0:
                self.shape_frame = self.videoAnalysis.draw_specific_shape(colour, self.current_shape_indexes[colour])
            else:
                self.shape_frame = np.ones((len(self.reference_frame), len(self.reference_frame[0]), 3), np.uint8, 'C')


    def update_shape(self, current_colour):
        self.shape_frame = self.videoAnalysis.draw_specific_shape(current_colour, self.current_shape_indexes[current_colour])

        

class SportsApp(QWidget):
    selected_color = "All Colors"  # Class variable to store the selected color

    def __init__(self):
        super().__init__()

        self.divingBackend = DivingVisualTracker()
        self.tracked_shapes = []  # List to store the shapes to be tracked

        self.initUI()

    def initUI(self):
        # Create a tab widget
        tab_widget = QTabWidget(self)
        tab_widget.addTab(self.createTab1(), "Image Processing")  # Renamed the tab
        tab_widget.addTab(self.createTab2(), "Graph Tab")

        # Set up the main layout
        main_layout = QVBoxLayout(self)

        # Create a widget for shape-related buttons and labels
        shape_widget = self.createShapeWidget()

        # Add the tab widget
        main_layout.addWidget(tab_widget)
        main_layout.addWidget(shape_widget)
        self.setLayout(main_layout)

        # Set the background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        background_color = QColor(Qt.cyan).lighter(150)  # Mild opaque industrial cyan blue
        palette.setColor(self.backgroundRole(), background_color)
        self.setPalette(palette)

        # Set up the main window
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Sports Visualization App')
        self.show()

    def createTab1(self):
        widget = QWidget()

        self.button_open_file = QPushButton('Open File', self)
        self.textbox_file_path = QLineEdit(self)
        self.label_image1 = QLabel(self)
        self.label_image2 = QLabel(self)
        self.button_process_image = QPushButton('Process Image', self)

        self.color_selection_combo = QComboBox(self)  # Add a combo box for color selection


        # Add color names to the combo box
        self.color_selection_combo.addItems(["All Colors"] + list(self.divingBackend.index.keys()))

        image_widget = QWidget()
        layout_images = QHBoxLayout(image_widget)
        layout_images.addWidget(self.label_image1)  # Placeholder for loaded image
        layout_images.addWidget(self.label_image2)  # Placeholder for loaded images
        
        

        # Connect button click events to functions
        self.button_open_file.clicked.connect(self.openFile)
        self.button_process_image.clicked.connect(self.processImage)

        self.color_selection_combo.currentIndexChanged.connect(self.colorSelected)

        # Initially hide the buttons and combo box
        self.button_process_image.hide()
        self.color_selection_combo.hide()

        # Set up the layout for the first tab
        layout_tab1 = QVBoxLayout(widget)
        layout_tab1.addWidget(self.button_open_file)
        layout_tab1.addWidget(self.textbox_file_path)
        layout_tab1.addWidget(image_widget)

        layout_tab1.addWidget(self.button_process_image)
        layout_tab1.addWidget(self.color_selection_combo)  # Add the color selection combo box

        layout_tab1.addStretch(1)

        return widget

    def createTab2(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        # Add your graph-related widgets or components here
        # For example, you might use Matplotlib or another plotting library
        layout.addWidget(QLabel("Graph Tab Content"))
        layout.addStretch(1)
        return widget


    def createShapeWidget(self):
        # Create a widget for shape-related buttons and labels
        shape_widget = QWidget()

        # Instantiate the new buttons here
        self.button_up = QPushButton('Up', self)
        self.button_down = QPushButton('Down', self)
        self.button_add_shape = QPushButton('Add Shape', self)
        self.button_remove_shape = QPushButton('Remove Shape', self)

        # Initialize label_shape_counter as a QLabel
        self.label_shape_counter = QLabel('Shape ID: 0', self)

        shape_layout = QVBoxLayout(shape_widget)
        shape_layout.addWidget(self.label_shape_counter)
        shape_layout.addWidget(self.button_up)
        shape_layout.addWidget(self.button_down)
        shape_layout.addWidget(self.button_add_shape)
        shape_layout.addWidget(self.button_remove_shape)

        

        self.button_down.clicked.connect(self.showNextShape)
        self.button_up.clicked.connect(self.showPreviousShape)
        self.button_add_shape.clicked.connect(self.addShape)
        self.button_remove_shape.clicked.connect(self.removeShape)

        # Initially hide the new shape-related buttons and labels
        self.button_up.hide()
        self.button_down.hide()
        self.label_shape_counter.hide()
        self.button_add_shape.hide()
        self.button_remove_shape.hide()

        return shape_widget


    def addShape(self):
        # ... (unchanged)
        pass

    def removeShape(self):
        # ... (unchanged)
        pass

    def updateShapeCounterLabel(self):
        if len(self.divingBackend.videoAnalysis.shape_dictionary[self.selected_color]) > 0:
            self.label_shape_counter.setText(f'Shape ID: {self.divingBackend.current_shape_indexes[self.selected_color]}')
        else:
            self.label_shape_counter.setText('No Shapes')

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        # Open a file dialog and get the selected file path
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Video or Image File", "", "All Files (*)", options=options)

        if file_path:
            # Display the file path in the text box
            self.textbox_file_path.setText(file_path)

            # Check if the file is an image and display it
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                
                self.showImages(self.divingBackend.process_picture(file_path), None)

                # Show the buttons and combo box after an image is loaded
                self.button_process_image.show()
                self.button_process_image.setEnabled(True)

            else:
                self.label_image1.clear()
                self.label_image2.clear()

                # Hide the buttons and combo box if no image is loaded
                self.button_process_image.hide()
                self.color_selection_combo.hide()

    def processImage(self):
        # Black box image processing
        # Replace this with your actual logic to process the image
        # Update self.divingBackend.currentPicture with the processed image
        self.divingBackend.start_shape_detetion(self.divingBackend.currentframe)

        # Show the processed image
        self.showImages(self.divingBackend.reference_frame, self.divingBackend.shape_frame)

        self.button_process_image.setDisabled(True)
        self.color_selection_combo.show()


    def colorSelected(self, index):
        # Handle the color selection change event
        self.selected_color = self.color_selection_combo.currentText()

        # Update the selected color as a class variable
        if self.selected_color != "All Colors":
            self.updateNavigationButtons()

        else:
            self.selected_color = "All Colors"

        self.divingBackend.select_colour(self.selected_color)


        # Update the UI based on the selected color
        self.updateUIForSelectedColor(self.selected_color)

        # Update the navigation buttons


    def updateUIForSelectedColor(self, selected_color):
        # Check if the color is "All Colors"
        if selected_color == "All Colors":
            # Show the original image
            self.showImages(self.divingBackend.reference_frame, self.divingBackend.shape_frame)
            self.color_selection_combo.show()
            self.button_down.hide()
            self.button_add_shape.hide()
            self.button_remove_shape.hide()
            self.button_up.hide()
            self.label_shape_counter.hide()


        else:
            self.showImages(self.divingBackend.reference_frame, self.divingBackend.shape_frame)
            self.button_down.show()
            self.button_add_shape.show()
            self.button_remove_shape.show()
            self.button_up.show()
            self.label_shape_counter.show()



    def showPreviousShape(self):
        self.divingBackend.current_shape_indexes[self.selected_color] -= 1
        self.updateNavigationButtons()
        self.divingBackend.update_shape(self.selected_color)
        self.updateShapeCounterLabel()
        self.showImages(self.divingBackend.reference_frame, self.divingBackend.shape_frame)

    def showNextShape(self):
        self.divingBackend.current_shape_indexes[self.selected_color] += 1
        self.updateNavigationButtons()
        self.divingBackend.update_shape(self.selected_color)
        self.updateShapeCounterLabel()
        self.showImages(self.divingBackend.reference_frame, self.divingBackend.shape_frame)


    def updateNavigationButtons(self):
        # Enable or disable the navigation buttons based on the current frame index
        self.button_up.setEnabled(True)

        if len(self.divingBackend.videoAnalysis.shape_dictionary[self.selected_color]) == 0:
            self.button_up.setDisabled(True)
            self.button_down.setDisabled(True)

            self.button_down.setText("No Shapes")
            self.button_up.setText("No Shapes")
            return

        if self.divingBackend.current_shape_indexes[self.selected_color] == 0:
            self.button_up.setDisabled(True)

        
        self.button_down.setEnabled(True)
        self.button_down.setText("Down: " + str(len(self.divingBackend.videoAnalysis.shape_dictionary[self.selected_color]) - 1 - self.divingBackend.current_shape_indexes[self.selected_color]))
        self.button_up.setText("Up: " + str(self.divingBackend.current_shape_indexes[self.selected_color]))



        if self.divingBackend.current_shape_indexes[self.selected_color] == len(self.divingBackend.videoAnalysis.shape_dictionary[self.selected_color]) - 1:
            self.button_down.setDisabled(True)
        
        



    def showImages(self, image1, image2):
        # Convert the image array to QImage
        height, width, channel = image1.shape
        bytes_per_line = 3 * width
        q_image = QImage(image1.data, width, height, bytes_per_line, QImage.Format_BGR888)

        # Display the QImage in the label
        self.label_image1.setPixmap(QPixmap.fromImage(q_image))
        
        if image2 is None:
            return
        # Convert the image array to QImage
        height, width, channel = image2.shape
        bytes_per_line = 3 * width
        q_image = QImage(image2.data, width, height, bytes_per_line, QImage.Format_BGR888)

        # Display the QImage in the label
        self.label_image2.setPixmap(QPixmap.fromImage(q_image))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sports_app = SportsApp()
    sys.exit(app.exec_())