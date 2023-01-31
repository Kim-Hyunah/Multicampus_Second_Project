from django import forms
from .models import Member
from django.contrib.auth.hashers import check_password

class LoginForm(forms.Form) :
    userid = forms.CharField (error_messages= {'required' : '아이디를 입력하세요'}, max_length=15, label="user 아이디")
    userpass = forms.CharField (error_messages= {'required' : '비밀번호를 입력하세요'}, widget=forms.PasswordInput, max_length=15, label="비밀번호")

    def clean(self):
        clean_data = super().clean()
        userid = clean_data.get("userid")
        userpass = clean_data.get("userpass")
        if userid and userpass:
            try:
                member = Member.objects.get(userid=userid)
            except Member.DoesNotExist:
                self.add_error('userid', '아이디가 존재하지 않습니다.')
                return
            if not check_password(userpass, member.userpass):
                self.add_error('userpass', '비밃번호가 다릅니다.')
            else:
                self.userid = member.userid