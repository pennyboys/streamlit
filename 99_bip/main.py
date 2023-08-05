import streamlit as st
import cv2
import numpy as np

def detect_toothbrush(image):
    # YOLOv4-tinyのモデルとクラス名リストをロード
    net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    # 歯ブラシのクラスIDは80（coco.namesの中で何番目か）
    toothbrush_class_id = 80

    # 画像を正規化（0から1の範囲にスケーリング）
    img = image.astype(np.float32) / 255.0

    # YOLOv4-tinyによる物体検出
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(net.getUnconnectedOutLayersNames())

    # 物体の境界ボックスを検出
    boxes = []
    confidences = []
    class_ids = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == toothbrush_class_id:
                return "歯磨き開始"

    return ""

def main():
    st.title("歯ブラシ識別アプリ")
    
    # カメラ起動ボタンを表示
    if st.button("カメラを起動"):
        # カメラを起動して画像を取得
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        # 画像を表示
        st.image(frame, channels="BGR")

        # 歯ブラシの識別を実行
        #result = detect_toothbrush(frame)
        #st.write(result)

if __name__ == "__main__":
    main()
