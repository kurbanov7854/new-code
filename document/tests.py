from django.contrib.auth.models import User, Group
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from .models import Document
from .factory import populate_test_db_users, populate_test_db_docs


class TestDocumentRulesGet(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('documents-list')
        # create user and group
        populate_test_db_users(User, Group)
        # create docs for users
        populate_test_db_docs(Document)

    def test_sergeant_permissions(self):
        self.client.login(username='sergeant', password='123456')
        self.response = self.client.get(self.url)
        print(self.response.json())
        self.assertContains(self.response, text='private document', status_code=200)

    def test_sergeant_no_permissions(self):
        self.client.login(username='sergeant', password='123456')
        self.response = self.client.get(self.url)
        print(self.response.json())
        self.assertNotContains(self.response, text='secret document', status_code=200)

    def test_general_create_error(self):
        self.client.login(username='general', password='123456')
        data = {
            'title':'asdasds',
            'status':'active',
            'text':'1223',
            'date_expired':'2020-06-06',
            'document_root':'public'
        }
        self.response = self.client.post(self.url,data)
        self.assertContains(self.response,text='YOu have no permissions!', status_code=400)


    def test_president_create(self):
        self.client.login(username='president', password='123456')
        data = {
            'title':'asdasds',
            'status':'active',
            'text':'1223',
            'date_expired':'2020-06-06',
            'document_root':'public'
        }
        self.response = self.client.post(self.url,data)
        self.assertEqual(self.response.status_code,status.HTTP_201_CREATED)

