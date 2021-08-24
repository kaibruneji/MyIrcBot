#-------Import modules---------------------
import socket
import sys
import time
import requests
import settings
import translate_krzb
import whois
import ast
from threading import Thread, Lock
from time import sleep
import os
import copy
from datetime import datetime
from random import randint

from urllib.parse import unquote

#delate error HTTP request certificate from my local
#import urllib3
#urllib3.disable_warnings()

#-------Functions---------------------------

# Function shortening of irc.send. 
def send(mes):
    ##if not a PONG send
    #if 'PONG :' not in mes:
    print(f'>> {mes}')
    return irc.send(bytes(mes,'utf-8'))

# Function of parcing of get TITLE from link.  
def link_title(n):
    if 'http://' in n or 'https://' in n:
        try:
            link_r = n.split('//',1)[1].split(' ',1)[0].rstrip()
        except:
            print('Link wrong!')      
    elif 'www.' in n:
        try:
            link_r = n.split('www.',1)[1].split(' ',1)[0].rstrip()    
        except:
            print('Link wrong!')
    link = 'http://'+link_r        
    max_t_link = 3
    t_link = time.time()
    for i in requests.get(link, stream=True, verify=False):        
        t2_link = time.time()
        if t2_link > t_link + max_t_link:
            requests.get(link, stream=True).close()
            print('Title - Ошибка! Превышено время ожидания!')
            link_stat = False
            break
        else:
            link_stat = True

    if link_stat == True:
        get_title = requests.get(link, timeout = 3)
        txt_title = get_title.content.decode('utf-8')
        if '</TITLE>' in txt_title or '</title>' in txt_title\
                      or '</Title>' in txt_title:
            if '</TITLE>' in txt_title:
                title = '\x02Title\x02: '+ txt_title.split('</TITLE>',1)[0].split('>')[-1]
            elif '</title>' in txt_title:
                title = '\x02Title\x02: '+ txt_title.split('</title>',1)[0].split('>')[-1]
            elif '</Title>' in txt_title:
                title = '\x02Title\x02: '+ txt_title.split('</Title>',1)[0].split('>')[-1]

            title_finish =  title.replace('\r','').replace('\n','').replace\
                   ('www.','').replace('http://','').replace\
                   ('https://','').strip()
            
            return title_finish            
            
        else:
            print('---Title is no!\n')
          
#-------Global changes variables------------

# Install min & max timer vote.  
min_timer = 30
max_timer = 300

#-------Connect server----------------------

network = settings.settings('network')
port = settings.settings('port')
irc = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
channel = settings.settings('channel')
botName = settings.settings('botName')
masterName = settings.settings('masterName')

#-------Conect to IRC-server----------------

irc.connect ((network, port))
#print (irc.recv(2048).decode("UTF-8"))
send('NICK '+botName+'\r\n')
send('USER '+botName+' '+botName+' '+botName+' :Python IRC\r\n')
send('JOIN '+channel+' \r\n')
send('NickServ IDENTIFY '+settings.settings('password')+'\r\n')
#send('MODE '+botName+' +x')

#-------Global_variables--------------------
   
name = ''
message = ''
message_voting = ''
voting_results = ''

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
time_vote = 0

time_of_ping = time.time()
time_of_ping_plus = 60

whois_ip = ''
whois_ip_get_text = ''

timer_exc = 0
time_exc = 0

where_mes_exc = ''
t2 = 0

send_NAMES_on_off = True
JOIN_time = 0

#-------Massives----------------------------

dict_users = {}
dict_count = {}
dict_voted = {}
list_vote_ip = []
list_users = []
list_ascces_to_del_quote = ['Think_Ebola']

# List who free from anti-flood function.
list_floodfree = settings.settings('list_floodfree')
list_bot_not_work = settings.settings('list_bot_not_work')

#-------Major_while-------------------------

while True:  

    #-----------Ping-Pong -------------
    if time_of_ping + time_of_ping_plus < time.time():
        send(f"PRIVMSG :PONG :{network}\n")
        time_of_ping = time.time()
  
    #----------get data message---------- 
    try:
        data = irc.recv(2048).decode("UTF-8")
    except UnicodeDecodeError:
        print('UnicodeDecodeError!!!')        
    
    # Make variables Name, Message, IP from user message.
    if data.find('PRIVMSG') != -1:
        name = data.split('!',1)[0][1:]
        message = data.split('PRIVMSG',1)[1].split(':',1)[1]
    try:
        ip_user=data.split('@',1)[1].split(' ',1)[0]
    except:
        print('no ip_user on 73 line')      
    
    #-----------Translate_krzb---------
    #if a user inter a command !t and text for translate
    if ' :!t' in data:
        if 'PRIVMSG '+channel in data or 'PRIVMSG '+botName in data:
            if 'PRIVMSG '+channel in data:
                where_message = channel            
            elif 'PRIVMSG '+botName in data:
                where_message = name            
            if '!t ' in data:
                tr_txt = message.split('!t ',1)[1].strip()
            else:
                tr_txt = prev_message
            res_txt = translate_krzb.tr(tr_txt)
            send('PRIVMSG '+where_message+' :\x02перевод:\x02 '+res_txt+'\r\n')

    #-----------Bot_help---------------

    if 'PRIVMSG '+channel+' :!помощь' in data or 'PRIVMSG '+botName+' :!помощь' in data:
        send('NOTICE %s : Помощь по командам бота:\r\n' %(name))
        send('NOTICE %s : ***Функция опроса: [!опрос (число) сек (тема опрос)], например\
(пишем без кавычек: \"!опрос 60 сек Вы любите ониме?\", если не писать время, то время\
установится на 60 сек\r\n' %(name))
        #send('NOTICE %s : ***Функция курса: просто пишите (без кавычек): \"!курс\". Писать\
#можно и в приват боту\r\n' %(name))
        send('NOTICE %s : ***Функция айпи: что бы узнать расположение IP, просто пишите\
(без кавычек): \"!где (IP)\", пример: \"!где \
188.00.00.01\". Писать можно и в приват к боту\r\n' %(name))
        send('NOTICE %s : ***Функция перевода с английских букв на русские \
: \"!t tekst perevoda\", пример: \"!t ghbdtn , или пишите просто \"!t\" \
чтобы перевести предыдущее сообщение\r\n' %(name))
        send('NOTICE %s : ***Функция цитат: Поиск цитаты по фразе: Случайная цитата: [!q] \
[!q (фраза поиска для цитаты или её номер)] Поиск следующей цитаты с той же поисковой \
фразой:[!q(номер от 1 до бесконечности) (поисковая фраза)], "например: !q2 ситроен" \
Добавление цитаты: [!aq (фраза для добавления в цитаты)] \
Удаление цитаты (доступно только людям из списка): [!dq (номер цитаты)]\r\n' %(name))

    #-----------Anti_flood-------------

    # Count of while.  
    while_count += 1
    if while_count == 50:
        while_count = 0
        dict_count = {}
            
    # Insert nick in dict: dic_count.  
    if data.find('PRIVMSG') != -1 and name not in dict_count and\
       name not in list_floodfree:
        dict_count[name] = int(1)
        if 'PRIVMSG '+channel in data:
            where_message = channel
        elif 'PRIVMSG '+botName in data:
            where_message = botName
    
    # If new message as last message: count +1.  
    if data.find('PRIVMSG') != -1 and message == dict_users.get(name)\
       and name not in list_floodfree:
        dict_count[name] += int(1)
    
    # Add key and value in massiv.  
    if data.find('PRIVMSG') != -1 and name not in list_floodfree:
        dict_users[name] = message
    
    # Message about flood and kick. 
    if data.find('PRIVMSG') != -1 and name not in list_floodfree:
        for key in dict_count: 
            if dict_count[key] == 3 and key != 'none':
                send('PRIVMSG '+where_message+' :'+key+', Прекрати флудить!\r\n')
                dict_count[key] += 1
            elif dict_count[key] > 5 and key != 'none':                
                send('KICK '+channel+' '+key+' :я же сказал не флуди!\r\n')                
                dict_count[key] = 0
            
    #--------Request-answer in channel-------------
      
    # Out command.  
    if data.find('PRIVMSG '+channel+' :!'+botName+' quit') != -1 and name == masterName:
        send('PRIVMSG '+channel+' :Хорошо, всем счастливо оставаться!\r\n')
        
        lock.acquire()
        stop_th_auto_ping = True
        lock.release()
        
        send('QUIT\r\n')
        sys.exit()

    # Message per bot.  
    if "PRIVMSG %s :!напиши "%(channel) in data or\
       "PRIVMSG %s :!напиши "%(botName) in data and name == masterName:
        mes_per_bot = message.split('!напиши ',1)[1]
        send(mes_per_bot)
        
    #---------Whois servis--------------------------

    if 'PRIVMSG '+channel+' :!где' in data\
      or 'PRIVMSG '+botName+' :!где' in data:

        if 'PRIVMSG '+channel+' :!где' in data:
            where_message_whois = channel
            
        elif 'PRIVMSG '+botName+' :!где' in data:
            where_message_whois = name
                      
        try:
            whois_ip = data.split('!где ',1)[1].split('\r',1)[0].strip()
            get_whois = whois.whois(whois_ip) 
            
            country_whois = get_whois['country']
            city_whois = get_whois['city']
            address_whois = get_whois['address']    
            print(get_whois)

            if country_whois == None:
                country_whois = 'None'
            if city_whois == None:
                city_whois = 'None'
            if address_whois == None:
                address_whois = 'None'    
                       
            whois_final_reply = ' \x02IP:\x02 '+whois_ip+' \x02Страна:\x02 '+\
            country_whois+' \x02Город:\x02 '+city_whois+' \x02Адресс:\x02 '+address_whois
            send('PRIVMSG '+where_message_whois+' :'+whois_final_reply+' \r\n')        

        except IndexError:
            print('except IndexError!')
            send('PRIVMSG '+where_message_whois+' :Ошибка! Вводите только IP адрес \
из цифр, разделенных точками!\r\n')
        
        except ValueError:
            print('except ValueError!')
            send('PRIVMSG '+where_message_whois+' :Ошибка! Вводите только IP адрес \
из цифр, разделенных точками!\r\n')
        
    #---------Info from link in channel-------------
    
    if 'PRIVMSG %s :'%(channel) in data and '.png' not in data and '.jpg' not in data and '.doc'\
        not in data and 'tiff' not in data and 'gif' not in data and '.jpeg' not in data and '.pdf' not in data:
        if 'http://' in data or 'https://' in data or 'www.' in data:
            try:
                text_title = link_title(data)            
                if text_title.strip() != 'None':
                    send('PRIVMSG %s :%s\r\n'%(channel,text_title))
            except requests.exceptions.ConnectionError:
                print('Ошибка получения Title (requests.exceptions.ConnectionError)\n')
                send('PRIVMSG '+channel+' :Ошибка, возможно такого адреса нет\n')
            except:
                print('Error link!\n')   
                
    #---------Voting--------------------------------
                
    t = time.time()
    if '!стоп опрос' in data and 'PRIVMSG' in data and name == masterName:
        t2 = 0
        print('счетчик опроса сброшен хозяином!\n')
    if 'PRIVMSG '+channel+' :!опрос ' in data and ip_user not in list_bot_not_work:
        if t2 == 0 or t > t2+time_vote:
            if ' сек ' not in data:
                time_vote = 60
                # Make variable - text-voting-title form massage.  
                message_voting = message.split('!опрос',1)[1].strip()
            if ' сек ' in data:
                try:
                    # Get time of timer from user message.  
                    time_vote = int(message.split('!опрос',1)[1].split('сек',1)[0].strip())
                    # Make variable - text-voting-title form massage.  
                    message_voting = message.split('!опрос',1)[1].split('сек',1)[1].strip()
                except:
                    time_vote = 60
                    # Make variable - text-voting-title form massage.  
                    message_voting = message.split('!опрос',1)[1].strip()

            if min_timer>time_vote or max_timer<time_vote:
                send('PRIVMSG %s :Ошибка ввода таймера голосования.\
Введите от %s до %s сек!\r\n'%(channel,min_timer,max_timer))
                continue
            
            t2 = time.time()
            count_vote_plus = 0
            count_vote_minus = 0
            vote_all = 0
            count_voting = 0
            list_vote_ip = []
            # Do null voting massiv.  
            dict_voted = {}
            send('PRIVMSG %s :Начинается опрос: \"%s\". Опрос будет идти \
%d секунд. Чтобы ответить "да", пишите: \"!да\" \
", чтобы ответить "нет", пишите: \"!нет\". Писать можно как открыто в канал,\
так и в приват боту, чтобы голосовать анонимно \r\n' % (channel,message_voting,time_vote))
            list_vote_ip = []
                
    # If find '!да' count +1.  
    if data.find('PRIVMSG '+channel+' :!да') != -1 or data.find('PRIVMSG '+botName+' :!да') != -1:
        if ip_user not in list_vote_ip and t2 != 0:
            count_vote_plus +=1
            dict_voted[name] = 'yes'
            list_vote_ip.append(ip_user)
            # Make notice massage to votes user.  
            send('NOTICE '+name+' :Ваш ответ \"да\" учтен!\r\n')

    # If find '!нет' count +1.  
    if data.find('PRIVMSG '+channel+' :!нет') != -1 or data.find('PRIVMSG '+botName+' :!нет') != -1:
        if ip_user not in list_vote_ip and t2 != 0:
            count_vote_minus +=1
            dict_voted[name] = 'no'
            list_vote_ip.append(ip_user)
            # Make notice massage to votes user.  
            send('NOTICE '+name+' :Ваш ответ \"нет\" учтен!\r\n')
   
    # If masterName send '!список голосования': send to him privat messag with dictonary Who How voted.  
    if data.find('PRIVMSG '+botName+' :!список опроса') !=-1 and name == masterName:
        for i in dict_voted:
            send('PRIVMSG '+masterName+' : '+i+': '+dict_voted[i]+'\r\n')

    # Count how much was message in channel '!голосование'.  
    if data.find('PRIVMSG '+channel+' :!опрос') != -1 and t2 != 0:
        count_voting += 1

    # If voting is not end, and users send '!голосование...': send message in channel.  
    t4 = time.time()
    if data.find('PRIVMSG '+channel+' :!опрос') != -1 and t4-t2 > 5:
        t3 = time.time()
        time_vote_rest_min = (time_vote-(t3-t2))//60
        time_vote_rest_sec = (time_vote-(t3-t2))%60
        if (time_vote-(t3-t2)) > 0:
            send('PRIVMSG %s : Предыдущий опрос: \"%s\" ещё не окончен, до окончания \
опроса осталось: %d мин %d сек\r\n \
' % (channel,message_voting,time_vote_rest_min,time_vote_rest_sec))

    # Make variable message rusults voting.  
    vote_all = count_vote_minus + count_vote_plus
    voting_results = 'PRIVMSG %s : результаты опроса: \"%s\", "Да" ответило: %d \
человек(а), "Нет" ответило: %d человек(а), Всего ответило: %d человек(а) \
\r\n' % (channel, message_voting, count_vote_plus, count_vote_minus, vote_all)

    # When voting End: send to channel ruselts and time count to zero.  
    if t-t2 > time_vote and t2 != 0:
        t2 = 0
        send('PRIVMSG '+channel+' : Опрос окончен!\r\n')
        send(voting_results)
    
    #---------Exchange-------------
    # Get exchange from internet API at regular time.   
    """
    if 'PRIVMSG '+channel in data and '!курс' in data or 'PRIVMSG '+botName+' :!курс' in data:
        if 'PRIVMSG '+channel in data and '!курс' in data:
            where_mes_exc = channel
        if 'PRIVMSG '+botName+' :!курс' in data:
            where_mes_exc = name
        
        #user_req_trend = "https://www.google.com/search?q=курс"+data.split("!курс")[1]
        user_req_trend = "https://www.google.com/search?q=курс+рубля+к+доллару"
        print("user_req_trend: "+user_req_trend+"\r\n")
        google_trend_get_req = requests.get(user_req_trend, timeout = 7)
        google_trend_text = google_trend_get_req.text
        print("google:\r\n"+google_trend_text+'\r\n')
        google_dig_trend = google_trend_text.split('data-value="')[1].split('">')[0]       

        send('PRIVMSG %s :%s\r\n'%(where_mes_exc,google_dig_trend))       
        """
    #---------Quotes-------------
    
    # func to find a quote    
    def find_quote(find_text, num_quote = 1, is_add_quote = False):
        #find numbers of all quotes
        with open('quotes/'+channel.split('#')[1]+'.txt', 'r+', encoding="utf8") as f:
            num_of_all_quotes = 0
            count_twin_q = 0
            count_quote = 1
            for line in f:
                num_of_all_quotes += 1
                
        #find a not digit request for quote        
        if not find_text.isdigit():
            #...find a number of all twins 
            with open('quotes/'+channel.split('#')[1]+'.txt', 'r', encoding="utf8") as f:                                            
                for line in f:                    
                    if find_text in line:
                        count_twin_q += 1
                            
            #find a quote with user request text
            with open('quotes/'+channel.split('#')[1]+'.txt', 'r', encoding="utf8") as f:                    
                    count_next = num_quote
                    if is_add_quote == False:
                        for line in f:
                            if find_text in line: 
                                if count_next == 1:                                
                                    return [count_quote, num_of_all_quotes, line, count_twin_q]                                
                                else:
                                    count_next -= 1
                            count_quote += 1
                        return False
                    #if find for add a quote        
                    else:
                        line_txt = ""
                        for line in f:
                            if line.count("|") == 2:
                                line_txt = line.split('|')[2].strip()
                            if line.count("|") == 3:
                                line_txt = line.split('|')[3].strip()
                            
                            if find_text == line_txt: 
                                if count_next == 1:
                                    print(f"count_quote: {count_quote}\nnum_of_all_quotes: {num_of_all_quotes}\nline: {line}\ncount_twin_q: {count_twin_q}")
                                    return [count_quote, num_of_all_quotes, line, count_twin_q]                                
                                else:
                                    count_next -= 1
                            count_quote += 1
                        return False        
                    
        # find a numeric quote            
        else:
            with open('quotes/'+channel.split('#')[1]+'.txt', 'r+', encoding="utf8") as f:
                for line in f:
                    if int(count_quote) == int(find_text):                        
                        return [count_quote, num_of_all_quotes, line, count_twin_q]
                    count_quote += 1                
    
    # show a random quote
    if f'PRIVMSG {channel} :!q\r\n' in data:
        try:
            num_all_q = copy.copy(find_quote('1'))
            random_num_quote = randint(1, (num_all_q[1]))
            data_q = find_quote(str(random_num_quote))
            send(f'PRIVMSG {channel} :\x0314({data_q[0]}/{data_q[1]} {data_q[2].split("|")[1]})\x03 \
{data_q[2].split("|")[2]}\n')
        except: send(f'PRIVMSG {channel} :ошибка показа цитаты!\n')
            
        
    # find a quote
    if f'PRIVMSG {channel} :!q ' in data and data.split('!q ') != '\r\n':
        try:
            quote_txt_find = data.split('!q ')[1].strip()
            if find_quote(quote_txt_find) == False:
                send(f'PRIVMSG {channel} :такой цитаты не найдено!\n')
            else:
                data_q = copy.copy(find_quote(quote_txt_find))
                #if search by digit
                if data_q[3] == 0:
                    #if no time stamp!
                    if data_q[2].count("|") == 2: 
                        send(f'PRIVMSG {channel} :\x0314({data_q[0]}/{data_q[1]} {data_q[2].split("|")[1]})\x03 \
{data_q[2].split("|")[2]}\n')
                    #if time stamp in quote file!
                    else:
                        send(f'PRIVMSG {channel} :\x0314{data_q[2].split("|")[1]}:({data_q[0]}/{data_q[1]} {data_q[2].split("|")[2]})\x03 \
{data_q[2].split("|")[3]}\n')
                #if search by string
                else:
                    #if no time stamp!
                    if data_q[2].count("|") == 2:
                        send(f'PRIVMSG {channel} :\x0314({data_q[0]}/{data_q[1]} {data_q[2].split("|")[1]}) \
[{data_q[3]}]\x03 {data_q[2].split("|")[2]}\n')
                    #if time stamp in quote file!
                    else:
                        send(f'PRIVMSG {channel} :\x0314{data_q[2].split("|")[1]}:({data_q[0]}/{data_q[1]} {data_q[2].split("|")[2]}) \
[{data_q[3]}]\x03 {data_q[2].split("|")[3]}\n')
        except: send(f'PRIVMSG {channel} :ошибка показа цитаты!\n')
        
            
    # find a quote with last request but next quote
    if f'PRIVMSG {channel} :!q' in data and data.split('!q')[1] != '\r\n':
        if data.split('!q')[1].split(' ')[0].isdigit():
            num_next_quote = data.split('!q')[1].split(' ')[0]            
            quote_txt_find = data.split('!q')[1].split(' ')[1].strip()            
            data_q = copy.copy(find_quote(quote_txt_find, int(num_next_quote)))
            if data_q == False:
                send(f'PRIVMSG {channel} :такой цитаты не найдено!\r\n')
            else:
                #if no time stamp!
                if data_q[2].count("|") == 2:
                    send(f'PRIVMSG {channel} :\x0314({data_q[0]}/{data_q[1]} {data_q[2].split("|")[1]}) \
[{num_next_quote}/{data_q[3]}]\x03 {data_q[2].split("|")[2]}\n')
                #if time stamp in quote file!
                else:
                    send(f'PRIVMSG {channel} :\x0314{data_q[2].split("|")[1]}:({data_q[0]}/{data_q[1]} {data_q[2].split("|")[2]}) \
[{num_next_quote}/{data_q[3]}]\x03 {data_q[2].split("|")[3]}\n')
                    
    # Add a new quote
    switch_add_q = False
    if f'PRIVMSG {channel} :!aq ' in data:
        req_user_quote = data.split('!aq ')[1].strip()
        #if a quote 500-1000 bytes
        try:
            quote_rart_1 = req_user_quote.split('\r\n')[0]
            quote_rart_2 = req_user_quote.split(f'PRIVMSG {channel} :')[1]
            req_user_quote = quote_rart_1 + quote_rart_2
        except:
            print("add a single quote\n")
        
        #add a quote
        if '|' in req_user_quote:
            send(f'PRIVMSG {channel} :в цитату нельзя добавлять символ "|"!\n')
            break
        elif req_user_quote == '':
            send(f'PRIVMSG {channel} :нельзя вводить пустое сообщение!\n')
        elif req_user_quote[0].isnumeric():
            send(f'PRIVMSG {channel} :нельзя вводить первым символом цифру!\n')
        else:            
            with open('quotes/'+channel.split('#')[1]+'.txt', 'a', encoding="utf8") as f:
                
                f.write(f'\n{channel}|{datetime.now().date()}|{name}|{req_user_quote}')
                switch_add_q = True                    
                
        #get and show number of added a quote        
        if switch_add_q == True:        
            data_q = copy.copy(find_quote(req_user_quote, 1, True))
            if data_q == False:    
                send(f'PRIVMSG {channel} :цитата добавлена, но его номер не получен\n')
            else:
                send(f'PRIVMSG {channel} :цитата добавлена под номером {data_q[0]}\n')
            switch_add_q = False
    
    # Delete a quote    
    if f'PRIVMSG {channel} :!dq' in data:
        if name == masterName or name in list_ascces_to_del_quote: 
            num_dq = data.split('!dq ')[1].strip()            
            if num_dq.isdigit():
                data_q = copy.copy(find_quote(num_dq))
                if data_q == False:
                    send(f'PRIVMSG {channel} :цитаты с таким номером не найдено!\r\n')
                else:        
                    with open('quotes/'+channel.split('#')[1]+'.txt', 'r', encoding="utf8") as f:
                        q_file = f.read()                        
                    with open('quotes/'+channel.split('#')[1]+'.txt', 'w', encoding="utf8") as f:
                        #if delete a last quote - delate and empty string
                        if str(num_dq) == str(data_q[1]):                            
                            f.write(q_file.replace(f'\n{data_q[2]}',''))
                        #if delete not a last quote
                        else:
                            print('if delete not a last quote\n')
                            f.write(q_file.replace(data_q[2],''))                        
            
                    send(f'PRIVMSG {channel} :цитата удалена!\r\n')            
        
            else:
                send('PRIVMSG '+channel+' :нужно ввести номер цитаты для удаления!\r\n')            
    
    prev_message = message
        
    #------------Printing---------------

    print(data)    
