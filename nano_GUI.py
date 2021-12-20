import tkinter as tk
from tkinter import ttk
import cv2
import csv
import time
import dlib, numpy
import nano_publisher as nap

global line_user_ID
global en_weightint
global count
global score
global date
predictor_path = "shape_predictor_68_face_landmarks.dat"  # 人臉68特徵點模型
face_rec_model_path = "dlib_face_recognition_resnet_model_v1.dat"  # 人臉辨識模型
detector = dlib.get_frontal_face_detector()  # 偵測臉部正面
sp = dlib.shape_predictor(predictor_path)  # 讀入人臉特徵點模型
facerec = dlib.face_recognition_model_v1(face_rec_model_path)  # 讀入人臉辨識模型



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
        return feature_array  # 轉換numpy array格式

def login_member():
    with open('member_info.csv', newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        v2 = {}
        for row in rows:
            v2[row['name']] = row['feature']

    def compareimage(v, filepath):  # 人臉比對
        v3 = v2[img]
        v4 = v3.split(' ')

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
    cap = cv2.VideoCapture(1)  # 開啟cam
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
            #new window
            newWin1 = tk.Toplevel(win)
            newWin1.title('快來運動吧')  # 更改視窗的標題
            newWin1.geometry('1024x768+200+50')  # 修改視窗大小(寬x高)
            newWin1.resizable(0, 0)  # 如果不想讓使用者能調整視窗大小的話就均設為False
            newWin1.iconbitmap('icorn.ico')  # 更改左上角的icon圖示
            newWin1.config(background="#323232")  # 更改背景色

            Font_welcome_lable = ("Comic Sans MS", 20, "bold")
            weight_lable = tk.Label(newWin1, bg="#323232", fg="white", text='Hello ' + img + '! 來輸入訓練重量吧',
                                     font=Font_welcome_lable)
            weight_lable.place(anchor=tk.CENTER, x=500, y=100)
            # entry box
            weight = tk.IntVar()
            en_weight = ttk.Entry(newWin1, state='readonly', textvariable=weight, width=50)
            en_weight.grid(rowspan=1)
            en_weight.place(anchor=tk.CENTER, x=512, y=150, height=50)
            weight_lable = tk.Label(newWin1, fg="#323232", text='KG', font=Font_welcome_lable)
            weight_lable.place(anchor=tk.CENTER, x=600, y=150)



            global exp

            exp = " "
            is_shift = False

            def press(num):
                global exp
                exp = exp + str(num)
                weight.set(exp)

            def Backspace():
                global exp
                exp = exp[:-1]
                weight.set(exp)

            def Clear():
                global exp
                exp = " "
                weight.set(exp)

            def Enter():
                en_weightint = en_weight.get()
                Font_welcome_lable = ("Comic Sans MS", 20, "bold")
                weight_lable = tk.Label(newWin1, bg="#323232", fg="white", text=en_weightint,
                                        font=Font_welcome_lable)
                weight_lable.place(anchor=tk.CENTER, x=500, y=700)





            def display():
                backspace = ttk.Button(newWin1, text='<---', width=6, command=Backspace)
                backspace.grid(rowspan=1, column=13, ipadx=20, ipady=10)
                backspace.place(anchor=tk.CENTER, x=665, y=150, height=50)

                enter = ttk.Button(newWin1, text='Enter', width=6, command=Enter)
                enter.grid(row=3, column=12, columnspan=2, ipadx=55, ipady=10)
                enter.place(anchor=tk.CENTER, x=750, y=150, height=50, width=125)

                clear = ttk.Button(newWin1, text='Clear', width=6, command=Clear)
                clear.grid(row=4, column=12, columnspan=2, ipadx=55, ipady=10)
                clear.place(anchor=tk.CENTER, x=560, y=550, height=50, width=125)



                num1 = ttk.Button(newWin1, text='1', width=6, command=lambda: press('1'))
                num1.grid(row=1, column=1, ipadx=6, ipady=10)
                num1.place(anchor=tk.CENTER, x=455, y=250, height=50)

                num2 = ttk.Button(newWin1, text='2', width=6, command=lambda: press('2'))
                num2.grid(row=1, column=2, ipadx=6, ipady=10)
                num2.place(anchor=tk.CENTER, x=525, y=250, height=50)

                num3 = ttk.Button(newWin1, text='3', width=6, command=lambda: press('3'))
                num3.grid(row=1, column=3, ipadx=6, ipady=10)
                num3.place(anchor=tk.CENTER, x=595, y=250, height=50)

                num4 = ttk.Button(newWin1, text='4', width=6, command=lambda: press('4'))
                num4.grid(row=1, column=4, ipadx=6, ipady=10)
                num4.place(anchor=tk.CENTER, x=455, y=350, height=50)

                num5 = ttk.Button(newWin1, text='5', width=6, command=lambda: press('5'))
                num5.grid(row=1, column=5, ipadx=6, ipady=10)
                num5.place(anchor=tk.CENTER, x=525, y=350, height=50)

                num6 = ttk.Button(newWin1, text='6', width=6, command=lambda: press('6'))
                num6.grid(row=1, column=6, ipadx=6, ipady=10)
                num6.place(anchor=tk.CENTER, x=595, y=350, height=50)

                num7 = ttk.Button(newWin1, text='7', width=6, command=lambda: press('7'))
                num7.grid(row=1, column=7, ipadx=6, ipady=10)
                num7.place(anchor=tk.CENTER, x=455, y=450, height=50)

                num8 = ttk.Button(newWin1, text='8', width=6, command=lambda: press('8'))
                num8.grid(row=1, column=8, ipadx=6, ipady=10)
                num8.place(anchor=tk.CENTER, x=525, y=450, height=50)

                num9 = ttk.Button(newWin1, text='9', width=6, command=lambda: press('9'))
                num9.grid(row=1, column=9, ipadx=6, ipady=10)
                num9.place(anchor=tk.CENTER, x=595, y=450, height=50)

                num0 = ttk.Button(newWin1, text='0', width=6, command=lambda: press('0'))
                num0.grid(row=1, column=10, ipadx=6, ipady=10)
                num0.place(anchor=tk.CENTER, x=455, y=550, height=50)

                Q = ttk.Button(newWin1, text='q', width=6, command=newWin1.destroy)
                Q.grid(row=2, column=2, ipadx=6, ipady=10)


            display()


            # 退出系統
            end_btn = tk.Button(newWin1, text="退出視窗", background="#323232", fg="white", command=newWin1.destroy)
            end_btn.place(x=900, y=700)
            Font_welcome_lable = ("Comic Sans MS", 30, "bold")
            welcome_lable = tk.Label(newWin1, bg="#323232", fg="white", text='登入成功！歡迎 ' + img + '！',
                                     font=Font_welcome_lable)
            welcome_lable.place(anchor=tk.CENTER, x=512, y=450)

            with open('member_info.csv', newline='') as csvfile:
                rows = csv.DictReader(csvfile)
                v2 = {}
                for row in rows:
                    v2[row['name']] = row['line_user_ID']
                if v2.get(img):
                    line_user_ID = v2[img]
                print(line_user_ID)

            print('登入成功！歡迎 ' + img + '！')
            success = True


            count = '9'
            score = '98'
            name = img
            mqtt = line_user_ID + ',' + name + ',' + count + ',' + score + en_weight
            print(mqtt)
            nap.publisher(mqtt)
            break

    if not success:  # 登入失敗
        print('登入失敗！你不是會員！')
        Font_welcome_lable = ("Comic Sans MS", 30, "bold")
        welcome_lable = tk.Label(win, bg="#323232", fg="white", text='登入失敗！你不是會員！',
                                 font=Font_welcome_lable)
        welcome_lable.place(anchor=tk.CENTER, x=512, y=650)









#登入
login_btn = tk.Button(text = "登入會員", background="#323232", fg="white", command=login_member)
Font_login = ("微軟正黑體", 15)  #字體
login_btn.config(font=Font_login)
login_btn.place(anchor=tk.CENTER, x=512, y=384, width=100, height=50)

#退出系統
end_btn = tk.Button(text = "退出系統", background="#323232", fg="white", command=win.destroy)
end_btn.place(x=900, y=700)


win.mainloop()