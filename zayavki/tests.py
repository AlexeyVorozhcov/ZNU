from django.test import TestCase
from .models import Zayavka, FiltersOfZayavok
from users.models import User, Roles, Category, Shops
from .services import get_count_of_filter, get_users_queryset, get_users_default_filter



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
    
    def test_get_users_queryset(self):
        user = User.objects.get(id=1)
        result_start = get_users_queryset(user).get(id=1).name        
        self.assertEqual(result_start, "Человек паук")  
        
    def test_get_users_default_filter(self):
        user = User.objects.get(id=1)    
        result_start=get_users_default_filter(user)
        self.assertEqual(result_start, "all")  
        
        
    def test_get_count_of_filter(self):
        user = User.objects.get(id=1)
        filter_ = FiltersOfZayavok.objects.get(label="Все")
        result_start = get_count_of_filter(user, filter_)
        # result_end = [{"label":"Все", "link":"all"}]
        result_end = 1
        self.assertEqual(result_start, result_end)    
    
  
        
        
        
        
        
        
        
             

    # def test_create_comments(self):
    #     com1 = Comments.objects.get(object_id=8)
    #     self.assertEqual(com1.autor, 'Седьмое небо')
    #     self.assertEqual(com1.body, 'Текст комментария')
        
    # def test_comments_str_(self): 
    #     com1 = Comments.objects.get(id=1)
    #     self.assertEquals(com1.__str__(), 'Текст комментария')   

