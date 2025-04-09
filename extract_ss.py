import requests
import base64
import json
import pyaes
import binascii
from datetime import datetime
import os

# 美化输出
print(" H͜͡E͜͡L͜͡L͜͡O͜͡ ͜͡W͜͡O͜͡R͜͡L͜͡D͜͡ ͜͡E͜͡X͜͡T͜͡R͜͡A͜͡C͜͡T͜͡ ͜͡S͜͡S͜͡ ͜͡N͜͡O͜͡D͜͡E͜͡")
print("𓆝 𓆟 𓆞 𓆟 𓆝 𓆟 𓆞 𓆟 𓆝 𓆟 𓆞 𓆟")
print("Author : 𝐼𝑢")
print(f"Date : {datetime.today().strftime('%Y-%m-%d')}")
print("Version: 1.1 (with file save & SSR/V2Ray support)")
print("𓆝 𓆟 𓆞 𓆟 𓆝 𓆟 𓆞 𓆟 𓆝 𓆟 𓆞 𓆟")

# API请求参数
url = 'http://api.skrapp.net/api/serverlist'
headers = {
    'accept': '/',
    'accept-language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
    'appversion': '1.3.1',
    'user-agent': 'SkrKK/1.3.1 (iPhone; iOS 13.5; Scale/2.00)',
    'content-type': 'application/x-www-form-urlencoded',
    'Cookie': 'PHPSESSID=fnffo1ivhvt0ouo6ebqn86a0d4'
}
payload = {
    'data': '4265a9c353cd8624fd2bc7b5d75d2f18b1b5e66ccd37e2dfa628bcb8f73db2f14ba98bc6a1d8d0d1c7ff1ef0823b11264d0addaba2bd6a30bdefe06f4ba994ed'
}

# AES密钥和IV
key = b'65151f8d966bf596'
iv = b'88ca0f0ea1ecf975'

# AES解密函数
def decrypt_aes(data, key, iv):
    aes = pyaes.AESModeOfOperationCBC(key, iv=iv)
    decrypted = b''.join([aes.decrypt(data[i:i+16]) for i in range(0, len(data), 16)])
    padding_len = decrypted[-1]
    return decrypted[:-padding_len]

# 保存到文件
def save_links_to_file(links, filename='ss_links.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        for link in links:
            f.write(link + '\n')
    print(f"\n✅ 已保存 {len(links)} 条 SS 链接到：{os.path.abspath(filename)}")

# 生成 SS 链接
def generate_ss_link(password, ip, port, title):
    ss_info = f"aes-256-cfb:{password}@{ip}:{port}"
    ss_encoded = base64.b64encode(ss_info.encode('utf-8')).decode('utf-8')
    return f"ss://{ss_encoded}#{title}"

# SSR/V2Ray扩展（可添加更多格式）
def generate_other_format(item):
    # TODO: 实现 SSR/V2Ray 解析（需要格式说明）
    return None  # 示例返回空

# 请求 + 解密 + 输出
try:
    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()
    hex_data = response.text.strip()
    encrypted_bytes = binascii.unhexlify(hex_data)
    decrypted_bytes = decrypt_aes(encrypted_bytes, key, iv)
    json_data = json.loads(decrypted_bytes)

    ss_links = []

    print("╔══════════════════════════════╗")
    print("║        SS 链接如下：         ║")
    print("╚══════════════════════════════╝")

    for item in json_data.get('data', []):
        ss_link = generate_ss_link(item['password'], item['ip'], item['port'], item['title'])
        print(ss_link)
        ss_links.append(ss_link)

        # 可选：扩展 SSR/V2Ray 支持（需进一步格式）
        # other_link = generate_other_format(item)
        # if other_link:
        #     print(other_link)
        #     ss_links.append(other_link)

    # 保存链接到文件
    save_links_to_file(ss_links)

except requests.RequestException as e:
    print(f"[ERROR] 请求失败: {e}")
except (binascii.Error, json.JSONDecodeError, KeyError) as e:
    print(f"[ERROR] 数据解析失败: {e}")
