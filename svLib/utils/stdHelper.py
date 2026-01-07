import re


def addToArray(array, element):
    if element not in array:
        array.append(element)
        return True
    return False


def savePage(file_path, page_str):
    w_str = page_str
    p_file = open(file_path, 'w')
    p_file.write(w_str)
    p_file.close()


def loadFileEntries(o_file):
    entries = []
    for line in o_file:
        last_pos = len(line) - 1
        line = str(line[:last_pos]) if line[last_pos] == '\n' or line[last_pos] == '\r' else str(line)
        entries.append(line)

    return entries


def isProxyString(string):
    return len(re.findall(r'(?:[A-Za-z0-9-]+\.)+[A-Za-z0-9]{1,3}:\d{1,6}', string)) > 0
