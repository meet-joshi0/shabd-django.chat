from chat.settings import MEDIA_ROOT, MEDIA_URL
from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()



@register.filter(name="getprofile", is_safe=True)
def profile_data(value,x):

   

    q = []
    x = x  if x else "null"
    value=value


    for i in value:

        if i['username'] > x:
            a = {}

            s = x +"/"+ i['username']
            a['url'] = f"/userroom/{ i['username'] }/{x}"

            a["img"] = i['userImage']

            a["username"] = i['username']

            q.append(a)

        elif i['username'] != x:
            a = {}

            j =  i['username'] +"/"+ x

            a['url'] = f"/userroom/{ i['username'] }/{x}"
            a["img"] =  i['userImage']

            a["username"] = i['username']

            q.append( a)


    return q


