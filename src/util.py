
import pafy


def get_stream(url):
    if(str.startswith(url, "https://")):
        video = pafy.new(url)
        return video.getbest(preftype="mp4").url
    else:
        return url
