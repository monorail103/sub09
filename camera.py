import mediapipe as mp
import cv2
import pickle
import numpy as np
import PySide6.QtGui as Qg
from PySide6.QtCore import Signal, QThread
from PySide6.QtGui import QImage

# 映像表示クラス定義 ####
class VideoThread(QThread):

    change_pixmap_signal = Signal(np.ndarray)
    playing = True
    
    def run(self):
        cap = cv2.VideoCapture(0)
        while self.playing:
            ret, frame = cap.read()
            if ret:
                # シグナルで画像を送信
                self.change_pixmap_signal.emit(frame)
                # カメラから画像取得

                
        cap.release()

    def stop(self):
        self.playing = False
        self.wait()

    