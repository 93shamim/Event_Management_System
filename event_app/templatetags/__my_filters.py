
# myapp/templatetags/my_filters.py

from datetime import datetime, timedelta

from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def timeuntil(value):
    now = datetime.now()
    diff = value - now
    if diff.total_seconds() <= 0:
        return 'Finished'
    else:
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        debug_output = f"Start Date: {value}, End Date: {now}, Current Time: {timezone.now()}"
        if days > 0:
            return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds ({debug_output})"
        elif hours > 0:
            return f"{hours} hours, {minutes} minutes, {seconds} seconds ({debug_output})"
        elif minutes > 0:
            return f"{minutes} minutes, {seconds} seconds ({debug_output})"
        else:
            return f"{seconds} seconds ({debug_output})"

@register.filter
def combine(value, time):
    date = datetime.strptime(value, "%Y-%m-%d")
    time = datetime.strptime(time, "%H:%M:%S").time()
    return datetime.combine(date, time)

@register.filter
def time_until(value):
    from datetime import datetime
    now = datetime.now()
    diff = value - now
    if diff.total_seconds() <= 0:
        return 'Finished'
    else:
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_string = []
        if days > 0:
            time_string.append(f"{days}d")
        if hours > 0:
            time_string.append(f"{hours}h")
        if minutes > 0:
            time_string.append(f"{minutes}m")
        if seconds > 0:
            time_string.append(f"{seconds}s")
        return ", ".join(time_string)

