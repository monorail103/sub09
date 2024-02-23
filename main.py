import sys
import PySide6.QtWidgets as Qw
import PySide6.QtGui as Qg
from PySide6.QtCore import Slot, QSize, QTimer
from PySide6.QtGui import QImage
import camera as cm
import hands
import cv2
import numpy as np

# MainWindowクラス定義 ####
class MainWindow(Qw.QMainWindow):

    video_size = QSize(320, 240)
  
    def __init__(self):
        super().__init__() 
        self.setWindowTitle('MainWindow') 
        self.setGeometry(100, 50, 700, 400)

        self.count = 0
        self.flag = True

        # 動画キャプチャ用のスレッドを作成
        self.thread = cm.VideoThread()
        # シグナルとスロットを接続
        self.thread.change_pixmap_signal.connect(self.update_image)
        # スレッドを開始
        self.thread.start()

        # タイマー
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.handchange)
        self.timer.start(1000)

        # Webカメラ表示
        self.lb_img1 = Qw.QLabel(self)
        
        # じゃんけんの手を表示
        self.lb_img2 = Qw.QLabel(self)

        # Webカメラ表示枠の設定
        self.lb_img1.setGeometry(10,35,320,240)

        # じゃんけんの手表示
        img2 = cv2.imread("files/janken_pa.jpg")
        height, width, ch = img2.shape
        bpl = ch * width
        qimg2 =Qg.QImage(img2.data, width, height, 
                            bpl, Qg.QImage.Format.Format_BGR888)
        self.lb_img2.setPixmap(Qg.QPixmap.fromImage(qimg2))
        self.lb_img2.setGeometry(350,35,width,height)

        # 結果表示のためのラベル
        self.lb_msg = Qw.QLabel('起動までしばらくお待ち下さい',self)
        self.lb_msg.setGeometry(170,10,500,30)


    def handchange(self):
        if self.flag:
            self.count += 1
        # print(f'現在のカウント：{self.count}')
        if self.count == 2:
            self.lb_msg.setText('最初はグー、じゃんけん…')
        elif self.count == 5:
            self.lb_msg.setText('ポン！')
            self.count = 0

    # 画像更新用のスロット
    @Slot(np.ndarray)
    def update_image(self, frame):
        h, w, ch = frame.shape
        bytesPerLine = ch * w
        image = QImage(frame, w, h, bytesPerLine, QImage.Format.Format_BGR888)
        # 画像設定
        self.lb_img1.setPixmap(Qg.QPixmap.fromImage(image))
        if self.count % 5 == 0:
            num = hands.imageprocess(frame)
            # パソコンが出す手
            # print(num)
            if num == None:
                self.lb_msg.setText("認識できません")
            else:
                path = ""
                if num==1:
                    path = "files/janken_pa.jpg"
                elif num==2:
                    path = "files/janken_gu.jpg"
                else:
                    path = "files/janken_choki.jpg"

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