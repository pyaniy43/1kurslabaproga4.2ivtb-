import ctypes

class ElementData(ctypes.Structure):
    _fields_ = [("a", ctypes.c_int),
                ("b", ctypes.c_char * 21)]

class StackCpp:
    def __init__(self, lib_path):
        self.lib = ctypes.CDLL(lib_path)

        # Сигнатуры функций
        self.lib.create_stack.restype = ctypes.c_void_p
        self.lib.destroy_stack.argtypes = [ctypes.c_void_p]

        self.lib.push.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p]
        self.lib.push.restype = ctypes.c_int

        self.lib.pop.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.c_char_p]
        self.lib.pop.restype = ctypes.c_int

        self.lib.peek.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.c_char_p]
        self.lib.peek.restype = ctypes.c_int

        self.lib.is_empty.argtypes = [ctypes.c_void_p]
        self.lib.is_empty.restype = ctypes.c_int

        self.lib.get_count.argtypes = [ctypes.c_void_p]
        self.lib.get_count.restype = ctypes.c_int

        self.lib.clear_stack.argtypes = [ctypes.c_void_p]

        self.lib.get_all.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
        self.lib.get_all.restype = ctypes.POINTER(ElementData)

        self.lib.free_array.argtypes = [ctypes.POINTER(ElementData)]

        self.obj = self.lib.create_stack()
        self.max_size = 20
        self.top = 0  # для имитации, обновляется через get_count

    def push(self, a, b):
        b_bytes = b.encode('utf-8')
        if not self.lib.push(self.obj, int(a), b_bytes):
            raise OverflowError("Стек переполнен")
        self.top += 1

    def pop(self):
        a = ctypes.c_int()
        b = ctypes.create_string_buffer(21)
        if not self.lib.pop(self.obj, ctypes.byref(a), b):
            raise IndexError("Стек пуст")
        self.top -= 1
        return (a.value, b.value.decode('utf-8'))

    def peek(self):
        a = ctypes.c_int()
        b = ctypes.create_string_buffer(21)
        if not self.lib.peek(self.obj, ctypes.byref(a), b):
            raise IndexError("Стек пуст")
        return (a.value, b.value.decode('utf-8'))

    def is_empty(self):
        return bool(self.lib.is_empty(self.obj))

    def is_full(self):
        return self.lib.get_count(self.obj) >= self.max_size

    def clear(self):
        self.lib.clear_stack(self.obj)
        self.top = 0

    def get_all(self):
        count = ctypes.c_int()
        arr_ptr = self.lib.get_all(self.obj, ctypes.byref(count))
        result = []
        for i in range(count.value):
            elem = arr_ptr[i]
            result.append((elem.a, elem.b.decode('utf-8')))
        if arr_ptr:
            self.lib.free_array(arr_ptr)
        return result

    def __del__(self):
        if hasattr(self, 'obj'):
            self.lib.destroy_stack(self.obj)