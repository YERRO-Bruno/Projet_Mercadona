from django.core.wsgi import get_wsgi_application

from django.test import TestCase
from mercadona.models import Category

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.create_category(Category(), label="TestCategory")['obj']

    def test_create_category(self):
        self.assertEqual(self.category.label, "TestCategory")

    def test_create_category_label_existant_deja(self):
        self.category = Category.create_category(Category(), label="TestCategory")['obj']
        self.assertIsNone(self.category)

    def test_create_category_empty_label(self):
        self.category = Category.create_category(Category(), label="")['obj']
        self.assertIsNone(self.category)

    def test_update_category(self):
        self.category_updated = Category.update_category(self=Category(), category_id=self.category.id,
                                                         label="NouveauLabel")['obj']
        self.assertEqual(self.category_updated.label, "NouveauLabel")

    def test_update_category_inexistent(self):
        self.category = Category.update_category(self=Category(), category_id=12345, label="NouveauLabel")['obj']
        self.assertIsNone(self.category)

    def test_delete_category(self):
        is_delete = Category.delete_category(self=Category(), category_id=self.category.id)['obj']
        self.assertTrue(is_delete)

    def test_delete_category_inexistante(self):
        is_deleted = Category.delete_category(self=Category(), category_id=12345)['obj']
        self.assertFalse(is_deleted)