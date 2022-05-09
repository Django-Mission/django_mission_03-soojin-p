from os import listdir
from xml.etree.ElementTree import Comment
from django.contrib import admin

from .models import Post, Comment

class CommentInline(admin.StackedInline): #TabularInline
    model = Comment
    extra = 5 #댓글 갯수 1개
    min_num = 3
    max_num = 5
    verbose_name = 'verbose_name 댓글'
    verbose_name_plural = 'verbose_name 댓글'
@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'content', 'created_at', 'view_count', 'writer')
    #list_editable =('content',) 
    #list_filter = ['created_at']
    list_filter = ('created_at',)
    search_fields = ('id','writer__username') #한 명을 특정하기 위함
    search_help_text = '계시판 번호, 작성자 검색이 가능합니다.'
    readonly_fields = ('created_at',)
    inlines = [CommentInline]

    actions = ['make_published']

    def make_published(modeladmin, request, queryset):
        for item in queryset:
            #item.update(content='운영 규정 위반으로 인한 게시글 삭제처리')
            item.content = '운영 규정 위반으로 인한 게시글 삭제 처리.'
            item.save()

#admin.site.register(Comment)