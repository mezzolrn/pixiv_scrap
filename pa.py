import urllib.request
import urllib.parse
import http.cookiejar
import re
import pandas as pd
import numpy as np
import os

BASE_URL = "https://www.pixiv.net/"
ToGetKeyURL = "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"
postURL = "https://accounts.pixiv.net/api/login?lang=zh"

Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
Origin = "https://accounts.pixiv.net"
Referer = "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"
Host = "accounts.pixiv.net"


def MyOpener():
    cookie = http.cookiejar.CookieJar()
    cookieHandle = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(cookieHandle)

    header = \
        {
            "User-Agent": Agent,
            "Origin": Origin,
            "Referer": Referer,
            "Host": Host
        }

    head = []

    for key, value in header.items():
        head.append((key, value))

    opener.addheaders = head
    return opener

def getpostKey(opener,url):
    content=opener.open(url).read().decode("utf-8")
    postkey=re.findall(r"<input.+?name=\"post_key\".+?>",content)[0].split(" ")[3].split("\"")[1]
    print(postkey)
    return postkey

def postData(opener):
    getInfo=getpostKey(opener, ToGetKeyURL)
    post_data=\
        {
            "pixiv_id":"mezzolrn@foxmail.com",
            "password":"******",
            #"captcha":"",
            #"g_recaptcha_response":"",
            "post_key":getInfo,
            #"source":"pc",
            #"ref":"wwwtop_accounts_index",
            #"return_to":"https://www.pixiv.net/",
         }
    post_data=urllib.parse.urlencode(post_data,"utf-8")
    print(post_data.encode("utf-8"))
    if opener.open(postURL,post_data.encode("utf-8")).getcode()==200:
        print("Login Successfully")
        return True
    else:
        print("Login failed")
        return False


pre = "https://i.pximg.net/img-master/img/"
end = "_p0_master1200.jpg"
file = pd.read_csv('colored_sketch_pair.csv', header=None)
# for i in range(file.shape[0]):
#     img = np.array(file[i:i+1])
#     img1 = int(img[0][:1])
#     img2 = int(img[0][1:])
pwd = os.getcwd()

if __name__ == "__main__":
    opener = MyOpener()
    if postData(opener):
        for i in range(1000, 1500):  #file.shape[0]
            path = pwd+'/'+str(i+1)
            if os.path.exists(path) is False:
                os.mkdir(path)
            img = np.array(file[i:i + 1])

            #上色
            img1 = int(img[0][:1])
            id_img = str(img1)
            try:
                text = opener.open("https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + id_img).read().decode(
                "utf-8")
                text = text[text.find("img-master\/img\/"):text.find(id_img + "_p0")].strip().split('\/')[2:]
                text = '/'.join(text)
                f = open(path+'/'+id_img + '_color.jpg', 'wb')
                f.write((opener.open(pre + text + id_img + end)).read())
                f.close()
            except:
                pass

            #线稿
            img2 = int(img[0][1:])
            id_img = str(img2)
            try:
                text = opener.open("https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + id_img).read().decode(
                    "utf-8")
                text = text[text.find("img-master\/img\/"):text.find(id_img + "_p0")].strip().split('\/')[2:]
                text = '/'.join(text)
                f = open(path+'/'+id_img + '_line.jpg', 'wb')
                f.write((opener.open(pre + text + id_img + end)).read())
                f.close()
            except:
                pass

        # id_img = "14534561"
        # text = opener.open("https://www.pixiv.net/member_illust.php?mode=medium&illust_id="+id_img).read().decode("utf-8")
        # text = text[text.find("img-master\/img\/"):text.find(id_img+"_p0")].strip().split('\/')[2:]
        # text = '/'.join(text)
        # f = open(id_img+'.jpg', 'wb')
        # f.write((opener.open(pre+text+id_img+end)).read())
        # f.close()
