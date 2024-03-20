from flask import Flask, request, jsonify  
  
app = Flask(__name__)  
  
@app.route('/')
def hello():
    return 'Hello world！ Flask  Docker！！'

# 假设你有一个函数可以根据城市名查询天气  
def get_weather_by_city(city_name):  
    # 这里只是模拟数据，实际情况你可能需要从API或数据库中获取  
    weather_data = {  
        '北京': {'temperature': 20, 'humidity': 50},  
        '上海': {'temperature': 22, 'humidity': 60},  
        '广州': {'temperature': 25, 'humidity': 70},  
    }  
    return weather_data.get(city_name, 'Unknown city')  
  
@app.route('/weather/<city>')  
def weather(city):  
    weather_info = get_weather_by_city(city)  
    if isinstance(weather_info, dict):  
        return jsonify(weather_info)  
    else:  
        return jsonify({'error': 'City not found'}), 404  
  
if __name__ == '__main__':  
    app.run(debug=True)
