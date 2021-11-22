from django.shortcuts import render
from comments.forms import CommentForm
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse


# Create your views here.

def add_comment(request):
    """ Обработка добавления комментария """
    print ("Я зашел в метод")
    _id = int(request.POST['_id'])
    print ("ID заявки: ", _id)
    if request.method=="POST":
        print ("Я зашел в пост")
        form = CommentForm(data=request.POST)
        if form.is_valid():
            print ("Я зашел в валид")
            form.autor = request.user
            form.object_id = _id
            form.save()            
            return HttpResponseRedirect(reverse('zayavki:zayavka-detail', args=(_id,)))
