import barcode
from barcode.writer import ImageWriter


def generate_barcode(data: str, filename: str):
    barcode_path = f"static/barcodes/{filename}.png"
    code128 = barcode.get_barcode_class('code128')
    barcode_instance = code128(data, writer=ImageWriter())
    barcode_instance.save(barcode_path[:-4])  # Видаляємо ".png" перед збереженням