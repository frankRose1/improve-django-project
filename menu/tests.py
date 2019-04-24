from datetime import datetime
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
from .models import Menu


class MenuModelTest(TestCase):
    def test_menu_creation(self):
        menu = Menu.objects.create(
          season='summer',
        )
        self.assertEqual(menu.season, 'summer')
        self.assertLessEqual(menu.created_date, timezone.now())


class MenuViewsTests(TestCase):
    
    def setUp(self):
        self.menu = Menu.objects.create(
          season='winter',
          expiration_date=datetime.strptime('12/25/2020 18', '%m/%d/%Y %H')
        )
        self.menu2 = Menu.objects.create(
          season='summer',
          expiration_date=datetime.strptime('08/15/2020 10', '%m/%d/%Y %H')
        )

    
    def test_menu_detail_view(self):
        res = self.client.get(reverse('menu:list'))
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.menu, res.context['menus'])
        self.assertIn(self.menu2, res.context['menus'])
        self.assertTemplateUsed(res, 'menu/list_current_menus.html')

    def test_menu_detail_view(self):
        res = self.client.get(reverse('menu:detail', kwargs={'pk': self.menu.id}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.menu, res.context['menu'])