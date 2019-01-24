from flask import Flask, jsonify, send_file
import os
import json

app = Flask(__name__)


def getDirect(path, ch):
    directories = {'name': os.path.basename(path)}
    directories['path'] = path.replace('\\','/')
    if os.path.isdir(path):
        directories['type'] = 'directory'
        if ch:
            directories['children'] = [getDirect(os.path.join(path,x), False) for x in os.listdir(path)]
    else:
        directories['type'] = 'file'
    return directories


@app.route('/')
def rules():
    r = ['/root  -  root ', ' /directory/<path:path> - get list of files in the specified path' ,' /new/<path:path>  -  new directory ',' /delete/<path:path>  -  delete file or empty directories ', ' /get/<path:path>  -  download file']
    return jsonify(r);


@app.route('/root')
def root():
    return json.dumps(getDirect('.', True))

#get list of files in the specified path
@app.route('/directory/<path:path>')
def directory(path):
    if os.path.exists(path):
        return json.dumps(getDirect(path, True))

'''@app.route('/directory/<path:path>')
def directory(path):
    if os.path.exists(path):
        children = [getDirect(os.path.join(path, x), False) for x in os.listdir(path)]
        return json.dumps(children)
    else:
        return jsonify('Directory ' + path + ' not found')'''

#creat new directory
@app.route('/new/<path:path>')
def new(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return jsonify('Create  directory ' + path)
    else:
        return jsonify('Directory ' + path + ' already exists')

#delete file or empty directory
@app.route('/delete/<path:path>')
def delete(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
            return jsonify("File " + path + " was Deleted")
        elif os.path.isdir and os.listdir:
            return jsonify("Directory " + path + " not empty")
        elif os.path.isdir(path):
            os.rmdir(path)
            return jsonify("Directory " + path + " was Deleted")
    else:
        return jsonify('The path does not exist')

#download file
@app.route('/get/<path:path>')
def get(path):
    if  os.path.exists(path):
        return send_file(os.path.abspath(path), as_attachment=True)


if __name__ == '__main__':
    app.run()