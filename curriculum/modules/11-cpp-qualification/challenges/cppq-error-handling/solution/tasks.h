// C++ Qualification 09: error handling and safety.
#pragma once
#include <exception>
#include <optional>
#include <stdexcept>
#include <string>
#include <variant>
#include <vector>

inline std::string safeAt(const std::vector<int>& v, std::size_t i) {
    try {
        return std::to_string(v.at(i));
    } catch (const std::out_of_range&) {
        return "out_of_range";
    }
}

[[nodiscard]] inline int square(int x) { return x * x; }

inline std::optional<int> parsePositive(int input) {
    if (input > 0) return input;
    return std::nullopt;
}

inline std::optional<float> safeDivide(float a, float b) {
    if (b == 0.0f) return std::nullopt;
    return a / b;
}

class SensorException : public std::exception {
public:
    explicit SensorException(int id) : msg_("sensor " + std::to_string(id) + " failed") {}
    const char* what() const noexcept override { return msg_.c_str(); }

private:
    std::string msg_;
};

inline int readSensor(int id) {
    if (id < 0) throw SensorException(id);
    return id * 10;
}

template <class T, class E>
class Result {
public:
    static Result ok(T value) { return Result(std::variant<T, E>(std::in_place_index<0>, std::move(value))); }
    static Result err(E error) { return Result(std::variant<T, E>(std::in_place_index<1>, std::move(error))); }
    bool isOk() const { return data_.index() == 0; }
    T value() const { return std::get<0>(data_); }
    E error() const { return std::get<1>(data_); }

private:
    explicit Result(std::variant<T, E> data) : data_(std::move(data)) {}
    std::variant<T, E> data_;
};

enum class LoadError { NotFound, Denied };

inline Result<std::string, LoadError> loadFile(const std::string& name) {
    using R = Result<std::string, LoadError>;
    if (name == "secret.cfg") return R::err(LoadError::Denied);
    if (name.rfind("data/", 0) != 0) return R::err(LoadError::NotFound);
    return R::ok("contents of " + name);
}
