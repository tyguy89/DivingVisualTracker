
import cv2
import numpy as np

from .shape_detection import RGBShapeDetection

class ImageAnalysisMain:
    def __init__(self):
        self.shapeTool = RGBShapeDetection()
        self.current_frame = None
        self.frames_processed = []
        self.current_colour_dictionary = None
        self.shape_dictionary = None


    def read_frame(self, frame: np.array):
        self.frames_processed.clear()
        self.current_frame = frame
        self.frames_processed.append(frame)
        self.blank_sized_canvas = np.zeros((len(frame), len(frame[0]), 3), np.uint8, 'C')


    def start_RGB_shape_detection(self, extract_background: bool, extract_colours: list, zoning_threshold_x: int, zoning_threshold_y: int, neighbour_limit: int):
        assert self.current_frame is not None
        self.current_frame = self.shapeTool.find_RGB_colour_in_image(self.current_frame)
        self.frames_processed.append(self.current_frame)

        self.current_frame, self.current_colour_dictionary = self.shapeTool.find_all_shape_edges(self.current_frame)
        self.frames_processed.append(self.current_frame)

        self.shape_dictionary = self.shapeTool.extract_shapes_from_np(self.current_colour_dictionary, zoning_threshold_x, zoning_threshold_y)

        return 0
    
    def start_HSV_shape_detection(self, img):


        pass

    def start_combined_shape_detection():
        pass
    
    def start_specific_targeted_RGB_detection():
        pass
    
    def start_specific_targeted_HSV_detection():
        pass
    
    def start_specific_targeted_combined_detection():
        pass
    
    def extract_background(self, img, colour_data):
        biggest = "white"
        for k in colour_data.keys():
            if len(colour_data[k]) > len(colour_data[biggest]):
                biggest = k
        
        for i in colour_data[biggest]:
            img[i[0]][i[1]] = np.array([0, 0, 0])
        
        return img

    def extract_colour(self, img, colour_data, colour_to_remove):
        colour_edges = np.zeros((len(img), len(img[0]), 3), np.uint8, 'C')
        for v in colour_data[colour_to_remove]:
            colour_edges[v[0]][v[1]] = img[v[0]][v[1]]
        

        return colour_edges

    def remove_colour(self, img, colour_data: dict, colour_to_delete):
        for i in colour_data[colour_to_delete]:
            img[i[0]][i[1]] = np.array([0, 0, 0])
        
        colour_data.pop(colour_to_delete)

        return img

    def paint_blank_with_coords(self, colour_data, canvas, colour):
        color_lottery = [self.index["aqua"], self.index["red"], self.index["blue"], self.index["white"], self.self.index["yellow"], self.index["orange"], self.index["green"], self.index["magenta"], self.index["pink"], self.index["aqua"], self.index["red"], self.index["blue"], self.index["white"], self.index["yellow"], self.index["orange"], self.index["green"], self.index["magenta"]]
        color_lottery += color_lottery
        color_lottery += color_lottery
        color_lottery += color_lottery
        color_lottery += color_lottery
        color_lottery += color_lottery
        color_lottery += color_lottery
        color_lottery += color_lottery
        color_lottery += color_lottery

        for shape in range(len(colour_data)):

            for i in colour_data[shape]:
                canvas[i[0]][i[1]] = color_lottery[shape]

        return canvas