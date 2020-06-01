import random


class Key:
    def __init__(self):
    def create_key(degree): #Шифрование Деффи-Хеллман
        key = (7**degree)%23
        if key==0:
            key = self.create_key(degree)
        return key

    def get_key(key,degree):
        check=(key**degree)%23
        return check

    


