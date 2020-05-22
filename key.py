import random

class Key:
    def create_key(degree): #Шифрование Деффи-Хеллман
        key=(7**degree)%23
        if key==0:
            key=create_key(degree)
        return key

    def get_key(key,degree):
        check=(key**degree)%23
        return check

    


