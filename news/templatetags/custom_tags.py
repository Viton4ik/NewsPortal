
from datetime import datetime
from django import template

import pytz
from django.utils import timezone


register = template.Library()

# get time
@register.simple_tag()
def current_time(format_string='%b %d %Y'):
   return datetime.utcnow().strftime(format_string)

# get time option 2
@register.simple_tag()
def current_time2():
   return datetime.utcnow().date() #datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')


# to replace tags with the same data when using filters
# if using pangination+filter -> not to cancel filter if click to the next page
@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()

#  
@register.simple_tag()
def time_zones_():
   timezones = pytz.common_timezones
   return timezones

#  
@register.simple_tag()
def current_time_():
   current_time = timezone.localtime(timezone.now()).strftime('%d/%m/%Y %H:%M')
   return current_time
