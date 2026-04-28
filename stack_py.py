# stack_py.py
class TElement:
    def __init__(self, a="", b=""):
        self.a = a
        self.b = b
    def __str__(self):
        return f"{self.a} | {self.b}"

class TStack:
    def __init__(self):
        # Используем обычный список Python – динамический
        self.data = []

    def is_empty(self):
        return len(self.data) == 0

    def push(self, element):
        # Добавляем в конец списка (вершина стека – последний элемент)
        self.data.append(element)

    def pop(self):
        if self.is_empty():
            raise IndexError("Стек пуст")
        return self.data.pop()  # возвращает и удаляет последний элемент

    def peek(self):
        if self.is_empty():
            raise IndexError("Стек пуст")
        return self.data[-1]

    def clear(self):
        self.data.clear()

    def get_all(self):
        # Возвращаем копию списка в порядке от вершины к дну (сверху вниз)
        return list(reversed(self.data))