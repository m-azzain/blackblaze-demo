
import base64
from flask import Flask, render_template, request
from flask_cors import CORS
from blackblaze import blackblaze_file_write
from blackblaze import blackblaze_file_read
app = Flask(__name__)
CORS(app, resources={r"/upload": {"origins": "*"}})


@app.get("/")
def index_get():
    return render_template("base.html")


@app.post("/upload")
def upload():
    files = request.get_json().get("files")
    for file in files:
        blackblaze_file_write(base64.b64decode(file['data'] or b''), file['name'])
        # Write it again, to check that it won't be uploaded twice
        # the logic to prevent multi writing of the same file is implemented in the blackblaze_file_write function
        blackblaze_file_write(base64.b64decode(file['data'] or b''), file['name'])
        # Download to make sure that the file can be read in the same request
        download = blackblaze_file_read(file['name'])
        with open(file['name'], 'wb') as f:
            f.write(download)
    return "Have been uploaded successfully!"


if __name__ == "__main__":
    app.run(debug=True)