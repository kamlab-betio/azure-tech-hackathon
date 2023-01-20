from flask import Flask
from flask import render_template
# from flask import request
import requests
# import sys
import cv2
import numpy as np
import base64
# from PIL import Image
# from io import BytesIO

app = Flask(__name__, static_folder='./images')

tag = "None"
prob = "None"

@app.route('/',methods=["POST","GET"])
def index():
    # tag = request.form["tag"]
    # prob = request.form["prob"]
    # if request.method == 'POST':
    #     print("post")
    #     if request.form['detection'] :
    #         print("request.form['detection']")
    try:
        response = requests.get('任意の値')
    # sys.stdout.write(response)
    # Left_count, Right_count, Smile_left, Smile_right, img_as_text
        print(response)
        analysis = response.json()
        Left_count = analysis["Left_count"]
        Right_count = analysis["Right_count"]
        Smile_left = analysis["Smile_left"]
        Smile_right = analysis["Smile_right"]
        
        if int(Left_count) >= 2 and int(Smile_left) == 0 and int(Right_count) >= 2 and int(Smile_right) == 1:
            table_number = 1
        elif int(Left_count) >= 2 and int(Smile_left) == 1 and int(Right_count) >= 2 and int(Smile_right) == 0:
            table_number = 2
        elif int(Left_count) >= 2 and int(Smile_left) == 1 and int(Right_count) >= 2 and int(Smile_right) == 1:
            table_number = 12
        elif int(Left_count) >= 2 and int(Smile_left) == 0 and int(Right_count) >= 2 and int(Smile_right) == 0:
            table_number = 12
        else :
            table_number = 0


        # tag = analysis["tag"]
        # prob = analysis["prob"]
        # 検出された空の皿の枚数を取得
        # prob = analysis["plates"]
        img_as_text = analysis["img_as_text"]
        # バイナリ文字列に変換
        img_binary = base64.b64decode(img_as_text.encode('utf-8'))
        # 配列に変換
        img_array = np.frombuffer(img_binary, dtype=np.uint8)
        img_from_text = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        # 画像の復元
        cv2.imwrite('./images/screen.jpg', img_from_text)
        filepath = './images/screen.jpg'

    except Exception as e:
        print(e)

    # img_binary = base64.b64decode(img_as_text.encode('utf-8'))
    # # 配列に変換
    # img_array = np.frombuffer(img_binary, dtype=np.uint8)
    # img_from_text = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    # cv2.imwrite('./screen.jpg', img_from_text)
    
    return render_template("index.html",
    table_number=table_number, 
    left_plates=Left_count, 
    right_plates=Right_count,
    smile_left=Smile_left,
    smile_right=Smile_right,
    filepath=filepath
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8015)
