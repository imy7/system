import requests
import os

def fetch_and_save_proxy_data():
    """从API获取代理数据并直接保存到文件"""
    api_url = "https://ipdb.api.030101.xyz/?type=bestproxy&country=true"
    output_path = "/cmliu/proxyip.txt"
    
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 获取API数据
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        
        # 直接保存原始响应内容（文本格式）
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print(f"成功保存代理数据到 {output_path}")
        return True
        
    except Exception as e:
        print(f"获取代理数据失败: {str(e)}")
        return False

if __name__ == "__main__":
    fetch_and_save_proxy_data()
