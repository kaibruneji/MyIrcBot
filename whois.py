from ipwhois import IPWhois

def whois(ip):
    data = IPWhois(ip, timeout = 15)
    data = data.lookup_whois()
    region = data['nets'][0]['region']
    country = data['nets'][0]['country']
    city = data['nets'][0]['city']    
    address = data['nets'][0]['address']
    return {'region' region,'city': city, 'country': country, 'address': address}
    
