import openai
from flask import Flask, request
from flask_cors import CORS
import psycopg2


app = Flask(__name__)

CORS(app)
openai.api_key = "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"


# 定义一个函数生成 ChatGPT 的回复

def generate_response(prompt, response=None):

    completions = openai.Completion.create(
        engine="text-davinci-003",  # 指定使用的引擎名称
        prompt=prompt,  # API 请求的提示信息
        max_tokens=1024,  # API 响应的最大令牌数
        n=1,  # API 请求的完成数
        stop="",  # API 响应的终止标志
        temperature=0.5,  # API 请求的温度参数，越低越可预测
    )

    # 从 API 响应中取得回复

    message = completions.choices[0].text.strip()

    return message


@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    input_text = data['input']
    context = input_text
    response = generate_response(context)
    conn = psycopg2.connect(
        host="localhost",
        database="chatbot",
        user="postgres",
        password="@you0331"
    )
    cur = conn.cursor()
    # 将对话存入数据库
    cur.execute("INSERT INTO chat_history (prompt, response) VALUES (%s, %s)", (context, response))
    # 提交更改
    conn.commit()
    # 关闭游标和连接
    cur.close()
    conn.close()

    return response


if __name__ == '__main__':
    app.run()
