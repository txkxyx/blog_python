import random
import string

def rand_str(n):
    '''
    引数の文字数分のランダム文字列を取得する
    '''
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))