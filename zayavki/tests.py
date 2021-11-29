from django.test import TestCase
from .models import Zayavka, FiltersOfZayavok
from users.models import User, Roles, Category, Shops


class FilterTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        shop = Shops.objects.create(nameshop="Седьмое небо")
        category = Category.objects.create(name="Книги")
        role = Roles.objects.create(namerole="Магазин")
        role.work_category.add(category)
        user = User.objects.create(username="7nebo", role=role, shop=shop)
        zayavka = Zayavka.objects.create(user=user,
                                        category=category,
                                        code="111111",
                                        name="Человек паук",
                                        description="Рваная страница",
                                        clarification="Принято у покупателя")
        filter_all = FiltersOfZayavok.objects.create(label="Все",
                                                    link="all")
        filter_all.for_roles.add(role)
        
    def test_listdict_for_template(self):
        user = User.objects.get(id=1)
        result_start = FiltersOfZayavok.listdict_for_template(user)
        result_end = [{"label":"Все", "link":"all", "count":1}]
        self.assertEqual(result_start, result_end)    
        
        
        
        
        
        
        
        
             

    # def test_create_comments(self):
    #     com1 = Comments.objects.get(object_id=8)
    #     self.assertEqual(com1.autor, 'Седьмое небо')
    #     self.assertEqual(com1.body, 'Текст комментария')
        
    # def test_comments_str_(self): 
    #     com1 = Comments.objects.get(id=1)
    #     self.assertEquals(com1.__str__(), 'Текст комментария')   

