from django import template

register = template.Library()

@register.filter
def sub(value, arg):    # 현재개수, 여러개의 값들을 받는 가변인자(시작인덱스,현재인덱스,+1을 받을거임)
    return value - arg