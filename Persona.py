class Persona:
    def __init__(self, name, image):
        self.name = name
        self.image = image

    def __get_name__(self):
        return f"{self.name}"
    def __get_image__(self):
        return f"{self.image}"
    def to_dict(self):
        return {'name': self.name, 'image': f"{self.name}.jpg"}
    def __str__(self):
        return f"Persona(name={self.name}, image={self.image})"


