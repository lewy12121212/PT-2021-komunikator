
def split_by_chars(word):
    return [char for char in word]

def split_msg(msg):
    iterator = 0

    while iterator <= len(msg):
        if iterator % 50 == 0:
            if msg[iterator] == " ":
                msg.insert(iterator, '\n')
            else:
                j = iterator
                while j>=0:
                    if msg[j] == " ":
                        msg[j] = '\n'
                        break
                    
                    if j == 0:
                        msg.insert(iterator, '\n')
                    j -= 1

                    
            
        iterator += 1

    msg_join = ''.join(msg)
    print(msg_join)
    return msg_join

def main_split(msg):
    msg_chars = split_by_chars(msg)
    msg_join = split_msg(msg_chars)
    return msg_join
