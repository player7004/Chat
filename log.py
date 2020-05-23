import os.path

class Log:
    def __init__(self,name):
        self.log_name=name
        if not os.path.isfile(name):
            self.file_log=open(name,"w")
        else:
            self.file_log=open(name,"r")

    @staticmethod
    def read_and_return_str(file_name):
        if not os.path.isfile(file_name):
            return -1
        file=open(file_name,"r")
        for line in file:
            print(line)

    @staticmethod
    def read_and_return_list(file_name):
        if not os.path.isfile(file_name):
            return []
        out=[]
        with open(file_name,"r") as file:
            for line in file:
                add=line[:line.find('\n')]
                out.append(add)
        return out

    @staticmethod
    def save_with_ignore_same(file_name, text): #Использовать только для сохранения пиров 
        if not os.path.isfile(file_name):
            file=open(file_name,"w")
            file.close()
        file=open(file_name,"r+")
        text+='\n'
        for line in file:
            if line==text:
                return
        file.write(text)
        file.close()

    def save_message(self, text):
        self.file_log.write(text + '\n')
        
    def close(self):
        self.file_log.close()