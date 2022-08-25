from flask import Flask, render_template, jsonify, request
from geopy.geocoders import Nominatim
from main import recommand # CBF 함수 가져오기
import random

def geocoding_reverse(lat_lng_str):
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    address = geolocoder.reverse(lat_lng_str)
    return address

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get_data', methods=['GET'])


def get_info():
    latitude_receive = request.args.get('latitude_give')
    longitude_receive = request.args.get('longitude_give')
    vector_receive = request.args.get('vector_give').split(",")
    distance_receive = int(request.args.get('distance_give'))

    address = geocoding_reverse(f"{latitude_receive}, {longitude_receive}")[0].split(",")[::-1][2:4]
    recommend_result = recommand(latitude_receive,longitude_receive,distance_receive,vector_receive)

    # 결과가 없을 경우
    if type(recommend_result) == str:
        return jsonify({'msg': "주변에 맛집이 없습니다 ㅠ 탐색범위를 넓혀주세요!", "res": "주변에 맛집이 없습니다 ㅠ 탐색범위를 넓혀주세요!"})

    return jsonify({'msg': f"{address[0]}{address[1]}  맛집 추천이 도착했습니다!\n      <<팝업 광고 위치>> ", "res": recommend_result})
    
@app.route('/get_vector', methods=['GET'])
def get_vector():
    vector_receive = request.args.get('vector')
    vector_receive = vector_receive.split(',') # string to list
    #vector_receive 정보를 받아 3개를 추출 후 보내기
    choicelist = random.sample(vector_receive, k=3)
    return jsonify({'msg': "취향 반영 완료!", "res": choicelist})

# def get_user_vector():
if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)
