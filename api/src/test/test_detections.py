from unittest.mock import MagicMock, patch

from src.routes.detections import Detections
from src.app import app


def test_detection_upload():
    # Arrange
    mock_request = MagicMock()
    mock_file = MagicMock()

    detection = Detections(
        [], 'api/storage/', MagicMock(), MagicMock(), 1)

    mock_request.form = {'bbox': '[[0, 0], [10, 0], [10, 10], [0, 10]]',
                         'enabled': True,
                         'confidence': 0.7,
                         'maxDistanceBetweenPoints': 20}
    mock_request.files = {'file': mock_file}
    mock_request.configure_mock(content_length=100)

    mock_file.filename = 'test.mp4'

    # Act
    with app.app_context():
        response = detection.upload_video(mock_request)

    # Assert
    assert response.status_code == 200
    assert response.json['id'] != None


def test_get_video():
    # Arrange
    mock_module_flask = MagicMock()
    mock_module_flask.send_from_directory = MagicMock()
    upload_folder = 'api/storage/'

    detection = Detections(
        [], upload_folder, None, None, 1)

    # Act
    with patch('api.routes.detections.send_from_directory', new=mock_module_flask):
        with app.app_context():
            response = detection.get_video('test')

    # Assert
    assert response != None
    assert response


def test_detection_save_file():
    # Arrange
    mock_file = MagicMock()
    mock_module_os = MagicMock()
    upload_folder = 'api/storage/'

    detection = Detections(
        [], upload_folder, None, None, 1)

    mock_file.filename = 'test.mp4'

    # Act
    with patch('api.routes.detections.os', new=mock_module_os):
        with app.app_context():
            response = detection.save_video_file(
                upload_folder + mock_file.filename, mock_file)

    # Assert
    assert response != None
    assert response == 'File saved'
    mock_file.save.assert_called_once
    mock_module_os.mkdir.assert_called_once


def test_detection_save_file_existing_path():
    # Arrange
    mock_file = MagicMock()
    mock_module_os = MagicMock()
    upload_folder = 'api/storage/'

    detection = Detections(
        [], upload_folder, None, None, 1)

    mock_file.filename = 'test.mp4'
    mock_module_os.mkdir.side_effect = FileExistsError()

    # Act
    with patch('api.routes.detections.os', new=mock_module_os):
        with app.app_context():
            response = detection.save_video_file(
                upload_folder + mock_file.filename, mock_file)

    # Assert
    assert response != None
    assert response == 'File saved'
    mock_file.save.assert_called_once
    mock_module_os.mkdir.assert_called_once
