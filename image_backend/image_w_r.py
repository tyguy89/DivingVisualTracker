#Tyler Boechler

import numpy as np
import cv2 as cv

def frame_count(video_path, manual=False):
    def manual_count(handler):
        frames = 0
        while True:
            status, frame = handler.read()
            if not status:
                break
            frames += 1
        return frames 

    cap = cv.VideoCapture(video_path)
    # Slow, inefficient but 100% accurate method 
    if manual:
        frames = manual_count(cap)
    # Fast, efficient but inaccurate method
    else:
        try:
            frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
        except:
            frames = manual_count(cap)
    cap.release()
    return frames

class FileReader:
    def __init__(self):
        pass
    
    def read_picture_from_path(self, path: str) -> np.array:
        img = cv.imread(path)

        return img


    def read_video_frames_from_path(self, path: str) -> list:
        images = []

        cap = cv.VideoCapture(path)
        while not cap.isOpened():
            cap = cv.VideoCapture(path)
            cv.waitKey(10)

        post_frame = cap.get(cv.CAP_PROP_POS_FRAMES)
        while True:
            frame_ready, frame = cap.read() # get the frame

            if frame is None:
                break
            
            if frame_ready:
                # The frame is ready and already captured
                # cv2.imshow('video', frame)

                # store the current frame in as a numpy array
                np_frame = cv.imread('video', frame)
                images.append(np_frame)
                
                counter = 0
            else:
                # The next frame is not ready, so we try to read it again
                cap.set(post_frame, post_frame-1)
                # It is better to wait for a while for the next frame to be ready
                cv.waitKey(10)


        return images

    def read_n_video_frames_from_path(self, path: str, n: int) -> list:
        images = []

        cap = cv.VideoCapture(path)
        while not cap.isOpened():
            cap = cv.VideoCapture(path)
            cv.waitKey(10)

        post_frame = cap.get(cv.CAP_PROP_POS_FRAMES)
        counter = n
        while True:
            frame_ready, frame = cap.read() # get the frame

            if frame is None or counter == 0:
                break
            
            if frame_ready:
                # The frame is ready and already captured
                # cv2.imshow('video', frame)

                # store the current frame in as a numpy array
                np_frame = cv.imread('video', frame)
                images.append(np_frame)
                
                counter -= 1
            else:
                # The next frame is not ready, so we try to read it again
                cap.set(post_frame, post_frame-1)
                # It is better to wait for a while for the next frame to be ready
                cv.waitKey(10)


        return images