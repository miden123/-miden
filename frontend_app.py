from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json, os

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"

# 初始化 JSON 文件
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)

# 用户提交页面
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# 添加用户数据接口
@app.route("/add", methods=["POST"])
def add_data():
    data = request.json
    if not data:
        return jsonify({"message": "提交数据为空"}), 400

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)

    users.append({
        "orderNo": data.get("orderNo"),
        "name": data.get("name"),
        "age": data.get("age"),
        "city": data.get("city")
    })

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

    return jsonify({"message": "数据添加成功!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
