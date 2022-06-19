#----- Help -----

# This module make a file for public in web server

#----- Import moduls -----

import sys
import re

#----- Settings -----

swapFile = ""

#----- main ------

def makeFileWWW(channel):
    #inFile = f'/root/git/quotes/{channel}.txt'
    #outFile = f'/var/www/oldrazor.ru/public_html/{channel}.html'
    #outFile = f'{channel}.html'    
    
    swapFile = ""
    
    with open(inFile, 'r', encoding='utf8') as f:  
        swapFile = f.read()
    
    reFile = re.sub(f'#{channel}','</p><p>',swapFile)
     
    with open(outFile, 'w', encoding='utf-8') as f:
        f.write(f'<html>\n<head><title>\nquotes of #magi\n</title>\n\
        <meta charset="utf-8">\n<meta name="robots" content="noindex"/>\n\
        </head>\n<body>\n<p>{reFile}\n</p>\n</body>\n</html>')
   
   