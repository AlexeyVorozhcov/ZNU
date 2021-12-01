# from django import forms
# from comments.models import Comments

# class CommentForm(forms.ModelForm):
    
#     class Meta:
#         model = Comments
#         fields = ('body',)
    
#     name_class = "form-control form-control-sm fw-bold"    
#     attrs_for_body = {"class" : name_class, "style" : "height: 70px",
#                     'placeholder' : "Введите комментарий"}   
#     body = forms.CharField(widget=forms.Textarea(attrs=attrs_for_body)) 