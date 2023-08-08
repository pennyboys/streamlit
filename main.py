import streamlit as st
import streamlit_toggle as tog
from google.cloud import vision
from google.oauth2 import service_account


def detect_toothbrush(image):

    service_account_key = {
        "type": "service_account",
        "project_id": st.secrets["GcpApiKey"]["project_id"],
        "private_key_id": st.secrets["GcpApiKey"]["private_key_id"],
        "private_key": st.secrets["GcpApiKey"]["private_key"],
        "client_email": st.secrets["GcpApiKey"]["client_email"],
        "client_id": st.secrets["GcpApiKey"]["client_id"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/my-project%40crypto-visitor-395006.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }
    credentials = service_account.Credentials.from_service_account_info(service_account_key)
    scoped_credentials = credentials.with_scopes(
        [
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/analytics.readonly'
        ])

    # Vision APIが扱える画像データにする
    print(type(image))
    image_va = vision.Image(content=image)
    print(type(image_va))
    # ImageAnnotatorClientのインスタンスを作成
    annotator_client = vision.ImageAnnotatorClient()

    objects = annotator_client.object_localization(image=image_va).localized_object_annotations

    print('--------------RESULT--------------')
    print(f"Number of objects found: {len(objects)}")
    for object_ in objects:
        print(f"{object_.name} (confidence: {object_.score})")
        if object_.name == 'Toothbrush' and object_.score > 0.5:
            print("対象写真")
            return "1", object_.score

    print("対象外写真")
    return "", 0


def main():
    st.title("大人の歯磨きアプリ")
    if tog.st_toggle_switch(
            label="カメラ起動",
            key="Key1",
            default_value=False,
            label_after=False,
            inactive_color='#D3D3D3',
            active_color="#11567f",
            track_color="#29B5E8"
            ):

        picture = st.camera_input("歯ブラシを撮って！")

        if picture:
            bytes_data = picture.getvalue()
            if detect_toothbrush(bytes_data)[0] == "1":
                per = str(round(detect_toothbrush(bytes_data)[1]*100, 2))
                st.subheader(':blue[' + per + ']' + 'パーセントの確率で歯ブラシが写ってます！')
                st.subheader('歯磨きを始めましょう！！')
            else:
                st.caption('歯ブラシ写ってないです')
        else:
            st.caption('')

            # 画像を表示
            st.image(picture)
    else:
        st.subheader('')
        st.subheader('')

        st.subheader('カメラを起動させて、歯ブラシを撮影して下さい')
        st.subheader('※歯ブラシだけが写るようにすると認識しやすいよ')
        ID = st.secrets["GcpApiKey"]["project_id"]
        st.subheader(ID)
        st.image("img.jpeg")


if __name__ == "__main__":
    main()
