
#admin.py
```
from django.contrib import admin
from .models import Faq, Answer, Inquiry

class AnsInline(admin.TabularInline):
    model = Answer
    verbose_name = '답변'

#admin.site.register(Faq)
@admin.register(Faq)
class FqaModelAdmin(admin.ModelAdmin):
    list_display = (
'title',
'category',
    )
    search_fields = ('title','category')
    search_help_text = '카테고리, 작성자, 최종 수정일시 검색'

    list_filter = ['category',]
    
@admin.register(Inquiry)
class InquiryModelAdmin(admin.ModelAdmin):
    list_display = ('title','category')
    search_fields = ('title','email','phone')
    search_help_text = '제목, 이메일, 전화번호 검색'
    list_filter = ['category',]
    
    inlines = [AnsInline]

@admin.register(Answer)
class AnsModelAdmin(admin.ModelAdmin):
    list_display = ('inquiry','content')
```
