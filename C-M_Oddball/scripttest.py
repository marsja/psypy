settings = open('ob_settings.txt', 'r')
di = {}
a=''
linj=[]
for line in settings:
    li=line.strip()
    if not li.startswith("#"):
        if li.endswith(']'):
            a = li[li.find('[')+len('['):li.rfind(']')]
            if len(a) > 3:
                di[a]=''
        n = li.replace('[' + a + ']', '')
        di[a] = n

settings.close()
