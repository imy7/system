import requests
import os
from concurrent.futures import ThreadPoolExecutor

# API配置列表
APIS = [
    {
        "name": "bestcf_api",
        "url": "https://ipdb.api.030101.xyz/?type=bestcf&country=true",
        "format": "ip#country"  # 假设返回格式是 "ip#country"（如 "1.1.1.1#US"）
    },
    {
        "name": "cloudflare1_api",
        "url": "https://addressesapi.090227.xyz/CloudFlareYes",
        "format": "ip_only"  # 假设返回纯IP列表（如 "1.1.1.1"）
    },
    {
        "name": "cloudflare2_api",
        "url": "https://addressesapi.090227.xyz/ip.164746.xyz",
        "format": "ip_only"  # 假设返回纯IP列表
    }
]

OUTPUT_FILE = "cmliu/ipv4.txt"
DEFAULT_COUNTRY_CODE = "UN"  # 默认国家代码（如果API未提供）

def parse_api_response(api_name, response_text, format_type):
    """解析不同API的响应格式"""
    parsed_data = []
    
    if format_type == "ip#country":
        # 格式示例: "1.1.1.1#US"（直接使用）
        for line in response_text.splitlines():
            line = line.strip()
            if line and "#" in line:
                parsed_data.append(line)
    
    elif format_type == "ip_only":
        # 格式示例: "1.1.1.1"（补上默认国家代码）
        for line in response_text.splitlines():
            ip = line.strip()
            if ip:
                parsed_data.append(f"{ip}#{DEFAULT_COUNTRY_CODE}")
    
    return parsed_data

def fetch_api_data(api):
    """获取单个API的数据并解析"""
    try:
        print(f"🔍 正在获取 {api['name']} 数据...")
        response = requests.get(api["url"], timeout=15)
        response.raise_for_status()
        
        # 解析响应数据
        parsed_data = parse_api_response(api["name"], response.text, api["format"])
        print(f"✅ {api['name']} 获取成功，共 {len(parsed_data)} 条数据")
        return parsed_data
    except Exception as e:
        print(f"⚠️ {api['name']} 获取失败: {str(e)}")
        return []

def process_and_save_data():
    """主处理函数"""
    # 并行获取所有API数据
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(fetch_api_data, APIS))
    
    # 合并所有数据并去重（基于IP部分）
    all_records = []
    seen_ips = set()
    
    for records in results:
        for record in records:
            ip = record.split("#")[0]  # 提取IP部分
            if ip not in seen_ips:
                seen_ips.add(ip)
                all_records.append(record)
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    # 写入文件（覆盖模式）
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(all_records))
        print(f"🎉 数据处理完成，共保存 {len(all_records)} 条记录到 {OUTPUT_FILE}")
        return True
    except Exception as e:
        print(f"❌ 文件保存失败: {str(e)}")
        return False

if __name__ == "__main__":
    success = process_and_save_data()
    if not success:
        exit(1)
