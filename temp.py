import re,os,time,sys,json,webbrowser
from win10toast_click import ToastNotifier


url="https://www.youtube.com/watch?v="
def open_url():
    try:
        webbrowser.open(url+latestVideoId)
    except:
        pass
def updateJson(jsonObj):
    with open("data.json","w")as jsonFile:
        jsonFile.write(json.dumps(jsonObj,indent=4))

def readJson():
    with open ("data.json","r")as jsonFile:
        jsonObj=json.loads(jsonFile.read())
        return jsonObj
global latest
latestVideoId=""
toast=ToastNotifier()

args=sys.argv
jsonObj=readJson()
if len(args)>1:
    if args[1]=="add":
        jsonObj["younot"].append({"channel_id":args[2],"channel_name":args[3],"title":"","prev":""})
        updateJson(jsonObj)
        sys.exit()
    if args[1]=="remove":
        for i,n in enumerate(jsonObj["younot"]):
            print(i+1,") ",n["channel_name"])
        ind=int(input("enter no.  : "))
        del(jsonObj["younot"][ind-1])
        updateJson(jsonObj)
        sys.exit()


while True:
    jsonObj=readJson()
    for i in jsonObj["younot"]:
        os.system(f"curl -s https://www.youtube.com/feeds/videos.xml?channel_id={i['channel_id']}>temp.xml")
        print(f"getting RSS feed for {i['channel_id']}")
        patternVideoId=re.compile(r'(<yt:videoId>)(.*)(</yt:videoId>)')
        patternTitle=re.compile(r'(<title>)(.*)(</title>)')
        with open ("temp.xml","r",encoding="utf8")as xemel:
            xml_str=xemel.read()
            videoId=patternVideoId.findall(xml_str)
            Titles=patternTitle.findall(xml_str)
            latestVideoId=videoId[0][1]
            latestTitle=Titles[1][1]
            if latestVideoId!=i["prev"]:
                print("new video uploaded")
                toast.show_toast(
                    "YouNot",
                    f"{i['channel_name']} Uploaded a video {latestTitle}",
                    duration=10,
                    threaded=True,
                    callback_on_click=open_url
                    )
                i["prev"]=latestVideoId
                i["title"]=latestTitle
                updateJson(jsonObj)
    time.sleep(10)