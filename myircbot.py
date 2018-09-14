import socket, sys, time, requests, signal # Import modules

#-------functions---------------------------

#function shortening of ic.send...
def send(mes):
  return irc.send(bytes(mes,'utf-8'))

#function of parcing of get TITLE from link

def link_title(n):  
    if 'http://' in n or 'https://' in n:
        link = n.split('//',1)[1].split(' ',1)[0].rstrip()

    elif 'www.' in n:
        link = n.split('www.',1)[1].split(' ',1)[0].rstrip()

    get_title = requests.get('http://%s'%(link), timeout = 10)
    txt_title = get_title.text
    if '</TITLE>' in txt_title or '</title>' in txt_title or '</Title>' in txt_title:        
        if '</TITLE>' in txt_title:
            title = '\x02Title\x02 of '+link+': '+txt_title.split('</TITLE>',1)[0].split('>')[-1]
        elif '</title>' in txt_title:
            title = '\x02Title\x02 of '+link+': '+txt_title.split('</title>',1)[0].split('>')[-1]
        elif '</Title>' in txt_title:
            title = '\x02Title\x02 of '+link+': '+txt_title.split('</Title>',1)[0].split('>')[-1]                

    return title.replace('\r','').replace('\n','').replace('www.','').replace('http://','').replace('https://','').strip()

#-------global changes variables------------

#count of while for anti-flood
exc_timer = 900

# install min & max timer vote
min_timer = 30
max_timer = 300

#-------connect server----------------------

network = 'irc.tambov.ru'  # IRC-server
port = 7770  # IRC-port
irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
channel = '#magi'  # Channel in IRC-server
botName = 'Govnotik'  # Name of this bot
masterName = 'Кай'  # Name of Master of this bot

#-------conect to IRC-server----------------

irc.connect ( ( network, port ) )
print (irc.recv(2048).decode("UTF-8"))
send('NICK '+botName+'\r\n')
send('USER '+botName+' '+botName+' '+botName+' :Python IRC\r\n')
send('JOIN '+channel+' \r\n')
send('NickServ IDENTIFY xxxxxx\r\n') #change xxxxxx for nick code  
send('MODE '+botName+' +x')

#-------global_variables--------------------
    
name = ''
message = ''
message_voting = ''
voting_results = ''
time_vote_rest = 0

count_voting = 0
count_vote_plus = 0
count_vote_minus = 0
count_vote_all = 0
while_count = 0
btc_usd = 0
eth_usd = 0
usd_rub = 0
eur_rub = 0
btc_rub = 0
btc_usd_old = 0
eth_usd_old = 0
usd_rub_old = 0
eur_rub_old = 0
btc_rub_old = 0
btc_usd_su = str('')
eth_usd_su = str('')
usd_rub_su = str('')
eur_rub_su = str('')
time_vote = 0  # how long time in seconds will voting

whois_ip = ''
whois_ip_get_text = ''

timer_exc = 0
time_exc = 0

where_mes_exc = ''
t2 = 0
lock_mes_ready = True

#-------massives----------------------------

dict_users = {}
dict_count = {}
dict_voted = {}
dict_whois = {} 
list_vote_ip = []

list_floodfree = ['Батый', 'Батый_', botName, masterName] #list who free from anti-flood function

#-------major_while-------------------------
  
while True:
    try:
        #if data.find ( 'PRIVMSG' ) != -1 or data.find ( 'PING' ) != -1:
              
        data = irc.recv(2048).decode("UTF-8")

        # ping-pong
        
        if data.find ( 'PING' ) != -1:
            send('PONG'+data.split()[1]+'\r\n')
        
        # make variables Name, Message, IP from user message   

        if data.find ( 'PRIVMSG' ) != -1: 
            name = data.split('!',1)[0][1:] 
            message = data.split('PRIVMSG',1)[1].split(':',1)[1]
        try:
            ip_user=data.split('@',1)[1].split(' ',1)[0]
        except:
            print('no ip_user on 73 line')

        #-----------bot_help---------------

        if 'PRIVMSG '+channel+' :!помощь' in data or 'PRIVMSG '+botName+' :!помощь' in data:
            send('NOTICE %s : Помощь по командам бота:\r\n' %(name))
            send('NOTICE %s : ***Функция опроса: [!опрос (число) сек (тема опрос)], например (пишем \
без кавычек: \"!опрос 60 сек Вы любите ониме?\", если не писат ьвремя, то время установится на 60 сек\r\n' %(name))
            send('NOTICE %s : ***Функция курса: просто пишите (без кавычек): \"!курс\". Писать можно и в приват боту\r\n' %(name))
            send('NOTICE %s : ***Функция айпи: что бы узнать расположение IP, просто пишите (без кавычек): \"!где айпи (IP)\", пример: \"!где айпи \
188.00.00.01\". Писать можно и в приват к боту\r\n' %(name))        

        #-----------anti_flood-------------

        # count of while
        while_count += 1 
        if while_count == 50:
            while_count = 0
            dict_count = {}
                
        # вносит ник в словарь dic_count
        if data.find ( 'PRIVMSG' ) != -1 and name not in dict_count and name not in list_floodfree:
            dict_count[name] = int(1)
            if 'PRIVMSG '+channel in data: #если сообщение в чат, то переменная такая
                where_message = channel
            elif 'PRIVMSG '+botName in data: #если сообщение боту в приват, то переменная такая
                where_message = botName
                
        # если новое сообщение от того же имени совпадает с предыдущим, то счетчик +1 
        if data.find ( 'PRIVMSG' ) != -1 and message == dict_users.get(name) and name not in list_floodfree:
            dict_count[name] += int(1)
          
        # добавляет ключ и значение в массив  
        if data.find ( 'PRIVMSG' ) != -1 and name not in list_floodfree:   
            dict_users[name] = message 
              
        # предупреждает о флуде и банит

        if data.find ( 'PRIVMSG' ) != -1 and name not in list_floodfree:
            for key in dict_count:      
                if dict_count[key] == 3 and key != 'none':
                    send('PRIVMSG '+where_message+' :'+key+', Прекрати флудить!\r\n')
                    dict_count[key] += 1
                elif dict_count[key] > 5 and key != 'none':
                    send('KICK '+channel+' '+key+' :Я же сказал не флуди!\r\n')
                    dict_count[key] = 0             
                
        #--------request-answer in channel-------------   
          
        # out command
        if data.find ( 'PRIVMSG '+channel+' :!бот выйди' ) != -1 and name == masterName: 
            send('PRIVMSG '+channel+' :Хорошо, всем счастливо оставаться!\r\n')
            send('QUIT\r\n')
            sys.exit()

        # message per bot
        if "PRIVMSG %s :!напиши "%(channel) in data or "PRIVMSG %s :!напиши "%(botName) in data and name == masterName:
            mes_per_bot = message.split('!напиши ',1)[1]
            send(mes_per_bot)
            
        #---------whois servis--------------------------

        if 'PRIVMSG '+channel+' :!где айпи' in data or 'PRIVMSG '+botName+' :!где айпи' in data:

            if 'PRIVMSG '+channel+' :!где айпи' in data:
                where_message_whois = channel
                
            elif 'PRIVMSG '+botName+' :!где айпи' in data:
                where_message_whois = name
                          
            try:            
                whois_ip = data.split('!где айпи',1)[1].split('\r',1)[0].strip()
                whois_list_split=whois_ip.split('.')            
                list_whois = []
                for i in whois_list_split:
                    list_whois.append(int(i))
                try: 
                    whois_ip_get = requests.get('https://api.2ip.ua/geo.xml?ip='+whois_ip, timeout = 5)
                except:
                    send('PRIVMSG %s :Ошибка! Не удоалось полчить IP через API!\r\n'%(where_message_whois))
                    continue

                if whois_ip in dict_whois:
                    send('PRIVMSG '+where_message_whois+' :IP взято из памяти:\r\n')
                    send('PRIVMSG %s :%s\r\n'%(where_message_whois,dict_whois[whois_ip]))
                    continue  
                  
                country_whois=whois_ip_get.text.split('<country_rus>',1)[1].split('</country_rus>',1)[0]
                city_whois=whois_ip_get.text.split('<city_rus>',1)[1].split('</city_rus>',1)[0]
                time_zone_whois=whois_ip_get.text.split('<time_zone>',1)[1].split('</time_zone>',1)[0]
                         
                whois_final_reply = ' \x02IP:\x02 '+whois_ip+' \x02Страна:\x02 '+country_whois+' \x02Город:\x02 '+city_whois+' \x02Часовой пояс \
:\x02 '+time_zone_whois+'\r\n'  
                send('PRIVMSG '+where_message_whois+' :'+whois_final_reply)

                #make a IP as kay and final relpy as value in a dict for future use for reply again                                 
                dict_whois[whois_ip] = whois_final_reply         

            except:            
                print('get Value Error in whois servis!')            
                send('PRIVMSG '+where_message_whois+' :Ошибка! Вводите только IP адрес из цифер, разделенных точками! Или существующий ник!\r\n')
                         
        #---------info from link in channel-------------
        try:
            if 'PRIVMSG %s :'%(channel) in data: 
                if 'http://' in data or 'https://' in data or 'www.' in data:
                    send('PRIVMSG %s :%s\r\n'%(channel,link_title(data)))
        except:
            print('Is no title')

        #---------voting--------------------------------          
                    
        t = time.time()   
        if '!стоп опрос' in data and 'PRIVMSG' in data and name == masterName:
            t2 = 0
            print('счетчик опроса сброшен хозяином!')
        if 'PRIVMSG '+channel+' :!опрос ' in data:            
            if t2 == 0 or t > t2+time_vote:
                if ' сек ' not in data:
                    time_vote = 60
                    message_voting = message.split('!опрос',1)[1].strip()  # Make variable - text-voting-title form massage
                if ' сек ' in data:
                    try:
                        time_vote = int(message.split('!опрос',1)[1].split('сек',1)[0].strip()) # get time of timer from user message
                        message_voting = message.split('!опрос',1)[1].split('сек',1)[1].strip()  # Make variable - text-voting-title form massage
                    except:
                        time_vote = 60
                        message_voting = message.split('!опрос',1)[1].strip()  # Make variable - text-voting-title form massage

                if min_timer>time_vote or max_timer<time_vote:
                    send('PRIVMSG %s :Ошибка ввода таймера голования. Введите от %s до %s сек!\r\n'%(channel,min_timer,max_timer))
                    continue
                
                t2 = time.time()
                count_vote_plus = 0
                count_vote_minus = 0
                vote_all = 0
                count_voting = 0
                list_vote_ip = []
                dict_voted = {}  # Обнуляет массив голосования
                send('PRIVMSG %s :Начинается опрос: \"%s\". Опрос будет идти %d секунд. Что бы ответить "да" пишите: \"!да\" \
", что бы ответить "нет" пишите: \"!нет\". Писать можно как открыто в канал, так и в приват боту, что бы голосовать анонимно \r\n' % (channel,message_voting,time_vote))
                list_vote_ip = []   
                    
        # if find '!да' count +1    
        if data.find ( 'PRIVMSG '+channel+' :!да' ) != -1 or data.find ( 'PRIVMSG '+botName+' :!да' ) != -1:
            if ip_user not in list_vote_ip and t2 != 0:
                count_vote_plus +=1            
                dict_voted[name] = 'yes'
                list_vote_ip.append(ip_user)
                send('NOTICE '+name+' :Ваш ответ \"да\" учтен!\r\n')  # Make notice massage to votes user

        # if find '!нет' count +1
        if data.find ( 'PRIVMSG '+channel+' :!нет' ) != -1 or data.find ( 'PRIVMSG '+botName+' :!нет' ) != -1:
            if ip_user not in list_vote_ip and t2 != 0:
                count_vote_minus +=1            
                dict_voted[name] = 'no'
                list_vote_ip.append(ip_user)
                send('NOTICE '+name+' :Ваш ответ \"нет\" учтен!\r\n')  # Make notice massage to votes user 
       
        # if masterName send '!список голосования': send to him privat messag with dictonary Who How voted        
        if data.find ( 'PRIVMSG '+botName+' :!список опроса' ) !=-1 and name == masterName:
            for i in dict_voted:
                send('PRIVMSG '+masterName+' : '+i+': '+dict_voted[i]+'\r\n')

        # count how much was message in channel '!голосование'    
        if data.find ( 'PRIVMSG '+channel+' :!опрос' ) != -1 and t2 != 0:
            count_voting += 1

        # if voting is not end, and users send '!голосование...': send message in channel
        t4 = time.time()
        if data.find ( 'PRIVMSG '+channel+' :!опрос' ) != -1 and t4-t2 > 5:
            t3 = time.time()
            time_vote_rest_min = (time_vote-(t3-t2))//60
            time_vote_rest_sec = (time_vote-(t3-t2))%60
            if (time_vote-(t3-t2)) > 0:
                send('PRIVMSG %s : Предыдущий опрос: \"%s\" ещё не окончен, до окончания опроса осталось: %d мин %d сек\r\n \
' % (channel,message_voting,time_vote_rest_min,time_vote_rest_sec))

        # make variable message rusults voting
        vote_all = count_vote_minus + count_vote_plus    
        voting_results = 'PRIVMSG %s : результаты опроса: \"%s\", "Да" ответило: %d человек(а), "Нет" ответило: %d человек(а), Всего ответило: %d человек(а) \
\r\n' % (channel, message_voting, count_vote_plus, count_vote_minus, vote_all)

        # when voting End: send to channel ruselts and time count to zero    
        if t-t2 > time_vote and t2 != 0:
            t2 = 0
            send('PRIVMSG '+channel+' : Опрос окончен!\r\n')         
            send(voting_results)                    
        
        #---------Exchange-------------

        # get exchange from internet API at regular time  
        time_exc = time.time()
        if timer_exc == 0 or time_exc - timer_exc >= exc_timer or name == masterName and '!обновить курс' in message:
            try:
                btc_usd_su = requests.get('https://free.currencyconverterapi.com/api/v6/convert?q=BTC_USD&compact=y', timeout = 5)
                btc_usd = btc_usd_su.text.split('val":',1)[1].split('}',1)[0][0:]
            except:
                print('проблемы с получением курса btc_usd')
            time.sleep(5)     
            try:
                eth_usd_su = requests.get('https://free.currencyconverterapi.com/api/v6/convert?q=ETH_USD&compact=y', timeout = 5)
                eth_usd = eth_usd_su.text.split('val":',1)[1].split('}',1)[0][0:]
            except:
                print('проблемы с получением курса eth_usd')            
            time.sleep(5)    
            try:
                usd_rub_su = requests.get('https://free.currencyconverterapi.com/api/v6/convert?q=USD_RUB&compact=y', timeout = 5)
                usd_rub = usd_rub_su.text.split('val":',1)[1].split('}',1)[0][0:]
            except:
                print('проблемы с получением курса usd_rub')
            time.sleep(5)    
            try:
                eur_rub_su = requests.get('https://free.currencyconverterapi.com/api/v6/convert?q=EUR_RUB&compact=y', timeout = 5)
                eur_rub = eur_rub_su.text.split('val":',1)[1].split('}',1)[0][0:]
            except:
                print('проблемы с получением курса eur_rub')

            timer_exc = time.time()

            # make numbers to as 0000.00
            float(btc_usd) 
            float(eth_usd)
            float(usd_rub)
            float(eur_rub) 
            float(btc_rub) 

            btc_usd = round(float(btc_usd), 2)
            eth_usd = round(float(eth_usd), 2)
            usd_rub = round(float(usd_rub), 2)
            eur_rub = round(float(eur_rub), 2)
            btc_rub = round(float(btc_usd*usd_rub), 2)

            # make trends symbols from last request
            if btc_usd > btc_usd_old:
                btc_usd_tend = '▲'
            elif btc_usd < btc_usd_old:
                btc_usd_tend = '▼'
            else:
                btc_usd_tend = '■'

            if eth_usd > eth_usd_old:
                eth_usd_tend = '▲'
            elif eth_usd < eth_usd_old:
                eth_usd_tend = '▼'
            else:
                eth_usd_tend = '■'    

            if btc_rub > btc_rub_old:
                btc_rub_tend = '▲'
            elif btc_rub < btc_rub_old:
                btc_rub_tend = '▼'
            else:
                btc_rub_tend = '■'    

            if usd_rub > usd_rub_old:
                usd_rub_tend = '▲'
            elif usd_rub < usd_rub_old:
                usd_rub_tend = '▼'
            else:
                usd_rub_tend = '■'

            if eur_rub > eur_rub_old:
                eur_rub_tend = '▲'
            elif eur_rub < eur_rub_old:
                eur_rub_tend = '▼'
            else:
                eur_rub_tend = '■'    

            # make variables from nubmers for make trends (see up)    
            btc_usd_old = btc_usd
            eth_usd_old = eth_usd
            usd_rub_old = usd_rub
            eur_rub_old = eur_rub
            btc_rub_old = btc_rub        

            btc_usd_str = str(btc_usd)
            eth_usd_str = str(eth_usd)
            usd_rub_str = str(usd_rub)
            eur_rub_str = str(eur_rub)
            btc_rub_str = str(btc_rub)            

            send_res_exc = '\x033Курсы: \x02BTC/USD:\x02 '+btc_usd_str+' '+btc_usd_tend+' \x02ETH/USD:\x02 '+eth_usd_str+' '+eth_usd_tend+' \x02USD/RUB:\x02 \
'+usd_rub_str+' '+usd_rub_tend+' \x02EUR/RUB:\x02 '+eur_rub_str+' '+eur_rub_tend+' \x02BTC/RUB:\x02 \
'+btc_rub_str+' '+btc_rub_tend+'\r\n'
            
        # give exchanges to user on his query 
        if 'PRIVMSG '+channel+' :!курс' in data or 'PRIVMSG '+botName+' :!курс' in data:        
            if 'PRIVMSG '+channel+' :!курс' in data:
                where_mes_exc = channel
            if 'PRIVMSG '+botName+' :!курс' in data:
                where_mes_exc = name
                
            exc_t_restInSec = (exc_timer-(time_exc - timer_exc)) #rest time in seconds for new parser frop API    
                
            send('PRIVMSG %s :%s\r\n'%(where_mes_exc,send_res_exc)) #send to user a message with exchange from memory variable
            send('PRIVMSG %s :курсы обновляются раз в %d мин %d сек, до очередного обновления осталось: %d мин %d \
сек.\r\n'%(where_mes_exc, exc_timer//60, exc_timer%60, exc_t_restInSec//60, exc_t_restInSec%60 ))

        #------------printing---------------      

        print(data)
        if lock_mes_ready == True:
            send('PRIVMSG '+channel+' :Я готов к работе!\r\n')
            lock_mes_ready = False
    except UnicodeDecodeError:
        print('UnicodeDecodeError!')
