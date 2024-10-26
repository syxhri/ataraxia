import requests, json, secrets, os, datetime, re
from enum import Enum

class ResponseError(Exception): pass

class Models(Enum):
	BLACKBOXAI = 'blackboxai'
	BBAI = 'blackboxai'
	ATARAXIA = 'blackboxai'
	GPT = 'gpt-4o'
	GPT_4O = 'gpt-4o'
	GEMINI = 'gemini-pro'
	GEMINI_PRO = 'gemini-pro'
	CLAUDE = 'claude-sonnet-3.5'
	CLAUDE_SONNET = 'claude-sonnet-3.5'
	CLAUDE_SONNET_3_5 = 'claude-sonnet-3.5'

class ChatResponse:
	def __init__(self, **kwargs):
		valid_data = all(key in kwargs for key in ['id', 'role', 'content'])
		if not valid_data: raise ValueError('data not provided correctly')
		self.___d___ = {'id': kwargs['id'], 'role': kwargs['role'], 'content': kwargs['content']}
		self.id = kwargs['id']
		self.role = kwargs['role']
		self.content = kwargs['content']
		if kwargs.get('createdAt'):
			self.___d___['createdAt'] = kwargs['createdAt']
			self.created_at = kwargs['createdAt']
	
	def __repr__(self):
		return f'ChatResponse<{self.id}, {self.role}>'
	
	def __str__(self):
		return self.content
	
	def __call__(self, stringify: bool = False) -> dict | str:
		return json.dumps(self.___d___) if stringify else self.___d___

class ImageResponse:
	def __init__(self, **kwargs):
		valid_data = all(key in kwargs for key in ['id', 'role', 'content'])
		if not valid_data: raise ValueError('data not provided correctly')
		self.___d___ = {'id': kwargs['id'], 'role': kwargs['role'], 'content': kwargs['content']}
		self.id = kwargs['id']
		self.role = kwargs['role']
		self.content = kwargs['content']
		if kwargs.get('createdAt'):
			self.___d___['createdAt'] = kwargs['createdAt']
			self.created_at = kwargs['createdAt']
		
		self.___parse___()
	
	def __repr__(self):
		return f'ImageResponse<{self.id}>'
	
	def __str__(self):
		return self.link
	
	def __call__(self, stringify: bool = False) -> dict | str:
		return json.dumps(self.___d___) if stringify else self.___d___
	
	def ___parse___(self):
		parsed_links = re.findall(r'\!\[(.*)\]\s?\((.*)\)', self.content)
		if parsed_links is not None and len(parsed_links) > 0:
			parsed_link = parsed_links[0]
			if len(parsed_link) > 0:
				self.link = parsed_link[1]
			else:
				raise ValueError('the image link is invalid')
		else:
			raise ResponseError('failed to generate image. the model is overload')
			# raise ValueError('the image link is empty or invalid: ' + self.content)
	
	def download(self) -> bytes:
		res = requests.get(self.link)
		if res.ok:
			return res.content
		else:
			res.raise_for_status()
			raise Exception('failed to download image: ' + response.text)
	
	def save(self, image_path: str) -> bool:
		try:
			buffer = self.download()
			with open(image_path, 'wb') as im:
				im.write(buffer)
			return True
		except Exception as e:
			print(e)
			return False

class Blackbox:
	def __init__(
		self,
		model: Models = Models.BLACKBOXAI,
		chat_id: str | None = None,
		system_prompt: str | None = None,
		coding_mode: bool = False,
		auto_save: bool = True,
		data_filepath: str = './ataraxia-{CHAT_ID}.json'
	):
		if type(model) is not Models:
			raise TypeError('model must be type of ataraxia.Models, not ' + type(model).__name__)
		
		self.model = model
		self.system_prompt = system_prompt
		self.coding_mode = coding_mode
		self.auto_save = auto_save
		self.data_filepath = data_filepath
		self.history = []
		self.__ids_ = {
			'chat': chat_id or None,
			'img2code': None
		}
		
		if self.__ids_['chat'] is not None:
			if os.path.exists(self.__format_filepath_(self.__ids_['chat'])):
				self.load_chat(self.__ids_['chat'])
			else:
				self.__ids_['chat'] = None
				raise ValueError('cannot load chat data with that id. try with different id or change the default data filepath')
	
	@property
	def chat_id(self) -> str:
		if self.__ids_['chat']:
			return self.__ids_['chat']
		else:
			raise Exception('please send message first to get chat id')
	
	def __generate_id_(self, ai_type='chat', change=True):
		if ai_type.lower() == 'chat':
			id = secrets.token_hex(8).replace('_', '').replace('-', '')
			if change: self.__ids_['chat'] = id
			return id
		elif ai_type.lower() == 'message':
			return secrets.token_hex(10).replace('_', '').replace('-', '')
		elif ai_type.lower() == 'imagine':
			return secrets.token_hex(8).replace('_', '').replace('-', '')
		elif ai_type.lower() == 'img2code':
			id = secrets.token_hex(16).replace('_', '').replace('-', '')
			if change: self.__ids_['img2code'] = id
			return id
		else:
			raise ValueError('ai_type must be "chat", "imagine", "message" or "img2code", not "' + ai_type + '"')
	
	def __format_filepath_(self, chat_id, filepath=None):
		filepath = filepath if filepath is not None else self.data_filepath
		if '{CHAT_ID}' in filepath:
			filepath = filepath.replace('{CHAT_ID}', chat_id)
		return filepath
	
	def chat(self, message: str, history: list = []) -> ChatResponse:
		msg = message.strip()
		hist = history if history else self.history
		if self.__ids_['chat'] is None:
			self.__generate_id_()
		msg_id = self.__generate_id_('message')
		msg_data = {'id': msg_id, 'role': 'user', 'content': msg}
		hist.append(msg_data)
		data = {
			'messages': hist,
			'id': self.__ids_['chat'],
			'codeModelMode': self.coding_mode,
			'userSystemPrompt': self.system_prompt,
			'userSelectedModel': self.model.value,
			'previewToken': None,
			'userId': None,
			'agentMode': {},
			'trendingAgentMode': {},
			'isMicMode': False,
			'maxTokens': 1024,
			'playgroundTopP': 0.9,
			'playgroundTemperature': 0.7,
			'isChromeExt': False,
			'githubToken': None,
			'clickedAnswer2': False,
			'clickedAnswer3': False,
			'clickedForceWebSearch': False,
			'visitFromDelta': False,
			'mobileClient': False
		}
		url = 'https://www.blackbox.ai/api/chat'
		headers = {
			'content-type': 'application/json',
			'user-agent': 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.2 Mobile Safari/537.36',
			'referer': f'https://www.blackbox.ai/chat/{self.__ids_["chat"]}?model={self.model.value}'
		}
		response = requests.post(url, data=json.dumps(data), headers=headers)
		if response.ok:
			date = datetime.datetime.strptime(response.headers['date'], '%a, %d %b %Y %H:%M:%S GMT')
			date_formatted = date.strftime('%Y:%m:%dT%H:%M:%S') + '.000Z'
			res_id = self.__generate_id_('message')
			res_data = {
				'id': res_id,
				'createdAt': date_formatted,
				'role': 'assistant',
				'content': response.text
			}
			hist.append(res_data)
			self.history = hist
			result = ChatResponse(**res_data)
			if self.auto_save:
				self.save_chat()
			return result
		else:
			# response.raise_for_status()
			raise ResponseError('failed to process chat. response is invalid: ' + response.text)
	
	def imagine(self, prompt: str) -> ImageResponse:
		prompt = prompt.strip()
		id = self.__generate_id_('imagine')
		data = {
			'messages': [
				{
					'id': id,
					'content': prompt,
					'role': 'user'
				}
			],
			'id': id,
			'codeModelMode': True,
			'userSelectedModel': None,
			'previewToken': None,
			'userId': None,
			'agentMode': {
				'mode': True,
				'id': 'ImageGenerationLV45LJp',
				'name': 'Image Generation'
			},
			'trendingAgentMode': {},
			'isMicMode': False,
			'maxTokens': 1024,
			'playgroundTopP': None,
			'playgroundTemperature': None,
			'isChromeExt': False,
			'githubToken': None,
			'clickedAnswer2': False,
			'clickedAnswer3': False,
			'clickedForceWebSearch': False,
			'visitFromDelta': False,
			'mobileClient': False
		}
		url = 'https://www.blackbox.ai/api/chat'
		headers = {
			'content-type': 'application/json',
			'user-agent': 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.2 Mobile Safari/537.36',
			'referer': f'https://www.blackbox.ai/chat/{id}'
		}
		response = requests.post(url, data=json.dumps(data), headers=headers)
		if response.ok:
			date = datetime.datetime.strptime(response.headers['date'], '%a, %d %b %Y %H:%M:%S GMT')
			date_formatted = date.strftime('%Y:%m:%dT%H:%M:%S') + '.000Z'
			res_data = {
				'id': id,
				'createdAt': date_formatted,
				'role': 'assistant',
				'content': response.text
			}
			result = ImageResponse(**res_data)
			return result
		else:
			response.raise_for_status()
			raise ResponseError('failed to process image. response is invalid: ' + response.text)
	
	def set_system_prompt(self, prompt: str | None = None) -> None:
		self.system_prompt = prompt.strip()
	
	def change_filepath(self, data_filepath: str) -> None:
		self.data_filepath = data_filepath.strip()
	
	def save_chat(self, filepath: str | None = None) -> None:
		with open(self.__format_filepath_(self.chat_id, filepath), 'w') as df:
			chat_data = {
				'chat_id': self.chat_id,
				'model': self.model.value,
				'system_prompt': self.system_prompt,
				'coding_mode': self.coding_mode,
				'history': self.history
			}
			df.write(json.dumps(chat_data))
	
	def load_chat(self, chat_id: str) -> dict:
		try:
			with open(self.__format_filepath_(chat_id)) as df:
				cdata = df.read()
			chat_data = json.loads(cdata)
			self.model = Models(chat_data['model'])
			self.system_prompt = chat_data['system_prompt']
			self.coding_mode = chat_data['coding_mode']
			self.history = chat_data['history']
			return chat_data
		except Exception as e:
			self.__ids_['chat'] = None
			raise ValueError('failed to load saved history: ' + str(e))
