from django.db.models.expressions import result
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habits
from users.models import User


class HabitsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="django@mail.ru")
        self.habit = Habits.objects.create(
            owner=self.user, place="Home", time="12:00:00", action="Зарядка"
        )
        self.client.force_authenticate(user=self.user)

    def test_habits_retrieve(self):
        url = reverse("habits:habits_retrieve", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("place"), self.habit.place)

    def test_habits_create(self):
        url = reverse("habits:habits_create")
        data = {
            "owner": self.user.pk,
            "place": "Home",
            "time": "12:00",
            "action": "Зарядка",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habits.objects.all().count(), 2)

    def test_habits_update(self):
        url = reverse("habits:habits_update", args=(self.habit.pk,))
        data = {
            "place": "Work",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habits.objects.get(pk=self.habit.pk).place, "Work")

    def test_habits_delete(self):
        url = reverse("habits:habits_delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habits.objects.all().count(), 0)

    def test_habits_list(self):
        url = reverse(
            "habits:habits_list",
        )
        response = self.client.get(url)
        data = response.json()
        print(data)
        result_list = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.pk,
                    "place": self.habit.place,
                    "time": self.habit.time,
                    "action": self.habit.action,
                    "is_good": self.habit.is_good,
                    "duration": self.habit.duration,
                    "prize": self.habit.prize,
                    "is_daily": self.habit.is_daily,
                    "is_public": self.habit.is_public,
                    "owner": self.user.pk,
                    "related": self.habit.related,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result_list)
