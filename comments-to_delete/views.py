# from django.shortcuts import render
# from comments.forms import CommentForm
# from django.shortcuts import HttpResponseRedirect
# from django.urls import reverse


# # Create your views here.

# def add_comment(request):
#     """ Обработка добавления комментария """
       
#     if request.method=="POST":
#         if request.POST['_id']: _id = int(request.POST['_id'])
#         else: _id = 0    
#         form = CommentForm(data=request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.autor = request.user
#             comment.object_id = _id  
#             comment.save()            
#             return HttpResponseRedirect(reverse('zayavki:zayavka-detail', args=(_id,)))
#         else:
#             print ("Что-то пошлдо не так.")
#             print (form.data)
#     else:
#         return HttpResponseRedirect(reverse('zayavki:zayavki_list'))        