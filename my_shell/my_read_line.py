import os

nxt = 0
limit = 0

def get_char():
    global nxt
    global limit

    if nxt == limit:
        nxt = 0
        limit = os.read(0,100)

        if limit == 0:
            return 'EOF'

    if nxt < len(limit) -1:
        char = chr(limit[nxt])
        nxt += 1
        return char

    else:
        return 'EOF'


def my_read_line():
    global nxt
    global limit

    string = ''
    char = get_char()

    while(char != '' and char != 'EOF'):
        string += char
        char = get_char()

    nxt = 0
    limit = 0

    return string

    
