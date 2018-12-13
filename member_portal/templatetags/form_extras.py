from django import template
register = template.Library()

@register.filter(name='formclass')
def formclass(field, css):
   return field.as_widget(attrs={"class":css})