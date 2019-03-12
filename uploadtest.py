from flask import Flask, make_response, request, send_file
from pydub import AudioSegment

app = Flask(__name__)

def reverseSong(song):
    return song.reverse()

@app.route('/')
def form():
    return """
            <html>
                <body>
                    <h1>Reverse Song Test</h1>
                    <form action="/reverse" method="post" enctype="multipart/form-data">
                        <input type="file" name="song" />
                        <input type="submit" />
                    </form>
                </body>
            </html>
    """

@app.route('/reverse', methods=["POST"])
def reverse():
    request_file = request.files['song']
    if not request_file:
        return "No file"
    file_contents = AudioSegment.from_mp3(request_file)
    reversed = reverseSong(file_contents)
    result = reversed.export("backwards.mp3", format="mp3")

    return send_file(result, attachment_filename="reversed.mp3")
    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=result.mp3"
    return response

if __name__ == "__main__":
    app.run()
