from django.test import TestCase
from mercadona.models import VerifAdmin


class VerifAdminModelTest(TestCase):
    def setUp(self):
        self.verifadmin = VerifAdmin.create_verifadmin(VerifAdmin(), verif_email="person@gmail.com")['obj']

    def test_create_verifadmin(self):
        self.assertEqual(self.verifadmin.email, "person@gmail.com")
        self.assertEqual(self.verifadmin.verification, "")

    def test_create_verifadmin_None_email(self):
        self.verifadmin = VerifAdmin.create_verifadmin(VerifAdmin(), verif_email=None)['obj']
        self.assertIsNone(self.verifadmin)

    def test_create_verifadmin_empty_email(self):
        self.verifadmin = VerifAdmin.create_verifadmin(VerifAdmin(), verif_email="")['obj']
        self.assertIsNone(self.verifadmin)

    def test_update_verifadmin(self):
        self.verifadmin_updated = VerifAdmin.update_verifadmin(VerifAdmin(), email=self.verifadmin.email,
                                                               verification="hashverification")['obj']
        self.assertEqual(self.verifadmin_updated.verification, "hashverification")

    def test_update_verifadmin_None_id(self):
        self.verifadmin_updated = VerifAdmin.update_verifadmin(VerifAdmin(), email=None,
                                                               verification="hashverification")['obj']
        self.assertEqual(self.verifadmin_updated, False)

    def test_update_verifadmin_None_email(self):
        self.verifadmin_updated = VerifAdmin.update_verifadmin(VerifAdmin(), email="",
                                                               verification="hashverification")['obj']
        self.assertEqual(self.verifadmin_updated, False)

    def test_delete_verifadmin(self):
        is_deleted = VerifAdmin.delete_verifadmin(VerifAdmin(), email=self.verifadmin.email)['obj']
        self.assertTrue(is_deleted)

    def test_delete_verifadmin_None_email(self):
        is_deleted = VerifAdmin.delete_verifadmin(VerifAdmin(), email=None)['obj']
        self.assertFalse(is_deleted)

    def test_delete_verifadmin_empty_id(self):
        is_deleted = VerifAdmin.delete_verifadmin(VerifAdmin(), email="")['obj']
        self.assertFalse(is_deleted)
