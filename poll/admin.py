#coding: utf8
from django.contrib import admin
from models import Polls, Options, Comments


class PollsAdmin(admin.ModelAdmin):
    pass

class OptionsAdmin(admin.ModelAdmin):
    pass


class CommentsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Polls, PollsAdmin)
admin.site.register(Options, OptionsAdmin)
admin.site.register(Comments, CommentsAdmin)