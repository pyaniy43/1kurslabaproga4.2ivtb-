extern "C" {
    struct StackSTL {
        std::stack<std::pair<int, std::string>> data;
        // max_size больше нет
    };

    __declspec(dllexport) int push(StackSTL* s, int a, const char* b) {
        s->data.push({a, std::string(b)});
        return 1;   // всегда успех
    }
    // остальное без изменений
}