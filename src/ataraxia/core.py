from os.path import exists
import requests
import validators
from base64 import b64encode
from .responses import ChatResponse, ImageResponse, SearchResult, ResponseError
from .helper import generate_id as genid, uuid, format_filepath as ffp, format_date as fdt, Json
from .helper.json import for_each
from .constants import Model

class Blackbox:
	def __init__(
		self,
		model: Model = Model.BLACKBOXAI,
		chat_id: str | None = None,
		instruction: str | None = None,
		auto_save: bool = True,
		save_path: str = 'ataraxia_{CHAT_ID}.json'
	):
		if type(model) is not Model:
			raise TypeError('model must be type of ataraxia.constants.Model, not ' + type(model).__name__)
		
		self.model = model
		self.instruction = instruction
		self.auto_save = auto_save
		self.save_path = save_path
		self.history = []
		self.__chat_id = chat_id or None
		
		if self.__chat_id is not None:
			if exists(ffp(self.__chat_id, self.save_path)):
				self.load_chat(self.__chat_id)
			else:
				self.__chat_id = None
				raise ValueError('cannot find save file with that id')
	
	def __apireq(
		self,
		path: str,
		data: dict | Json,
		headers: dict | Json = {
			'content_type': 'application/json',
			'user-agent': 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.2 Mobile Safari/537.36'
		}
	) -> requests.Response:
		if type(data) is Json: data = data()
		if type(headers) is Json: headers = headers()
		response = requests.post(
			'https://api.blackbox.ai/api' + path,
			json=data,
			headers=headers
		)
		if response.ok:
			return response
		else:
			try:
				response.raise_for_status()
			except Exception as e:
				raise ResponseError('api request failed. error detail:\n' + str(e))
			raise ResponseError('api request failed. response content:\n' + response.text)
	
	@property
	def chat_id(self):
		return self.__chat_id
	
	def change_instruction(self, instruction: str):
		self.instruction = instruction.strip()
	
	def change_save_path(self, save_path: str):
		self.save_path = save_path
	
	def load_chat(self, chat_id: str) -> dict:
		try:
			with open(ffp(chat_id, self.save_path)) as df:
				cdata = df.read()
			chat_data = Json(cdata)
			self.model = Model(chat_data.model)
			self.instruction = chat_data.instruction
			self.history = chat_data.history
			return chat_data
		except Exception as e:
			self.__chat_id = None
			raise Exception('failed to load saved history: ' + str(e))
	
	def save_chat(self, save_path: str | None = None):
		with open(ffp(self.chat_id, save_path or self.save_path), 'w') as df:
			chat_data = Json(
				chat_id = self.chat_id,
				model = self.model.value,
				instruction = self.instruction,
				history = self.history
			)
			df.write(str(chat_data))
	
	def chat(
		self,
		message: str,
		image: str | bytes | None = None,
		history: list = [],
		max_tokens: int = 1024,
		top_p: float = 0.9,
		temperature: float = 0.7
	) -> ChatResponse:
		message = message.strip()
		ch = history if history else self.history
		if self.__chat_id is None:
			self.__chat_id = genid(14)
		
		message_id = genid(16)
		msg = Json(id=message_id, content=message, role='user')
		if image is not None:
			if type(image) is str:
				if validators.url(image):
					msg['data'] = Json(imagesData=[
						Json(
							filePath = 'MultipleFiles/' + image.split('/')[-1],
							contents = 'data:image/png;base64,' + b64encode(requests.get(images).content).decode('utf-8')
						)()
					])()
				elif validators.base64(image):
					msg['data'] = Json(imagesData=[
						Json(
							filePath = 'MultipleFiles/image.png',
							contents = 'data:image/png;base64,' + image
						)()
					])()
				elif ';base64,' in image:
					msg['data'] = Json(imagesData=[
						Json(
							filePath = 'MultipleFiles/image.png',
							contents = image
						)()
					])()
				else:
					raise ValueError('invalid image data')
			elif type(image) is bytes:
				msg['data'] = Json(imagesData=[
					Json(
						filePath = 'MultipleFiles/image.png',
						contents = 'data:image/png;base64,' + b64encode(image).decode('utf-8')
					)()
				])()
			else:
				raise TypeError('image type must be str (image link, base64 data) or bytes')
		ch.append(msg())
		data = Json(
			messages = ch,
			agentMode = {},
			id = self.chat_id,
			previewToken = None,
			userId = None,
			codeModelMode = False,
			trendingAgentMode = {},
			isMicMode = False,
			userSystemPrompt = self.instruction,
			maxToken = max_tokens,
			playgroundTopP = top_p,
			playgroundTemperature = temperature,
			isChromeExt = False,
			githubToken = None,
			clickedAnswer2 = False,
			clickedAnswer3 = False,
			clickedForceWebSearch = False,
			visitFromDelta = False,
			mobileClient = False,
			userSelectedModel = self.model.value,
			imageGenerationMode = False
		)
		response = self.__apireq('/chat', data)
		response_id = genid(16)
		response_data = Json(
			id = response_id,
			content = response.text.strip(),
			role = 'assistant',
			createdAt = fdt(response.headers)
		)
		ch.append(response_data())
		self.history = ch.copy()
		chat_response = ChatResponse(**response_data())
		
		if self.auto_save:
			self.save_chat()
		return chat_response
	
	def search(self, query: str) -> list:
		query = query.strip()
		msg = Json(id=genid(16), content=query, role='user')
		data = Json(
			messages = [msg()],
			agentMode = {},
			id = genid(14),
			previewToken = None,
			userId = None,
			codeModelMode = True,
			trendingAgentMode = {},
			isMicMode = False,
			userSystemPrompt = None,
			maxToken = 1024,
			playgroundTopP = None,
			playgroundTemperature = None,
			isChromeExt = False,
			githubToken = "",
			clickedAnswer2 = False,
			clickedAnswer3 = False,
			clickedForceWebSearch = False,
			visitFromDelta = False,
			mobileClient = False,
			userSelectedModel = None,
			validated = uuid(),
			imageGenerationMode = False,
			webSearchModePrompt = True,
			deepSearchMode = False,
			domains = None,
			vscodeClient = False
		)
		response = self.__apireq('/check', data)
		response = Json(response.json())
		if not response.results or not response.results.organic:
			raise ResponseError('result not found')
		
		search_results = []
		for_each(
			response.results.organic,
			lambda v: search_results.append(SearchResult(**v()))
		)
		return search_results
	
	def deep_search(self, query: str) -> list:
		query = query.strip()
		msg = Json(id=genid(16), content=query, role='user')
		data = Json(
			messages = [msg()],
			agentMode = {},
			id = genid(14),
			previewToken = None,
			userId = None,
			codeModelMode = True,
			trendingAgentMode = {},
			isMicMode = False,
			userSystemPrompt = None,
			maxToken = 1024,
			playgroundTopP = None,
			playgroundTemperature = None,
			isChromeExt = False,
			githubToken = "",
			clickedAnswer2 = False,
			clickedAnswer3 = False,
			clickedForceWebSearch = False,
			visitFromDelta = False,
			mobileClient = False,
			userSelectedModel = None,
			validated = uuid(),
			imageGenerationMode = False,
			webSearchModePrompt = False,
			deepSearchMode = True,
			domains = None,
			vscodeClient = False
		)
		response = self.__apireq('/check', data)
		return SearchResult(text=response.text)
	
	def imagine(self, prompt: str) -> ImageResponse:
		prompt = prompt.strip()
		data = Json(
			messages = [{'id': genid(16), 'content': prompt, 'role': 'user'}],
			id = genid(14),
			codeModelMode = True,
			userSelectedModel = None,
			previewToken = None,
			userId = None,
			agentMode = Json(
				mode = True,
				id = 'ImageGenerationLV45LJp',
				name = 'Image Generation'
			)(),
			trendingAgentMode = {},
			isMicMode = False,
			maxTokens = 1024,
			playgroundTopP = None,
			playgroundTemperature = None,
			isChromeExt = False,
			githubToken = None,
			clickedAnswer2 = False,
			clickedAnswer3 = False,
			clickedForceWebSearch = False,
			visitFromDelta = False,
			mobileClient = False
		)
		response = self.__apireq('/chat', data)
		response_id = genid(16)
		response_data = Json(
			id = response_id,
			content = response.text.strip(),
			role = 'assistant',
			createdAt = fdt(response.headers)
		)
		image_response = ImageResponse(**response_data())
		return image_response