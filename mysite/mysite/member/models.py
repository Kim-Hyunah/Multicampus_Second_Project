from django.db import models

class Member(models.Model):
    userid = models.CharField(max_length=15, verbose_name='User ID')
    username = models.CharField(max_length=25, verbose_name='User Name')
    userpass = models.CharField(max_length=15, verbose_name='User Password')
    email = models.EmailField(max_length=50, verbose_name='User Email')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='가입날짜')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='마지막 수정일')

    def __str__(self):
        return self.userid

    class Meta:
        db_table = 'members'
        verbose_name = "회원(멤버)정보"
        verbose_name_plural = "회원(멤버)정보"
