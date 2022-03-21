# computer-vision-vehicle-counter

This project includes a frontend built with with Vue and a backend API built with Python.
The API will detect objects using a machine learning model, currently it's configured to use the Yolov5 model, but can be configured
to use a custom model.

Via the frontend, you can upload a video with different options like ROI (region of interest) and it will be sent to the backend,
where the results will be sent to a database, and showed in the frontend oncec complete.

# Python Dependencies guide:
<br>
- Python version: 3.9.x (tested with 3.9.10)
## Due to pafy having a issue with dislike-count (see https://github.com/mps-youtube/pafy/pull/305#issuecomment-986212672)
- pip install git+https://github.com/Cupcakus/pafy
## Download master for Norfair, due to label function not being released yet.
- pip install git+https://github.com/tryolabs/norfair@master 
- install Pytorch (https://pytorch.org/) tested with both CPU and Cuda(GPU)
- pip install -r requirements.txt (for all dependancy requirements)
- https://github.com/ultralytics/yolov5
- FFmpeg (https://github.com/BtbN/FFmpeg-Builds/releases)<br>

# Frontend vue guide:<br>
- Add a .env file to the root of the frontend folder, containing the API url: <br>
  VUE_APP_PROCESSING_ENDPOINT=<INSERT_API_URL_HERE>
- npm i (to install all node dependencies)


## Sources

- [Highway.mp4](https://www.youtube.com/watch?v=KBsqQez-O4w) - Nick Martinez
