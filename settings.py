import json

network = 'irc.tambov.ru'
port = 7770
botName = 'boty'
masterName = 'Кай'
list_floodfree = ['Батый', 'Батый_', botName, masterName]
list_bot_not_work = ['iphone.telenet.ru', 'ec2-54-211-164-67.compute-1.amazonaws.com']

#----input_password-----
with open('code.json', 'r') as code_json:
    code=code_json.read()   

obj = json.loads(code)

password = str(obj['password'])
channel = str(obj['channel'])

def settings(x):
    if x == 'network':
        return network
    elif x == 'port':
        return port
    elif x == 'botName':
        return botName
    elif x == 'masterName':
        return masterName
    elif x == 'password':
        return password
    elif x == 'list_floodfree':
        return list_floodfree
    elif x == 'channel':
        return channel
    elif x == 'list_bot_not_work':
        return list_bot_not_work
