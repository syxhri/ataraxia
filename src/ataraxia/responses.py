import re
import requests
from .helper import Json

class ResponseError(Exception): pass

class Response:
	def __init__(self, **r):
		valid = all(k in r for k in ['id', 'content', 'role'])
		if not valid:
			raise ValueError('response data not provided correctly')
		self.__d = Json(r)
	
	@property
	def id(self) -> str:
		return self.__d.id
	
	@property
	def content(self) -> str:
		return self.__d.content
	
	@property
	def role(self) -> str:
		return self.__d.role
	
	@property
	def created_at(self) -> str:
		return self.__d.createdAt
	
	def __repr__(self) -> str:
		return f'{self.__class__.__name__}<{self.id}>'
	
	def __str__(self) -> str:
		return self.content
	
	def __len__(self) -> int:
		return len(self.content)
	
	def __call__(self, stringify: bool = False) -> dict | str:
		if stringify:
			return str(self.__d)
		else:
			return self.__d()

class ChatResponse(Response):
	def __init__(self, **r):
		super().__init__(**r)

class ImageResponse(Response):
	def __init__(self, **r):
		super().__init__(**r)
		self.__parse()
	
	def __parse(self):
		parsed_links = re.findall(r'\!\[(.*)\]\s?\((.*)\)', self.content)
		if parsed_links is not None and len(parsed_links) > 0:
			parsed_link = parsed_links[0]
			if len(parsed_link) > 0:
				self.link = parsed_link[1]
			else:
				raise ValueError('the image link is invalid')
		else:
			raise ResponseError('failed to generate image. the model is overload')
	
	def download(self) -> bytes:
		res = requests.get(self.link)
		if res.ok:
			return res.content
		else:
			res.raise_for_status()
			raise Exception('failed to download image: ' + response.text)
	
	def save(self, path: str) -> bool:
		try:
			buffer = self.download()
			with open(path, 'wb') as im:
				im.write(buffer)
			return True
		except Exception as e:
			print('error saving image', e)
			return False

class SearchResult:
	def __init__(self, **r):
		if r.get('text'):
			self.__d = Json(content=r['text'].strip())
		else:
			valid = all(k in r for k in ['link', 'position', 'snippet', 'title'])
			if not valid:
				raise ValueError('result data not provided correctly')
			self.__d = Json(r)
	
	@property
	def link(self) -> str:
		return self.__d.link
	
	@property
	def position(self) -> int:
		return self.__d.position
	
	@property
	def date(self) -> str:
		return self.__d.date
	
	@property
	def missing(self) -> str:
		return self.__d.attributes.Missing if self.__d.attributes and self.__d.attributes.Missing else None
	
	@property
	def snippet(self) -> str:
		return self.__d.snippet
	
	@property
	def title(self) -> str:
		return self.__d.title
	
	@property
	def content(self) -> str:
		return self.__d.content
	
	def __repr__(self) -> str:
		return f'{self.__class__.__name__}<{self.title or "OK"}>'
	
	def __str__(self) -> str:
		return self.snippet or self.content
	
	def __len__(self) -> int:
		return len(self.snippet or self.content)
	
	def __call__(self, stringify: bool = False) -> dict | str:
		if stringify:
			return str(self.__d)
		else:
			return self.__d()