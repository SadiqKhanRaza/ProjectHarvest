import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/UploadFolder'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    flash('allowed   file')
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file & allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return """
    <!DOCTYPE html>
<html lang="en">
<head>
    <title>Crop Harvestors</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <style>
               html {
               background: url(images.crop) no-repeat center fixed;
               background-size: cover;
               }

        *{
            box-sizing: border-box;
        }
        h2.double{outline-style: double;}
        body{
                         font-family: Arial,Helvetica,sans-serif;
        }
        p.oblique{
            font-style: oblique;
        }
p {
  font-size: 25px;
}
        header{
            background-color: #666;
            padding: 30px;
            text-align: center;
            font-size: 35px;
            color: white;
        }
               .center {
               text-align: center;
               }
    </style>
</head>
<header>
    <h2>Welcome!</h2>
</header>
<h2 class="double", style="text-align:center;">Identification Of Crops For Harvesting</h2>
<p style="color: black;">hgfdhfghfghgfHarvesting is the act of removing a crop from where it was growing and moving it to a more secure location for processing, consumption, or storage. Some root crops and tree fruit can be left in the field or orchard and harvested as needed, but most crops reach a period of maximum quality that is, they ripen or mature and will deteriorate if left exposed to the elements. While the major factor determining the time of harvest is the maturity of the crop, other factors such as weather, availability of harvest equipment, pickers, packing and storage facilities, and transport are important considerations.</p>
<div class="center">
<form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
<h2>Result After Processing</h2>
<form action="/action_page.php">
Look Below:<br>
    <input type="text" name="Result">
    <br>
</form>
</div>
</body>
</html>

    """


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=False)
