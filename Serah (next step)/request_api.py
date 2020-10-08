import requests

url = "http://localhost:9000/prediction"
filename = 'C:\\Users\\Juvin\\Desktop\\ITC_Final_Project\\ITC_FinalProject_Gender_Voice_Recognition\\Serah (next ' \
           'step)\\ENG_M (1).wav'


def read_file(filename_):
    with open(filename_, 'rb') as _file:
        data = _file.read()
        return data


headers = {'authorization': "1234",
           'Content-Type': 'audio/wave'}

response = requests.post(url, headers=headers, files={'file':read_file(filename)})

print(response.text.encode('utf8'))
