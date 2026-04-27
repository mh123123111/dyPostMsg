import requests
import json
import random
import time
import queue
from douyin.liveMan import DouyinLiveWebFetcher
from send_chat_request import send_chat_request
product_features = [
    "极速恒温体验",
    "3秒即开即热技术，无需等待",
    "30-55℃人体工程恒温系统，杜绝忽冷忽热",
    "智能变频功率（50瓦-5500瓦），自动适应季节水温变化（夏季省电/冬季强劲）",
    "304不锈钢一体成型内胆（无缝防漏）",
    "IPX4整机防水认证（可直接淋水使用）",
    "水电分离+自动断电保护（断水/断电双重保险）",
    "零门槛安装方案",
    "免打孔设计",
    "快装接口设计（老人小孩3分钟可完成）",
    "ABS加钢化微晶防爆面板+液晶触控（0学习成本操作）",
    "待机0功耗技术（省电模式）",
    "德国变频芯片（节能30%对比传统4000瓦机型）",
    "5500瓦峰值功率（行业顶级制热效率）",
    "超行业标准服务",
    "太平洋保险承保（质量双保险）",
    "7天无理由退换",
    "终身保价承诺（买贵补差）",
    "运费险都做到链接里的",
    "颠覆性价格体系",
    "千元级品质，厂家直补价<200元",
    "省安装费（无需专业人员）",
    "省后期维护（十年免维修费）"
]




def send_comment(content):
    """
    发送评论到直播间
    :param content: 评论内容
    :return: 响应结果
    """
    data = {
        "operate_type": 2,
        "content": content
    }
    data_json = json.dumps(data, separators=(',', ':'))
    try:
        response = requests.post(
            SEND_COMMENT_URL,
            headers=SEND_COMMENT_HEADERS,
            cookies=SEND_COMMENT_COOKIES,
            params=SEND_COMMENT_PARAMS,
            data=data_json
        )
        print(f"发送评论成功: {content}")
        print(f"响应: {response.text}")
        return response
    except Exception as e:
        print(f"发送评论失败: {e}")
        return None

def process_message_with_llm(message):
    """
    处理消息与大模型交互
    注意：这里需要根据实际的大模型API进行实现
    :param message: 接收到的消息
    :return: 大模型回复
    """


    print(f"[大模型处理] 收到消息: {message}")
    # TODO: 集成大模型API
    # 示例：调用OpenAI API或其他大模型API
    # response = openai.ChatCompletion.create(...)
    # return response.choices[0].message.content
    
    # 检查是否是特殊用户名，不需要回复
    if message.get('user') == "潮流小铺琪琪分享":
        print(f"[特殊用户] 跳过回复: {message['user']}")
        return None
    
    # 使用大模型处理消息
    if message['type'] == 'chat':
        try:
            # 调用send_chat_request函数处理用户消息
            llm_response = send_chat_request(message['content'])
            return f"感谢 {message['user']} 的问题！{llm_response}"
        except Exception as e:
            print(f"大模型处理失败: {e}")
            return f"感谢 {message['user']} 的问题！我们会尽快回复您。"
    elif message['type'] == 'member':
        return f"欢迎 {message['user']} 进入直播间！"
    return "感谢您的互动！"

def run_live_room_bot():
    """
    运行直播间机器人
    - 当没有收到用户消息时，定期发送产品卖点
    - 当收到用户消息时，调用大模型处理并回复
    """
    live_id = ('')
    msg_queue = queue.Queue()
    last_activity_time = time.time()
    product_feature_interval = 30  # 发送产品卖点的时间间隔（秒）
    
    def message_callback(msg):
        """消息回调函数，将消息放入队列"""
        msg_queue.put(msg)
    
    # 初始化直播间连接
    room = DouyinLiveWebFetcher(live_id)
    room.message_callback = message_callback
    room.get_room_status()
    
    # 启动直播间连接
    import threading
    def start_room():
        room.start()
    
    thread = threading.Thread(target=start_room)
    thread.daemon = True
    thread.start()
    
    print("直播间机器人启动成功！")
    print("按Ctrl+C停止")
    
    try:
        while True:
            current_time = time.time()
            
            # 检查是否需要发送产品卖点（当长时间没有用户活动时）
            if current_time - last_activity_time > product_feature_interval:
                # 随机选择一个产品卖点
                feature = random.choice(product_features)
                send_comment(feature)
                last_activity_time = current_time
            
            # 检查是否有用户消息
            try:
                msg = msg_queue.get(timeout=1)
                last_activity_time = current_time
                
                # 处理用户消息
                print(f"收到用户消息: {msg}")
                
                # 调用大模型处理消息
                llm_response = process_message_with_llm(msg)
                
                # 发送大模型回复（如果有）
                if llm_response:
                    send_comment(llm_response)
                else:
                    print("[跳过发送] 没有生成回复")
                    
            except queue.Empty:
                # 没有消息，继续循环
                time.sleep(1)
                continue
                
    except KeyboardInterrupt:
        print("\n停止直播间机器人")
        room.stop()
        return

def test_get_room_text(self):
    """
    测试获取直播间文本消息，只输出进场msg和聊天msg，收到一条返回一条
    """
    live_id = '398157811671'
    msg_queue = queue.Queue()
    
    def message_callback(msg):
        """消息回调函数，将消息放入队列"""
        msg_queue.put(msg)
    
    room = DouyinLiveWebFetcher(live_id)
    room.message_callback = message_callback
    room.get_room_status()
    
    # 启动直播间连接
    import threading
    def start_room():
        room.start()
    
    thread = threading.Thread(target=start_room)
    thread.daemon = True
    thread.start()
    
    # 持续返回收到的消息
    try:
        while True:
            # 等待消息，超时时间10秒
            try:
                msg = msg_queue.get(timeout=10)
                print(f"返回消息: {msg}")
                yield msg
            except queue.Empty:
                print("等待消息超时，继续等待...")
                continue
    except KeyboardInterrupt:
        print("停止接收消息")
        room.stop()
        return

# 发送评论的相关参数
SEND_COMMENT_HEADERS = {}

SEND_COMMENT_COOKIES = {}

SEND_COMMENT_URL = "https://buyin.jinritemai.com/api/anchor/comment/operate_v2"

SEND_COMMENT_PARAMS = {}

if __name__ == '__main__':
    # 运行直播间机器人
    run_live_room_bot()

