from django.contrib.auth.hashers import check_password

from django import forms
from .models import Post

class PostForm(forms.Form):
    title = forms.CharField(error_messages={
        'required': '제목을 입력하세요.'}, max_length=100, label="게시글 제목")
    content = forms.CharField(error_messages={
        'required': '내용을 입력하세요.'}, widget=forms.Textarea, label="게시글 내용")
    #imgfile = forms.ImageField(allow_empty_file=True, label="파일 업로드")
