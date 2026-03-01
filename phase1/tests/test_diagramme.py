import pytest

from phase1.src.diagramme_triangulation import centre_cercle_circonscrit, cross_product, distance

def test_should_return_zero_given_collinear_points():
    p1, p2, p3 = (0, 0), (1, 1), (2, 2)
    result = cross_product(p1, p2, p3)
    assert result == 0

def test_should_return_positive_given_counter_clockwise_points():
    p1, p2, p3 = (0, 0), (1, 0), (0, 1)
    result = cross_product(p1, p2, p3)
    assert result > 0

def test_should_return_negative_given_clockwise_points():
    p1, p2, p3 = (0, 0), (0, 1), (1, 0)
    result = cross_product(p1, p2, p3)
    assert result < 0

def test_should_return_middle_of_hypotenuse_given_right_triangle():
    p1, p2, p3 = (0, 0), (4, 0), (0, 4)
    result = centre_cercle_circonscrit(p1, p2, p3)
    assert result == (2.0, 2.0)

def test_should_return_origin_given_symmetric_triangle():
    p1, p2, p3 = (-2, 0), (2, 0), (0, 2)
    result = centre_cercle_circonscrit(p1, p2, p3)
    assert result == (0.0, 0.0)

def test_should_return_zero_given_identical_points():
    p1, p2 = (5, 5), (5, 5)
    result = distance(p1, p2)
    assert result == 0

def test_should_return_squared_euclidean_distance_given_different_points():
    p1, p2 = (0, 0), (3, 4)
    result = distance(p1, p2)
    assert result == 25