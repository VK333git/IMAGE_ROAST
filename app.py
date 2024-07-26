from flask import Flask, request, render_template_string, send_from_directory
import os
import PIL.Image
import textwrap
import logging
import google.generativeai as genai

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

html_template = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Image Upload</title>
    <style>
      body {{
        background-color: #f2f2f2;
        font-family: Arial, sans-serif;
      }}
      .container {{
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
      }}
      h1 {{
        color: #333333;
      }}
      form {{
        margin-top: 20px;
      }}
      input[type="file"] {{
        padding: 10px;
        width: calc(100% - 22px);
        border: 1px solid #cccccc;
        border-radius: 5px;
        margin-bottom: 20px;
      }}
      button {{
        padding: 10px 20px;
        background-color: #007bff;
        color: #ffffff;
        border: none;
        border-radius: 5px;
        cursor: pointer;
      }}
      button:hover {{
        background-color: #0056b3;
      }}
      .uploaded-image, .bw-image {{
        margin-top: 20px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Image Upload and Process</h1>
      <form method="POST" enctype="multipart/form-data">
        <label for="file">Choose an image:</label>
        <input type="file" id="file" name="file" accept="image/*" required>
        <button type="submit">Upload Image</button>
      </form>
      {result}
    </div>
  </body>
</html>
"""

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    result = ''
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            img = PIL.Image.open(file_path)
            # Pass the image to the GEMINI model
            prompt = "Imagine you’re a stand-up comedian at IIT BHU, ready to entertain freshers with your wit.Your task is to roast the face in the image in front of the audience . The roast should be funny and cheeky but do not overdo it.Make sure it’s something that would make even the toughest audience crack a smile while blushing a bit"

            # Assuming model.generate_content takes a list with the prompt and image path
            response = model.generate_content([prompt, img])
            out = to_markdown(response.text)
            # out = out.data

            result = f'''
            <div class="uploaded-image">
                <h2>Uploaded Image:</h2>
                <img src="/uploads/{file.filename}" alt="Uploaded Image" width="300">
            </div>
            <div class="ROAST">
                <h2>ROAST :</h2>
                <h2>{out}</h2>
            </div>
            '''
            
    return html_template.format(result=result)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
