import unidecode


class Persona:
    def _init_(self, name, image_path, phone):
        # Asegura que el nombre no tenga tildes, esté en minúsculas y no tenga espacios
        self.name = unidecode.unidecode(name.lower().replace(" ", "_"))
        self.image_path = image_path

    def _get_name_(self):
        return f"{self.name}"
    def _get_image_(self):
        return f"{self.image}"
    def to_dict(self):
        return {'name': self.name, 'image': f"{self.name}.jpg"}
    def _str_(self):
        return f"Persona(name={self.name}, image={self.image})"