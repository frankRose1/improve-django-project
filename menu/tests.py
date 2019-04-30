from datetime import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from .models import Menu, Item, Ingredient


class MenuModelTests(TestCase):
    def test_menu_creation(self):
        menu = Menu.objects.create(
          season='summer',
        )
        self.assertEqual(menu.season, 'summer')
        self.assertLessEqual(menu.created_date, timezone.now())


class ItemModelTests(TestCase):
    def test_item_creation(self):
        chef = User.objects.create_user(
            username='top_chef45',
            email='top.chef45@gmail.com',
            password='top_secret_pw'         
        )
        item = Item.objects.create(
            name='Orange Juice',
            standard=False,
            chef=chef   
        )
        self.assertEqual(item.name, 'Orange Juice')
        self.assertEqual(chef.id, item.chef_id)
        self.assertLessEqual(item.created_date, timezone.now())


class IngredientModelTests(TestCase):
    def test_ingredient_creation(self):
        ingredient = Ingredient.objects.create(
            name='sugar'
        )
        self.assertEqual(ingredient.name, 'sugar')
        self.assertEqual(ingredient.id, 1)


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
        self.assertTemplateUsed(res, 'menu/menu_detail.html')


class ItemViewsTests(TestCase):

    def setUp(self):
        self.chef = User.objects.create_user(
          username='testUser123',
          email='test.user@gmail.com',
          password='testPassword567!'
        )
        self.item = Item.objects.create(
            name='New Menu Item',
            standard=True,
            chef=self.chef
        )

    def test_item_detail(self):
        res = self.client.get(reverse('menu:item_detail', kwargs={'pk': self.item.id}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.item, res.context['item'])
        self.assertTemplateUsed(res, 'menu/item_detail.html')
