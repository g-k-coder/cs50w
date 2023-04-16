from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    uuid = models.UUIDField(editable=False, verbose_name='Universally Unique IDentifier (UUID)', null=False, blank=False, default=uuid.uuid4())

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'firstName': self.first_name,
            'lastName': self.last_name,
        }


class Post(models.Model):
    user = models.ForeignKey(User, verbose_name="Posted by", on_delete=models.CASCADE,
                             related_name='post_user', null=False, blank=False)
    content = models.TextField(max_length=3000, null=False, blank=False,
                               verbose_name='Post Content')
    time = models.DateTimeField(
        auto_now_add=True, null=False, blank=True, verbose_name='Posted on')

    def __str__(self):
        return f"@{self.user.username} posted on {self.time.strftime('%d/%m/%Y at %H:%M')}"

    def serialize(self):
        return {
            'id': self.id,
            'user': self.user,
            'content': self.content,
            'time': self.time,
        }

    """ 
        Project 3 - Mail
        Serialize example
        
        return {
            "id": self.id,
            "sender": self.sender.email,
            "recipients": [user.email for user in self.recipients.all()],
            "subject": self.subject,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%m/%d/%Y, %H:%M:%S"),
            "read": self.read,
            "archived": self.archived
        }
    """


class Like(models.Model):
    post = models.ForeignKey(Post, verbose_name="Post", on_delete=models.CASCADE,
                             related_name='post', null=False, blank=False)
    user = models.ForeignKey(User, verbose_name="Liked by", on_delete=models.CASCADE,
                             related_name='like', null=False, blank=False)

    def __str__(self):
        return f"{self.user.username} liked a post by {self.post.user.username}"

    @classmethod
    def create(cls, user, post):
        like  = cls(user=user, post=post)
        like.save()
        return True

class Follow(models.Model):
    user = models.ForeignKey(User, verbose_name="Following", on_delete=models.CASCADE,
                             related_name='origin_user', null=False, blank=False)
    follower = models.ForeignKey(User, verbose_name="Follower", on_delete=models.CASCADE,
                                 related_name='follower_user', null=False, blank=False)

    def __str__(self):
        return f"{self.follower.user.username} follows {self.user.username}"

    @classmethod
    def create(cls, user, follower):
        follow = cls(user=user, follower=follower)
        follow.save()
        return True