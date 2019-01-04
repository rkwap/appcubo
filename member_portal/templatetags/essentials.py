from django import template
register = template.Library()

@register.filter(name='store_stol')
def store_stol(shortstore):
    if shortstore=='AND':
        store = 'android'
    elif shortstore == 'IOS':
        store = 'ios'
    elif shortstore == 'UWP':
        store = 'windows-10'
    elif shortstore == 'PWA':
        store = 'pwa'
    elif shortstore == 'LIN':
        store = 'linux'
    elif shortstore == 'W32':
        store = 'win-32-classic'
    elif shortstore == 'MAC':
        store = 'mac-os'
    else:
        store=''
    return store

@register.filter(name='store_ltos')
def store_ltos(longstore):
    if longstore=='android':
        store = 'AND'
    elif longstore == 'ios':
        store = 'IOS'
    elif longstore == 'windows-10':
        store = 'UWP'
    elif longstore == 'pwa':
        store = 'PWA'
    elif longstore == 'linux':
        store = 'LIN'
    elif longstore == 'win-32-classic':
        store = 'W32'
    elif longstore == 'mac-os':
        store = 'MAC'
    else:
        store = ''
    return store