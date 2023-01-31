from django.db import models

class Post(models.Model) :
    title = models.CharField(max_length=100, verbose_name="제목")
    content = models.TextField(verbose_name="내용")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="최종수정일")
    author = models.ForeignKey('member.Member', on_delete=models.CASCADE, verbose_name="작성자")
    imgfile = models.ImageField (null=True, upload_to="", blank=True)

    def __str__(self):
        return f'[{self.pk}]{self.title}'
    class Meta:
        db_table = 'boards'
        verbose_name = '게시판'
        verbose_name_plural = '게시판'