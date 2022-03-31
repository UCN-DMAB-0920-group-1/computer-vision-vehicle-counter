from unittest.mock import MagicMock, patch
from src.tracking_module.tracking import Tracking
import cv2


def test_tracking():
    # Assign
    image_path = 'api/res/highway_1.jpg'
    tracker = Tracking(roi_area=[[0, 0], [1920, 0], [1920, 1080], [0, 1080]])
    image = cv2.imread(image_path)

    # Act
    mask, offset = tracker.mask_create(image)

    # Assert
    assert mask.any()
    assert offset != None
    assert len(offset) == 2


def test_track_small_roi():
    image_path = 'api/res/highway_1.jpg'
    tracker = Tracking(roi_area=[[0, 0], [1, 0], [1, 1], [0, 1]])
    mock_module_opencv = MagicMock()

    mock_stream = MagicMock()
    mock_stream.side_effect = image_path

    with patch('api.routes.detections.send_from_directory', new=mock_module_opencv):
        pass
