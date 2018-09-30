network = 'irc.tambov.ru'
port = 7770
channel = '#magi'
botName = 'Govnotik'
masterName = 'Кай'
password = 'xxxxxx'
list_floodfree = ['Батый', 'Батый_', botName, masterName]

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
