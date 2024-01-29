import unidecode

#Clase persona donde se guardaran los datos
class Persona:
    def __init__(self, name, image_path, phone):
        # Asegura que el nombre no tenga tildes, esté en minúsculas y no tenga espacios
        self.name = unidecode.unidecode(name.lower().replace(" ", ""))
        self.image_path = image_path
        self.phone = phone

    def __get_name__(self):
        return f"{self.name}"
    def __get_image__(self):
        return f"{self.image}"

    def __get_phone__(self):
        return f"{self.phone}"
    def to_dict(self):
        return {'name': self.name, 'image': f"{self.name}.jpg", 'phone': f"{self.phone}"}
    def __str__(self):
        return f"Persona(name={self.name}, image={self.image}, phone={self.phone})"
