from django.db import models
import re


# Create your models here.
class ThreadReply(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="creator")
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE, default=None, null=True, blank=True)
    parent_reply = models.ForeignKey('ThreadReply', on_delete=models.CASCADE, default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    deleted_by = models.ForeignKey('users.User', on_delete=models.CASCADE, default=None, null=True, blank=True)

    edited_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    edited_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="reply_edited_by", null=True, blank=True)

    def get_child_replies(self):
        return ThreadReply.objects.filter(parent_reply=self).order_by('-created_at')
    
    def get_active_child_replies(self):
        return ThreadReply.objects.filter(parent_reply=self).filter(is_deleted=False).order_by('-created_at')


class ThreadVisit(models.Model):
    viewed_by = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE)

    def __str__(self):
        return self.viewed_by

class ThreadTag(models.Model):
    name = models.CharField(max_length=200)
    is_sticky = models.BooleanField(default=False)

    color = models.CharField(max_length=16)

    def __str__(self):
        return self.name + "(" + self.color + ")"
    


class Thread(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="author")
    forum = models.ForeignKey('Forum', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    content = models.TextField()

    is_deleted = models.BooleanField(default=False, null=True)
    deleted_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    deleted_by = models.ForeignKey('users.User', on_delete=models.CASCADE, default=None, null=True, blank=True)

    thread_tag = models.ForeignKey("ThreadTag", on_delete=models.CASCADE, null=True, default=None, blank=True)

    edited_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    edited_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="thread_edited_by", null=True, blank=True)

    def get_slug(self):
        return re.sub('[^0-9a-zA-Z]+', '_', self.title.lower().replace(" ", "_"))

    def get_formatted_date(self):
        return self.created_at.strftime("%b d, %Y")

    def short_content(self):
        return self.content[0:300]

    def get_visits(self):
        return ThreadVisit.objects.filter(thread=self)

    def short_title(self):
        if (len(self.title) > 15):
            return self.title[0:12] + "..."
        return self.title

    #Will autoignore all of the deleted ones
    def get_all_replies_count(self):
        count = 0

        for reply in self.get_active_replies():
            count += 1

            count += len(reply.get_active_child_replies())

        return count

    def get_latest_reply(self):
        replies = self.get_replies()

        if len(replies) == 0:
            return None
        else:
            return replies[0]

    def get_replies(self):
        return ThreadReply.objects.filter(thread=self).order_by('-created_at')

    def get_active_replies(self):
        return ThreadReply.objects.filter(thread=self).filter(is_deleted=False).order_by('-created_at')

    def __str__(self):
        return self.title


class Forum(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, default=None, null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    is_news = models.BooleanField(default=False)
    is_overview = models.BooleanField(default=False)

    def get_slug(self):
        return self.name.lower().replace(" ", "_")

    def __str__(self):
        return self.name

    def get_threads(self):
        if self.is_overview:
            return Thread.objects.order_by('-created_at')
        
        return Thread.objects.filter(forum=self).order_by('-created_at')

    #Super slow way of doing this
    def get_replies_count(self):
        count = 0;

        for thread in self.get_threads():
            for reply in thread.get_replies():
                count += len(reply.get_active_child_replies())

        return count
    

    def get_latest_thread(self):
        threads = self.get_threads()

        if len(threads) == 0:
            return None
        else:
            return threads[0]


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_forums(self):
        return Forum.objects.filter(category=self)
