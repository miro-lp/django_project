from django import template

register = template.Library()


@register.filter(name='friend_request_exist')
def friend_request_exist(friend_requests, to_user_id):
    for friend_request in friend_requests:
        if friend_request.to_user.user_id == to_user_id:
            return True
