import unidecode


class Persona:
    def __init__(self, name, image_path, phone):
        # Asegura que el nombre no tenga tildes, esté en minúsculas y no tenga espacios
        self.name = unidecode.unidecode(name.lower().replace(" ", "_"))
        self.image_path = image_path

    def __get_name__(self):
        return f"{self.name}"
    def __get_image__(self):
        return f"{self.image}"
    def to_dict(self):
        return {'name': self.name, 'image': f"{self.name}.jpg"}
    def __str__(self):
        return f"Persona(name={self.name}, image={self.image})"


