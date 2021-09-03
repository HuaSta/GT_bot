import os
PATH = 'c:/Users/colez/Documents/VS python code/Discord bot/tracking.txt'
blacklist = ['Don\'t', 'A', 'A Few', 'A Little', 'All', 'An', 'Another', 'Any', 'Anybody', 
             'Anyone', 'Anything', 'Anywhere', 'Both', 'Certain', 'Each', 'Either', 'Enough', 
             'Every', 'Everybody', 'Everyone', 'Everything', 'Everywhere', 'Few', 'Fewer', 'Fewest', 
             'Last', 'Least', 'Less', 'Little', 'Many', 'Many A', 'More', 'Most', 'Much', 'Neither', 
             'Next', 'No', 'No One', 'Nobody', 'None', 'Nothing', 'Nowhere', 'Once', 'One', 'Said', 
             'Several', 'Some', 'Somebody', 'Something', 'Somewhere', 'Sufficient', 'That', 'The', 
             'These', 'This', 'Those', 'Us', 'We', 
             'What', 'Whatever', 'Which', 'Whichever', 'You', 'I', 'To', 'It', 'Is', 'In',
             'And', 'Have', 'Be', 'Of', 'Oh', 'My', 'For', 'Was', 'Just', 'Not', 'On', 'Me', 'Do'
             'At', 'So', 'With', 'Like', 'Your', 'Can', 'But', 'When', 'It\'s', 'Are']
def update(person, string):
    with open(PATH, 'r', encoding='utf-8') as f:
        text = f.read()
        if text:
            word_dict = eval(text)
        else:
            word_dict = {person: {}}
    string = string.split(sep=' ')
    if person not in word_dict:
        word_dict[person] = {}
    for word in string:
        if word == '':
            continue
        if word[-1] in '.,!?':
            word = word[:-1]
        if word in blacklist:
            continue
        if word not in word_dict[person]:
            word_dict[person][word] = 1
        else:
            word_dict[person][word] += 1
    word_dict = str(word_dict)
    with open(PATH, 'w', encoding='utf-8') as f:
        f.write(word_dict)

def topWords(person):
    with open(PATH, 'r', encoding='utf-8') as f:
        text = f.read()
    if text:
        word_dict = eval(text)
    else:
        return 'None'
    output = ''
    count = 0
    for x, y in sorted(word_dict[person].items(), key=lambda x: x[1], reverse=True):
        if count >= 10:
            break
        if len(x) > 8:
            x = x[0:8] + '...:'
        x = x + ' '*(16-len(x))    
        output += f'{x} {y}\n'
        count += 1
    return output

def serverTop():
    with open(PATH, 'r', encoding='utf-8') as f:
        text = f.read()
    if text:
        word_dict = eval(text)
    else:
        return 'None'
    output = ''
    count = 0
    new_dict = {}
    for person in word_dict:
        for word in word_dict[person]:
            if word not in new_dict:
                new_dict[word] = word_dict[person][word]
            else:
                new_dict[word] += word_dict[person][word]
    for x, y in sorted(new_dict.items(), key=lambda x: x[1], reverse=True):
        if count >= 10:
            break
        if len(x) > 8:
            x = x[0:8] + '...:'
        x = x + ' '*(16-len(x))  
        output += f'{x} {y}\n'
        count += 1
    return output

'''
with open(PATH, 'r', encoding='utf-8') as f:
    text = f.read()
if text:
    word_dict = eval(text)
for person in word_dict:
    for name in blacklist:
        word_dict[person].pop(name, None)
with open(PATH, 'w', encoding='utf-8') as f:
    f.write(str(word_dict))
'''
