import streamlit as st
import streamlit_toggle as tog
from google.cloud import vision
from google.oauth2 import service_account


def detect_toothbrush(image):

    service_account_key = {
        "type": "service_account",
        "project_id": "crypto-visitor-395006",
        "private_key_id": "c535a81cf017677f38546d95cf253e03f0ea884b",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDMlvawnNt5fzg9\nWwiyQKhYEdbKD65vR18aCFYVPFRFvrF7AxhVWBBX0rpRsZOHK59RF0R9FKFlqqWS\nt94tua9ZBK3lW8fgfO1n9kvl2Zgqobe8cO6eBVQoPlBhNFPogZEcadBsjLOw+44g\nEJORSSQL6rn6xj4AlFKfQLXvw3sVRb+lowXyRg7QeiUQx7B94wYc8YcdAK1vaeVc\n1fDjhMzBq4VQAydng9Ntftb2A06RrObNXfHcSCCrFdJwdJ4LJ70P1DGy3p4itvIZ\nIiZ3gHr2lIXeZDEO5/3Xt1gbcswAr+l+cpWKauliIDzUGmEPMG5XcI2HrDo1oKPf\nqPAJ7m8fAgMBAAECggEANDZ018b4Vi4LFtGESyWoMO3AkMnmvRyMX1LwUTQX18Le\nfaPhEmrKpPcxOMcmfPE7lBDpmDhrJkyiO+rz51yDrSa+EJJXVOndFtKrNQpOxNaH\n0y5JH4gBndGlZuFZZrWmaIdyuzk/ZLQWZgWE+6ecbPQnKaJtUW2JFn6H0Bxl7Zvt\n/bQYgXgDyEZmeyCdrvpV0tFW0agY6aW8XCty3A/HC7oxf63rev5zo8ACiAAarLKB\ndXJTLgydA/74Z+dAjWm6n/bIP5NV9DMWOm02+7zVld8jPkmere36L8KtfDzNK4yW\nUIBXbswC0EEBXobT5xM/vHtxmicFCVB1o2w7/AnyYQKBgQDrF9DXc1PgB934IOId\n15JZuQPgWQ2NSBPUsMcQgf+rul7BoojaHYCe6hT1JQksdeAXl+bOjwIIUKUPT2Tg\nuC+6HwWS3koYoOnNQ0YNB6njNw09httlzhFzg7SO/uQAPyoI81ylLaRF64kL6uu4\n2/v3pHqihu7O0Vb8N80l7VKo4QKBgQDeyLOmkfqLKoEWc8OM8l7F8u/qJHKN7KC8\nNSI3EuQjoWWOe9OQWoF4PTnNPrQZHJnQr8VjQoBm+IFkxwWN2aBcfDsJehcI+iTX\nLiseKNQ5Gb0JD3+30F4MyujkS9dY/nuSFWNXm1El8U0jjlC6rQHtHikvHOyLL05g\npTxLiOwX/wKBgQDSIxOVwYxzcBTEuf/j1NEISgxg+LjYVFkFgI4u/0RdZ9VTF8lj\nzYMuiOX6ygQNLcAE1s6ES+fxLsSbjsgI5hojL593zCJHKW5S/5MaCoOciZTYLjbm\nJPAMZOl79/ItFkiof3+MVePEa+iwMmhJcLkkfmzv4dSMISqzf91rzVpZgQKBgFLV\n7XaR8MauFzFx+dP+ip6vpeU5iB6dTWatmvs/WvSknk5MXG3gOSOsIEHgfraXm9ms\ngYhWwceHvxTpq3cC5E1/I7RyYP5FhE0+LWoZZE+W8mLcEHEYWOAI0m+Qg5Hjja7T\npQx+A75H6pa94+aFTaINBOMvrgRSoqHszm6HisGhAoGAH+QjpY2gzTtkn3OfJcqo\nRhi7tyeKLeDzLlQiUcV2tblFF2hrFeKM/buYNiwnYEMQOjOYaRsXqDqj5VgXybQO\nBBi4NbuBE7GIZnS0qjwpPq44I3pqnVD9ZZkfjNQFtqQ2zdTz/HfTrQBz5/9V/Kj9\n5pdeniuSC0eQM0IJWhweZfg=\n-----END PRIVATE KEY-----\n",
        "client_email": "my-project@crypto-visitor-395006.iam.gserviceaccount.com",
        "client_id": "111524740235394368765",
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
