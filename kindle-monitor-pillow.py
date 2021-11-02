import time, requests, feedparser, qrcode
from PIL import Image, ImageDraw, ImageFont

#value
SCREEN_W, SCREEN_H = 758, 1024
blank = 20
thick = 5
seniversePK = '' #心知天气API私钥
fontFile = ""

def show_time(hour, minite):
    ampm = ampmList[hour // 12]
    ke = minite // 15
    if minite % 15 > 7:
        ke += 1
    if ke == 4:
        ke = 0
        hour += 1
    shike = shikeList[ke]
    return ampm + chsHourList[hour % 13] + '点' + shike

def show_txt(img, text, size, x, y):
    AA = 4 #抗锯齿
    font = ImageFont.truetype(fontFile, size * AA)
    x_offset, y_offset = font.getoffset(text)
    w, h = font.getsize(text)
    textImg = Image.new('RGBA', (w * AA, h * AA), (255, 255, 255, 0))
    drawText = ImageDraw.Draw(textImg)
    drawText.text([0, 0], text, (0, 0, 0, 255), font)
    textImg = textImg.resize((w, h), resample=Image.ANTIALIAS)
    img.alpha_composite(textImg, (x - (x_offset // AA), y - (y_offset // AA)))

def date(year, month, day, weekday):
    chsWeekday = chsWeekdayList[weekday]
    return str(year) + '年' + str(month) + '月' + str(day) + '日 星期' + chsWeekday

def center(text, size, width = SCREEN_W):
    return (width - (len(text) * size)) // 2

def weather(location):
    r = requests.get('https://api.seniverse.com/v3/weather/now.json?key=' + seniversePK + '&location=' + location + '&language=zh-Hans&unit=c')
    temp = r.json()['results'][0]['now']['temperature']
    stat = r.json()['results'][0]['now']['text']
    code = r.json()['results'][0]['now']['code']
    loc = r.json()['results'][0]['location']['name']
    return(temp, stat, loc, code)

def poem(type):
    r = requests.get('https://v1.jinrishici.com/' + type + '.json')
    content = r.json()['content']
    author = r.json()['author']
    return content, author

def new_line_show_txt(img, text, size, x, y):
    #根据字数换行
    newText = text[:7]
    lineCnt = 1
    for i in range(1, len(text)):
        if i % 7 == 0:
            newText = newText + '\n' + text[i:i + 7]
            lineCnt += 1
    AA = 4 #抗锯齿
    font = ImageFont.truetype(fontFile, size * AA)
    '''
    lineCnt, width, nlFlag = 1, 0, 0
    newText = ''
    for i in range(len(text)): #根据像素数判断是否换行
        w, h = font.getsize(text[i])
        width += w
        if width >= 7 * size * AA - 80:
            newText = newText + text[nlFlag:i] + '\n'
            nlFlag = i
            width = 0
            lineCnt += 1
    newText = newText + text[nlFlag:]
    '''
    x_offset, y_offset = font.getoffset(newText)
    w, h = 7 * size, lineCnt * size
    textImg = Image.new('RGBA', (w * AA, h * AA), (255, 255, 255, 0))
    drawText = ImageDraw.Draw(textImg)
    drawText.text([0, 0], newText, (0, 0, 0, 255), font)
    textImg = textImg.resize((w, h), resample=Image.ANTIALIAS)
    img.alpha_composite(textImg, (x - (x_offset // AA), y - (y_offset // AA)))

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=1,
    border=0,
)

#time data
year = time.localtime().tm_year
month = time.localtime().tm_mon
day = time.localtime().tm_mday
weekday = time.localtime().tm_wday
hour = time.localtime().tm_hour
minite = time.localtime().tm_min
ampmList = ['上午', '下午']
shikeList = ['整', '一刻', '半', '三刻']
chsHourList = ['一', '两', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二']
chsWeekdayList = ['一', '二', '三', '四', '五', '六', '天']
if hour <= 12:
        chsHourList.insert(0, '零')
culueTime = show_time(hour, minite) #粗略时间的英文应该是什么……
date = date(year, month, day, weekday)

#main
img = Image.new('RGBA', (SCREEN_W, SCREEN_H), (255, 255, 255, 255))
draw = ImageDraw.Draw(img)
draw.rectangle([blank, blank, SCREEN_W - blank, blank + 200], None, (0, 0, 0, 255), thick) #时间
draw.rectangle([blank, blank * 2 + 200, (SCREEN_W // 2) - (blank // 2), 700], None, (0, 0, 0, 255), thick) #天气
draw.rectangle([(SCREEN_W // 2) + (blank // 2), blank * 2 + 200, SCREEN_W - blank, 700], None, (0, 0, 0, 255), thick) #新闻
draw.rectangle([blank, 720, SCREEN_W - blank, 1004], None, (0, 0, 0, 255), thick) #诗词

#show time
show_txt(img, '现在是', 48, center('现在是', 48), 40)
show_txt(img, culueTime, 64, center(culueTime, 64), 100)
show_txt(img, date, 36, 190, 170)

#show weather
temp, stat, loc, code = weather('shanghai')
weatherImg = Image.open('weather-icons/' + code + '.png')
weatherImg = weatherImg.resize((200, 200), resample=Image.ANTIALIAS)
show_txt(img, loc + '天气', 48, center(loc + '天气', 48, SCREEN_W // 2), 260)
show_txt(img, str(temp) + '℃', 64, center(temp, 64, SCREEN_W // 2), 330)
show_txt(img, stat, 72, center(stat, 72, SCREEN_W // 2), 420)
img.alpha_composite(weatherImg, (center('空', 200, SCREEN_W // 2), 500))

#show poem
content, author = poem('all')
print(content)
lineCnt = 0
poemLine1, poemLine2, poemLine3 = '', '', ''
for c in range(len(content) - 1): #分段
    if content[c] == '，' or content[c] == '。' or content[c] == '、':
        if poemLine1 == '':
            poemLine1 = content[:c + 1]
            poemLine2 = content[c + 1:]
            continue
        poemLine3 = poemLine2[c - len(poemLine1) + 1:]
        poemLine2 = poemLine2[:c - len(poemLine1) + 1]
show_txt(img, poemLine1, 50, blank + thick + 20, 750)
show_txt(img, poemLine2, 50, blank + thick + 40, 830)
show_txt(img, poemLine3, 50, blank + thick + 60, 910)
show_txt(img, '----' + author, 48, center(author, 48) + 180, 920)

#show news
rss = feedparser.parse('http://www.people.com.cn/rss/politics.xml')
rssTitle = rss.entries[minite // 5].title
rssLink = rss.entries[minite // 5].link
new_line_show_txt(img, rssTitle, 48, SCREEN_W // 2 + blank, 260)
qr.add_data(rssLink)
qr.make(fit=True)
qrcodeImg = qr.make_image(fill_color="black", back_color="white").resize((200, 200))
img.paste(qrcodeImg, (SCREEN_W // 2 + center('空', 200, SCREEN_W // 2), 480))
print(rssTitle)

#save to image
img = img.convert('L').rotate(180) #转换为灰度图片并旋转180度
img.save('kindle-monitor.png')
