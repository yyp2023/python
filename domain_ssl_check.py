import ssl
import OpenSSL
import socket
import requests
from datetime import datetime
from urllib3.contrib import pyopenssl
import  os
'''
该脚本主要是获取可以通过request请求有返回的域名清单，
当前目录下需要存在domain_list.txt清单，文档内容为域名前缀，执行结果的域名前缀放入domain_result.txt文件
比如
xx1
xx2
xx3
'''
def get_ssl_certificate(domain):
    try:
        certificate = pyopenssl.ssl.get_server_certificate((domain, 443))
        data = pyopenssl.OpenSSL.crypto.load_certificate(pyopenssl.OpenSSL.crypto.FILETYPE_PEM, certificate)
        expire_time = datetime.strptime(data.get_notAfter().decode()[0:-1], '%Y%m%d%H%M%S')
        expire_days = (expire_time - datetime.now()).days
        create_time = datetime.strptime(data.get_notBefore().decode()[0:-1], '%Y%m%d%H%M%S')
        # c = data.get_issuer()
        components = data.get_subject().get_components()
        components = {
            i[0].decode('utf-8'): i[1].decode('utf-8')
            for i in components
        }
        # return True, 200, {
        #     **components,
        #     'domain': domain,
        #     'expire_time': str(expire_time),
        #     'expire_days': expire_days,
        #     'create_time': str(create_time)
        # }
        info = domain  + "#" + str(expire_time) + "#" + str(expire_days) + "#" + components['CN']
        return info
    except Exception as e:
        return False, 500, str(e)


if __name__ == '__main__':
    yuming = ".yingxiong.com"
    with open("domain_list.txt", 'r') as file:
        lines = file.readlines()

    # domain_list = []
    if os.path.exists("domain_result.txt"):
        os.remove("domain_result.txt")
    for i in lines:
        domain_tmp = i.strip('\n')
        domain = "https://" + domain_tmp  + yuming
        try:
            res = requests.get(domain,timeout=1)
        except Exception as e:
            res.status_code = "xx"
        if res.status_code != "xx":
            domain_q = domain_tmp
            print(domain_q)
            with open('domain_result.txt', 'a') as file:
                domain = domain_q + yuming
                print(get_ssl_certificate(domain))
                result = str(get_ssl_certificate(domain)) + "\n"
                file.write(result)

            # domain_list.append(domain_q)

    # with open('domain_result.txt','a') as file:
    #     for domain_i in domain_list:
    #         domain = domain_i + yuming
    #         print(get_ssl_certificate(domain))
    #         file.write(get_ssl_certificate(domain))
    #




# get_ssl_expire_date(domain)

