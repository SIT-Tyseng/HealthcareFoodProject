import cv2
from PIL import Image

from ultralytics import YOLO

model = YOLO("yolo11n.pt")
# accepts all formats - image/dir/Path/URL/video/PIL/ndarray. 0 for webcam
# results = model.predict(source="0")
# results = model.predict(source="folder", show=True)  # Display preds. Accepts all YOLO predict arguments

# from PIL
# im1 = Image.open("bus.jpg")
# results = model.predict(source=im1, save=True)  # save plotted images

# from ndarray
def infer(path):
    img = cv2.imread(path)
    results = model.predict(source=img, save=True, save_txt=True, exist_ok=True)  # save predictions as labels
    return img

im1 = infer("/dataset/Ayam_Penyet/Ayam_Penyet_18.jpg")
im2 = infer("/dataset/Chicken_Rice_Roasted/Chicken_Rice_Roasted_29.jpg")
im3 = infer("/dataset/Economy_Rice/Economy_Rice_4.jpg")
im4 = infer("/dataset/Satay/Satay_4.jpg", "Satay")
im5 = infer("/dataset/Laksa/Laksa_22.jpg", "Laksa")
im6 = infer("/dataset/Lor_Mee/Lor_Mee_31_w.jpg", "Lor_Mee")


# from list of PIL/ndarray
results = model.predict(source=[im1, im2, im3, im4])