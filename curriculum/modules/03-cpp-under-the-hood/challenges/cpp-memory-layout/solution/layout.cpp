#include "layout.hpp"

bool decode_header(const uint8_t* data, std::size_t size, header* out)
{
    if (data == nullptr || out == nullptr || size < 6) {
        return false;
    }
    out->tag[0] = static_cast<char>(data[0]);
    out->tag[1] = static_cast<char>(data[1]);
    out->sequence = static_cast<uint16_t>(data[2] | (data[3] << 8));
    out->flags = data[4];
    out->length = data[5];
    return true;
}
