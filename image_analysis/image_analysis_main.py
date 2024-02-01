
import cv2
import numpy as np

from .shape_detection import RGBShapeDetection

class ImageAnalysisMain:
    def __init__(self):
        self.shapeTool = RGBShapeDetection()
        self.all_colour_frames = []
        self.current_frame = None
        self.reference_frame = None
        self.current_colour_dictionary = None
        self.shape_dictionary = None


    def read_frame(self, frame: np.array):
        self.all_colour_frames.clear()

        self.current_frame = frame
        self.all_colour_frames.append(frame)
        self.blank_sized_canvas = np.zeros((len(frame), len(frame[0]), 3), np.uint8, 'C')


    def start_RGB_shape_detection(self, extract_background: bool, extract_colours: list, zoning_threshold_x: int, zoning_threshold_y: int, neighbour_start: int, neighbour_end: int):
        assert self.current_frame is not None and neighbour_start <= neighbour_end
        self.current_frame = self.shapeTool.find_RGB_colour_in_image(self.current_frame)

        self.all_colour_frames.append(self.current_frame)

        self.current_frame, self.current_colour_dictionary = self.shapeTool.find_all_shape_edges(self.current_frame, neighbour_start, neighbour_end)
        self.reference_frame = self.current_frame
        
        self.shape_dictionary = self.shapeTool.extract_shapes_from_np(self.current_colour_dictionary, zoning_threshold_x, zoning_threshold_y)

        return 0
    
    def start_HSV_shape_detection(self, extract_background: bool, extract_colours: list, zoning_threshold_x: int, zoning_threshold_y: int, neighbour_start: int, neighbour_end: int):

        assert self.current_frame is not None and neighbour_start <= neighbour_end
        self.current_frame = self.shapeTool.find_HSV_colour_in_image(self.current_frame)

        self.all_colour_frames.append(self.current_frame)

        self.current_frame, self.current_colour_dictionary = self.shapeTool.find_all_shape_edges(self.current_frame, neighbour_start, neighbour_end)
        self.reference_frame = self.current_frame
        
        self.shape_dictionary = self.shapeTool.extract_shapes_from_np(self.current_colour_dictionary, zoning_threshold_x, zoning_threshold_y)

        return 0

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
    
    
    def extract_colour_by_dict(self, img, colour_to_extract):
        if colour_to_extract == "black":
            colour_edges = np.ones((len(img), len(img[0]), 3), np.uint8, 'C')
        else:
            colour_edges = np.zeros((len(img), len(img[0]), 3), np.uint8, 'C')

        for i in self.current_colour_dictionary[colour_to_extract]:
            colour_edges[i[0]][i[1]] = self.shapeTool.index_bgr[colour_to_extract]
        
        return colour_edges


    def extract_colour_by_pixel(self, img, colour_to_extract):
        if colour_to_extract == "black":
            colour_edges = np.ones((len(img), len(img[0]), 3), np.uint8, 'C')
        else:
            colour_edges = np.zeros((len(img), len(img[0]), 3), np.uint8, 'C')

        for x in range(len(img)):
            for y in range(len(img[0])):
                if self.shapeTool.reversed_index_bgr[str(img[x][y])] ==  colour_to_extract:
                    colour_edges[x][y] = img[x][y]
        
        return colour_edges
    
    def draw_specific_shape(self, current_colour, current_shape_id):
        if current_colour == "black":
            blank = np.ones((len(self.blank_sized_canvas), len(self.blank_sized_canvas[0]), 3), np.uint8, 'C')
        
        else:
            blank = np.zeros((len(self.blank_sized_canvas), len(self.blank_sized_canvas[0]), 3), np.uint8, 'C')
    
        if self.shape_dictionary[current_colour][current_shape_id] is None:
            return None
        
        for pixels in self.shape_dictionary[current_colour][current_shape_id][1]:
            # - Shape is (x1, x2, y1, y2) [pixels]
            blank[pixels[0]][pixels[1]] = self.shapeTool.index_bgr[current_colour]
        
        return blank


    def draw_list_of_shapes(self, shape_list):
        """
        shape_list elements in the form (id, colour)
        """
        blank = np.zeros((len(self.blank_sized_canvas), len(self.blank_sized_canvas[0]), 3), np.uint8, 'C')
        
        for shape in shape_list:
            if self.shape_dictionary[shape[1]][shape[0]] is None:
                return None
            for pixels in self.shape_dictionary[shape[1]][shape[0]][1]:
                blank[pixels[0]][pixels[1]] = self.shapeTool.index_bgr[shape[1]]
           
        return blank

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