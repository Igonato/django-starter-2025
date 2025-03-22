from django.test import TestCase

from .models import User


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser", email="test@example.com"
        )
        self.user.set_password("password123")
        self.user.save()

    def test_user_creation(self):
        """Test that a user can be created"""
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")

    def test_password_set(self):
        """Test that password is set correctly"""
        self.assertTrue(self.user.check_password("password123"))
        self.assertFalse(self.user.check_password("wrongpassword"))

    def test_user_saved(self):
        """Test that the user was saved to the database"""
        saved_user = User.objects.get(username="testuser")
        self.assertEqual(saved_user.email, "test@example.com")
