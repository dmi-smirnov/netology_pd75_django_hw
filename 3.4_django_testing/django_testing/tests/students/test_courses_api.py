# def test_example():
#     assert False, "Just test example"

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture(scope='module')
def course_factory():
    def return_function(**kwargs):
        return baker.make(Course, **kwargs)
    return return_function

@pytest.fixture(scope='module')
def student_factory():
    def return_function(**kwargs):
        return baker.make(Student, **kwargs)
    return return_function

@pytest.fixture(scope='module')
def api_client():
    return APIClient()

@pytest.fixture(scope='module')
def api_base_route():
    return '/api/v1/'

@pytest.fixture(scope='module')
def course_route(api_base_route):
    return f'{api_base_route}courses/'

@pytest.mark.django_db
def test_get_first_course(api_client, course_factory, course_route):
    # Arrange
    course = course_factory()

    # Act
    resp = api_client.get(f'{course_route}{course.id}/')
    
    # Assert
    assert resp.status_code == status.HTTP_200_OK
    
    data = resp.data
    assert isinstance(data, dict)
    assert data['id'] == course.id
    assert data['name'] == course.name


@pytest.mark.django_db
def test_get_list_courses(api_client, course_factory, course_route):
    COURSES_AMT = 100
    
    # Arrange
    courses = course_factory(_quantity=COURSES_AMT)

    # Act
    resp = api_client.get(course_route)

    # Assert
    assert resp.status_code == status.HTTP_200_OK
    
    data = resp.data
    assert isinstance(data, list)
    assert len(data) == COURSES_AMT
    for model_course in courses:
        course = None
        for resp_course in data:
            if resp_course['id'] == model_course.id:
                course = resp_course
                break
        assert course
        assert course['name'] == model_course.name


@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory, course_route):
    COURSES_AMT = 100

    # Arrange
    courses = course_factory(_quantity=COURSES_AMT)
    course = courses[34]

    # Act
    resp = api_client.get(
        path=course_route,
        data={'id': course.id}
    )
                         
    # Assert
    assert resp.status_code == status.HTTP_200_OK

    data = resp.data
    assert isinstance(data, list)
    assert len(data) == 1
    assert isinstance(data[0], dict)
    assert data[0]['id'] == course.id
    assert data[0]['name'] == course.name


@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory, course_route):
    COURSES_AMT = 100

    # Arrange
    courses = course_factory(_quantity=COURSES_AMT)
    course = courses[34]

    # Act
    resp = api_client.get(
        path=course_route,
        data={'name': course.name}
    )
                         
    # Assert
    assert resp.status_code == status.HTTP_200_OK

    data = resp.data
    assert isinstance(data, list)
    assert len(data)
    for resp_course in data:
        assert isinstance(resp_course, dict)
        assert resp_course['name'] == course.name


@pytest.mark.django_db
def test_create_course(api_client, course_route):
    # Arrange
    post_data = {
        'name': 'Test course'
    }

    # Act
    resp = api_client.post(
        path=course_route,
        data=post_data,
        format='json'
    )

    # Assert
    assert resp.status_code == status.HTTP_201_CREATED

    resp_data = resp.data
    assert isinstance(resp_data, dict)
    created_course = Course.objects.get(id=resp_data['id'])
    assert created_course
    assert created_course.name == post_data['name']


@pytest.mark.django_db
def test_update_course(course_factory, api_client, course_route):
    # Arrange
    course = course_factory()
    patch_data = {
        'name': 'Test course'
    }

    # Act
    resp = api_client.patch(
        path=f'{course_route}{course.id}/',
        data=patch_data,
        format='json'
    )

    # Assert
    assert resp.status_code == status.HTTP_200_OK

    updated_course = Course.objects.get(id=course.id)
    assert updated_course.name == patch_data['name']


@pytest.mark.django_db
def test_delete_course(course_factory, api_client, course_route):
    # Arrange
    course = course_factory()

    # Act
    resp = api_client.delete(f'{course_route}{course.id}/')

    # Assert
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    assert not Course.objects.filter(id=course.id)

@pytest.mark.parametrize(
    'students_max_per_course, students_amt, post_status_code, patch_status_code',
    [
        (3, 2, status.HTTP_201_CREATED,     status.HTTP_200_OK),
        (3, 3, status.HTTP_201_CREATED,     status.HTTP_200_OK),
        (3, 4, status.HTTP_400_BAD_REQUEST, status.HTTP_400_BAD_REQUEST),
        (3, 5, status.HTTP_400_BAD_REQUEST, status.HTTP_400_BAD_REQUEST)
    ]
)
@pytest.mark.django_db
def test_validate_max_students_per_course(settings, students_max_per_course,
                                          student_factory, students_amt,
                                          course_factory, api_client,
                                          course_route, post_status_code,
                                          patch_status_code):
    # Arrange
    settings.STUDENTS_MAX_PER_COURSE = students_max_per_course

    students = student_factory(_quantity=students_amt)
    patch_req_course = course_factory()

    req_data = {
        'name': 'Test course',
        'students': [s.id for s in students]
    }

    # Act
    post_resp = api_client.post(
        path=course_route,
        data=req_data,
        format='json'
    )
    patch_resp = api_client.patch(
        path=f'{course_route}{patch_req_course.id}/',
        data=req_data,
        format='json'
    )

    # Assert
    assert post_resp.status_code == post_status_code
    assert patch_resp.status_code == patch_status_code