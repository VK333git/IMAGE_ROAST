import pathlib
import textwrap
import os
import PIL.Image
import logging
import pathlib
import textwrap
import io
import base64

import google.generativeai as genai

from IPython.display import Markdown

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow INFO and WARNING messages
os.environ['GRPC_VERBOSITY'] = 'ERROR' 

logging.getLogger('tensorflow').setLevel(logging.ERROR)

import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

import tensorflow as tf
import logging
logging.getLogger('tensorflow').setLevel(logging.ERROR)

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

genai.configure(api_key = os.getenv("API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')
img = PIL.Image.open('D:\\IMAGE_ROAST\\Screenshot 2024-07-14 163051.png')
response = model.generate_content(["Imagine you're a stand-up comedian at IIT BHU, ready to entertain freshers with your sharp wit. You've just been handed an image of a student's face, and your task is to craft a joke that’s funny and cheekily offensive, directly targeting the face in the photo. Keep it focused on their features and expressions, and make it a roast that the audience won't forget. Remember, it’s all in good fun, but don’t hold back.Generate the roast in hinglish", img])
markdown_response = to_markdown(response.text)
print(markdown_response.data)





