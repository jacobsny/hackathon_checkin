from PIL import Image
import pygame
import time

from google.cloud import translate
from googleapiclient import discovery
from src import mic
from src import sheets
import pygame.camera


def detect_faces():
    """Detects number of faces in an image."""
    from google.cloud import vision
    import io
    from google.cloud.vision import types
    client = vision.ImageAnnotatorClient()
    with io.open("image.png", 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    boo = False
    for face in faces:
        vertices = ([[vertex.x, vertex.y] for vertex in face.bounding_poly.vertices])
        side1 = abs(vertices[0][0] - vertices[1][0])
        side2 = abs(vertices[0][1] - vertices[2][1])
        area = side1 * side2
        # print(area, 400*400)
        if area > (400 * 400):
            boo = True
    return boo


def text_to_speech(text,lang):
    from google.cloud import texttospeech

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code=lang,
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)
    with open('output.mp3', 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
    pygame.mixer.music.load('output.mp3')
    pygame.mixer.music.play(0)


def speech_to_text(path, lang):
    import io
    import os

    # Imports the Google Cloud client library
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types

    # Instantiates a client
    client = speech.SpeechClient()

    # Loads the audio into memory
    with io.open(path, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=lang)

    # Detects speech in the audio file
    response = client.recognize(config, audio)
    responseString = ""
    for result in response.results:
        responseString += result.alternatives[0].transcript
    return responseString


def checkID():
    pygame.camera.init()
    cam = pygame.camera.Camera('/dev/video0', (1280, 720))
    cam.start()
    image = cam.get_image()
    pil_string_image = pygame.image.tostring(image, "RGB")
    im = Image.frombytes("RGB", (1280, 720), pil_string_image)
    im.save("image.png", "PNG")
    # im.show()
    cam.stop()
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()
    with io.open("image.png", 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    responseLabels = client.label_detection(image=image)
    labels = responseLabels.label_annotations
    ID_present = False
    for label in labels:
        if label.description == "Identity document":
            ID_present = True
    while not ID_present:
        cam.start()
        image = cam.get_image()
        pil_string_image = pygame.image.tostring(image, "RGB")
        im = Image.frombytes("RGB", (1280, 720), pil_string_image)
        im.save("image.png", "PNG")
        cam.stop()
        with io.open("image.png", 'rb') as image_file:
            content = image_file.read()
        image = vision.types.Image(content=content)
        responseLabels = client.label_detection(image=image)
        labels = responseLabels.label_annotations
        ID_present = False
        for label in labels:
            if label.description == "Identity document":
                ID_present = True
    responseText = client.text_detection(image=image)
    texts = responseText.text_annotations
    textList = []
    generic = ["the", "at", "of", "college", "university", "state", "new", "my", "student"]
    characters = ["&", "\n", ".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "#"]
    for text in texts:
        name = text.description
        if name.lower() not in generic:
            boo = True
            for char in characters:
                if char in name:
                    boo = False
            if boo and len(name) > 1:
                textList.append(name.upper())
    textList.sort(key=len, reverse=True)
    rsvp = False
    spreadsheet_id = '1entWz5u4M0q0t1OqS7gsMNKuaGHUEzgfuxMjjKe2Qsc'
    range_name = "Sheet2"
    credentials = None
    service = discovery.build('sheets', 'v4', credentials=credentials)
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()["values"]
    name = ""
    for arr in result:
        if arr[0].upper() in textList and arr[1].upper() in textList:
            rsvp = True
            name = arr[0] + " " + arr[1]
    response = client.face_detection(image=image)
    faces = response.face_annotations
    return rsvp, name


def wordCount(str):
    arr = str.split(" ")
    return len(arr)

