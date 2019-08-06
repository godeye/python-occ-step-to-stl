from flask import Flask, request, send_file, after_this_request
import urllib
from step2stl import read_step, write_stl
import os
import time
import requests
app = Flask(__name__)

# api = Api(app)

@app.route('/')
def convert_to_stl():
    url = request.args.get('url')
    if not url:
        return {'fail': 'not valid url'} 
    print(url)
    file_name = url.split('/')[-1]
    print(file_name)
    # step_file = urllib.urlretrieve(url)
    r = requests.get(url, verify=False)
    path = 'files/{}'.format(file_name)
    # urllib.urlretrieve(url, path)
    # step_file = r.content
    # file_id = 'files/' + str(int(time.time())) + '.step'
    # with open('files/%s'.format(file_name), 'wb') as output:
        # output.write(step_file.read())
    print(path)
    with open(path, 'wb') as f:
        f.write(r.content)
    shape = read_step(path)
    file_output = 'files/output/{}'.format(file_name.replace('.step','.stl').replace('.STEP', '.stl'))
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