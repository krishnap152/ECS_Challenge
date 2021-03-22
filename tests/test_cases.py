import requests


def test_course_check_status_code_equals_200():
    response = requests.get("http://localhost:5000/course/101")
    assert response.status_code == 200

def test_course_check_status_code_equals_404():
    response = requests.get("http://localhost:5000/course/1001")
    assert response.status_code == 404


