import flask
import docxlib
import io
import os

app = flask.Flask(__name__, static_url_path='')


@app.route('/api/get_changes_metadata', methods=['POST'])
def get_changes_metadata():
    file = flask.request.files['file']
    metadata = docxlib.get_changes_metadata(file)
    return flask.jsonify(metadata)


@app.route('/api/remove_timestamps', methods=['POST'])
def remove_timestamps():
    docx = flask.request.files['file']
    b = io.BytesIO()
    docxlib.remove_comment_timestamps(docx, b)
    b.seek(0)
    filename, ext = os.path.splitext(docx.filename)
    newname = filename + '-notimestamps' + ext
    return flask.send_file(
        b,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        as_attachment=True,
        attachment_filename=newname)


if __name__ == "__main__":
    app.run()
