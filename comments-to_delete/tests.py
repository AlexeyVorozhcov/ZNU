# from django.test import TestCase
# from .models import Comments

# class CommentsTestCase(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         Comments.objects.create(object_id=8, autor="Седьмое небо", body="Текст комментария")        

#     def test_create_comments(self):
#         com1 = Comments.objects.get(object_id=8)
#         self.assertEqual(com1.autor, 'Седьмое небо')
#         self.assertEqual(com1.body, 'Текст комментария')
        
#     def test_comments_str_(self): 
#         com1 = Comments.objects.get(id=1)
#         self.assertEquals(com1.__str__(), 'Текст комментария')   


