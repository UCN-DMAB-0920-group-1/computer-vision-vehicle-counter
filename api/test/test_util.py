import numpy as np
from tracking_module import util as module


def test_uneven_center():
    assert module.center_pos(np.array([[0, 0], [2, 4]])) == (1, 2)


def test_zero_point():
    assert module.center_pos(np.array([[0, 0], [0, 0]])) == (0, 0)


def test_negative_to_postitive():
    assert module.center_pos(np.array([[-1, -1], [1, 1]])) == (0, 0)


def test_rounding():
    assert module.center_pos(np.array([[0, 0], [1, 1]])) == (0, 0)
