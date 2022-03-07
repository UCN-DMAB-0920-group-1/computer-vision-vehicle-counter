
import pafy
import numpy as np
from typing import Tuple


def get_stream(url):

    # If the url is a m3u8 stream, return url
    if(str.endswith(url, ".m3u8")):
        return url

    # url is a youtube stream, let pafy work its magic to find the m3u8 link
    if(str.startswith(url, "https://www.youtube.com")):
        video = pafy.new(url)
        return video.getbest(preftype="mp4").url
    else:
        return url  # url is most likely a file, return path


def centroid(tracked_points: np.array) -> Tuple[int, int]:
    num_points = tracked_points.shape[0]
    sum_x = np.sum(tracked_points[:, 0])
    sum_y = np.sum(tracked_points[:, 1])
    return int(sum_x / num_points), int(sum_y / num_points)
