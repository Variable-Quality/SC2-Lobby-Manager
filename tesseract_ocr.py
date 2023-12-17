from pytesseract import Output
import pytesseract
import argparse
import cv2

class TesseractManager():

    def __init__(self, img="", min_conf=0):
       self.image = img
       self.min_conf = min_conf
       

    def read_image(self, debug = False):
        image = cv2.imread(self.image)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = pytesseract.image_to_data(rgb, output_type=Output.DICT)

        #Tuple containing confidence and coordinates
        ret = {}
        for i in range(0, len(result["text"])):
            x = result["left"][i]
            y = result["top"][i]
            w = result["width"][i]
            h = result["height"][i]

            text = result["text"][i]
            conf = int(result["conf"][i])

            if conf > self.min_conf:
                #print(f"Confidence: {conf}")
                #print(f"Text: {text}") 
                #print("===================")
                ret[text] = ([x, y, x + w, y + h], conf)
                text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
                if debug:
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                1.2, (0, 0, 255), 3)
                    cv2.imshow("Image", image)
                    cv2.waitKey(0)
                
        return ret
        