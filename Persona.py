class Persona:
    def __init__(self, name, image):
        self.name = name
        self.image = image

    def __get_name__(self):
        return f"{self.name}"
    def __get_image__(self):
        return f"{self.image}"


