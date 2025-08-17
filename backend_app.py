from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import json, os

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"

# 后台管理页面
@app.route("/admin")
def admin():
    return send_from_directory(".", "admin.html")

# 列出所有用户
@app.route("/list")
def list_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)
    return jsonify(users)

# 后台添加用户
@app.route("/add", methods=["POST"])
def add_user():
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

    return jsonify({"message": "添加成功"})

# 删除指定用户
@app.route("/delete/<int:index>", methods=["DELETE"])
def delete_user(index):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)

    if 0 <= index < len(users):
        users.pop(index)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)
        return jsonify({"message": "删除成功"})
    return jsonify({"message": "删除失败"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
