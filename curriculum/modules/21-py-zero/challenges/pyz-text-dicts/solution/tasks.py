"""Python from Zero 07: strings and dictionaries."""


def clean_upper(text):
    return text.strip().upper()


def words(sentence):
    return sentence.split()


def dashed(parts):
    return "-".join(parts)


def make_station(name, freq):
    return {"name": name, "freq": freq}


def mode_of(station):
    return station.get("mode", "FM")


def parse_pair(line):
    key, value = line.split("=", 1)
    return [key.strip(), value.strip()]


def count_words(sentence):
    counts = {}
    for word in sentence.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts
