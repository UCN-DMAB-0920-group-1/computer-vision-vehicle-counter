from unittest.mock import Mock
import detections as module


def test_():
    mock = Mock()
    Detection = module.Detections([], 'api/storage/', Mock(), Mock())

    mock.form = {'bbox': [[0, 0], [10, 0], [10, 10], [0, 10]]}

    print(mock.form['bbox'])

    Detection.upload_video(mock)


test_()
