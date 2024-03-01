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


@app.route("/api/v1/library/울산대학교", methods=['GET'])
def library():
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
    return jsonify(response)

@app.route("/api/v1/announcement/울산대학교",methods=['GET'])
def announcement():
    list = []

    response = requests.get('https://www.ulsan.ac.kr/kor/CMS/Board/Board.do?mCode=MN113')

    if response.status_code == 200:
        print('성공')
    else:
        print('실패')
    soup = bs(response.text, "html.parser")

    elements = soup.select('tbody > tr > td.subject > p > a')

    for a in elements:
        response = requests.get('https://www.ulsan.ac.kr/kor/CMS/Board/Board.do'+a['href'])

        soup = bs(response.text, "html.parser")

        top = soup.select_one('h4.vtitle')
        content = soup.select_one('#boardContents')

        topList = top.get_text().split(']',maxsplit=1)

        type = topList[0].strip()[1:]
        title = topList[1].strip()
        
        list.append({
            "title":title,
            "type":type,
            "content":str(content)
        })
    
    response = {
        "isSuccess": True,
        "code": "COMMON200",
        "message": "성공입니다",
        "result":{
            "list":list
        }
    }
    return jsonify(response)
    


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8090)