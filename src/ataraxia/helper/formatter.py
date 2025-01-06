import datetime

def format_filepath(
	chat_id: str,
	filepath: str = 'ataraxia_{CHAT_ID}.json'
) -> str:
	return filepath.replace('{CHAT_ID}', chat_id)

def format_date(response_headers: dict) -> str:
	date = datetime.datetime.strptime(response_headers.get('date') or '', '%a, %d %b %Y %H:%M:%S GMT')
	date_formatted = date.strftime('%Y:%m:%dT%H:%M:%S') + '.000Z'
	return date_formatted
