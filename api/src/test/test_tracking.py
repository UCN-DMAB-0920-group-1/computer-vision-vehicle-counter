from unittest.mock import MagicMock, patch

import cv2
import numpy as np

from src.tracking_module.tracker import Tracker, create_mask


def test_masking():
    # Assign
    image_path = 'api/res/highway_1.jpg'
    image = cv2.imread(image_path)

    # Act
    mask, offset = create_mask(
        image,
        roi=[[0, 0], [1920, 0], [1920, 1080], [0, 1080]],
        bounding_rect=[[0, 0], [1920, 1080]])

    # Assert
    assert mask.any()
    assert offset != None
    assert len(offset) == 2


def test_masking_small():
    # Assign
    image_path = 'api/res/highway_1.jpg'
    tracker = Tracker()
    image = cv2.imread(image_path)

    # Act
    mask, offset = create_mask(
        image,
        roi=[[0, 0], [1, 0], [1, 1], [0, 1]],
        bounding_rect=[[0, 0], [1, 1]])

    # Assert
    assert mask.any()
    assert offset != None
    assert len(offset) == 2
    assert offset == (0, 0)


def test_track_square_mask():
    video_path = 'api/res/highway-1-sec_Trim.mp4'
    tracker = Tracker(should_save=False, should_draw=False)
    mock_function_stream = MagicMock(side_effect=lambda x: x)

    with patch('src.tracking_module.tracker.get_stream', new=mock_function_stream):
        detections = tracker.track(video_path,
                                   roi=[[0, 0], [500, 0], [500, 500], [0, 500]])

    assert type(detections) is dict
    assert len(detections) > 0
    assert 'car' in detections
    assert detections['car'] > 0


def test_track_polygon_mask():
    video_path = 'api/res/highway-1-sec_Trim.mp4'
    tracker = Tracker(should_save=False, should_draw=False)
    mock_function_stream = MagicMock(side_effect=lambda x: x)

    with patch('src.tracking_module.tracker.get_stream', new=mock_function_stream):
        detections = tracker.track(video_path,
                                   roi=[[0, 0], [1, 0], [1, 1], [0, 1]])


def test_track_too_small_mask():
    video_path = "api/res/highway-1-sec_Trim.mp4"
    tracker = Tracker(should_save=False, should_draw=False)
    mock_function_stream = MagicMock(side_effect=lambda x: x)

    with patch('src.tracking_module.tracker.get_stream', new=mock_function_stream):
        detections = tracker.track(video_path,
                                   roi=[[0, 0], [1, 0], [1, 1], [0, 1]])

    assert type(detections) is dict
    assert len(detections) == 0


def test_track_two_points_mask():
    video_path = "api/res/highway-1-sec_Trim.mp4"
    tracker = Tracker(should_save=False, should_draw=False)
    mock_function_stream = MagicMock(side_effect=lambda x: x)

    with patch('src.tracking_module.tracker.get_stream', new=mock_function_stream):
        try:
            detections = tracker.track(video_path,
                                       roi=[[0, 0], [1, 0]])
        except Exception:
            assert True


def test_track_no_roi():
    video_path = "api/res/highway-1-sec_Trim.mp4"
    tracker = Tracker(should_save=False, should_draw=False)
    mock_function_stream = MagicMock(side_effect=lambda x: x)

    with patch('src.tracking_module.tracker.get_stream', new=mock_function_stream):
        detections = tracker.track(video_path)

    assert type(detections) is dict
    assert len(detections) > 0
    assert 'car' in detections
    assert detections['car'] > 0
