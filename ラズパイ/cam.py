# 必要モジュールのインポート
from pickle import FALSE
import cv2  # OpenCV: カメラからの画像を読み取る
import requests  # requests: CustomVisionに最新スクリーンショットを送信し、その結果を受け取る
from time import time  # カメラからのスクリーンショット取得間隔を指定
import json
from io import BytesIO
import base64

import lcd

###############################################
# OpenCVの設定
###############################################
cam = cv2.VideoCapture(0)
# Windowサイズの指定（横）
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# Windowサイズの指定（縦）
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# カメラ映像からのスクリーンショットを切り出すタイミングを指定(秒)
limit_time = 2
# 前回読み込んだ時間の初期化
previous_time = 0


tag = "None"
prob = "None"

###############################################
# ユーザー入力欄
###############################################
# Azure Custom Visionポータル -> Performance -> Prediction URL より取得可能
# ※ENDPOINTとKEYは外部に公開しないでください※
# DET_ENDPOINT = "https://congnitive-services-test.cognitiveservices.azure.com/customvision/v3.0/Prediction/dfb4f449-224f-4549-915b-f02b2a40010e/classify/iterations/food2/image"
# DET_KEY = "94b862a6012e4563843eae033d1514bf"

DET_ENDPOINT = "https://foodteamc-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/e78564bd-6599-4090-9050-9ec3a2c42a7c/detect/iterations/Iteration2/image"
DET_KEY = "c9fedd66297749f996942e5dea71aa2d"

# CAMERA_NUM = 1   # 0:内蔵カメラ 1:USBカメラ

###############################################
# プログラム本体
###############################################
# Azure上にあるAIモデルにAPI経由でリクエストを送信する


def detection():
    global tag
    global prob
    
    url = DET_ENDPOINT
    headers = {'content-type': 'application/octet-stream',
               'Prediction-Key': DET_KEY}
    # tmpフォルダ保存された画像を送信
    response = requests.post(url, data=open(
        "./tmp/screen.jpg", "rb"), headers=headers)
    response.raise_for_status()
    # JSON形式で結果を受け取る
    analysis = response.json()

    # print(analysis)

    # 検出した不良の数だけJSON形式で返ってくる
    # 多分ここをfor文で,得られた全ての結果を変数に格納する必要がある
    # 全ての結果を変数として格納するのではなく,左いくつ,右いくつなど,まとまった値として格納する方法を考える
    # if len(analysis["predictions"]) != 0:
    #     tag = analysis["predictions"][0]["tagName"]
    #     prob = analysis["predictions"][0]["probability"]
    #     # box = analysis["predictions"][0]["boundingBox"]
    #     return tag, prob
    # else:
    #     return "-", "-"

    analysis_len = len(analysis["predictions"])
    print()
    print(f"Analysis len: {analysis_len}")

    print()
    Empty_count = 0
    Left_count = 0
    Right_count = 0
    Smile_left = 0
    Smile_right = 0

    img = cv2.imread("./tmp/screen.jpg")
    # 入力画像のサイズ（高さ、幅）を取得
    height, width = img.shape[:2]

    for num in range(len(analysis["predictions"])):
        # 空の皿の検出：　推論結果 tagNameがEmpty_Foodであり,精度が80%以上の場合を取り出す
        if analysis["predictions"][num]["tagName"] == "Empty_Food" and float(analysis["predictions"][num]["probability"]) >= 0.8:
            Empty_count += 1
            # 推論の結果が画像の中心(740px)より左であればleft_count += 1
            if int(analysis["predictions"][num]["boundingBox"]["left"]*width) < int(width/2):
                Left_count += 1
                print(int(analysis["predictions"][num]["boundingBox"]["left"]*width))
            else :
                Right_count += 1
        # 笑顔の検出: 笑顔だったらSmile_count += 1
        if analysis["predictions"][num]["tagName"] == "smile" and float(analysis["predictions"][num]["probability"]) >= 0.8 :
            if int(analysis["predictions"][num]["boundingBox"]["left"]*width) < int(width/2):
                Smile_left += 1
            else:
                Smile_right += 1
            

    print(f"Empty_count: {Empty_count}")
    print(f"Left_count: {Left_count}")
    print(f"Right_count: {Right_count}")
    print(f"Smile_left: {Smile_left}")
    print(f"Smile_right: {Smile_right}")

    try:
        return Left_count, Right_count, Smile_left, Smile_right, analysis, analysis_len
    except :
        return "-", "-", "-", "-", "-", "-"


###############################################
# メイン処理
###############################################
# while True:
# for num in range(5):
    # print(num)
    # print()
def capture():
    global tag
    global prob
    cam = cv2.VideoCapture(0)
    # Windowサイズの指定（横）
    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1500)
    # Windowサイズの指定（縦）
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 350)
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1100)

    # Windowサイズの指定（横）
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    # Windowサイズの指定（縦）
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # カメラ映像からのスクリーンショットを切り出すタイミングを指定(秒)
    limit_time = 2
    # 前回読み込んだ時間の初期化
    previous_time = 0

    print("capute on")
    # try:

    ############################################################################
    # カメラ映像からスクリーンショットの取得
    _, img = cam.read()
    
    # スクリーンショットの取得
    cv2.imwrite('./tmp/screen.jpg', img)
    print("imrite")
    #############################################################################

    # img_bytes = open("./tmp/screen.jpg", "rb")
    # with open('./tmp/screen.jpg','rb') as f: img_bytes = f.read()

    # # img は cv2.imread などで得られる画像を読み込んだnumpy.ndarray
    # _, buffer = cv2.imencode('.jpg', img)
    # # base64のバイナリ文字列をdecodeで文字列に変換
    # img_as_text = base64.b64encode(buffer).decode('utf-8')
    
    # CustomVisionに送信、タグ名と自信度をname, predに表示
    # tag, prob = detection()


    #############################################################################
    # img = cv2.imread('./tmp/no_smile-4.jpg')
    ##############################################################################


    # 入力画像のサイズ（高さ、幅）を取得
    height, width = img.shape[:2]

    Left_count, Right_count, Smile_left, Smile_right, analysis, analysis_len = detection()
    print("detectation")

    # LCDに推論した結果を表示させる
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
        
    lcd.writeLCD_2(table_number)

    print()
    # print(f"tag: {tag}, prob: {prob}")

    # # 入力画像のサイズ（高さ、幅）を取得
    # height, width = img.shape[:2]

    # 前回取得時間を更新
    # previous_time = time()

    # # カメラ映像に表示する文字のフォントの設定
    font = cv2.FONT_HERSHEY_SIMPLEX

    # テキストの色の設定
    text_color = (0, 0, 255)  # 赤

    # print("error_check_point-1")

    # # バウンディングボックスの描画
    for num in range(analysis_len):
        # print("error_check_point-1-1")
        box = analysis["predictions"][num]["boundingBox"]
        # print("error_check_point-1-2")
        if analysis["predictions"][num]["tagName"] == "Empty_Food" or analysis["predictions"][num]["tagName"] == "smile" :
            # print("error_check_point-1-3") 
            if float(analysis["predictions"][num]["probability"]) >= 0.8:
                # print("error_check_point-1-4")
                # バウンディングボックスの描画
                img = cv2.rectangle(img, (int(box["left"]*width), int(box["top"]*height)), (int(
                    box["left"]*width+box["width"]*width), int(box["top"]*height+box["height"]*height)), text_color, 5)
                # print("error_check_point-1-5")

            # # タグ名の画面上の表示位置やサイズの設定
            # cv2.putText(img, str(tag), (10, 100), font,
            #             2, text_color, 3, cv2.LINE_AA)
            # # 自信度の画面上の表示位置やサイズの設定
            # cv2.putText(img, str(round(prob, 3)), (10, 180), font,
            #             2, text_color, 3, cv2.LINE_AA)
            # 設定の反映と表示

            ## ここでなぜかエラーを吐いたので,コメントアウトしました
            # cv2.imshow("detect", img)
            # print("error_check_point-2")

    # 画像の保存
    cv2.imwrite('./new_smile-1.jpg', img)
    # print("error_check_point-3")


    # img は cv2.imread などで得られる画像を読み込んだnumpy.ndarray
    _, buffer = cv2.imencode('.jpg', img)
    # base64のバイナリ文字列をdecodeで文字列に変換
    img_as_text = base64.b64encode(buffer).decode('utf-8')

    return Left_count, Right_count, Smile_left, Smile_right, img_as_text
# capture()

# 終了キー押下後、後処理
cam.release()
cv2.destroyAllWindows()

