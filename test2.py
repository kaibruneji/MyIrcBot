from ipwhois import IPWhois


data = IPWhois('213.129.33.83', timeout = 15)
print(data)
print('*********')
data = data.lookup_whois()
print(data)
country = data['nets'][0]['country']
city = data['nets'][0]['city']


    
