import os.path


class Log:
    def __init__(self,name):
        self.log_name = name
        if not os.path.isfile(name):
            self.file_log = open(name,"w")
        else:
            self.file_log = open(name,"a")

    @staticmethod
    def read_and_return_list(file_name):  # Читает из файла и возвращает лист
        if not os.path.isfile(file_name):
            return []
        out = []
        with open(file_name,"r") as file:
            for line in file:
                add = line[:line.find('\n')]
                out.append(add)
        return out

    @staticmethod
    def read_and_return_dict(file_name):  # Читает из файла и возвращает словарь
        if not os.path.isfile(file_name):
            return {}
        out = {}
        with open(file_name, "r") as file:
            for line in file:
                add = line[:line.find("\n")].split(":", 1)
                try:
                    out.update({add[0]: add[1]})
                except IndexError:
                    break
        return out

    @staticmethod
    def save_with_ignore_same(file_name, text):  # Сохраняет в файл данные, игнорирую повторяющиеся
        if not os.path.isfile(file_name):
            file = open(file_name,"w")
            file.close()
        text += "\n"
        with open(file_name, "r+") as file:
            for line in file:
                if line == text:
                    return
            file.write(text)
            file.close()

    @staticmethod
    def save_dict(dictionary, file_name):  # Сохраняет словарь
        with open(file_name, "w") as file:
            for i in dictionary:
                file.write("{}:{}\n".format(str(i), str(dictionary.get(i))))
        file.close()

    def save_message(self, text):
        self.file_log.write(text + '\n')
        
    def close(self):
        self.file_log.close()