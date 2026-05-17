from django.test import TestCase, RequestFactory
from django.contrib import admin
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest

import json

from search_admin_autocomplete.admin import SearchAutoCompleteAdmin
from sample.models import DummyModel, Client, Category


class GetFieldValueTest(TestCase):
    """Test _get_field_value method with direct and related fields."""

    def setUp(self):
        self.client_obj = Client.objects.create(name='Test Client', email='test@example.com')
        self.category_obj = Category.objects.create(title='Test Category', slug='test-category')
        self.instance = DummyModel.objects.create(
            name='Test Item',
            description='Test Description',
            client=self.client_obj,
            category=self.category_obj
        )
        self.admin = SearchAutoCompleteAdmin(DummyModel, admin.site)

    def test_direct_field(self):
        """Test getting direct field value."""
        result = self.admin._get_field_value(self.instance, 'name')
        self.assertEqual(result, 'Test Item')

    def test_direct_field_null(self):
        """Test getting direct field that is null."""
        self.instance.name = None
        self.instance.save()
        result = self.admin._get_field_value(self.instance, 'name')
        self.assertIsNone(result)

    def test_related_field(self):
        """Test getting related field value (FK__field)."""
        result = self.admin._get_field_value(self.instance, 'client__name')
        self.assertEqual(result, 'Test Client')

    def test_related_field_second_relation(self):
        """Test getting another related field value."""
        result = self.admin._get_field_value(self.instance, 'category__title')
        self.assertEqual(result, 'Test Category')

    def test_related_field_null_fk(self):
        """Test getting related field when FK is null."""
        self.instance.client = None
        self.instance.save()
        result = self.admin._get_field_value(self.instance, 'client__name')
        self.assertIsNone(result)

    def test_nested_related_field(self):
        """Test that nested relations return None gracefully."""
        result = self.admin._get_field_value(self.instance, 'client__email')
        self.assertEqual(result, 'test@example.com')


class GetInstanceNameTest(TestCase):
    """Test get_instance_name method with various field configurations."""

    def setUp(self):
        self.client_obj = Client.objects.create(name='Test Client', email='test@example.com')
        self.category_obj = Category.objects.create(title='Test Category', slug='test-category')
        self.admin = SearchAutoCompleteAdmin(DummyModel, admin.site)

    def test_direct_fields_only(self):
        """Test instance name with direct fields only."""
        instance = DummyModel.objects.create(name='Item', description='Desc')
        self.admin.search_fields = ['name', 'description']
        result = self.admin.get_instance_name(instance)
        self.assertEqual(result, 'Item, Desc')

    def test_related_fields_only(self):
        """Test instance name with related fields only."""
        instance = DummyModel.objects.create(
            name='Item',
            client=self.client_obj,
            category=self.category_obj
        )
        self.admin.search_fields = ['client__name', 'category__title']
        result = self.admin.get_instance_name(instance)
        self.assertEqual(result, 'Test Client, Test Category')

    def test_mixed_fields(self):
        """Test instance name with mix of direct and related fields."""
        instance = DummyModel.objects.create(
            name='Item',
            description='Desc',
            client=self.client_obj,
            category=self.category_obj
        )
        self.admin.search_fields = ['name', 'client__name', 'category__title']
        result = self.admin.get_instance_name(instance)
        self.assertEqual(result, 'Item, Test Client, Test Category')

    def test_null_related_field_skipped(self):
        """Test that null related fields are skipped."""
        instance = DummyModel.objects.create(
            name='Item',
            client=None,
            category=self.category_obj
        )
        self.admin.search_fields = ['name', 'client__name', 'category__title']
        result = self.admin.get_instance_name(instance)
        self.assertEqual(result, 'Item, Test Category')

    def test_all_null_fields(self):
        """Test instance name when all fields are null."""
        instance = DummyModel.objects.create(name=None, client=None, category=None)
        self.admin.search_fields = ['name', 'client__name', 'category__title']
        result = self.admin.get_instance_name(instance)
        self.assertEqual(result, '')


class SearchAPITest(TestCase):
    """Test search_api endpoint."""

    def setUp(self):
        self.factory = RequestFactory()
        self.client_obj = Client.objects.create(name='Acme Corp', email='acme@example.com')
        self.category_obj = Category.objects.create(title='Electronics', slug='electronics')
        self.item1 = DummyModel.objects.create(
            name='Widget',
            description='A widget',
            client=self.client_obj,
            category=self.category_obj
        )
        self.item2 = DummyModel.objects.create(
            name='Gadget',
            description='A gadget',
            client=self.client_obj,
            category=self.category_obj
        )
        self.item3 = DummyModel.objects.create(
            name='Thingamajig',
            description='Something else',
            client=None,
            category=None
        )
        self.admin = SearchAutoCompleteAdmin(DummyModel, admin.site)
        self.admin.search_fields = ['name', 'client__name']

    def test_search_direct_field(self):
        """Test searching by direct field."""
        self.admin.search_fields = ['name']
        request = self.factory.get('/admin/sample/dummymodel/search/Widget')
        response = self.admin.search_api(request, 'Widget')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['keyword'], 'Widget')

    def test_search_related_field(self):
        """Test searching by related field."""
        self.admin.search_fields = ['client__name']
        request = self.factory.get('/admin/sample/dummymodel/search/Acme')
        response = self.admin.search_api(request, 'Acme')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

    def test_search_mixed_fields(self):
        """Test searching by mix of direct and related fields."""
        self.admin.search_fields = ['name', 'client__name']
        request = self.factory.get('/admin/sample/dummymodel/search/Acme')
        response = self.admin.search_api(request, 'Acme')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

    def test_search_no_results(self):
        """Test search with no matching results."""
        self.admin.search_fields = ['name']
        request = self.factory.get('/admin/sample/dummymodel/search/NonExistent')
        response = self.admin.search_api(request, 'NonExistent')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 0)

    def test_search_no_fields_defined(self):
        """Test search when no search_fields defined."""
        self.admin.search_fields = []
        request = self.factory.get('/admin/sample/dummymodel/search/test')
        response = self.admin.search_api(request, 'test')
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_search_respects_max_results(self):
        """Test that search respects max_results limit."""
        self.admin.search_fields = ['name']
        self.admin.max_results = 1
        request = self.factory.get('/admin/sample/dummymodel/search/a')
        response = self.admin.search_api(request, 'a')
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

    def test_search_response_format(self):
        """Test that search response has correct format."""
        self.admin.search_fields = ['name']
        request = self.factory.get('/admin/sample/dummymodel/search/Widget')
        response = self.admin.search_api(request, 'Widget')
        data = json.loads(response.content)
        self.assertIn('keyword', data[0])
        self.assertIn('url', data[0])
