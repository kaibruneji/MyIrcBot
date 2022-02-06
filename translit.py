dict_translit = {'a':'а','b':'б','v':'в','g':'г','d':'д','e':'е','jo':'ё','i':'и','j':'й','k':'к','l':'л',
'm':'м','n':'н','o':'о','p':'п','r':'р','s':'с','t':'т','u':'у','f':'ф','h':'х','x':'х','c':'ц',
'w':'щ','y':'ы','q':'я'}

list_translit_message = []

def func_translit(get_message):
    get_message_lower = get_message.lower()
    for i in get_message_lower:
        if i not in dict_translit:
            list_translit_message.append(i)
        if i in dict_translit:
            list_translit_message.append(dict_translit.get(i[, default]))
    return list_translit_message
        
