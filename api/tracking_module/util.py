from cv2 import Algorithm
import pafy
import jwt as pyjwt
import numpy as np


def get_stream(url: str) -> str:

    # If the url is a m3u8 stream, return url
    if (str.endswith(url, ".m3u8")):
        return url

    # url is a youtube stream, let pafy work its magic to find the m3u8 link
    if (str.startswith(url, "https://www.youtube.com")):
        video = pafy.new(url)
        return video.getbest(preftype="mp4").url
    else:
        return url  # url is most likely a file, return path


def center_pos(tracked_points: np.ndarray) -> tuple[int, int]:
    num_points = tracked_points.shape[0]
    sum_x = np.sum(tracked_points[:, 0])
    sum_y = np.sum(tracked_points[:, 1])
    return int(sum_x / num_points), int(sum_y / num_points)


def get_payload_from_jwt(request, key, secret_key):
    if "Authorization" in request.headers:
        jwt = (request.headers["Authorization"])
        headers = pyjwt.get_unverified_header(jwt)
        try:
            _token = pyjwt.decode(jwt=jwt,
                                  key=secret_key,
                                  algorithms=headers["alg"])
            return _token[key]
        except:
            pass
