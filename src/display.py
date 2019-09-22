settings = {'resolution': (1600, 900), 'fullscreen': False, 'preserve_aspect_ratio': True, 'framerate': 30,
            'debug': True, 'directory': '/home/jacob/PycharmProjects/hackathon_checkin/src/pictures',
            'transition': 'fade', 'transition_time': 1, 'image_time': 50000}
import time

import pygame.camera
from PIL import Image
from google.cloud import translate

from src import helper, mic, sheets
from src.slider.slider import Main

if __name__ == '__main__':

    pygame.init()

    main = Main(settings)

    # pygame.time.set_timer(pygame.USEREVENT, int(settings['image_time'] * 1000))
    pygame.camera.init()
    cam = pygame.camera.Camera('/dev/video0', (1280, 720))
    while True:
        time.sleep(5)
        cam.start()
        image = cam.get_image()
        pil_string_image = pygame.image.tostring(image, "RGB")
        im = Image.frombytes("RGB", (1280, 720), pil_string_image)
        im.save("image.png", "PNG")
        cam.stop()
        while not helper.detect_faces():
            cam.start()
            image = cam.get_image()
            pil_string_image = pygame.image.tostring(image, "RGB")
            im = Image.frombytes("RGB", (1280, 720), pil_string_image)
            im.save("image.png", "PNG")
            cam.stop()
            time.sleep(1)
        main.transition()
        row = []
        with open("que.txt") as f:
            lines = f.readlines()
        mainQ = lines.pop(0)
        helper.text_to_speech(mainQ, 'en')
        time.sleep(helper.wordCount(mainQ) * .4)
        translate_client = translate.Client()

        languageInEnglish = mic.main('en')
        language = 'en'
        with open("/home/jacob/PycharmProjects/hackathon_checkin/src/dict.txt") as dict:
            dictLines = dict.readlines()
            for dictline in dictLines:
                arr = dictline.split("\t")
                if arr[0].lower() == languageInEnglish.lower():
                    language = arr[-1][:-1]
                    break
        row.append(language)
        card = lines.pop(0)
        newCard = translate_client.translate(card, target_language=language)['translatedText']
        main.transition()
        helper.text_to_speech(newCard, language)
        time.sleep(helper.wordCount(newCard) * .4)
        idCheck, name = helper.checkID()
        row = [name] + row
        if idCheck:
            for line in lines:
                # line translated from en to lang
                translatedText = translate_client.translate(line, target_language=language)
                line = translatedText['translatedText']
                main.transition()
                helper.text_to_speech(line, language)
                time.sleep(helper.wordCount(line) * .4)
                response = mic.main(language)
                # response translated from lang to en
                translatedText = translate_client.translate(response, target_language='en')
                response = translatedText['translatedText']
                row.append(response)
            sheets.main(row)

        else:
            for i in range(len(lines)+1):
                main.transition()
            print("something with our system didn't match up with your records")
            print("please see a staff member to clear this up")
        time.sleep(15)

