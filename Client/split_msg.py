
def split_by_chars(word):
    return [char for char in word]

def split_msg(msg):
    iterator = 0
    old_iterator = 50
    while iterator <= len(msg) -1:
        if iterator % 50 == 0:
            if msg[iterator] == " ":
                msg[iterator] = '\n'
            else:
                j = iterator
                while j>=old_iterator:
                    if msg[j] == " ":
                        msg[j] = '\n'
                        break
                    
                    if j == old_iterator:
                        msg[iterator] = '\n'
                    j -= 1

                    
        old_iterator = iterator
        iterator += 50

    msg_join = ''.join(msg)
    print(msg_join)
    return msg_join

def main_split(msg):
    msg_chars = split_by_chars(msg)
    msg_join = split_msg(msg_chars)
    return msg_join
