from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from pdm.apps.demographics.tests.factories import (
    VillageFactory
)
from pdm.apps.financial_inclusion.models import (
    Initiative,
    BusinessDevelopmentService
)

client = APIClient()


class FinancialInclusionGETMethodsAPITest(APITestCase):
    def setUp(self):
        self.vilage = VillageFactory.create()
        self.initiative = Initiative.objects.create(
            name="Savings"
        )
        self.training = BusinessDevelopmentService.objects.create(
            initiative=self.initiative,
            village = self.vilage,
            budget_spend = 290000,
            attendance = 50,
            date = '2022-02-04',
            topic = "Savings Agenda"
        )

    def test_can_get_trainings_national_dashboard_data(self):
        url = reverse("trainings_national_dashboard")
        response = client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)









