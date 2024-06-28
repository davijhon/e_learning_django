from django import template
from courses.models import ContentIsComplete

register = template.Library()


@register.filter
def user_content_complete(user, content):
    content_id = content.id

    try:
        c = ContentIsComplete.objects.get(id=content_id, student=user)
        if c.is_complete:
            return "<i class='fa fa-check fa-1x'></i>"
        return ""
    except ContentIsComplete.DoesNotExist:
        return ""
