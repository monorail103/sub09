import mediapipe as mp
import cv2
import pickle
import numpy as np

def imageprocess(img):
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
                try:
                    y_pred=clf.predict(X_test)
                    pred = y_pred[0]
                    return pred
                except Exception as e:
                    return 5