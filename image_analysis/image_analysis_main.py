
import cv2
import numpy as np

from .shape_detection import RGBShapeDetection

class ImageAnalysisMain:
    def __init__(self):
        self.shapeTool = RGBShapeDetection()
        self.all_colour_frames = []
        self.current_frame = None
        self.frames_display = []
        self.current_colour_dictionary = None
        self.shape_dictionary = None


    def read_frame(self, frame: np.array):
        self.frames_display.clear()
        self.all_colour_frames.clear()

        self.current_frame = frame
        self.frames_display.append(frame)
        self.all_colour_frames.append(frame)
        self.blank_sized_canvas = np.zeros((len(frame), len(frame[0]), 3), np.uint8, 'C')


    def start_RGB_shape_detection(self, extract_background: bool, extract_colours: list, zoning_threshold_x: int, zoning_threshold_y: int, neighbour_limit: int):
        assert self.current_frame is not None
        self.current_frame = self.shapeTool.find_RGB_colour_in_image(self.current_frame)

        self.frames_display.append(self.current_frame)
        self.all_colour_frames.append(self.current_frame)

        self.current_frame, self.current_colour_dictionary = self.shapeTool.find_all_shape_edges(self.current_frame, 3, 5)
        #self.frames_display.append(self.current_frame)
        #self.all_colour_frames.append(self.current_frame)
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
    
    def extract_background(self, img):
        biggest = "white"
        for k in self.current_colour_dictionary.keys():
            if len(self.current_colour_dictionary[k]) > len(self.current_colour_dictionary[biggest]):
                biggest = k
        
        for i in self.current_colour_dictionary[biggest]:
            img[i[0]][i[1]] = np.array([0, 0, 0])
        
        return img

    def extract_colour(self, img, colour_to_extract):
        colour_edges = np.zeros((len(img), len(img[0]), 3), np.uint8, 'C')
        for v in self.current_colour_dictionary[colour_to_extract]:
            colour_edges[v[0]][v[1]] = img[v[0]][v[1]]
        
        return colour_edges
    
    def draw_specific_shape(self, current_colour, current_shape_id)


    def draw_list_of_shapes(self):
        pass

    def remove_colour(self, img, colour_data: dict, colour_to_delete):
        for i in colour_data[colour_to_delete]:
            img[i[0]][i[1]] = np.array([0, 0, 0])
        
        colour_data.pop(colour_to_delete)

        return img
    


    def paint_blank_with_shapes(self, colour_data, canvas, shape):
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