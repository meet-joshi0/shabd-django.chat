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

# @register.filter(name="fri_lst_url", is_safe=True)
# def friend_list_url(string, sep):
   
#     """Return the string split by sep.

#     Example usage: {{ value|split:"/" }}
#     """
#     str = string.split(sep)
#     param = str[0]+" "+str[1]
#     return str

