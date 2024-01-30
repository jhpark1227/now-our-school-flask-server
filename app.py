from flask import Flask, request, json, jsonify
import requests
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup as bs
load_dotenv()

app = Flask(__name__)

@app.route("/test", methods=['GET'])
def test():

    response = {
        "result": "ok"
    }
    return jsonify(response)


@app.route("/api/v1/library", methods=['GET'])
def library():
    university = request.args.get('university')

    if university=='울산대학교':
        session = requests.Session()

        login_data = {
            'username': os.getenv('USERNAME'),
            'password': os.getenv('PASSWORD')
        }
        response = session.post(os.getenv('LOGIN_URL'), data=login_data)

        if response.status_code == 200:
            print('로그인 성공')
        else:
            print('로그인 실패')

        response = session.get(os.getenv('CRAWLING_URL'))
        soup = bs(response.text, "html.parser")

        elements = soup.select('#table_board_list > tbody > tr > td')

        for element in elements:
            print(element.get_text().strip())

        response = {
            "isSuccess": True,
            "code": "COMMON200",
            "message": "성공입니다",
            "result": {
                "list": [
                    {
                        "name" : elements[0].get_text().strip(),
                        "total": int(elements[1].get_text().strip()),
                        "current": int(elements[2].get_text().strip()),
                        "percent": elements[3].get_text().strip(),
                        "status": elements[4].get_text().strip()
                    },
                    {
                        "name" : elements[6].get_text().strip(),
                        "total": int(elements[7].get_text().strip()),
                        "current": int(elements[8].get_text().strip()),
                        "percent": elements[9].get_text().strip(),
                        "status": elements[10].get_text().strip()
                    },
                    {
                        "name" : elements[12].get_text().strip(),
                        "total": int(elements[13].get_text().strip()),
                        "current": int(elements[14].get_text().strip()),
                        "percent": elements[15].get_text().strip(),
                        "status": elements[16].get_text().strip()
                    }
                ]
            }
        }
    else :
        response = {
            "isSuccess": False,
            "code": "COMMON400",
            "message": "결과가 존재하지 않습니다."
        }
    return jsonify(response)



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8090)