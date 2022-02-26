PATH = '.\\texts\\dictionary.txt'

def get_dict():
    """get the contents of dictionary.txt and return it as a dictionary"""
    with open(PATH, 'r', encoding='utf-8') as f:
        s = f.read()
        return eval(s)

def update_dict(ssname, discord_id):
    """Update dictionary.txt with spreadsheet name and discord ID"""
    print(ssname)
    with open(PATH, 'r', encoding='utf-8') as f:
        content = f.readlines()
    if not content:
        print("no content")
        content = "{{\'{0}\': {1}}}".format(ssname, discord_id)
        print('first ',content)
    else:
        for item in content:
            print(item)
            if ssname == item.split('\'')[1]:
                return "Name matches another one already in the registry!"
        print('second ', content)
        content[-1] = content[-1][:-1] + ',\n'
        content.append('\'{0}\': {1}}}'.format(ssname, discord_id))
        content = "".join(content)
        print('third ', content)

    with open(PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    return "Added {} into the registry".format(ssname)

def delete_item(ssname):
    """Deletes an item from dictionary.txt"""
    flag = False
    with open(PATH, 'r', encoding='utf-8') as f:
        content = f.readlines()
    for content_item in content:
        if ssname in content_item:
            """Check if another name matches the name searched..."""
            count = 0
            for item in content:
                if ssname in item:
                    count += 1
                if ssname == item.split('\'')[1]:
                    content_item = item
                    flag = True
                    break
            if count > 1 and flag == False:
                return "Found 2 or more names that match the term {}, please specify".format(ssname)
            content.remove(content_item)
            if content:
                if '}' in content_item:
                    content[-1] = content[-1][:-2] + '}'
                content = "".join(content)
            else:
                content = ""
            with open(PATH, 'w', encoding='utf-8') as f:
                f.write(content)
            name = content_item.split('\'')[1]
            return "Removed {}".format(name)
    return "{} was not found, note that this is case sensitive. Use $list for a list of names".format(ssname)

def list_names():
    with open(PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    if not content:
        return ["Nothing"]
    keys = list(eval(content).keys())
    keys.sort()
    return keys
