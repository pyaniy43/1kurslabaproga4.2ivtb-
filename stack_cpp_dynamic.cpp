// stack_cpp_dynamic.cpp
#include <cstring>

struct Element {
    int a;
    char b[21];
    Element* next;
};

struct Stack {
    Element* top;
    int count;
};

extern "C" {
    __declspec(dllexport) Stack* create_stack() {
        Stack* s = new Stack;
        s->top = nullptr;
        s->count = 0;
        return s;
    }

    __declspec(dllexport) void destroy_stack(Stack* s) {
        while (s->top) {
            Element* temp = s->top;
            s->top = s->top->next;
            delete temp;
        }
        delete s;
    }

    __declspec(dllexport) int push(Stack* s, int a, const char* b) {
        Element* e = new Element;
        e->a = a;
        strncpy(e->b, b, 20);
        e->b[20] = '\0';
        e->next = s->top;
        s->top = e;
        s->count++;
        return 1;
    }

    __declspec(dllexport) int pop(Stack* s, int* a, char* b) {
        if (!s->top) return 0;
        Element* temp = s->top;
        *a = temp->a;
        strcpy(b, temp->b);
        s->top = temp->next;
        delete temp;
        s->count--;
        return 1;
    }

    __declspec(dllexport) int peek(Stack* s, int* a, char* b) {
        if (!s->top) return 0;
        *a = s->top->a;
        strcpy(b, s->top->b);
        return 1;
    }

    __declspec(dllexport) int is_empty(Stack* s) {
        return s->top == nullptr ? 1 : 0;
    }

    __declspec(dllexport) int get_count(Stack* s) {
        return s->count;
    }

    __declspec(dllexport) void clear_stack(Stack* s) {
        while (s->top) {
            Element* temp = s->top;
            s->top = s->top->next;
            delete temp;
        }
        s->count = 0;
    }

    struct ElementData {
        int a;
        char b[21];
    };

    __declspec(dllexport) ElementData* get_all(Stack* s, int* out_count) {
        *out_count = s->count;
        if (*out_count == 0) return nullptr;
        ElementData* arr = new ElementData[*out_count];
        Element* cur = s->top;
        for (int i = 0; i < *out_count; i++) {
            arr[i].a = cur->a;
            strcpy(arr[i].b, cur->b);
            cur = cur->next;
        }
        return arr;
    }

    __declspec(dllexport) void free_array(ElementData* arr) {
        delete[] arr;
    }
}