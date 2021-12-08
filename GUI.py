import tkinter as tk
import cv2
import pymysql
import time
from datetime import datetime
import dlib, numpy
from skimage import io


predictor_path = "shape_predictor_68_face_landmarks.dat"  # 人臉68特徵點模型
face_rec_model_path = "dlib_face_recognition_resnet_model_v1.dat"  # 人臉辨識模型
detector = dlib.get_frontal_face_detector()  # 偵測臉部正面
sp = dlib.shape_predictor(predictor_path)  # 讀入人臉特徵點模型
facerec = dlib.face_recognition_model_v1(face_rec_model_path)  # 讀入人臉辨識模型

#連接資料庫，將會員資料讀出並
conn = pymysql.connect(host='127.0.0.1',
                       port=3306,
                       user='user1',
                       passwd='12345',
                       db='member_db')  # 連接資料庫
cursor = conn.cursor()
sqlstr = 'SELECT * FROM member_info'  # 讀取會員資料表
cursor.execute(sqlstr)
rows = cursor.fetchall()  # 取得會員資料
member = []
for row in rows:  # 儲存所有會員帳號
    member.append(row[0])

v2 = {}  # 會員帳號、檔名字典
for row in rows:
    v2[row[0]] = row[2]

#視窗設計
win = tk.Tk()                    # 如果使用直譯器的話，在這行run後就會先看到一個視窗了！
win.title('trAInsformers')    # 更改視窗的標題
win.geometry('1024x768+200+50')          # 修改視窗大小(寬x高)
# #win.resizable(0, 0)      # 如果不想讓使用者能調整視窗大小的話就均設為False
win.iconbitmap('icorn.ico')    # 更改左上角的icon圖示
win.config(background="#323232")         #更改背景色

title = tk.Label(text="Welcome to trAInsformer", bg="#323232", fg="skyblue")

Font_title = ("Comic Sans MS", 30, "bold")  #字體
title.config(font=Font_title)
title.place(x=260, y=50)

def getFeature(imgfile):
    img = dlib.load_rgb_image(imgfile)  # 讀取圖片
    dets = detector(img, 1)
    for det in dets:
        shape = sp(img, det)  # 特徵點偵測
        feature = facerec.compute_face_descriptor(img, shape)  # 取得128維特徵向量
        feature_array = numpy.array(feature)
        return feature  # 轉換numpy array格式



def createNewWindow():

    def signup_id():
        en_message = en.get()
        while True:
            memberid = en_message
            if memberid == '':  # 未輸入帳號就結束
                break
            elif memberid in member:  # 帳號已存在
                welcome_lable.config(text="此帳號已存在，不可重複！ ")
                print("此帳號已存在，不可重複！")
                break
            else:  # 建立帳號
                picfile = memberid + '.jpg'  # 會員圖片檔名稱
                member.append(memberid)
                cv2.namedWindow("frame")
                cap = cv2.VideoCapture(0)  # 開啟cam
                while (cap.isOpened()):  # 如果cam已開啟
                    ret, img = cap.read()  # 讀取影像
                    if ret == True:
                        cv2.imshow("frame", img)  # 顯示影像
                        k = cv2.waitKey(100)  # 0.1秒檢查一次按鍵
                        if k == ord("z") or k == ord("Z"):  # 按下「Z」鍵
                            cv2.imwrite('memberPic/' + picfile, img)  # 儲存影像
                            break
                cap.release()  # 關閉cam
                cv2.destroyWindow("frame")

                imgFeature = getFeature('memberPic/' + picfile)
                sqlstr = 'INSERT INTO member_info values("{}","{}","{}")'.format(memberid,
                                                                                 picfile,
                                                                                 imgFeature)  # 將帳號及影像檔名稱寫入資料表
                cursor.execute(sqlstr)
                conn.commit()

                welcome_lable.config(text="Hi! " + en_message + " 帳號建立成功!")
            break

    newWin = tk.Toplevel(win)
    newWin.title('快來註冊吧')  # 更改視窗的標題
    newWin.geometry('1024x768+200+50')  # 修改視窗大小(寬x高)
    newWin.resizable(0, 0)  # 如果不想讓使用者能調整視窗大小的話就均設為False
    newWin.iconbitmap('icorn.ico')  # 更改左上角的icon圖示
    newWin.config(background="#323232")  # 更改背景色

    title = tk.Label(newWin, text="輸入英文名字當作會員ID ：", bg="#323232", fg="skyblue")
    Font_title = ("Comic Sans MS", 20, "bold")  # 字體
    title.config(font=Font_title)
    title.place(anchor=tk.CENTER, x=512, y=200)

    Font_welcome_lable = ("Comic Sans MS", 30, "bold")
    welcome_lable = tk.Label(newWin, bg="#323232", fg="white", text=" ", font=Font_welcome_lable)
    welcome_lable.place(anchor=tk.CENTER, x=512, y=450)

    en = tk.Entry(newWin, width=25, font=("Calibri 20"))
    en.place(anchor=tk.CENTER, x=510, y=250, height=35)

    btn_OK = tk.Button(newWin, text="註冊", background="#323232", fg="white", command=signup_id)
    btn_OK.place(anchor=tk.CENTER, x=400, y=350, width=100, height=50)

    btn_cancel = tk.Button(newWin, text="取消", background="#323232", fg="white", command=newWin.destroy)
    btn_cancel.place(anchor=tk.CENTER, x=625, y=350, width=100, height=50)

def login_member():
    def compareimage(v, filepath):  # 人臉比對
        v3 = v2[img]
        v4 = v3.split('\n')

        v5 = []
        for i in v4:
            v6 = float(i)
            v5.append(v6)
            # print(v5)
        v7 = numpy.array(v5)
        dist = numpy.linalg.norm(v - v7)  # 計算歐式距離,越小越像
        if dist < 0.3:
            return True
        else:
            return False
    timenow = time.time()  # 取得現在時間數值
    cv2.namedWindow("frame")
    cap = cv2.VideoCapture(0)  # 開啟cam
    while (cap.isOpened()):  # cam開啟成功
        count = 7 - int(time.time() - timenow)  # 倒數計時5秒
        ret, img = cap.read()
        if ret == True:
            imgcopy = img.copy()  # 複製影像
            cv2.putText(imgcopy, str(count), (10, 75), cv2.FONT_HERSHEY_DUPLEX, 3, (201, 230, 252), 10)  # 在複製影像上畫倒數秒數
            cv2.imshow("frame", imgcopy)  # 顯示複製影像
            k = cv2.waitKey(100)  # 0.1秒讀鍵盤一次
            if k == ord("z") or k == ord("Z") or count == 0:  # 按「Z」鍵或倒數計時結束
                cv2.imwrite("media/tem.jpg", img)  # 將影像存檔
                break
    cap.release()  # 關閉cam
    cv2.destroyWindow("frame")

    success = False  # 記錄登入是否成功
    v = getFeature("media/tem.jpg")

    for img in v2:  # 逐一比對會員圖片
        if compareimage(v, v2[img]):  # 判斷為同一人
            print('登入成功！歡迎 ' + img + '！')
            success = True
            savetime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # 目前時刻字串
            sqlstr = 'INSERT INTO login values("{}","{}")'.format(img, savetime)  # 將帳號及現在時刻寫入資料表
            cursor.execute(sqlstr)
            conn.commit()
            break
    if not success:  # 登入失敗
        print('登入失敗！你不是會員！')

    newWin1 = tk.Toplevel(win)
    newWin1.title('快來運動吧')  # 更改視窗的標題
    newWin1.geometry('1024x768+200+50')  # 修改視窗大小(寬x高)
    newWin1.resizable(0, 0)  # 如果不想讓使用者能調整視窗大小的話就均設為False
    newWin1.iconbitmap('icorn.ico')  # 更改左上角的icon圖示
    newWin1.config(background="#323232")  # 更改背景色

    Font_welcome_lable = ("Comic Sans MS", 30, "bold")
    welcome_lable = tk.Label(newWin1, bg="#323232", fg="white", text='登入成功！歡迎 ' + img + '！' , font=Font_welcome_lable)
    welcome_lable.place(anchor=tk.CENTER, x=512, y=450)









#註冊
signup_btn = tk.Button(win, text = "註冊會員", background="#323232", fg="white", command=createNewWindow)
Font_signup = ("微軟正黑體", 15)  #字體
signup_btn.config(font=Font_signup)
signup_btn.place(x=420, y=300, width=100, height=50)

#登入
login_btn = tk.Button(text = "登入系統", background="#323232", fg="white", command=login_member)
Font_login = ("微軟正黑體", 15)  #字體
login_btn.config(font=Font_login)
login_btn.place(x=540, y=300, width=100, height=50)


def conn_close():
    conn.close()
    win.destroy()

#退出系統
end_btn = tk.Button(text = "退出系統", background="#323232", fg="white", command=conn_close)
end_btn.place(x=900, y=700)


win.mainloop()                    # 在一般python xxx.py的執行方式中，呼叫mainloop()才算正式啟動