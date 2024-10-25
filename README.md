# Ataraxia 🦇

Ataraxia is unofficial Python wrapper of [Blackbox AI](https://www.blackbox.ai).
The name ataraxia is taken from the clan of a vampire girl from a Webtoon

## Installation
```bash
pip install ataraxia
```

## Usage
### Chat
```python
from ataraxia import Blackbox, Models, ChatResponse

# Use Models.BLACKBOXAI by default
blackbox = Blackbox()
response = blackbox.chat('How do you think about gen alpha?') # ChatResponse<CHAT_ID, ROLE>
print(response)

# Use other model from Models
blackbox = Blackbox(Models.GPT_4O)

# Set system instruction prompt
blackbox = Blackbox(system_prompt='You are a gen alpha assistant')
# or
blackbox.set_system_prompt('You are a gen alpha assistant')

# Load chat data and history from saved file
blackbox = Blackbox(chat_id='SAVED_CHAT_ID')
# or
blackbox.load_chat('SAVED_CHAT_ID')

# Save chat data and history to file
blackbox.save_chat()
# or
blackbox.save_chat('./ataraxia-FILE_ID.json')

# Change data filepath
blackbox.change_filepath('filename_{CHAT_ID}.extension') # must includes the {CHAT_ID} to makes the file can be loaded using Blackbox.load_chat()
```

### Image Generation (Imagine)
```python
from ataraxia import Blackbox, ImageResponse

blackbox = Blackbox() # no need to set model for image generation
result = blackbox.imagine('A whale flying in the hell') # ImageResponse<IMAGE_ID>
print(result) # https://storage.googleapis.com/...

# Download the image to bytes
image_bytes = result.download()

# Save the image to file
result.save('./imagine.jpg') # True if success False otherwise
```

### Params
|      Param      |   Type   |                                                                               Description                                                                              |                      Required                    |
|:---------------:|:--------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:------------------------------------------------:|
|     `model`     | `Models` | Set the Blackbox AI (chat) default model                                                                                                                               |        No. Default is `Models.BLACKBOXAI`        |
|    `chat_id`    |   `str`  | Set the saved `chat_id` to load the `history` and chat data                                                                                                            |            No. Default is `None`                 |
| `system_prompt` |   `str`  | Set the system instruction for every chat request                                                                                                                      |            No. Default is `None`                 |
|  `coding_mode`  |  `bool`  | Set coding mode. Will answer using coding context if `True`                                                                                                            |            No. Default is `False`                |
|   `auto_save`   |  `bool`  | Will save chat data and history to `data_filepath` if `True`                                                                                                           |            No. Default is `True`                 |
| `data_filepath` |   `str`  | File path to save chat data like `model`, `system_prompt`, `coding_mode`, and `history`. It is recommended to always insert `{CHAT_ID}` so that it can be loaded later |    No. Default is `./ataraxia-{CHAT_ID}.json`    |

## Buy me tanghulu
https://trakteer.id/alfi-syahri
