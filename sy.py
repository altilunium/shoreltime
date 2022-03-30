import pystray
import time
from PIL import Image, ImageDraw, ImageFont
import threading
import math
import datetime
import pickle



cmonth = datetime.datetime.now().month
day = datetime.datetime.now().day
now = datetime.datetime.now()
now = now.strftime("%H.%M")

lamd = 106.9977272014839
#Masukkan latitude (south = negative)
phi = -6.296397800971034
#Masukkan zona waktu (GMT+/-)
td = 7

rad = 3.14159 / 180
lamd = (lamd / 360) * 24
phi = phi * rad
n0 = 0


def toSec(x):
    return (x.hours * 3600) + (x.minutes * 60) + (x.seconds)

def something():
    global x, tloc,st,n,a,z
    t = n + ((a - lamd)/24)
    m = ((0.9856*t) - 3.289)*rad
    l = m + (1.916*rad*math.sin(m)) + (0.02*rad*math.sin(2*m)) + (282.634*rad)
    lh = (l/3.14159)*12
    ql = int(lh/6) + 1
    if ((int(ql/2)*2)-ql) != 0:
        ql = ql -1
    ra = math.atan(0.91746*math.tan(l))/3.14159*12
    ra = ra + (ql*6)
    sind = 0.39782*math.sin(l)
    cosd = math.sqrt(1-sind*sind)
    x = (math.cos(z) - sind*math.sin(phi))/(cosd*math.cos(phi))
    if abs(x) > 1:
        return
    else:
        atnx = math.atan(math.sqrt(1-x*x)/x)/rad
        if atnx < 0:
            atnx = atnx + 180
        h = (360-atnx)*24/360
        if a == 18:
            h = 24-h
        tloc = h + ra - (0.06571*t) - 6.622
        tloc = tloc + 24
        tloc = tloc - (int(tloc/24)*24)
        st = tloc - lamd + td

def getShoTime():
    global n,a,z
    month = [31,28,31,30,31,30,31,31,30,31,30,31]
    currentmonth = 1
    currentday = 0
    for d in month:
        for k in range(1,d+1):
            t = [0,0,0,0,0,0]

            currentday = currentday + 1
            #n = n0 + k
            n = currentday


            #subuh azimut 108
            a = 6
            z = 108*rad
            something()
            if abs(x) <= 1:
                t[0] = st

            #sunrise azimut 90+5/6
            z = (90+5/6)*rad
            something()
            t[1] = st


            #sunset azimut 90+5/6
            a = 18
            z = (90+5/6)*rad
            something()
            sunset = st

            #magrib = sunset + toleransi 2/60
            t[4] = st + 2/60

            #isya azimut 108
            z = 108*rad
            something()
            if abs(x) <= 1:
                t[5] = st

            #midday = (sunrise + sunset)/2
            midday = (t[1] + sunset)/2

            #zuhur = midday + padding 2/60
            t[2] = midday + 2/60

            #ashar = (zuhur + magrib)/2
            t[3] = (t[2] + t[4])/2


            if (k == day) and (currentmonth == cmonth):
                bagSha = []
                bagSa = ["I","s","z","a","m","i"]
                #print(str(k)+"\t",end='')
                counter = 0

                bagSha.append(datetime.time(0,0,0))
                for jadwal in t:
                    th = int(jadwal)
                    tm = int((jadwal-th)*60)
                    nya = datetime.time(th,tm,0)
                    if counter != 1:
                        bagSha.append(nya)
                    #print(str(th)+":"+str(tm)+"\t",end='')
                    counter = counter + 1
                #print("\n")
                bagSha.append(datetime.time(23,59,59))

                cache = dict()
                timestring = str(cmonth) +"-"+str(day)
                cache['bagSha'] = bagSha
                pickle.dump(cache,open(timestring,'wb'))

                counter = 0
                for i in bagSha:
                    now = datetime.datetime.now().time()
                    #now = datetime.time(19,45,0)
                    if now < i:
                        seli = datetime.datetime.combine(datetime.date.today(), i) - datetime.datetime.combine(datetime.date.today(), now)
                        gap = datetime.datetime.combine(datetime.date.today(), i) - datetime.datetime.combine(datetime.date.today(), bagSha[counter-1])
                        perc = 100 - int(seli.seconds / gap.seconds * 100)
                        #print(bagSa[counter-1]+str(perc))
                        return bagSa[counter-1]+str(perc)
                        break
                    counter = counter + 1   
                            
        currentmonth = currentmonth + 1





def getShoTime_c():
    try:
        timestring = str(cmonth) +"-"+str(day)
        a = pickle.load(open(timestring,'rb'))
        print("Loaded!")
        bagSha = a['bagSha']
        for i in bagSha:
            now = datetime.datetime.now().time()
            if now < i:
                seli = datetime.datetime.combine(datetime.date.today(), i) - datetime.datetime.combine(datetime.date.today(), now)
                gap = datetime.datetime.combine(datetime.date.today(), i) - datetime.datetime.combine(datetime.date.today(), bagSha[counter-1])
                perc = 100 - int(seli.seconds / gap.seconds * 100)
                #print(bagSa[counter-1]+str(perc))
                return bagSa[counter-1]+str(perc)
                break
            counter = counter + 1  

    except:
        return getShoTime()





def create_image(width, height, x, bg,fc):
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), bg)
    dc = ImageDraw.Draw(image)
    '''
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)
    '''
    font_type  = ImageFont.truetype("arial.ttf", 48)
    c ="21"
    dc.text((8,5), f"{x}", fill=fc, font = font_type)

    return image




isEnd = False    

def stop():
    print("Quitting")
    global isEnd
    icon.stop()
    isEnd = True
    


# In order for the icon to be displayed, you must provide an icon
icon = pystray.Icon(
    'test name',
    icon=create_image(64, 64, ".", "green","black"),
    menu=pystray.Menu(pystray.MenuItem("Quit",stop)))

def updateIcon():
    global isEnd
    n = 1
    isFirst = True
    while not isEnd:
        print("Alive!")
        sho = getShoTime_c()
        code = sho[0]
        num = sho[1:]

        pagi = (146,207,233)
        siang = (0,83,156)
        sore = (246,215,115)
        magrib = (216,51,51)
        malam = (32,52,63)

        if code =='I':
            back = "black"
            front = "white"
        elif code == 's':
            back = pagi
            front = "black"
        elif code == 'z':
            back = siang
            front = "white"
        elif code == 'a':
            back = sore
            front = "black"
        elif code == 'm':
            back = magrib
            front = "white"
        elif code == 'i':
            back = malam
            front = "white"


        icon.icon = create_image(64, 64, num, malam,"white")

        if isFirst:
            isFirst = False
            time.sleep(60)
        else:
            time.sleep(60)


x = threading.Thread(target=updateIcon)
x.start()
icon.run()
quit()




