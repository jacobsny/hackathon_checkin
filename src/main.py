from PIL import Image


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


def text_to_speech(text):
    from google.cloud import texttospeech

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)
    return response


def speech_to_text(path):
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
        language_code='en-US')

    # Detects speech in the audio file
    response = client.recognize(config, audio)
    responseString = ""
    for result in response.results:
        responseString += result.alternatives[0].transcript
    return responseString


def main():
    with open("src/que.txt") as f:
        lines = f.readlines()
    mainQ = lines.pop(0)
    text_to_speech(mainQ)
    """trigger listen and speech to text"""
    for line in lines:
        text_to_speech(line)
        """trigger more listening and append response in array"""
    """append array to end of google sheets"""
