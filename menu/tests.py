from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from .models import Menu, Item, Ingredient
from .forms import MenuForm


class MenuModelTests(TestCase):
    def setUp(self):
        self.menu = Menu.objects.create(
            season='summer',
        )

    def test_menu_creation(self):
        self.assertEqual(self.menu.season, 'summer')
        self.assertLessEqual(self.menu.created_date, timezone.now())

    def test_get_absolute_url(self):
        url = self.menu.get_absolute_url()
        self.assertEqual(f'/menu/{self.menu.id}/', url)

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
            expiration_date=timezone.make_aware(datetime.strptime('12/25/2020 18', '%m/%d/%Y %H'))
        )
        self.menu2 = Menu.objects.create(
            season='summer',
            expiration_date=timezone.make_aware(datetime.strptime('08/15/2020 10', '%m/%d/%Y %H'))
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

    # TODO --> test may be failing because date is not properly formatted and form is not submitting
    # def test_post_new_menu_view(self):
    #     data = {
    #         'season': 'Posting A New Menu',
    #         'expiration_date_year': 2021,
    #         'expiration_date_month': 10,
    #         'expiration_date_day': 15,
    #         # 'items': [1, 4, 6], 
    #     }
    #     res = self.client.post(reverse('menu:new'), data=data)
    #     self.assertRedirects(res, '/menu/4', status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(res, 'menu/menu_detail.html')


class MenuFormTests(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            name='Strawberry Soda',
            standard=True,
            chef=User.objects.create(
                username='cool.chef',
                email='coo.chef@gmail.com',
                password='password123'
            )
        )

    def test_valid_data(self):
        form = MenuForm({
                'season': 'Posting A New Menu',
                'expiration_date_year': 2022,
                'expiration_date_month': 10,
                'expiration_date_day': 15,
                'items': [self.item.id]
            })
        self.assertTrue(form.is_valid())
        menu = form.save()
        self.assertEqual(menu.season, 'Posting A New Menu')
        self.assertLessEqual(menu.expiration_date, timezone.make_aware(datetime.strptime('2022 10 15', '%Y %m %d')))

    def test_invalid_data(self):
        form =  MenuForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'season': ['This field is required.'],
            'items': ['This field is required.']
        })

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
        self.assertTemplateUsed(res, 'menu/item_list.html')