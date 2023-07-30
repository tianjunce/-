from flask import Flask, request, jsonify, render_template
from utility_em import *

# 创建 Flask 应用
app = Flask(__name__)

# # 模拟超额死亡数据（假设已经准备好了）
# # 这里示例数据为一个简单的字典，key 为国家名称，value 为超额死亡数据
# excess_deaths_data = {
#     'USA': [100, 200, 150, 300, 250],   # 假设有 5 个数据点
#     'UK': [50, 80, 70, 90, 110],
#     '美国': [100, 200, 150, 300, 250], 
#     # 其他国家的数据...
# }

data1=data_load()



# 定义根 URL 路由和对应的视图函数
@app.route('/')
def index():
    return render_template('index.html')

# 后端路由：接收前端发送的国家名称参数，返回超额死亡数据
@app.route('/get_excess_deaths', methods=['GET'])
def get_excess_deaths():
    # 获取前端发送的国家名称参数
    country = request.args.get('country')

    # 查询超额死亡数据
    data = data_gen(data1,country,web=1)
    
    #print(country,data)
    # 将数据转换成 JSON 格式，并作为 HTTP 响应返回给前端
    return jsonify(data)

if __name__ == '__main__':
    # 启动 Flask 应用
    app.run()
