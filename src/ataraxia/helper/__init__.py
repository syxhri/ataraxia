from .json import Json
from .formatter import format_filepath, format_date

def generate_id(length: int = 8) -> str:
	from secrets import token_hex
	return token_hex(length).replace('_', '').replace('-', '')

def uuid():
	from uuid import uuid4
	return str(uuid4())