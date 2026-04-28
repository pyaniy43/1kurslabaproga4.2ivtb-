// stack_cpp_stl.cpp
#include <stack>
#include <string>
#include <cstring>
#include <utility>

extern "C" {
    struct StackSTL {
        std::stack<std::pair<int, std::string>> data;
    };

    __declspec(dllexport) StackSTL* create_stack() {
        return new StackSTL;
    }

    __declspec(dllexport) void destroy_stack(StackSTL* s) {
        delete s;
    }

    __declspec(dllexport) int push(StackSTL* s, int a, const char* b) {
        s->data.push({a, std::string(b)});
        return 1;   // всегда успех
    }

    __declspec(dllexport) int pop(StackSTL* s, int* a, char* b) {
        if (s->data.empty()) return 0;
        auto top = s->data.top();
        *a = top.first;
        strcpy(b, top.second.c_str());
        s->data.pop();
        return 1;
    }

    __declspec(dllexport) int peek(StackSTL* s, int* a, char* b) {
        if (s->data.empty()) return 0;
        auto top = s->data.top();
        *a = top.first;
        strcpy(b, top.second.c_str());
        return 1;
    }

    __declspec(dllexport) int is_empty(StackSTL* s) {
        return s->data.empty() ? 1 : 0;
    }

    __declspec(dllexport) int get_count(StackSTL* s) {
        return s->data.size();
    }

    __declspec(dllexport) void clear_stack(StackSTL* s) {
        while (!s->data.empty()) s->data.pop();
    }

    struct ElementData {
        int a;
        char b[21];
    };

    __declspec(dllexport) ElementData* get_all(StackSTL* s, int* out_count) {
        *out_count = s->data.size();
        if (*out_count == 0) return nullptr;
        ElementData* arr = new ElementData[*out_count];
        std::stack<std::pair<int, std::string>> temp = s->data;
        for (int i = 0; i < *out_count; i++) {
            arr[i].a = temp.top().first;
            strcpy(arr[i].b, temp.top().second.c_str());
            temp.pop();
        }
        return arr;
    }

    __declspec(dllexport) void free_array(ElementData* arr) {
        delete[] arr;
    }
}