from google.cloud import vision

def_analyze_image(image_path):

    # jpgファイルの読み込み
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Vision APIが扱える画像データにする
    image_va = vision.Image(content=content)

    # ImageAnnotatorClientのインスタンスを作成
    annotator_client = vision.ImageAnnotatorClient()

    responce_data = annotator_client.label_detection(image=image_va)
    labels = responce_data.label_annotations

    objects = annotator_client.object_localization(image=image_va).localized_object_annotations

    print('--------------RESULT--------------')
    print(f"Number of objects found: {len(objects)}")
    for object_ in objects:
        print(f"{object_.name} (confidence: {object_.score})")
        if object_.name == 'Toothbrush' and object_.score > 0.7:
            print("対象写真")
        else:
            print("対象外写真")


    print('--------------RESULT--------------')

    return ""

    # export GOOGLE_APPLICATION_CREDENTIALS="/Users/yasudakeinin/Documents/
    # vision-ai-test/crypto-visitor-395006-c535a81cf017.json"
