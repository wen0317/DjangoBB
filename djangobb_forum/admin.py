# coding: utf-8

from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.models import User as auth_User
from django.utils.translation import ugettext_lazy as _

from djangobb_forum.models import Category, Forum, Topic, Post, Profile, Reputation, \
    Report, Ban, Attachment, Poll, PollChoice, PostTracking

from django.contrib.auth import get_user_model

class BaseModelAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        # disabled, because delete_selected ignoring delete model method
        actions = super(BaseModelAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class CategoryAdmin(BaseModelAdmin):
    list_display = ['name', 'position', 'forum_count']

class ForumAdmin(BaseModelAdmin):
    list_display = ['name', 'category', 'position', 'topic_count']
    raw_id_fields = ['moderators', 'last_post']

class TopicAdmin(BaseModelAdmin):
    def subscribers2(self, obj):
        return ", ".join([user.username for user in obj.subscribers.all()])
    subscribers2.short_description = _("subscribers")

    list_display = ['name', 'forum', 'created', 'head', 'post_count', 'subscribers2']
    search_fields = ['name']
    raw_id_fields = ['user', 'subscribers', 'last_post']

class PostAdmin(BaseModelAdmin):
    list_display = ['topic', 'user', 'created', 'updated', 'summary']
    search_fields = ['body']
    raw_id_fields = ['topic', 'user', 'updated_by']

class ProfileAdmin(BaseModelAdmin):
    list_display = ['user', 'status', 'time_zone', 'location', 'language']
    raw_id_fields = ['user']

class PostTrackingAdmin(BaseModelAdmin):
    list_display = ['user', 'last_read', 'topics']
    raw_id_fields = ['user']

class ReputationAdmin(BaseModelAdmin):
    list_display = ['from_user', 'to_user', 'post', 'sign', 'time', 'reason']
    raw_id_fields = ['from_user', 'to_user', 'post']

class ReportAdmin(BaseModelAdmin):
    list_display = ['reported_by', 'post', 'zapped', 'zapped_by', 'created', 'reason']
    raw_id_fields = ['reported_by', 'post']

class BanAdmin(BaseModelAdmin):
    list_display = ['user', 'ban_start', 'ban_end', 'reason']
    raw_id_fields = ['user']

class UserAdmin(auth_admin.UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        return patterns('',
                        url(r'^(\d+)/password/$', self.admin_site.admin_view(self.user_change_password), name='user_change_password'),
                        ) + super(auth_admin.UserAdmin, self).get_urls()

class AttachmentAdmin(BaseModelAdmin):
    list_display = ['id', 'name', 'size', 'path', 'hash', ]
    search_fields = ['name']
    list_display_links = ('name',)
    list_filter = ("content_type",)


class PollChoiceInline(admin.TabularInline):
    model = PollChoice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    list_display = ("question", "active",)
    list_display_links = ("question",)
    list_editable = ("active",)
    list_filter = ("active",)
    inlines = [PollChoiceInline]

User = get_user_model()
if isinstance(User, auth_User):
    admin.site.unregister(User)
    admin.site.register(User, UserAdmin)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(PostTracking, PostTrackingAdmin)
admin.site.register(Reputation, ReputationAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Ban, BanAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Poll, PollAdmin)

