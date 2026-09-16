from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import EmotionIngredient, Potion
from .templatetags.brew_tags import vibe_stars, vibe_emoji, percentage


class EmotionIngredientModelTest(TestCase):
    def test_creation_and_str(self):
        em = EmotionIngredient.objects.create(
            name='Joy', emoji='😄', color_hex='#FFD93D',
            css_class='chip-joy', category='POSITIVE'
        )
        self.assertEqual(str(em), '😄 Joy')
        self.assertEqual(em.category, 'POSITIVE')


class PotionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', password='test1234')
        self.joy = EmotionIngredient.objects.create(name='Joy', emoji='😄')
        self.sad = EmotionIngredient.objects.create(name='Sadness', emoji='🌧️')
        self.potion = Potion.objects.create(
            brewer=self.user, title='Test Brew', vibe_rating=7,
            reflection='A test reflection.'
        )
        self.potion.ingredients.set([self.joy, self.sad])

    def test_potion_str(self):
        self.assertIn('Test Brew', str(self.potion))

    def test_vibe_label(self):
        self.assertEqual(self.potion.vibe_label, '😊 Good')

    def test_vibe_percentage(self):
        self.assertEqual(self.potion.vibe_percentage, 70)

    def test_ingredient_count(self):
        self.assertEqual(self.potion.ingredient_count, 2)

    def test_foreign_key_brewer(self):
        self.assertEqual(self.potion.brewer.username, 'tester')

    def test_many_to_many(self):
        names = list(self.potion.ingredients.values_list('name', flat=True))
        self.assertIn('Joy', names)
        self.assertIn('Sadness', names)


class AuthViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('brewmaster', password='secret123')

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_success_redirects(self):
        response = self.client.post(reverse('login'), {
            'username': 'brewmaster', 'password': 'secret123'
        })
        self.assertEqual(response.status_code, 302)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_dashboard_works_authenticated(self):
        self.client.login(username='brewmaster', password='secret123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)


class PotionCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('crafter', password='craft123')
        self.client.login(username='crafter', password='craft123')
        self.joy = EmotionIngredient.objects.create(name='Joy', emoji='😄')
        self.potion = Potion.objects.create(
            brewer=self.user, title='CRUD Test Potion', vibe_rating=6
        )
        self.potion.ingredients.add(self.joy)

    def test_potion_list(self):
        response = self.client.get(reverse('potion_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CRUD Test Potion')

    def test_potion_detail(self):
        response = self.client.get(reverse('potion_detail', kwargs={'pk': self.potion.pk}))
        self.assertEqual(response.status_code, 200)

    def test_potion_create_form_loads(self):
        response = self.client.get(reverse('potion_create'))
        self.assertEqual(response.status_code, 200)

    def test_toggle_favorite(self):
        self.assertFalse(self.potion.is_favorite)
        response = self.client.get(reverse('toggle_favorite', kwargs={'pk': self.potion.pk}))
        self.assertEqual(response.status_code, 302)
        self.potion.refresh_from_db()
        self.assertTrue(self.potion.is_favorite)

    def test_search_filter(self):
        response = self.client.get(reverse('potion_list') + '?q=CRUD')
        self.assertContains(response, 'CRUD Test Potion')
        response = self.client.get(reverse('potion_list') + '?q=nonexistent')
        self.assertNotContains(response, 'CRUD Test Potion')


class TemplateTagTests(TestCase):
    def test_vibe_stars(self):
        self.assertEqual(vibe_stars(3), '⭐⭐⭐☆☆☆☆☆☆☆')
        self.assertEqual(vibe_stars(10), '⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐')

    def test_vibe_emoji(self):
        self.assertEqual(vibe_emoji(1), '💀')
        self.assertEqual(vibe_emoji(10), '✨')
        self.assertEqual(vibe_emoji(5), '🙂')

    def test_percentage(self):
        self.assertEqual(percentage(7, 10), 70)
        self.assertEqual(percentage(0, 10), 0)
