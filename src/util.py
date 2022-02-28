
import pafy


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
