def detect_faces(path):
    """Detects number of faces in an image."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations
    return len(faces)


def main():
    image_path = ""
    while detect_faces(image_path) > 0:


