from django.test import TestCase
from django.urls import reverse

from .models import Performance


class PetCrudTests(TestCase):
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
