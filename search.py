def match(pattern, word):
    position = 0
    index = 0
    while index != len(pattern):
        try:
            new_position = word.index(pattern[index], position)
        except ValueError:
            return False
        index += 1
        position = new_position
    return True


w = 'name'
p = 'nm'

print(match(p, w))