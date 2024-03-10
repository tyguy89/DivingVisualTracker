#Tyler Boechler

from .image_w_r import FileReader
import time
import numpy as np

class VideoReader:
    """
    Giving a path on initialization, can read frames from video files or pictures
    """

    source = None
    readingTool = FileReader()

    def __init__(self, path: str):
        """
    Giving a path on initialization, can read frames from video files or pictures
        """
        self.source = path
        

    def start_continuous_feed(self, delay: float):
 
        pass

    def read_n_frames(self, n: int) -> list:
        return self.readingTool.read_n_video_frames_from_path(self.source, n)

    def read_all_video_frames_source(self) -> list:
        return self.readingTool.read_video_frames_from_path(self.source)
        

    def get_picture__feed_source(self, source: str) -> np.array:
        return self.readingTool.read_picture_from_path(source)

    def get_picture_source(self) -> np.array:
        return self.readingTool.read_picture_from_path(self.source)

    def set_source(self, path: str):
        self.source = path
