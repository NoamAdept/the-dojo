## Error Handling and Safety

*cppq-error-handling · medium*

**Goal.** Practise three error styles in `tasks.h`: exceptions (`try`/`catch`, a custom exception), `[[nodiscard]]` and `std::optional`, and a small `Result<T, E>` type built on `std::variant`.

**You need to know.**

- `vector::at` throws `std::out_of_range`; catch by `const&`.
- `[[nodiscard]]` turns an ignored return value into a warning.
- `std::optional<T>` and `std::nullopt` for "maybe no value".
- `std::variant<T, E>`, `index()` and `std::get<N>` (README result-type section).

**Walkthrough.**

1. Run `./check`. The starter already has all includes. Note that Task 2 is a Python test (`tests/task2.py`) that compiles two tiny programs itself.

2. Task 1, catching range errors.

   ```cpp
   inline std::string safeAt(const std::vector<int>& v, std::size_t i) {
       try {
           return std::to_string(v.at(i));
       } catch (const std::out_of_range&) {
           return "out_of_range";
       }
   }
   ```

3. Task 2, nodiscard. The test compiles `square(3);` with `-Wall -Werror` and expects that to fail, which only happens with the attribute.

   ```cpp
   [[nodiscard]] inline int square(int x) { return x * x; }
   ```

4. Tasks 3 and 4, optional. Return the value or `std::nullopt`.

   ```cpp
   inline std::optional<int> parsePositive(int input) {
       if (input > 0) return input;
       return std::nullopt;
   }
   inline std::optional<float> safeDivide(float a, float b) {
       if (b == 0.0f) return std::nullopt;
       return a / b;
   }
   ```

5. Task 5, custom exception. Build the message once in the constructor and keep it in a member, because `what()` returns a `const char*` that must stay valid.

   ```cpp
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
   ```

6. Task 6, Result type. Index 0 is "ok", index 1 is "error". `std::in_place_index` picks the slot explicitly, which still works when `T` and `E` are the same type.

   ```cpp
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
   ```

7. Task 7, file loader. Check `secret.cfg` first, then the `data/` prefix. `rfind(prefix, 0) == 0` is the C++17 way to say "starts with".

   ```cpp
   enum class LoadError { NotFound, Denied };

   inline Result<std::string, LoadError> loadFile(const std::string& name) {
       using R = Result<std::string, LoadError>;
       if (name == "secret.cfg") return R::err(LoadError::Denied);
       if (name.rfind("data/", 0) != 0) return R::err(LoadError::NotFound);
       return R::ok("contents of " + name);
   }
   ```

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Returning `("sensor " + ...).c_str()` straight from `what()`: the temporary string dies and the message is garbage.
- Forgetting `[[nodiscard]]`, so task 2 says "ignoring square()'s result should warn: mark it [[nodiscard]]".
- Checking the `data/` prefix before `secret.cfg`: then `secret.cfg` returns NotFound instead of Denied.
