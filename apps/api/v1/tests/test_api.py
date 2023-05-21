from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from apps.users.models import Student, User


# Task 6
class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {
            "username": "sanjarbek",
            "email": "sanjarbek@gmail.com",
            "password": "sanjarbek@123456",
            "password2": "sanjarbek@123456"
        }
        response = self.client.post(reverse("auth-register"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class StudentViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user",
            email="testuser@gmail.com",
            password="12346"
        )
        self.user_2 = User.objects.create_user(username="test", email="test@gamil.com", password="123456")
        self.student = Student.objects.create(user=self.user, university="TDTU")

    def tearDown(self):
        print(f"{self._testMethodName} Done 👍")

    def test_get_student_detail(self):
        url = reverse('student-info', kwargs={"pk": self.student.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_create(self):
        url = reverse('student-create')
        data = {
            'user': {
                "username": "test1", "email": "test2@gmail.com", "fullname": "Sanjarbek"
            },
            'university': 'University 2',
            "contract": 150000
        }
        self.client.login(username='admin@gmail.com', password='admin@123456')
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)

    def test_update_student(self):
        url = reverse('student-update', kwargs={"pk": self.student.pk})
        data = {'university': 'TATU', 'contract': 25000000}

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['university'], 'TATU')
        self.assertEqual(response.data['contract'], 25000000)

    def test_delete_student(self):
        url = reverse('student-delete', kwargs={"pk": self.student.pk})
        self.client.login(username='admin@gmail.com', password='admin@123456')

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), 0)
