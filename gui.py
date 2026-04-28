import tkinter as tk
from tkinter import scrolledtext, messagebox
import os

from stack_py import TStack, TElement
from stack_cpp_wrapper import StackCpp


class StackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Стек (Python / C++)")
        self.root.geometry("550x720")
        self.root.resizable(False, False)

        self.bg_color = "#f0f0f0"
        self.root.configure(bg=self.bg_color)

        # По умолчанию используется Python-реализация
        self.stack = TStack()
        self.current_module = "Python"

        self.create_widgets()
        self.update_stack_display()

    def create_widgets(self):
        # Заголовокswitch_module
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=50)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        tk.Label(title_frame, text="Управление стеком", font=("Arial", 16, "bold"),
                 bg="#2c3e50", fg="white").pack(expand=True)

        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Выбор модуля
        module_frame = tk.LabelFrame(main_frame, text="Реализация стека", font=("Arial", 10, "bold"),
                                     bg=self.bg_color)
        module_frame.pack(fill=tk.X, pady=5)

        self.module_var = tk.StringVar(value="python")
        tk.Radiobutton(module_frame, text="Python", variable=self.module_var,
                       value="python", command=self.switch_module,
                       bg=self.bg_color, font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(module_frame, text="C++ (dynamic)", variable=self.module_var,
                       value="cpp_dyn", command=self.switch_module,
                       bg=self.bg_color, font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(module_frame, text="C++ (STL)", variable=self.module_var,
                       value="cpp_stl", command=self.switch_module,
                       bg=self.bg_color, font=("Arial", 9)).pack(side=tk.LEFT, padx=5)

        # Уведомления
        notif_frame = tk.Frame(main_frame, bg="#2c3e50", height=40)
        notif_frame.pack(fill=tk.X, pady=(5, 10))
        notif_frame.pack_propagate(False)
        self.notif_label = tk.Label(notif_frame, text="Ожидание действий...",
                                    font=("Arial", 11, "bold"), bg="#2c3e50", fg="white", anchor="w")
        self.notif_label.pack(fill=tk.BOTH, padx=10, pady=8)

        # Отображение стека
        disp_frame = tk.LabelFrame(main_frame, text="Элементы стека", font=("Arial", 12, "bold"),
                                   bg=self.bg_color)
        disp_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.stack_display = scrolledtext.ScrolledText(disp_frame, wrap=tk.WORD,
                                                       width=50, height=12, font=("Courier", 11))
        self.stack_display.pack(fill=tk.BOTH, expand=True)

        # Статус
        status_frame = tk.Frame(main_frame, bg=self.bg_color)
        status_frame.pack(fill=tk.X, pady=5)
        self.status_label = tk.Label(status_frame, text="", font=("Arial", 10),
                                     bg=self.bg_color, fg="#2c3e50")
        self.status_label.pack(side=tk.LEFT)

        # Кнопки операций
        ops_frame = tk.LabelFrame(main_frame, text="Операции", font=("Arial", 12, "bold"),
                                  bg=self.bg_color)
        ops_frame.pack(fill=tk.X, pady=5)

        f1 = tk.Frame(ops_frame, bg=self.bg_color)
        f1.pack(fill=tk.X, pady=2)
        tk.Button(f1, text="Очистить стек", command=self.clear_stack,
                  bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                  relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        tk.Button(f1, text="Показать вершину", command=self.peek_stack,
                  bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                  relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)

        f2 = tk.Frame(ops_frame, bg=self.bg_color)
        f2.pack(fill=tk.X, pady=2)
        tk.Button(f2, text="Удалить вершину (Pop)", command=self.pop_stack,
                  bg="#9f2e8e", fg="white", font=("Arial", 10, "bold"),
                  relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        tk.Button(f2, text="Обновить список", command=self.update_stack_display,
                  bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
                  relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)

        # Добавление элемента
        add_frame = tk.LabelFrame(main_frame, text="Добавить элемент", font=("Arial", 12, "bold"),
                                  bg=self.bg_color)
        add_frame.pack(fill=tk.X, pady=5)

        inp_frame = tk.Frame(add_frame, bg=self.bg_color)
        inp_frame.pack(fill=tk.X, pady=5)
        tk.Label(inp_frame, text="Параметр 1:", font=("Arial", 10), bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        self.entry_a = tk.Entry(inp_frame, font=("Arial", 10), width=15)
        self.entry_a.pack(side=tk.LEFT, padx=5)
        tk.Label(inp_frame, text="Параметр 2:", font=("Arial", 10), bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        self.entry_b = tk.Entry(inp_frame, font=("Arial", 10), width=15)
        self.entry_b.pack(side=tk.LEFT, padx=5)

        btn_frame = tk.Frame(add_frame, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=5)
        tk.Button(btn_frame, text="Добавить (Push)", command=self.push_stack,
                  bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                  relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        tk.Button(btn_frame, text="Очистить поля", command=self.clear_entries,
                  bg="#701717", fg="white", font=("Arial", 10, "bold"),
                  relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # Выход
        tk.Button(main_frame, text="Выход", command=self.exit_app,
                  bg="#1956b1", fg="white", font=("Arial", 12, "bold"),
                  relief=tk.RAISED, borderwidth=2).pack(pady=10)

    def switch_module(self):
        """Переключение между реализациями стека (Python / C++ dynamic / C++ STL)."""
        choice = self.module_var.get()
        try:
            if choice == "python":
                self.stack = TStack()
                self.current_module = "Python"
            elif choice == "cpp_dyn":
                if not os.path.exists("stack_cpp.dll"):
                    messagebox.showerror("Ошибка", "Файл stack_cpp.dll не найден. Скомпилируйте C++ модуль.")
                    self.module_var.set("python")
                    return
                # Абсолютный путь к папке с gui.py
                base = os.path.dirname(os.path.abspath(__file__))
                self.stack = StackCpp(os.path.join(base, "stack_cpp.dll"))
                self.current_module = "C++ (dynamic)"
            elif choice == "cpp_stl":
                if not os.path.exists("stack_cpp_stl.dll"):
                    messagebox.showerror("Ошибка", "Файл stack_cpp_stl.dll не найден. Скомпилируйте C++ модуль STL.")
                    self.module_var.set("python")
                    return
                base = os.path.dirname(os.path.abspath(__file__))
                self.stack = StackCpp(os.path.join(base, "stack_cpp_stl.dll"))
                self.current_module = "C++ (STL)"
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить модуль: {e}")
            self.module_var.set("python")
            self.stack = TStack()
            self.current_module = "Python"

        self.clear_entries()
        self.update_stack_display()
        self.show_notification(f"Модуль: {self.current_module}")

    def show_notification(self, msg, is_success=True):
        """Выводит уведомление в верхней панели."""
        self.notif_label.config(text=msg, fg="white" if is_success else "#ff9999")
        self.root.after(3000, lambda: self.notif_label.config(text="Ожидание действий...", fg="white"))

    def update_stack_display(self):
        """Обновляет список элементов стека в области отображения."""
        self.stack_display.delete(1.0, tk.END)
        if self.stack.is_empty():
            self.stack_display.insert(tk.END, "Стек пуст\n")
            elements_count = 0
        else:
            elements = self.stack.get_all()
            elements_count = len(elements)
            for i, elem in enumerate(elements, 1):
                if isinstance(elem, tuple):
                    text = f"{elem[0]} | {elem[1]}"
                else:
                    text = str(elem)
                self.stack_display.insert(tk.END, f"{i}. {text}\n")

        status = f"Элементов: {elements_count}"
        self.status_label.config(text=status)

    def push_stack(self):
        """Добавляет элемент в стек."""
        a = self.entry_a.get().strip()
        b = self.entry_b.get().strip()
        if not a or not b:
            self.show_notification("Заполните оба параметра!", False)
            return
        try:
            if self.current_module == "Python":
                elem = TElement(a, b)
                self.stack.push(elem)
            else:
                # C++ обёртка принимает два отдельных значения
                self.stack.push(a, b)
        except Exception as e:
            self.show_notification(f"Ошибка: {e}", False)
            return
        self.clear_entries()
        self.update_stack_display()
        self.show_notification(f"Добавлен: {a} | {b}")

    def pop_stack(self):
        """Удаляет элемент с вершины стека."""
        try:
            elem = self.stack.pop()
        except IndexError as e:
            self.show_notification(str(e), False)
            return
        except Exception as e:
            self.show_notification(f"Ошибка: {e}", False)
            return
        self.update_stack_display()
        if isinstance(elem, tuple):
            self.show_notification(f"Удалён: {elem[0]} | {elem[1]}")
        else:
            self.show_notification(f"Удалён: {elem}")

    def peek_stack(self):
        """Показывает элемент на вершине стека."""
        try:
            elem = self.stack.peek()
        except IndexError as e:
            self.show_notification(str(e), False)
            return
        except Exception as e:
            self.show_notification(f"Ошибка: {e}", False)
            return
        if isinstance(elem, tuple):
            self.show_notification(f"Вершина: {elem[0]} | {elem[1]}")
        else:
            self.show_notification(f"Вершина: {elem}")

    def clear_stack(self):
        """Полностью очищает стек."""
        self.stack.clear()
        self.update_stack_display()
        self.show_notification("Стек очищен")

    def clear_entries(self):
        """Очищает поля ввода параметров."""
        self.entry_a.delete(0, tk.END)
        self.entry_b.delete(0, tk.END)

    def exit_app(self):
        """Закрывает приложение."""
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = StackApp(root)
    root.mainloop()