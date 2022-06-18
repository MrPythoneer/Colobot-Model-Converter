import geometry

# base class for formats
class ModelFormat:
    description: str
    ext: str

    def get_extension(self) -> str:
        return None

    def read(self, filename: str, model: geometry.Model, params: dict[str, str]) -> bool:
        print('Reading not implemented')
        return False

    def write(self, filename: str, model: geometry.Model, params: dict[str, str]) -> bool:
        print('Writing not implemented')
        return False