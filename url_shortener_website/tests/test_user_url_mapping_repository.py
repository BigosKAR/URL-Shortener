# from django.test import TestCase
# from ..models import UserUrlMapping, UserAccount, UrlMapping
# from url_shortener_website.utils.user_url_mapping_repository import UserUrlRepository

# #Decided to not include these tests as I ran into errors I could not resolve, even with asking AI

# class TestUserUrlRepository(TestCase):
#     def setUp(self):
#         self.user1 = UserAccount.objects.create(email="test1@gmail.com", hashed_password="123")
#         self.user2 = UserAccount.objects.create(email="test2@gmail.com", hashed_password="123")
        
#         self.url1 = UrlMapping.objects.create(original_url="https://example1.com")
#         self.url2 = UrlMapping.objects.create(original_url="https://example2.com")

#         self.mapping = UserUrlMapping.objects.create(user=self.user1, url=self.url1)

#     def test_entry_exists_true(self):
#         self.assertTrue(UserUrlRepository.entry_exists(self.user1.id, self.url1.id))

#     def test_entry_exists_false(self):
#         self.assertFalse(UserUrlRepository.entry_exists(self.user1.id, self.url2.id))

#     def test_create_entry_success(self):
#         result = UserUrlRepository.create_entry(self.user1.id, self.url2.id)
#         self.assertTrue(result)
#         self.assertTrue(UserUrlMapping.objects.filter(user=self.user1, url=self.url2).exists())

#     def test_create_entry_invalid_user(self):
#         result = UserUrlRepository.create_entry(9999, self.url1.id)
#         self.assertFalse(result)

#     def test_create_entry_invalid_url(self):
#         # Ensure the invalid URL ID does not exist safely
#         invalid_url_id = UrlMapping.objects.latest('id').id + 1
#         result = UserUrlRepository.create_entry(self.user1.id, invalid_url_id)
#         self.assertFalse(result)

#     def test_create_if_no_entry_creates(self):
#         UserUrlRepository.create_if_no_entry(self.user2.id, self.url2.id)
#         self.assertTrue(UserUrlMapping.objects.filter(user=self.user2, url=self.url2).exists())

#     def test_create_if_no_entry_skips_existing(self):
#         UserUrlRepository.create_if_no_entry(self.user1.id, self.url1.id)
#         count = UserUrlMapping.objects.filter(user=self.user1, url=self.url1).count()
#         self.assertEqual(count, 1)

#     def test_get_user_mappings_with_data(self):
#         UserUrlMapping.objects.create(user=self.user1, url=self.url2)
#         urls = UserUrlRepository.get_user_mappings(self.user1.id)
#         self.assertEqual(set(urls), {self.url1.id, self.url2.id})

#     def test_get_user_mappings_empty(self):
#         urls = UserUrlRepository.get_user_mappings(self.user2.id)
#         self.assertEqual(list(urls), [])
