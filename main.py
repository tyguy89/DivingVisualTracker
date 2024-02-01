from image_backend.image_processing_main import VideoReader
from image_analysis.image_analysis_main import ImageAnalysisMain

import config
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator

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

    def start_RGB_shape_detetion(self, first_frame: np.array, nstart, nend, x, y) -> None:
        self.id = 1
        self.videoAnalysis.read_frame(first_frame)
        if 0 == self.videoAnalysis.start_RGB_shape_detection(False, [], x, y, nstart, nend):
            self.reference_frame = self.videoAnalysis.reference_frame
            self.shape_frame = self.videoAnalysis.all_colour_frames[1]
            
            for val in self.current_shape_indexes.keys():
                self.current_shape_indexes[val] = (0, None) [len(self.videoAnalysis.shape_dictionary[val]) == 0]

            return True
        else:
            return False
        
        

    def start_HSV_shape_detetion(self, first_frame: np.array,  nstart, nend, x, y) -> None:
        self.id = 1
        self.videoAnalysis.read_frame(first_frame)
        if 0 == self.videoAnalysis.start_HSV_shape_detection(False, [], x, y, nstart, nend):
            self.reference_frame = self.videoAnalysis.reference_frame
            self.shape_frame = self.videoAnalysis.all_colour_frames[1]

            for val in self.current_shape_indexes.keys():
                self.current_shape_indexes[val] = (0, None) [len(self.videoAnalysis.shape_dictionary[val]) == 0]

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
            self.reference_frame = self.videoAnalysis.extract_colour_by_dict(self.videoAnalysis.reference_frame, colour)
            if len(self.videoAnalysis.shape_dictionary[colour]) != 0:
                self.shape_frame = self.videoAnalysis.draw_specific_shape(colour, self.current_shape_indexes[colour])
            else:
                self.shape_frame = np.ones((len(self.reference_frame), len(self.reference_frame[0]), 3), np.uint8, 'C')

    def select_colour_shapes(self, colour, shape_list: list):
        if colour == "All Colors":
            self.reference_frame = self.videoAnalysis.reference_frame
            self.shape_frame = self.videoAnalysis.all_colour_frames[1]
        else:

            self.reference_frame = self.videoAnalysis.extract_colour_by_dict(self.videoAnalysis.reference_frame, colour)
            if len(self.videoAnalysis.shape_dictionary[colour]) != 0 or len(shape_list) != 0:
                self.shape_frame = self.videoAnalysis.draw_list_of_shapes(shape_list)
            else:
                self.shape_frame = np.ones((len(self.reference_frame), len(self.reference_frame[0]), 3), np.uint8, 'C')


    def update_shape(self, current_colour):
        if self.current_shape_indexes[current_colour] is None:
            print("Shape null saved error")
            return
        self.shape_frame = self.videoAnalysis.draw_specific_shape(current_colour, self.current_shape_indexes[current_colour])

    def update_shape_list(self, current_colour, list_of_shapes: list):
        list_of_shapes = list_of_shapes.copy()
        if self.current_shape_indexes[current_colour] is not None and (self.current_shape_indexes[current_colour], current_colour) not in list_of_shapes:
            list_of_shapes.append((self.current_shape_indexes[current_colour], current_colour))
        self.shape_frame = self.videoAnalysis.draw_list_of_shapes(list_of_shapes)

class SportsApp(QWidget):
    selected_color = "All Colors"  # Class variable to store the selected color

    def __init__(self):
        super().__init__()

        self.divingBackend = DivingVisualTracker()
        self.tracked_shapes = []  # List to store the shapes to be tracked

        self.image_processing_mode = "RGB"

        self.pixel_neighbour_min = 3
        self.pixel_neighbour_max = 5

        self.shape_zoning_x = 5
        self.shape_zoning_y = 5
        self.show_targeted_shapes = False

        # self.current_shape = None

        self.initUI()

    def initUI(self):
        # Create a tab widget
        tab_widget = QTabWidget(self)
        tab_widget.addTab(self.createTab1(), "Image Processing")  # Renamed the tab
        tab_widget.addTab(self.createImageSettingsTab(), "Image Processing Settings")
        tab_widget.addTab(self.createTab2(), "Graph Tab")

        # Set up the main layout
        main_layout = QVBoxLayout(self)

        # Create a widget for shape-related buttons and labels

        # Add the tab widget
        main_layout.addWidget(tab_widget)
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

    def createImageSettingsTab(self):
        widget = QWidget()

        layout_tab = QVBoxLayout(widget)
        self.colour_mode_label = QLabel("Image Processing Method:", self)
        # button_box = QHBoxLayout(widget)

        # button_box.addSpacing(20)

        self.buttonRGB = QPushButton("RGB", self)
        self.buttonHSV = QPushButton("HSV", self)

        if self.image_processing_mode == "RGB":
            self.buttonHSV.setStyleSheet("background-color : lightgrey")
            self.buttonRGB.setStyleSheet("background-color : lightblue")

        elif self.image_processing_mode == "HSV":
            self.buttonHSV.setStyleSheet("background-color : lightblue")
            self.buttonRGB.setStyleSheet("background-color : lightgrey")

        self.buttonRGB.clicked.connect(self.RGB_setting_button)
        self.buttonHSV.clicked.connect(self.HSV_setting_button)

        # button_box.addWidget(self.buttonRGB)
        # button_box.addWidget(self.buttonHSV)

        self.shape_bound_label = QLabel("Shape definition boundaries (how many pixels surrounding a main pixel need to be a different colour for it to be considered an edge): \n Min \n Max ", self)
        self.textbox_min_neighbour_setting = QLineEdit("3", self)
        self.textbox_max_neighbour_setting = QLineEdit("5", self)

        self.shape_zone_label = QLabel("Shape zone size starting point (pixels) +/- in both directions: \n X Val \n Y Val ", self)

        self.textbox_x_pixel_shape_range = QLineEdit("5", self)
        self.textbox_y_pixel_shape_range = QLineEdit("5", self)

        onlyInt1, onlyInt2, onlyInt3 = QIntValidator(), QIntValidator(), QIntValidator()
        onlyInt1.setRange(1, 7)
        self.textbox_min_neighbour_setting.setValidator(onlyInt1)
        onlyInt2.setRange(1, 8)
        self.textbox_max_neighbour_setting.setValidator(onlyInt2)
        onlyInt3.setRange(1, 500)
        self.textbox_x_pixel_shape_range.setValidator(onlyInt3)
        self.textbox_y_pixel_shape_range.setValidator(onlyInt3)

        self.textbox_min_neighbour_setting.editingFinished.connect(self.min_neighbour_setting)
        self.textbox_min_neighbour_setting.editingFinished.connect(self.max_neighbour_setting)

        self.textbox_x_pixel_shape_range.editingFinished.connect(self.x_setting)
        self.textbox_y_pixel_shape_range.editingFinished.connect(self.y_setting)


        layout_tab.addWidget(self.colour_mode_label)
        # layout_tab.addWidget(button_box)
        layout_tab.addWidget(self.buttonRGB)
        layout_tab.addWidget(self.buttonHSV)
        layout_tab.addWidget(self.shape_bound_label)
        layout_tab.addWidget(self.textbox_min_neighbour_setting)
        layout_tab.addWidget(self.textbox_max_neighbour_setting)
        layout_tab.addWidget(self.shape_zone_label)
        layout_tab.addWidget(self.textbox_x_pixel_shape_range)
        layout_tab.addWidget(self.textbox_y_pixel_shape_range)

        layout_tab.addSpacing(20)


        layout_tab.addStretch(1)

        return widget
    
    def min_neighbour_setting(self):
        self.pixel_neighbour_min = int(self.textbox_min_neighbour_setting.text())
    
    def max_neighbour_setting(self):
        self.pixel_neighbour_max = int(self.textbox_max_neighbour_setting.text())

    def x_setting(self):
        self.shape_zoning_x = int(self.textbox_x_pixel_shape_range.text())

    def y_setting(self):
        self.shape_zoning_y = int(self.textbox_y_pixel_shape_range.text())

    def RGB_setting_button(self):
        self.image_processing_mode = "RGB"


        self.buttonHSV.setStyleSheet("background-color : lightgrey")
        self.buttonRGB.setStyleSheet("background-color : lightblue")
        self.button_process_image.setText('Process Image - ' + str(self.image_processing_mode))



    def HSV_setting_button(self):
        self.image_processing_mode = "HSV"
        
        self.buttonHSV.setStyleSheet("background-color : lightblue")
        self.buttonRGB.setStyleSheet("background-color : lightgrey")
        self.button_process_image.setText('Process Image - ' + str(self.image_processing_mode))

    def createTab1(self):
        widget = QWidget()

        self.button_open_file = QPushButton('Open File', self)
        # self.textbox_file_path = QLineEdit(self)
        self.label_image1 = QLabel(self)
        self.label_image2 = QLabel(self)
        self.button_process_image = QPushButton('Process Image - ' + str(self.image_processing_mode), self)

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

        shape_widget = self.createShapeWidget()
        layout_images.addWidget(shape_widget)

        self.color_selection_combo.currentIndexChanged.connect(self.colorSelected)

        # Initially hide the buttons and combo box
        self.button_process_image.hide()
        self.color_selection_combo.hide()

        # Set up the layout for the first tab
        layout_tab1 = QVBoxLayout(widget)
        layout_tab1.addWidget(self.button_open_file)
        # layout_tab1.addWidget(self.textbox_file_path)
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
        self.button_add_shape = QPushButton('Add Current Shape', self)
        self.button_remove_shape = QPushButton('Delete ALL Saved Shapes', self)

        self.button_toggle_show_tracked_shapes = QPushButton("Show Selected Shapes - Amount:" + str(len(self.tracked_shapes)))

        # Initialize label_shape_counter as a QLabel
        self.label_shape_counter = QLabel('Shape ID: 0', self)

        shape_layout = QVBoxLayout(shape_widget)
        shape_layout.addWidget(self.label_shape_counter)
        shape_layout.addWidget(self.button_up)
        shape_layout.addWidget(self.button_down)
        shape_layout.addWidget(self.button_toggle_show_tracked_shapes)
        shape_layout.addWidget(self.button_add_shape)
        shape_layout.addWidget(self.button_remove_shape)


        self.button_toggle_show_tracked_shapes.clicked.connect(self.toggle_show_tracked_shapes)

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
        self.button_toggle_show_tracked_shapes.hide()

        return shape_widget

    def toggle_show_tracked_shapes(self):
        self.show_targeted_shapes = not self.show_targeted_shapes

        if not self.show_targeted_shapes:
            self.button_toggle_show_tracked_shapes.setStyleSheet("background-color : lightgrey")
            self.divingBackend.update_shape(self.selected_color)
        else:
            self.button_toggle_show_tracked_shapes.setStyleSheet("background-color : lightblue")
            self.divingBackend.update_shape_list(self.selected_color, self.tracked_shapes)

        self.updateUIForSelectedColor(self.selected_color)


    def addShape(self):

        if self.divingBackend.current_shape_indexes[self.selected_color] is None:
            print("NOOOOO! u dont")
            return

        if (self.divingBackend.current_shape_indexes[self.selected_color], self.selected_color) in self.tracked_shapes:
            print("Shape already tracked")
            return
        
        self.tracked_shapes.append((self.divingBackend.current_shape_indexes[self.selected_color], self.selected_color))
        self.button_toggle_show_tracked_shapes.setText("Show Selected Shapes - Amount:" + str(len(self.tracked_shapes)))


    def removeShape(self):
        self.tracked_shapes.clear()
        self.button_toggle_show_tracked_shapes.setText("Show Selected Shapes - Amount:" + str(len(self.tracked_shapes)))
        

    def updateShapeCounterLabel(self):
        if self.selected_color == "All Colors":
            print("Tyler needs to fix this, shouldnt happen")
            return
        if self.divingBackend.current_shape_indexes[self.selected_color] is not None:
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
            # self.textbox_file_path.setText(file_path)

            # Check if the file is an image and display it
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                
                self.showImages(self.divingBackend.process_picture(file_path), None)

                # Show the buttons and combo box after an image is loaded
                self.button_process_image.show()
                self.label_image2.clear()
                self.button_process_image.setEnabled(True)
                self.selected_color = "All Colors"
                self.color_selection_combo.hide()


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

        if self.image_processing_mode == "RGB":
            self.divingBackend.start_RGB_shape_detetion(self.divingBackend.currentframe, self.pixel_neighbour_min, self.pixel_neighbour_max, self.shape_zoning_x, self.shape_zoning_y)
        elif self.image_processing_mode == "HSV":
            self.divingBackend.start_HSV_shape_detetion(self.divingBackend.currentframe, self.pixel_neighbour_min, self.pixel_neighbour_max, self.shape_zoning_x, self.shape_zoning_y)
        

        # Show the processed image
        self.showImages(self.divingBackend.reference_frame, self.divingBackend.shape_frame)

        self.button_process_image.setDisabled(True)
        self.color_selection_combo.show()
        self.show_targeted_shapes = False


    def colorSelected(self, index):
        # Handle the color selection change event
        self.selected_color = self.color_selection_combo.currentText()
        
        # Update the selected color as a class variable
        if self.selected_color != "All Colors":
            self.updateNavigationButtons()

        else:
            self.selected_color = "All Colors"

        if self.show_targeted_shapes:
            self.divingBackend.select_colour_shapes(self.selected_color, self.tracked_shapes)
            self.divingBackend.update_shape_list(self.selected_color, self.tracked_shapes)

        # else:
        self.divingBackend.select_colour(self.selected_color)


        # Update the UI based on the selected color
        self.updateUIForSelectedColor(self.selected_color)

        # Update the navigation buttons


    def updateUIForSelectedColor(self, selected_color):
        self.updateShapeCounterLabel()

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
            self.button_toggle_show_tracked_shapes.show()



    def showPreviousShape(self):
        self.divingBackend.current_shape_indexes[self.selected_color] -= 1
        self.updateNavigationButtons()

        if self.show_targeted_shapes:
            self.divingBackend.update_shape_list(self.selected_color, self.tracked_shapes)
            # self.tracked_shapes.remove((self.divingBackend.current_shape_indexes[self.selected_color] + 1, self.selected_color))

        else:
            self.divingBackend.update_shape(self.selected_color)

        self.updateShapeCounterLabel()
        self.showImages(self.divingBackend.reference_frame, self.divingBackend.shape_frame)

    def showNextShape(self):
        self.divingBackend.current_shape_indexes[self.selected_color] += 1
        self.updateNavigationButtons()

        if self.show_targeted_shapes:
            self.divingBackend.update_shape_list(self.selected_color, self.tracked_shapes)
            # self.tracked_shapes.remove((self.divingBackend.current_shape_indexes[self.selected_color] - 1, self.selected_color))


        else:
            self.divingBackend.update_shape(self.selected_color)

        self.updateShapeCounterLabel()
        self.showImages(self.divingBackend.reference_frame, self.divingBackend.shape_frame)


    def updateNavigationButtons(self):
        # Enable or disable the navigation buttons based on the current frame index
        if self.selected_color == "All Colors":
            print("Tyler Should figure out this thing, shouldnt happen")
            return
        
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
        scaled_pixmap = None
        # Display the QImage in the label
        pixmap = QPixmap.fromImage(q_image)
        if height > 900 and width > 1000:
            scaled_pixmap = pixmap.scaled(1000, 850, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        elif height > 900:
            scaled_pixmap = pixmap.scaled(width, 850, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        elif width > 1000:
            scaled_pixmap = pixmap.scaled(1000, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            scaled_pixmap  = pixmap

        self.label_image1.setPixmap(scaled_pixmap)
        
        
        if image2 is None:
            return
        # Convert the image array to QImage
        height, width, channel = image2.shape
        bytes_per_line = 3 * width
        q_image = QImage(image2.data, width, height, bytes_per_line, QImage.Format_BGR888)

        # Display the QImage in the label
        pixmap = QPixmap.fromImage(q_image)
        if height > 900 and width > 1000:
            scaled_pixmap = pixmap.scaled(1000, 900, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        elif height > 900:
            scaled_pixmap = pixmap.scaled(width, 900, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        elif width > 1000:
            scaled_pixmap = pixmap.scaled(1000, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            scaled_pixmap  = pixmap

            
        self.label_image2.setPixmap(scaled_pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sports_app = SportsApp()
    sys.exit(app.exec_())