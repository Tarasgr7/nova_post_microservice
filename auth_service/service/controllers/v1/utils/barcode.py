import barcode
from barcode.writer import ImageWriter
import os
import uuid

def create_barcode_id():
    return str(uuid.uuid4().int)[:14] 

def generate_barcode(data: str, filename: str, user: bool):
    barcode_path = f"static/barcodes/{filename}.png"
    code128 = barcode.get_barcode_class('code128')
    barcode_instance = code128(data, writer=ImageWriter())
    barcode_instance.save(barcode_path[:-4])  # Видаляємо ".png" перед збереженням
    return barcode_path
