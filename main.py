import sys
import PySide6.QtWidgets as Qw
import PySide6.QtTest as Qt
import PySide6.QtGui as Qg
import pickle
import mediapipe as mp
import cv2
import numpy as np

# 画像から手の形解析camera関数
def camera(img):
    # 学習済みモデルを開封
    with open('model.pickle', mode='rb') as f:
        clf = pickle.load(f)

    # mediapipeによる手の関節測定
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=1,                # 最大検出数
        min_detection_confidence=0.7,   # 検出信頼度
        min_tracking_confidence=0.7     # 追跡信頼度
    )

    # データ取得用
    ids = [0,4,8,12,16,20]
    pos = []
    base = []

    # カメラから画像取得

    img = cv2.flip(img, 1)          # 画像を左右反転
    img_h, img_w, _ = img.shape     # サイズ取得
    pos = []
    results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
                for i,lm in enumerate(hand_landmarks.landmark):
                    if i in ids:
                        if i==0:
                            base = np.array([int(lm.x * img_w), int(lm.y * img_h)])
                        else:
                            p = np.array([int(lm.x * img_w),int(lm.y * img_h)])
                            pos.append(np.linalg.norm(p-base))
                            # cv2.circle(img, lm_pos, 3, (255, 0, 0), -1)
                        # cv2.putText(img, f'{posx},{posy}', lm_pos, cv2.FONT_HERSHEY_DUPLEX, 1.0, (255,255,255))
                # 判定
                X_test = [pos]
                a = None
                try:
                    y_pred=clf.predict(X_test)
                    return y_pred[0]
                except UnboundLocalError:
                    return 0

    

# MainWindowクラス定義 ####
class MainWindow(Qw.QMainWindow):
  
    def __init__(self):
        super().__init__() 
        self.setWindowTitle('MainWindow') 
        self.setGeometry(100, 50, 700, 400) 

        # QLabelに画像 qimg_1 を設定する
        self.lb_img1 = Qw.QLabel(self)
        
        # じゃんけんの手を表示
        self.lb_img2 = Qw.QLabel(self)

        img = cv2.imread("files/default.jpg")
        height, width, ch = img.shape

        # リサイズを行う
        img = cv2.resize(img,(320,240),interpolation=cv2.INTER_LANCZOS4)
        height, width, ch = img.shape
        bpl = ch * width
        qimg =Qg.QImage(img.data, width, height, 
                        bpl, Qg.QImage.Format.Format_BGR888)

        self.lb_img1.setPixmap(Qg.QPixmap.fromImage(qimg))
        self.lb_img1.setGeometry(15,35,width,height)

        # じゃんけんの手表示
        img2 = cv2.imread("files/janken_pa.jpg")
        height, width, ch = img2.shape
        bpl = ch * width
        qimg2 =Qg.QImage(img2.data, width, height, 
                        bpl, Qg.QImage.Format.Format_BGR888)

        self.lb_img2.setPixmap(Qg.QPixmap.fromImage(qimg2))
        self.lb_img2.setGeometry(350,35,width,height)

        #じゃんけんボタン
        self.btn_run = Qw.QPushButton('じゃんけん',self)
        self.btn_run.setGeometry(10,10,100,20)
        self.btn_run.clicked.connect(self.btn_run_clicked)

        # 結果表示のためのラベル
        self.lb_msg = Qw.QLabel('ボタンを押下してください。',self)
        self.lb_msg.setGeometry(120,10,500,30)

    #「実行」ボタンの押下処理
    def btn_run_clicked(self):   
        for i in range(2):
            self.lb_msg.setText(f"{2-i}秒後に撮影します。最初はグー、じゃんけん")
            Qt.QTest.qWait(1000)
        else:
            self.lb_msg.setText("ただいま撮影を行っています。少々お待ちください")
        cap = cv2.VideoCapture(0)
        _, img = cap.read()
        self.lb_msg.setText("ポン！")
        # 画像
        #num→1：グー、2：チョキ、3：パー
        num = camera(img)
        # パソコンが出す手
        if num == 0:
            self.lb_msg.setText("認識できませんでした。もう一度お試し下さい。")
        else:
            path = ""
            if num==1:
                path = "files/janken_pa.jpg"
            elif num==2:
                path = "files/janken_gu.jpg"
            else:
                path = "files/janken_choki.jpg"
            # 出した手の画像を貼り付け
            img = cv2.resize(img,(320,240),interpolation=cv2.INTER_LANCZOS4)
            height, width, ch = img.shape
            bpl = ch * width
            qimg =Qg.QImage(img.data, width, height, 
                            bpl, Qg.QImage.Format.Format_BGR888)

            self.lb_img1.setPixmap(Qg.QPixmap.fromImage(qimg))
            self.lb_img1.setGeometry(15,35,width,height)

            # じゃんけんの手イラスト表示
            img2 = cv2.imread(path)
            height, width, ch = img2.shape
            bpl = ch * width
            qimg2 =Qg.QImage(img2.data, width, height, 
                            bpl, Qg.QImage.Format.Format_BGR888)

            self.lb_img2.setPixmap(Qg.QPixmap.fromImage(qimg2))
            self.lb_img2.setGeometry(350,35,width,height)



# 本体
if __name__ == '__main__':
  app = Qw.QApplication(sys.argv)
  main_window = MainWindow()
  main_window.show()
  sys.exit(app.exec())