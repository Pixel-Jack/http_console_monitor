FILE_NAME = 'this_app.log'

def write(data):
    with open(FILE_NAME, 'a') as f:
        f.write(str(data))