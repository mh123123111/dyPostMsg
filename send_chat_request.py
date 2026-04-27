import requests
import json
import re

def send_chat_request(content):
    # 1. 配置请求基本信息
    url = "http://127.0.0.1:3000/api/chat/completions"

    # 请求头（包含Bearer Token认证）
    headers = {
        "Authorization": "",
        "Content-Type": "application/json"
    }

    # 请求体数据
    data = {
        "model": "msg2",
        "messages": [
            {"role": "user", "content": content}
        ],
        "stream": False
    }

    try:
        # 2. 发送POST请求
        response = requests.post(
            url=url,
            headers=headers,
            json=data,  # 自动将字典转为JSON格式
            timeout=30  # 设置超时时间，避免无限等待
        )

        # 3. 检查请求是否成功
        response.raise_for_status()  # 如果状态码不是200，抛出异常

        # 4. 解析响应数据
        response_data = response.json()

        # 5. 提取目标结果："304不锈钢内胆 [1]"
        # 从choices列表中找到第一个元素的message.content
        result = response_data["choices"][0]["message"]["content"]
        cleaned_result = re.sub(r'\s*\[\d+\]$', '', result)
        print(cleaned_result)  # 输出：304不锈钢内胆 [1]
        return cleaned_result

    except requests.exceptions.RequestException as e:
        # 捕获所有请求相关的异常（超时、连接失败、状态码错误等）
        print(f"请求发生错误：{e}")
        return None
    except KeyError as e:
        # 捕获响应数据结构异常（比如字段不存在）
        print(f"响应数据解析失败，缺少字段：{e}")
        print(f"完整响应数据：{json.dumps(response_data, ensure_ascii=False, indent=2)}")
        return None


# 执行函数
if __name__ == "__main__":
    send_chat_request()