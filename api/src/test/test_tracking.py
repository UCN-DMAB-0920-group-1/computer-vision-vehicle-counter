from unittest.mock import MagicMock, patch

import cv2
import numpy as np
from tracker import Tracker


def test_masking():
    # Assign
    image_path = 'api/res/highway_1.jpg'
    tracker = Tracker(roi_area=[[0, 0], [1920, 0], [1920, 1080], [0, 1080]])
    image = cv2.imread(image_path)

    # Act
    mask, offset = tracker.mask_create(image)

    # Assert
    assert mask.any()
    assert offset != None
    assert len(offset) == 2


def test_masking_small():
    # Assign
    image_path = 'api/res/highway_1.jpg'
    tracker = Tracker(roi_area=[[0, 0], [1, 0], [1, 1], [0, 1]])
    image = cv2.imread(image_path)

    # Act
    mask, offset = tracker.mask_create(image)

    # Assert
    assert mask.any()
    assert offset != None
    assert len(offset) == 2
    assert offset == (0, 0)


def test_track_square_mask():
    video_path = 'api/res/highway-1-sec_Trim.mp4'
    tracker = Tracker(
        roi_area=[[0, 0], [500, 0], [500, 500], [0, 500]], should_save=False, should_draw=False)
    mock_function_stream = MagicMock(side_effect=lambda x: x)

    with patch('src.tracking_module.tracking.get_stream', new=mock_function_stream):
        detections = tracker.track(video_path)

    assert type(detections) is dict
    assert len(detections) > 0
    assert 'car' in detections
    assert detections['car'] > 0


def test_track_polygon_mask():
    video_path = 'api/res/highway-1-sec_Trim.mp4'
    tracker = Tracker(
        roi_area=[[0, 0], [1, 0], [1, 1], [0, 1]], should_save=False, should_draw=False)
    mock_function_stream = MagicMock(side_effect=lambda x: x)

    with patch('src.tracking_module.tracking.get_stream', new=mock_function_stream):
        detections = tracker.track(video_path)


def test_track_too_small_mask():
    video_path = "api/res/highway-1-sec_Trim.mp4"
    tracker = Tracker(
        roi_area=[[0, 0], [1, 0], [1, 1], [0, 1]], should_save=False, should_draw=False)
    mock_function_stream = MagicMock(side_effect=lambda x: x)

    with patch('src.tracking_module.tracking.get_stream', new=mock_function_stream):
        detections = tracker.track(video_path)

    assert type(detections) is dict
    assert len(detections) == 0


def test_track_two_points_mask():
    video_path = "api/res/highway-1-sec_Trim.mp4"
    tracker = Tracker(
        roi_area=[[0, 0], [1, 0], [1, 1], [0, 1]], should_save=False, should_draw=False)
    mock_function_stream = MagicMock(side_effect=lambda x: x)

    with patch('src.tracking_module.tracking.get_stream', new=mock_function_stream):
        try:
            detections = tracker.track(video_path)
        except Exception:
            pass

    assert detections is None


def test_track_no_roi():
    video_path = "api/res/highway-1-sec_Trim.mp4"
    tracker = Tracker(should_save=False, should_draw=False)
    mock_function_stream = MagicMock(side_effect=lambda x: x)

    with patch('src.tracking_module.tracking.get_stream', new=mock_function_stream):
        detections = tracker.track(video_path)

    assert tracker.roi_area == np.array(
        [[0, 0], [1280, 0], [1280, 720], [0, 720]])
