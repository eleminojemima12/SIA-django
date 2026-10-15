from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Performance


class PetCrudTests(TestCase):
    def test_dashboard_has_links_to_separate_pages(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your pet dashboard')
        self.assertContains(response, f'href="{reverse("pet_list")}"')
        self.assertContains(response, f'href="{reverse("pet_gallery")}"')
        self.assertNotContains(response, 'id="management"')
        self.assertNotContains(response, 'id="gallery"')

    def test_pet_management_and_gallery_have_separate_pages(self):
        pet = Performance.objects.create(
            pet_id=202,
            pet_name='Clover',
            pet_type='Cat',
            breed='Tabby',
            age=2,
            gender='Female',
            owner_name='Jamie Lee',
            contact_number='0700000000',
            date_registered='2026-10-15',
        )

        management_response = self.client.get(reverse('pet_list'))
        gallery_response = self.client.get(reverse('pet_gallery'))

        self.assertEqual(management_response.status_code, 200)
        self.assertContains(management_response, 'Pet management')
        self.assertContains(management_response, 'Clover')
        self.assertContains(management_response, 'aria-current="page"')
        self.assertEqual(gallery_response.status_code, 200)
        self.assertContains(gallery_response, 'Pet gallery')
        self.assertContains(gallery_response, 'Clover')
        self.assertContains(gallery_response, reverse('pet_detail', args=[pet.pk]))
        self.assertContains(gallery_response, 'aria-current="page"')

    def test_home_is_a_separate_welcome_page(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A happier home for every pet.')
        self.assertContains(response, f'href="{reverse("dashboard")}"')
        self.assertContains(response, f'href="{reverse("pet_list")}"')
        self.assertContains(response, f'href="{reverse("pet_gallery")}"')
        self.assertContains(response, f'href="{reverse("account_create")}"')
        self.assertContains(response, 'aria-current="page"')

    def test_login_and_sign_out(self):
        user = User.objects.create_user(username='pet-owner', password='safe-test-password')

        login_response = self.client.get(reverse('login'))
        self.assertEqual(login_response.status_code, 200)
        self.assertContains(login_response, 'Log in to Paw &amp; Co')
        self.assertContains(login_response, 'Log in')

        response = self.client.post(
            reverse('login'),
            {'username': user.username, 'password': 'safe-test-password'},
        )
        self.assertRedirects(response, reverse('dashboard'))

        dashboard_response = self.client.get(reverse('dashboard'))
        self.assertContains(dashboard_response, 'pet-owner')
        self.assertContains(dashboard_response, 'Sign out')

        logout_response = self.client.post(reverse('logout'))
        self.assertRedirects(logout_response, reverse('index'))
        self.assertContains(self.client.get(reverse('index')), 'Log in')

    def test_account_creation_validates_password_and_signs_user_in(self):
        response = self.client.get(reverse('account_create'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create your account')
        self.assertContains(response, f'href="{reverse("login")}"')

        response = self.client.post(
            reverse('account_create'),
            {
                'username': 'new-pet-owner',
                'password1': 'A-Strong-Passphrase-482!',
                'password2': 'A-Strong-Passphrase-482!',
            },
        )

        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(User.objects.filter(username='new-pet-owner').exists())
        self.assertContains(self.client.get(reverse('dashboard')), 'new-pet-owner')

    def test_account_creation_rejects_mismatched_passwords(self):
        response = self.client.post(
            reverse('account_create'),
            {
                'username': 'new-pet-owner',
                'password1': 'A-Strong-Passphrase-482!',
                'password2': 'Another-Strong-Passphrase-482!',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The two password fields didn’t match.')
        self.assertFalse(User.objects.filter(username='new-pet-owner').exists())

    def test_pet_crud_flow(self):
        create_url = reverse('pet_create')
        list_url = reverse('pet_list')

        response = self.client.post(
            create_url,
            {
                'pet_id': 101,
                'pet_name': 'Buddy',
                'pet_type': 'Dog',
                'breed': 'Labrador',
                'age': 3,
                'gender': 'Male',
                'owner_name': 'Alice Johnson',
                'contact_number': '0712345678',
                'date_registered': '2026-09-23',
            },
        )

        self.assertEqual(response.status_code, 302)
        pet = Performance.objects.get(pet_name='Buddy')
        self.assertEqual(pet.owner_name, 'Alice Johnson')

        response = self.client.get(list_url)
        self.assertContains(response, 'Buddy')

        update_url = reverse('pet_update', args=[pet.pk])
        response = self.client.post(
            update_url,
            {
                'pet_id': 101,
                'pet_name': 'Buddy',
                'pet_type': 'Dog',
                'breed': 'Golden Retriever',
                'age': 4,
                'gender': 'Male',
                'owner_name': 'Alice Johnson',
                'contact_number': '0712345679',
                'date_registered': '2026-09-23',
            },
        )
        self.assertEqual(response.status_code, 302)
        pet.refresh_from_db()
        self.assertEqual(pet.breed, 'Golden Retriever')
        self.assertEqual(pet.contact_number, '0712345679')

        delete_url = reverse('pet_delete', args=[pet.pk])
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Performance.objects.filter(pk=pet.pk).exists())
