# def test_example():
#     assert False, "Just test example"

from django.test import override_settings
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
    resp = api_client.get(f'{course_route}?id={course.id}')
                         
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
    resp = api_client.get(f'{course_route}?name={course.name}')
                         
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


@pytest.mark.django_db
@override_settings(STUDENTS_MAX_PER_COURSE=3)
def test_validate_max_students_per_course(settings, student_factory,
                                          course_factory, api_client,
                                          course_route):
    # Arrange
    settings.STUDENTS_MAX_PER_COURSE = 3

    students = student_factory(_quantity=settings.STUDENTS_MAX_PER_COURSE + 1)
    ok_patch_req_course = course_factory()
    bad_patch_req_course = course_factory()

    ok_req_data = {
        'name': 'Test course',
        'students': [s.id for s in students[:settings.STUDENTS_MAX_PER_COURSE]]
    }

    bad_req_data = {
        'name': 'Test course',
        'students': [s.id for s in students]
    }

    # Act
    ok_post_resp = api_client.post(
        path=course_route,
        data=ok_req_data,
        format='json'
    )
    ok_patch_resp = api_client.patch(
        path=f'{course_route}{ok_patch_req_course.id}/',
        data=ok_req_data,
        format='json'
    )
    bad_post_resp = api_client.post(
        path=course_route,
        data=bad_req_data,
        format='json'
    )
    bad_patch_resp = api_client.patch(
        path=f'{course_route}{bad_patch_req_course.id}/',
        data=bad_req_data,
        format='json'
    )

    # Assert
    assert ok_post_resp.status_code == status.HTTP_201_CREATED
    ok_post_resp_data = ok_post_resp.data
    assert isinstance(ok_post_resp_data, dict)
    assert 'id' in ok_post_resp_data
    created_course = Course.objects.get(id=ok_post_resp_data['id'])
    assert created_course.students.count() <= settings.STUDENTS_MAX_PER_COURSE

    assert ok_patch_resp.status_code == status.HTTP_200_OK
    assert ok_patch_req_course.students.count() <= settings.STUDENTS_MAX_PER_COURSE

    assert bad_post_resp.status_code == status.HTTP_400_BAD_REQUEST

    assert bad_patch_resp.status_code == status.HTTP_400_BAD_REQUEST