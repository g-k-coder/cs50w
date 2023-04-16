from django import template
from network.models import Follow, Post, Like

register = template.Library()   

@register.filter
def datetime(date):
    """ Reformat data-time representation  """
    return date.strftime('%d/%m/%Y at %H:%M')

@register.filter
def get_followers(id):
    """ Get the number of followers """
    return len(Follow.objects.filter(user_id=id))


@register.filter
def get_following(id):
    """ Get the number of following """
    return len(Follow.objects.filter(follower_id=id))


@register.filter
def get_posts(id):
    """ Get the number of posts by the user """
    return len(Post.objects.filter(user_id=id))

@register.filter
def get_likes(id):
    """ Get the number of likes for the post """
    return len(Like.objects.filter(post_id=id))

@register.simple_tag
def check_like(id, post):
    """ Check if user already liked this post """
    if Like.objects.filter(user_id=id, post_id=post).exists():
        return 'true'
    else:
        return 'false'