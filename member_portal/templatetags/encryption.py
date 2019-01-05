from django import template
register = template.Library()
from hashids import Hashids

salt = 'This is my salt for test.'
hashids = Hashids(salt=salt,min_length=11)

## encrypts the string
@register.filter(name='encode')
def encode(string):
    return hashids.encode(string)


## decrypts the string
@register.filter(name='decode')
def decode(hashid):
    if hashids.decode(hashid): # if can be decoded
        result =  str(hashids.decode(hashid)[0]) # returns decoded string
    else: # else if cannot be decoded
        result = 0 # returns int 0
    return result


hashids = Hashids(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',salt=salt,min_length=20)

## encrypts the string (** returns only alphabets)
@register.filter(name='encode_alpha')
def encode_alpha(string):
    return hashids.encode(string)

## decrypts the string (** returns only alphabets)
@register.filter(name='decode_alpha')
def decode_alpha(hashid):
    if hashids.decode(hashid): # if can be decoded
        result =  str(hashids.decode(hashid)[0]) # returns decoded string
    else: # else if cannot be decoded
        result = 0 # returns int 0
    return result

