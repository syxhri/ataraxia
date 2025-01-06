import json as _j
from string import ascii_letters as _al, digits as _dg
import re as _re
from inspect import stack as _stk

class JsonError(Exception): pass
class ForbiddenItem(Exception): pass

class Json(object):
	def __init__(self, json_data: dict | list | str = None, **kwargs):
		self.__dict__['__jd_'] = {}
		if json_data is not None:
			if isinstance(json_data, Json):
				self.__jd_ = dict(json_data)
			if isinstance(json_data, dict):
				self.__jd_ = json_data
			elif isinstance(json_data, list):
				self.__jd_ = json_data
			elif isinstance(json_data, str):
				if not Json.__validate_(json_data): raise JsonError('invalid json string')
				self.__jd_ = _j.loads(json_data)
			else:
				raise JsonError('expecting dict, list, or str type but {} received'.format(json_data.__class__.__name__))
		else:
			self.__jd_ = dict(kwargs)
		
		self.__reserved_kw_ = ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
		self.__valid_char_ = list(_al + _dg + '_')
		self.__process_self_()
	
	def __repr__(self):
		# return f'Json<{len(self.__jd_)}>'
		return repr(self.__jd_)
	
	def __call__(self):
		a = self.__jd_.copy()
		b = {} if isinstance(self.__jd_, dict) else []
		if b == {}:
			for k, v in a.items():
				if isinstance(v, Json):
					v = v()
				b[k] = v
		else:
			for i in a:
				if isinstance(i, Json):
					i = i()
				b.append(i)
		return b
	
	def __str__(self):
		return _j.dumps(self.__jd_)
	
	def __len__(self):
		return len(self.__jd_)
	
	def __iter__(self):
		if self.__type_ == dict:
			yield from self.__dict__['__jd_'].items()
		elif self.__type_ == list:
			yield from items(self)
	
	def __getitem__(self, k: str | int):
		if '__jd_' not in self.__dict__:
			return None
		else:
			try:
				return self.__jd_[k]
			except KeyError:
				koi = 'key' if type(self.__jd_) == dict else 'index'
				raise JsonError(f'invalid {koi}: {k}')
	
	def __setitem__(self, k: str | int, v: object):
		self.__jd_[k] = v
		self.__process_self_()
	
	def __getattr__(self, n: str):
		if n.startswith('__'):
			raise ForbiddenItem('are you trying to access private attribute?')
		elif '__jd_' in self.__dict__:
			if n in self.__jd_: return self.__jd_[n]
	
	# def __setattr__(self, n, v):
		# if n.startswith('__'):
			# # super().__setattr__(n, v)
			# self.__dict__[n] = v
		# else:
			# if '__jd_' in self.__dict__:
				# self.__jd_[n] = v
				# self.__process_self_()
			# else:
				# self.__dict__[n] = v
	
	@property
	def __type_(self):
		return type(self.__jd_)
	
	@property
	def __copy_(self):
		return Json(self.__jd_)
	
	def __validate_(data: str):
		cfc = _stk()[1].function != '<module>'
		if not cfc: raise ForbiddenItem('this function is forbidden')
		
		try:
			_j.loads(data)
			return True
		except:
			return False
	
	def __sa_(self, n: str, v: object):
		cfc = _stk()[1].function != '<module>'
		if not cfc: raise ForbiddenItem('this function is forbidden')
		
		if isinstance(v, dict):
			v = Json(v)
		elif isinstance(v, list):
			v = Json(v)
		setattr(self, n, v)
	
	def __ga_(self, n: str):
		cfc = _stk()[1].function != '<module>'
		if not cfc: raise ForbiddenItem('this function is forbidden')
		
		return getattr(self, n, None)
	
	def __process_self_(self):
		cfc = _stk()[1].function != '<module>'
		if not cfc: raise ForbiddenItem('this function is forbidden')
		
		jd = self.__jd_.copy()
		if isinstance(jd, dict):
			for k, v in jd.items():
				if k in self.__reserved_kw_: continue
				if k not in self.__valid_char_:
					k = _re.sub(r'[^\w]', '_', k)
				self.__sa_(k, v)
		elif isinstance(jd, list):
			njd = []
			for v in jd:
				if isinstance(v, dict) or isinstance(v, list):
					njd.append(Json(v))
				else:
					njd.append(v)
			self.__jd_ = njd

def load(path: str):
	with open(path) as f:
		return Json(f.read())

def save(path: str, json: Json):
	with open(path, 'w') as f:
		f.write(str(json))

def stringify(json: Json):
	return str(json)

def parse(json: dict | list | str):
	return Json(json)

def keys(json: Json):
	t = json._Json__type_
	d = json._Json__jd_
	
	if t == dict:
		return d.keys()
	elif t == list:
		return list(range(len(d)))

def values(json: Json):
	t = json._Json__type_
	d = json._Json__jd_
	
	if t == dict:
		return d.values()
	elif t == list:
		return d

def items(json: Json):
	t = json._Json__type_
	d = json._Json__jd_
	
	if t == dict:
		return d.items()
	elif t == list:
		k = keys(json)
		v = values(json)
		return dict(zip(k, v))

def for_each(json: Json, func):
	t = json._Json__type_
	d = json._Json__jd_
	
	if t is not list:
		raise TypeError('only list can used this function')
	for i in range(len(d)):
		func(d[i])
