from flask import Flask, request, send_file, after_this_request
import urllib
from step2stl import read_step, write_stl
import os
import time
import requests
import urllib

app = Flask(__name__)

# api = Api(app)

@app.route('/', methods=['POST'])
def convert_to_stl():
    content = request.json
    url = content['url']
    if not url:
        return {'fail': 'not valid url'} 

    print('url s3')
    print(url)
    print(urllib.unquote(url))
    file_name = url.split('/')[-1]
    print(file_name)
    # step_file = urllib.urlretrieve(url)
    r = requests.get(url)
    path = 'input.step'
    # urllib.urlretrieve(url, path)
    # step_file = r.content
    # file_id = 'files/' + str(int(time.time())) + '.step'
    # with open('files/%s'.format(file_name), 'wb') as output:
        # output.write(step_file.read())
    print('path')    
    print(path)
    with open('input.step', 'wb') as f:
        f.write(r.content)
    shape = read_step('input.step')
    file_output = 'output.stl'
    print('generating file')
    write_stl(shape, file_output)
    print('file generated')
    # remove files

    @after_this_request
    def remove_files(response):
        try:
            os.remove(path)
            os.remove(file_output)
        except Exception as err:
            app.logger.error('Error removing files')
        return response
    return send_file(file_output, as_attachment=True)
    # return {'hello': 'world'} 

# class Convert2Stl(Resource):
#     def get(self):

#         return {'hello': 'world'} 

# api.add_resource(Convert2Stl, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')