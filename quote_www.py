#----- Help -----

# This module make a file for public in web server

#----- Import moduls -----

import sys
import re

#----- Settings ------


OutFile = "/var/www/oldrazor.ru/public_html/magi.html"
swapFile = ""

#----- main ------

def makeFileWWW(fileName, channel):
    with open(fileName, 'r', encoding='utf8') as f:                
        #f.write(f'\n{channel}|{datetime.now().date()}|{name}|{req_user_quote}')
        swapFile = f.read()
    
     reFile = re.sub('channel','<br>',swapFile)
     
     with open(OutFile, 'w', encoding='utf-8') as f:
         f.write(f'<html>\n<head><title>\nquotes of #magi\n</title>\n\
         <meta charset="utf-8">\n<meta name="robots" content="noindex"/>\n\
         </head>\n<body>\n<p>{reFile}\n</p>\n</body>\n</html>')
   
   