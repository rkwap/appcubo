from django import template
register = template.Library()
from hashids import Hashids

salt = 'This is my salt for test.'

# hashids = Hashids(salt=salt,min_length=11)
# hashid = hashids.encode(123)

# test = hashids.decode(hashid)
# print(str(test[0]))

@register.filter(name='encode')
def encode(string):
    hashids = Hashids(salt=salt,min_length=11)
    return hashids.encode(string)

@register.filter(name='decode')
def decode(hashid):
    hashids = Hashids(salt=salt,min_length=11)
    return str(hashids.decode(hashid)[0])

