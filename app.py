import subprocess
from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        print(request.json)
        file_number = request.json.get('file_number')
        file_dict = {
            '1': 'file1.png',
            '2': 'file2.png',
            '3': 'file3.png',
            '4': 'file4.png',
            '5': 'file5.png',
        }
        file_name = file_dict.get(str(file_number), 'default.png')
        subprocess.run(['open', file_name], check=True)
        return 'success', 200
    else:
        abort(400)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
