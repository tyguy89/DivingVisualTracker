#Tyler Boechler

import cv2 as cv
import numpy as np
from collections import defaultdict


class RGBShapeDetection:
    def __init__(self):
        self.index_bgr = {
        "black": np.array([0, 0, 0]), "white": np.array([255, 255, 255]),
        "red": np.array([0, 0, 255]), "green": np.array([0, 255, 0]),
        "blue": np.array([255, 0, 0]), "light blue": np.array([255, 157, 0]),
        "cyan": np.array([255, 255, 0]), "aqua": np.array([190, 255, 0]),
        "pink": np.array([255, 0, 190]), "magenta": np.array([255, 0, 255]),
        "purple": np.array([255, 0, 100]), "light green": np.array([0, 255, 150]),
        "yellow": np.array([0, 255, 255]), "orange": np.array([0, 165, 255]), "red_back": np.array([0, 0, 255]), "red_front": np.array([0, 0, 255]), "grey": np.array([140, 140, 140])
        }
        self.reversed_index_bgr = {}
        for k in self.index_bgr:
            if k == "red_front" or k == "red_back":
                continue
            self.reversed_index_bgr[str(self.index_bgr[k])] = k

    # def find_pixel_neighbours(self, img, x, y):
    #     pad_img = np.pad(img, ((1,1),(1,1),(0,0)), mode='constant')
    #     neighbours = pad_img[x:x+3, y:y+3]
    #     return neighbours

    def find_HSV_colour_in_image(self, img):
        hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        color_masks = {
            "orange": cv.inRange(hsv_img, np.array([10, 30, 30]), np.array([25, 255, 255])),
            "yellow": cv.inRange(hsv_img, np.array([25, 30, 30]), np.array([35, 255, 255])),
            "green": cv.inRange(hsv_img, np.array([35, 30, 30]), np.array([75, 255, 255])),
            "aqua": cv.inRange(hsv_img, np.array([75, 30, 30]), np.array([85, 255, 255])),
            "cyan": cv.inRange(hsv_img, np.array([85, 30, 30]), np.array([95, 255, 255])),
            "light blue": cv.inRange(hsv_img, np.array([95, 30, 30]), np.array([110, 255, 255])),
            "blue": cv.inRange(hsv_img, np.array([110, 30, 30]), np.array([130, 255, 255])),
            "purple": cv.inRange(hsv_img, np.array([130, 30, 30]), np.array([140, 255, 255])),
            "magenta": cv.inRange(hsv_img, np.array([140, 30, 30]), np.array([155, 255, 255])),
            "pink": cv.inRange(hsv_img, np.array([155, 30, 30]), np.array([170, 255, 255])),
            "red_back": cv.inRange(hsv_img, np.array([0, 30, 30]), np.array([10, 255, 255])),
            "red_front": cv.inRange(hsv_img, np.array([170, 30, 30]), np.array([180, 255, 255])),
            "black": cv.inRange(hsv_img, np.array([0, 0, 0]), np.array([180, 255, 30])),
            "white": cv.inRange(hsv_img, np.array([0, 0, 30]), np.array([180, 30, 255])),
            "grey": cv.inRange(hsv_img, np.array([0, 0, 20]), np.array([180, 30, 230])) 
        }

        for color, mask in color_masks.items():
            img[mask > 0] = self.index_bgr[color]

        return img

    def find_BGR_colour_in_image(self, img):
        new_array = np.zeros((len(img), len(img[0]), 3), np.uint8, 'C')
        
        counter = [0, 0]
        # np.set_printoptions(threshold=np. inf)
        for i in range(0, len(img)):
            for j in range(0, int(len(img[i]))):
                
                    #print(img[i][j])


                local_pixel = img[i][j]
                r = local_pixel[2]
                g = local_pixel[1]
                b = local_pixel[0]

                new_r = 0 
                new_g = 0
                new_b = 0
                

                
                
                if r <= 200 and r > 20 and g <= 200 and g > 20 and b <= 200 and b > 20 and abs(r - b) < 40 and abs(r - g) < 40 and abs(g - b) < 40 and new_r == 0 and new_b == 0 and new_g == 0:
                    new_r = 140
                    new_g = 140
                    new_b = 140
                #WHITE DOMINANT COLOUR
                elif r >= 200 and g >= 200 and b >= 200:
                    new_r = 255
                    new_g = 255
                    new_b = 255
                #BLACK DOMINANT COLOUR
                elif r <= 50 and g <= 50 and b <= 50 and new_r == 0 and new_b == 0 and new_g == 0:
                    new_r = 0
                    new_g = 0
                    new_b = 0
                
                #RED DOMINANT COLOUR
                elif r >= g and r > b and new_r == 0 and new_b == 0 and new_g == 0:
                    if g / r > 0.4:
                        if g/r > 0.75:
                            #YELLOW
                            new_g = 255
                        else:
                            #ORANGE
                            new_g = 165
                    else:
                        if b / r > 0.55:
                            #MAGENTA
                            new_b = 255

                    new_r = 255


                #GREEN DOMINANT COLOUR
                elif g >= r and g >= b and new_r == 0 and new_b == 0 and new_g == 0:
                    if r / g > 0.5:
                        if r/g > 0.75:
                            #YELLOW
                            new_r = 255
                        else:
                            #LIGHT GREEN
                            new_r = 150
                    else:
                        if b / g > 0.6:
                            if b/g > 85:
                                #LIGHT BLUE
                                new_b = 255
                            else:
                                #AQUA 
                                new_b = 190
                                
                    new_g = 255
                

                #BLUE DOMINANT COLOUR
                elif b >= r and b >= g and new_r == 0 and new_b == 0 and new_g == 0:
                    if g / b > 0.5:
                        if g/b > 0.75:
                            #CYAN
                            new_g = 255
                        else:
                            #LIGHT BLUE
                            new_g = 157
                        
                    else:
                        if r / b > 0.3:
                            if r/b > 0.5:
                                if r/b > 0.75:
                                    #MAGENTA
                                    new_r = 255
                                else:
                                    #PINK
                                    new_r = 190
                            else:
                                #PURPLE
                                new_r = 100
                        
                            
                    new_b = 255
                
                #UNKNOWN
                elif new_r == 0 and new_b == 0 and new_g == 0:
                    print(img[i][j])
                    new_r = 0
                    new_g = 0
                    new_b = 0

                new_array[i][j] = np.array([new_b, new_g, new_r])
                counter[1] += 1
            counter[0] += 1

        print(counter)
        # r, g, b = img[:, :, 2], img[:, :, 1], img[:, :, 0]
        # new_r, new_g, new_b = np.zeros_like(r), np.zeros_like(g), np.zeros_like(b)

        # white_indices = (r >= 175) & (g >= 175) & (b >= 175)
        # black_indices = (r <= 50) & (g <= 50) & (b <= 50)
        # red_indices = (r > g) & (r > b) & (g / r <= 0.8) & (b / r <= 0.8)  # Condition for red
        # green_indices = (g > r) & (g > b) & (r / g <= 0.8) & (b / g <= 0.8)  # Condition for green
        # blue_indices = (b > r) & (b > g) & (g / b <= 0.8) & (r / b <= 0.8)  # Condition for blue
        # gray_indices = (r <= 200) & (r > 20) & (g <= 200) & (g > 20) & (b <= 200) & (b > 20) & (abs(r - b) < 40) & (abs(r - g) < 40) & (abs(g - b) < 40)  # Condition for gray

        # new_r[white_indices] = 255
        # new_g[white_indices] = 255
        # new_b[white_indices] = 255

        # new_r[black_indices] = 0
        # new_g[black_indices] = 0
        # new_b[black_indices] = 0

        # new_r[red_indices] = 255
        # new_g[red_indices] = np.where(g[red_indices] / r[red_indices] > 0.75, 0, np.where(g[red_indices] / r[red_indices] <= 0.75, 165, 0))  # Set green to 0 if red, else 165
        # new_b[red_indices] = np.where(b[red_indices] / r[red_indices] > 0.55, 0, 0)  # Ensure red remains red

        # new_g[green_indices] = 255
        # new_r[green_indices] = np.where(r[green_indices] / g[green_indices] > 0.75, 150, np.where(r[green_indices] / g[green_indices] <= 0.75, 0, 0))  # Ensure red remains unchanged, else 150
        # new_b[green_indices] = np.where(b[green_indices] / g[green_indices] > 0.6, 0, 0)  # Ensure green remains green

        # new_b[blue_indices] = 255
        # new_g[blue_indices] = np.where(g[blue_indices] / b[blue_indices] > 0.75, 255, np.where(g[blue_indices] / b[blue_indices] <= 0.75, 157, 255))  # Set green to 255 if blue, else 157
        # new_r[blue_indices] = np.where(r[blue_indices] / b[blue_indices] > 0.5, 0, 0)  # Ensure blue remains blue

        # new_r[gray_indices] = 140
        # new_g[gray_indices] = 140
        # new_b[gray_indices] = 140

        # new_array = np.dstack((new_b, new_g, new_r))  # Return the merged BGR image
        # # # Update only if the pixel corresponds to a defined color
        # print("New array shape after processing:", new_array.shape)  # Add this line
        # cv.imshow("txt", new_array)        # import matplotlib
        # cv.waitKey(0)

        
        return new_array


    def is_edge_of_shape(self, array, threshold_start: int, threshold_end: int):
        # print("Array shape:", array.shape)
        # print(array)
        center_pixel = array[0, 0, 1, 1, 1]
        count = np.count_nonzero(array != center_pixel)
        return threshold_start <= count <= threshold_end
    
    def is_edge_of_shape_vectorized(self, neighbors, threshold_start: int, threshold_end: int):
        center_pixel_values = neighbors[:, :, 0, 1, 1, :]
        # print(center_pixel_values.shape)
        # Create an array containing the center pixel values replicated along the new dimensions
        center_pixel_array = center_pixel_values[:, :, np.newaxis, np.newaxis, np.newaxis, :]

        # Repeat along the appropriate axes to match the desired shape
        # center_pixel_array = np.repeat(center_pixel_array, 3, axis=3)  # Repeat for each color channel
        center_pixel_array = np.repeat(center_pixel_array, 3, axis=3)  # Repeat along the 3x3 grid horizontally
        center_pixel_array = np.repeat(center_pixel_array, 3, axis=4)  # Repeat along the 3x3 grid vertically

        # Now, the shapes of the two arrays should be compatible for subtraction
        difference = np.abs(center_pixel_array - neighbors)
        # print(difference.shape)


        # Count the number of different pixels
        num_different_pixels = np.sum(difference > 0, axis=(-1, -2))

        # Sum along both axes (-1 and -2) to collapse them into a single axis
        num_different_pixels_collapsed = np.sum(num_different_pixels, axis=-1)        
        # print(num_different_pixels_collapsed.shape)

        # Check if the number of different pixels is within the specified range
        in_range = (num_different_pixels_collapsed >= threshold_start) & (num_different_pixels_collapsed <= threshold_end)
        in_range_repeated = np.repeat(in_range[...], 3, axis=-1)  # Repeat along the last axis (color channels)
        # print(in_range_repeated)
        
        return in_range_repeated
    
    
        
    def find_all_shape_edges(self, filtered_img, threshold_start, threshold_end):
        def sliding_window_view(arr, window_shape):
            arr = np.asarray(arr)
            window_shape = tuple(window_shape)
            strides = arr.strides + arr.strides
            shape = tuple(np.subtract(arr.shape, window_shape) + 1) + window_shape
            strides = arr.strides + arr.strides
            return np.lib.stride_tricks.as_strided(arr, shape=shape, strides=strides)
        # Initialize edge_colours dictionary
        edge_colours = {k: [] for k in self.index_bgr if k not in ["red_back", "red_front"]}
            
        # Padding the image to handle boundary pixels
        padded_img = np.pad(filtered_img, ((1,1),(1,1),(0,0)), mode='constant', constant_values=0)
        # print("padded image shape", padded_img.shape)
        # print("padded image", padded_img)
        # Create 3x3 neighborhood arrays around each pixel using sliding window
        window_shape = (3, 3, 3)

        ninebynine_arrays = sliding_window_view(padded_img, window_shape)
        # print("Sliding window view shape:", ninebynine_arrays.shape, ninebynine_arrays)

        # Perform edge detection on all neighborhoods simultaneously
        edge_masks = self.is_edge_of_shape_vectorized(ninebynine_arrays, threshold_start, threshold_end)
        # print("Shape of edge mask: " + str(edge_masks.shape))

        # Extract pixels where edge detection is true

        colors_image = np.copy(filtered_img)
        colors_image[~edge_masks]= -1
        # print("colouredges image shape:", colors_image.shape)  # Add this line
        # cv.imshow("yes", colors_image)
        # cv.waitKey(0)

        # Get unique non-black colors
        # Create a mask for non-black pixels
        non_black_mask = np.any(colors_image != [None, None, None], axis=-1)
        # Get the pixel values for non-black pixels
        non_black_pixels = colors_image[non_black_mask]

        # Convert the pixel values to tuples
        # pixel_strings = [str(np.array(pixel)) for pixel in non_black_pixels]

        # Get the indices of non-black pixels
        # non_black_coords = np.argwhere(non_black_mask)
        color_dictionary = {}
        # Create a dictionary to store each color
        for color in self.index_bgr.keys():
            # Create a mask for pixels of the current color
            mask = np.all(colors_image == self.index_bgr[color], axis=-1)
            # Check if any pixels match the color
            if np.any(mask):
                # Get the coordinates of pixels for the current color
                coordinates = np.argwhere(mask)
                # Add the coordinates to the color dictionary
                color_dictionary[color] = coordinates.tolist()

        # Use NumPy indexing to directly populate the color dictionary
        # for coord, pixel_str in zip(non_black_coords, pixel_strings):
        #     color_dictionary[self.reversed_index_bgr[pixel_str]].append(tuple(coord))

        for color_key in self.index_bgr.keys():
            # Check if the color key is not present in the color dictionary
            if color_key not in color_dictionary:
                # Add the missing color key with an empty list
                color_dictionary[color_key] = []

        # Reshape colour_edges to match the shape of the original image
        # colour_edges = colour_edges.reshape(filtered_img.shape)
            
            # Get coordinates of edge pixels
            # rows, cols = np.nonzero(colour_edges)
            # for row, col in zip(rows, cols):
            #     edge_colours[self.reversed_index_bgr[str(filtered_img[row, col])]].append([row, col])
        colors_image[~edge_masks] = 0
        # cv.imshow("txt", colour_edges)        # import matplotlib
        # cv.waitKey(0)
        print("end")
        return colors_image, color_dictionary

    def extract_shapes_from_np(self, colour_data: dict, zoning_threshold_x: int, zoning_threshold_y: int): 
        def find_zone(vertex: tuple, zones: dict):
            v_count = len(zones.keys())
            
            for value in list(zones.keys()):
            
                if vertex[0] >= zones[value][0][0] - zoning_threshold_x and vertex[0] <= zones[value][0][1] + zoning_threshold_x and vertex[1] >= zones[value][0][2] - zoning_threshold_y and vertex[1] <= zones[value][0][3] + zoning_threshold_y:
                    if vertex[0] < zones[value][0][0] or vertex[0] > zones[value][0][1] or vertex[1] < zones[value][0][2] or vertex[1] > zones[value][0][3]:
                        return_vals = [zones[value][0][0], zones[value][0][1], zones[value][0][2], zones[value][0][3]]
                        if vertex[0] < zones[value][0][0]:
                            return_vals[0] = vertex[0]
                        if vertex[0] > zones[value][0][1]:
                            return_vals[1] = vertex[0]
                        if vertex[1] < zones[value][0][2]:
                            return_vals[2] = vertex[1]
                        if vertex[1] > zones[value][0][3]:
                            return_vals[3] = vertex[1]
                        
                        return (value, (return_vals[0], return_vals[1], return_vals[2], return_vals[3]))
                    else:
                        return value, zones[value][0]
                    
            # print("ADDING NEW SHAPE", v_count)        
            return (v_count, (vertex[0]-zoning_threshold_x, vertex[0]+zoning_threshold_x, vertex[1]-zoning_threshold_y, vertex[1]+zoning_threshold_y))      

        zones = dict()

        for colour in colour_data.keys():
            zones[colour] = dict()
            for v in colour_data[colour]:
                if len(zones[colour].keys()) == 0:
                    zones[colour][0] = ((v[0]-zoning_threshold_x, v[0]+zoning_threshold_x, v[1]-zoning_threshold_y, v[1]+zoning_threshold_y), [v])
                else:
                    cur_zones = list(zones[colour].keys())

                    v_zone = find_zone(v, zones[colour])

                    if v_zone[0] not in cur_zones:
                        zones[colour][v_zone[0]] = (v_zone[1], [v])
                    else:
                        #print(zones[colour][v_zone[0]][1])
                        zones[colour][v_zone[0]][1].append(v)
                        #print(zones[colour][v_zone[0]][1])
                        #print("---")
                        zones[colour][v_zone[0]] = (v_zone[1], zones[colour][v_zone[0]][1])

        return zones

    # def extract_nprgb_path_of_image(self, path):
    #     img = cv.imread(path)

    #     return img

    

    

        #start = time.time()
        #colour_object = extract_nprgb_path_of_image("python_projects/DivingVisualTracker/image_analysis/IMG_8880.jpg")
        #blank = np.zeros((len(colour_object), len(colour_object[0]), 3), np.uint8, 'C')

        #filtered_image = find_colour_in_image(colour_object)
        #edges_of_colours = find_all_shape_edges(filtered_image)
        #focus_colour = "orange"
        #single_colour = extract_shapes_from_np({focus_colour: edges_of_colours[1][focus_colour]}, 5, 5)
        #print(single_colour)
        #print("Process time = " + str(time.time() - start))
        #start = time.time()
        #shape_list = []

        #for i in single_colour[focus_colour].keys():
        #    shape_list.append(single_colour[focus_colour][i][1])

        #blank = paint_blank_with_coords(shape_list, blank, focus_colour)
        #cv.imshow("img", blank)
        #print("Process time = " + str(time.time() - start))


        #cv.waitKey(0)
        #cv.destroyAllWindows()

