import os
from datetime import datetime
from flask import Flask, request, render_template, send_from_directory,session,jsonify
from flask_session import Session
import json
from main import infer_by_web
from SpellChecker import correct_sentence
__author__ = 'Samiksha'

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
APP_ROOT = os.path.dirname(os.path.abspath(__file__)) # project abs path



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload_page", methods=["GET"])
def upload_page():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():
    # folder_name = request.form['uploads']
    result='Not Detected'
    target = os.path.join(APP_ROOT, 'static/')
    print('file path is :',target)
    if not os.path.isdir(target):
        os.mkdir(target)
    print( 'recieved file: ',request.files.getlist("file"))
    option = request.form.get('optionsPrediction')
    print("Selected Option:: {}".format(option))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png"):
            print("File supported moving on...")
        else:
            render_template("Error.html", message="Files uploaded are not supported...")
        savefname = datetime.now().strftime('%Y-%m-%d_%H_%M_%S') + "."+ext
        destination = "/".join([target, savefname])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)
        result = predict_image(destination, option)
        corrected = correct_sentence(result)
        print("Prediction: ", result)
    session['result']=result
    #render_template('res_include.html',result=result)
    #return ('', 204)

    #return json.dumps(result)
    #return  render_template("index.html", result=result, image_name=savefname)
    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("complete.html", image_name=savefname, result=result, corrected= corrected)


def predict_image(path, type):
    print(path)
    return infer_by_web(path, type)


if __name__ == "__main__":
    app.run(port=4555, debug=True)