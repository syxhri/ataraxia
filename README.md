# Ataraxia (Blackbox)

Ataraxia is unofficial Python wrapper for [Blackbox AI](https://www.blackbox.ai).

## Installation
```bash
pip install ataraxia
```

## Usage
### Chat
```python
from ataraxia import Blackbox, Model

# Use Models.BLACKBOXAI by default
blackbox = Blackbox()
response = blackbox.chat('What do you think about gen alpha?') # ChatResponse<CHAT_ID>
print(response)

# Chat with image
response = blackbox.chat('What do you think about this image?', 'https://example.com/image.png') # from image link
response = blackbox.chat('What do you think about this image?', 'QWt1IFBIUA==') # from base64 string
response = blackbox.chat('What do you think about this image?', 'data:image/png;base64,QWt1IFBIUA==') # from base64 image data
response = blackbox.chat('What do you think about this image?', b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x03\xe8\x00\x00') # from image bytes

# Use other model from Model
blackbox = Blackbox(Model.GPT_4O)

# Set system instruction prompt
blackbox = Blackbox(instruction='You are a gen alpha assistant')
# or
blackbox.change_instruction('You are a gen alpha assistant')

# Load chat data and history from saved file
blackbox = Blackbox(chat_id='SAVED_CHAT_ID')
# or
blackbox.load_chat('SAVED_CHAT_ID')

# Save chat data and history to JSON file
blackbox.save_chat()
# or
blackbox.save_chat('./ataraxia_{CHAT_ID}.json') # {CHAT_ID} will be replaced with current chat id

# Change save path
blackbox.change_save_path('filename_{CHAT_ID}.json')
```

### Image Generation (Imagine)
```python
from ataraxia import Blackbox

blackbox = Blackbox()
result = blackbox.imagine('A pregnant kitten') # ImageResponse<IMAGE_ID>
print(result) # https://storage.googleapis.com/...

# Download the image to bytes
image_bytes = result.download()

# Save the image to file
result.save('./imagine.jpg') # True if success False otherwise
```

### Search
```python
from ataraxia import Blackbox

blackbox = Blackbox()
results = blackbox.search('Schall meaning') # list of SearchResult<TITLE>
print(results[0]) # Schall. [ʃal]Maskulinum | masculine m...
```

### Deep Search
```python
from ataraxia import Blackbox

blackbox = Blackbox()
result = blackbox.deep_search('Schall meaning') # SearchResult<OK>
print(result)
```

### Blackbox Params
|      Param      |   Type   |                                                                               Description                                                                              | Required |           Default           |
|:---------------:|:--------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:--------:|:---------------------------:|
|     `model`     | `Models` | Set the Blackbox AI (chat) default model                                                                                                                               |    No    |      `Model.BLACKBOXAI`     |
|    `chat_id`    |   `str`  | Set the saved `chat_id` to load the `history` and chat data                                                                                                            |    No    |            `None`           |
|  `instruction`  |   `str`  | Set the system instruction for every chat request                                                                                                                      |    No    |            `None`           |
|   `auto_save`   |  `bool`  | Will save chat data and history to `save_path` if `True`                                                                                                               |    No    |            `True`           |
|   `save_path`   |   `str`  | File path to save chat data like `model`, `instruction`, and `history`. It is recommended to always insert `{CHAT_ID}` so that it can be loaded with load_chat()       |    No    | `./ataraxia_{CHAT_ID}.json` |

### Blackbox.chat Params
|     Param     |      Type      |                               Description                                     | Required | Default |
|:-------------:|:--------------:|:-----------------------------------------------------------------------------:|:--------:|:-------:|
|   `message`   |     `str`      |                              Message to send                                  |    Yes   |    -    |
|    `image`    | `str \| bytes` |                              Additional image                                 |    No    | `None`  |
|   `history`   |     `list`     |                                Chat history                                   |    No    |  `[]`   |
|  `max_tokens` |     `int`      |                             Response max tokens                               |    No    | `1024`  |
|    `top_p`    |    `float`     | Probability sampling to determine the selected set of tokens for the response |    No    |  `0.9`  |
| `temperature` |    `float`     |      Set the level of creativity or randomness in the generated response      |    No    |  `0.7`  |

## Buy me tanghulu
https://trakteer.id/alfi-syahri
