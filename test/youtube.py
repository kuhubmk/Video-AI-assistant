import yt_dlp
import whisper
import requests
import json
import os
import torch

# 确保 ffmpeg 和 ffprobe 路径在环境变量中
ffmpeg_path = 'D:\\ffmpeg-n7.0-latest-win64-gpl-7.0\\ffmpeg-n7.0-latest-win64-gpl-7.0\\bin'  # 替换为你的 ffmpeg 路径
os.environ['PATH'] += os.pathsep + ffmpeg_path

print("Current PATH:", os.environ['PATH'])

# 百度API的配置
API_KEY = "7VIE3vD5hS9m15kURpKUB5ky"
SECRET_KEY = "XG1LvU5LUC82S9t2mKDN1ATKywHkXvyW"

def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token
    """
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}"
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers)
    response_data = response.json()
    if 'access_token' in response_data:
        return response_data['access_token']
    else:
        raise Exception("获取access_token失败: ", response_data)

# 下载YouTube视频音频并转换为wav格式
def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloaded_audio.%(ext)s',
        'ffmpeg_location': ffmpeg_path  # 添加ffmpeg路径
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # 返回下载后的音频文件路径
    return 'downloaded_audio.wav'

# 使用Whisper进行语音转文本
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# 使用Whisper进行语音转文本，并利用CUDA加速
def transcribe_audio(audio_path):
    try:
        print(f"开始转录音频文件: {audio_path}")
        model = whisper.load_model("small", device=device)  # 加载Whisper模型，并指定设备为CUDA
        print("Whisper模型加载成功")
        result = model.transcribe(audio_path)
        transcript = result["text"]
        return transcript
    except Exception as e:
        print(f"音频转录失败: {e}")
        return ""

# 使用百度文心大模型进行文本总结
def summarize_text_baidu(text):
    try:
        access_token = get_access_token()
        url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={access_token}"
        
        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": f"阅读文字内容，保留文章的原有文字和给它进行一个主题分段落，不要删减文字内容：\n\n{text}"
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        result = response.json()
        print("百度API响应: ", result)  # 调试输出完整的API响应
        if 'result' in result:
            summary = result['result']
            return summary
        else:
            print("百度API返回的响应中没有'result': ", result)
            return "总结失败"
    except Exception as e:
        print(f"文本总结失败: {e}")
        return "总结失败"

# 创建视频笔记
def create_video_notes(video_url):
    try:
        audio_path = download_audio(video_url)
        print(f"音频文件已下载: {audio_path}")
        
        transcript = transcribe_audio(audio_path)
        if not transcript:
            print("转录文本生成失败")
            return None
        
        summary = summarize_text_baidu(transcript)
        print(f"文本总结已完成: {summary}")
        
        return {
            "video_url": video_url,
            "transcript": transcript,
            "summary": summary
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # 输入视频URL
    video_url = "https://www.youtube.com/watch?v=R2sXT6m8NBM"
    
    # 生成笔记
    notes = create_video_notes(video_url)
    
    if notes:
        # 打印笔记
        print(f"Video URL: {notes['video_url']}")
        print(f"Transcript: {notes['transcript']}")
        print(f"Summary: {notes['summary']}")
    else:
        print("Failed to create video notes.")
