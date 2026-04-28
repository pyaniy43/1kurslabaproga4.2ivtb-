extern "C" {
    // ... (структуры без изменений)

    __declspec(dllexport) int push(Stack* s, int a, const char* b) {
        // больше нет проверки на max_size
        Element* e = new Element;
        e->a = a;
        strncpy(e->b, b, 20);
        e->b[20] = '\0';
        e->next = s->top;
        s->top = e;
        s->count++;
        return 1;
    }
    // остальные функции без изменений
}