from ipwhois import IPWhois

def whois(ip):
    data = IPWhois(ip, timeout = 15)
    data = data.lookup_whois()    
    
    return data
    
