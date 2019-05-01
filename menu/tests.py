from datetime import datetime
from django.urls import reverse
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
        # self.chef = User.objects.create_user(
        #     username='gordon.ramsay',
        #     email='gordon.ramsay@gmail.com',
        #     password='top_secret_pw'         
        # )
        self.menu = Menu.objects.create(
            season='winter',
            expiration_date=datetime.strptime('12/25/2020 18', '%m/%d/%Y %H')
        )
        self.menu2 = Menu.objects.create(
            season='summer',
            expiration_date=datetime.strptime('08/15/2020 10', '%m/%d/%Y %H')
        )
        # self.item = Item.objects.create(
        #     title='Testing Item',
        #     chef=self.chef,
        #     description='Lorem ipsum lorem ipsum lorem ipsum loprem',
        #     standard=True
        # )

    
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

    def test_get_new_menu_view(self):
        res = self.client.get(reverse('menu:new'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed('menu/menu_form.html')

    def test_get_edit_menu_view(self):
        res = self.client.get(reverse('menu:edit', kwargs={'pk': self.menu.id}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['form'].instance, self.menu)
        self.assertTemplateUsed('menu/menu_form.html')

    def test_post_new_menu_view(self):
        data = {
            'season': 'Posting A New Menu',
            'expiration_date': datetime.strptime('09/12/2021 10', '%m/%d/%Y %H'),
            'items': ['one item', 'two item'],
            
        }
        res = self.client.post(reverse('menu:new'), data=data)
        self.assertEquals(res.status_code, 200)
        self.assertRedirects(res, '/menu/4', status_code=302, target_status_code=200)

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
        self.item2 = Item.objects.create(
            name='Another Menu Item',
            standard=False,
            chef=self.chef
        )
        self.item3 = Item.objects.create(
            name='Third Menu Item!!!',
            standard=True,
            chef=self.chef
        )

    def test_item_detail_view(self):
        res = self.client.get(reverse('menu:item_detail', kwargs={'pk': self.item.id}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.item, res.context['item'])
        self.assertTemplateUsed(res, 'menu/item_detail.html')

    def test_item_list_view(self):
        res = self.client.get(reverse('menu:item_list'))
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.item, res.context['items'])
        self.assertIn(self.item2, res.context['items'])
        self.assertIn(self.item3, res.context['items'])
        self.assertTemplateUsed(res, 'menu/item_list.html')