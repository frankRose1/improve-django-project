from django.test import TestCase
from django.utils import timezone
from .models import Menu


class MenuModelTest(TestCase):
    def test_menu_creation(self):
        menu = Menu.object.create(

        )
        now = timezone.now()
        self.assertLess(menu.created_at, now)
