from unittest.mock import Mock
import api.routes.detections as module
from flask import Flask
from api.app import app


def test_detection_upload():
    # Arrange
    mock_request = Mock()
    mock_file = Mock()

    detection = module.Detections([], 'api/storage/', Mock(), Mock(), 1)

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


def test_detection_upload():
    mock_request = Mock()

    detection = module.Detections([], 'api/storage/', Mock(), Mock(), 1)

    mock_request.form = {'bbox': '[[0, 0], [10, 0], [10, 10], [0, 10]]',
                         'enabled': True,
                         'confidence': 0.7,
                         'maxDistanceBetweenPoints': 20}

    with app.app_context():
        response = detection.upload_video(mock_request)

    assert response.status_code == 200
    assert response.json['id'] != None
