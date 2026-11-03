#!/usr/bin/env python3

def parse_frames(data):
    payloads = []
    i = 0
    while True:
        i = data.find(b"\xaa\x55", i)
        if i == -1:
            break
        if i + 2 >= len(data):
            break
        length = data[i + 2]
        end = i + 2 + 1 + length + 1
        if end > len(data):
            i += 1
            continue
        payload = data[i + 3:i + 3 + length]
        check = 0
        for b in payload:
            check ^= b
        if check == data[end - 1]:
            payloads.append(bytes(payload))
            i = end
        else:
            i += 1
    return payloads

if __name__ == "__main__":
    import sys
    raw = bytes.fromhex(sys.argv[1])
    for payload in parse_frames(raw):
        print(payload.hex())
