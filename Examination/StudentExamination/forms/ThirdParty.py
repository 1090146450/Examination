import requests
import datetime, re


def get_kd(dh):
    """获取快递编码"""
    data = [
        r"^([GA]|[KQ]|[PH]){2}[0-9]{9}([2-5][0-9]|[1][1-9]|[6][0-5])$|^[99]{2}[0-9]{11}$|^[96]{2}[0-9]{11}$|^[98]{2}[0-9]{11}$",
        r"^[0-9]{8,10}$|^\\d{15,}[-\\d]+$",
        r"^[A-Za-z0-9]{11,20}$",
        r"^[A-Za-z0-9]{12,15}$",
        r"^[A-Za-z0-9]{4,35}$",
        r"^(3(([0-6]|[8-9])\\d{8})|((2|4|5|6)\\d{9})|(7(?![0|1|2|3|4|5|7|8|9])\\d{9})|(8(?![2-9])\\d{9})|(2|4)\\d{11})$",
        r"^[0-9]{12}$|^[0-9]{14}$|^[0-9]{15}$",
        r"^[0-9]{12,15}$"]
    kdbm = {"ems": 3011, "debangwuliu": 190174, "jt": 191143,
            "jd": 191121, "shunfeng": 190766, "yuantong": 190157,
            "zhongtong": 190455, "yunda": 190341, }
    for i in data:
        re1 = re.compile(i)
        if re1.fullmatch(dh):
            now = datetime.datetime.now()
            timestamp = now.timestamp()
            re1 = re.compile(r".*\"(.*?)\".")
            params = {
                "Content-Type": "application/javascript; charset=utf-8",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Accept": "*/*",
                "Cookie": "BIDUPSID=A412AD29217981C3265D94D4BC00B823; PSTM=1697633315;"
                          " BAIDUID=A412AD29217981C33A7B969011876766:SL=0:NR=10:FG=1; BDUSS=216NGhLdk43Nnp3UlVKOWRnUVZWYlJ1UGJnLXNsMmIxM0hJbi1JazNhVGJvMkpsRVFBQUFBJCQAAAAAAAAAAAEAAAAxee5Mx8DM4tChxNzK1gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANsWO2XbFjtld; "
                          "BDUSS_BFESS=216NGhLdk43Nnp3UlVKOWRnUVZWYlJ1UGJnLXNsMmIxM0hJbi1JazNhVGJvMkpsRVFBQUFBJCQAAAAAAAAAAAEAAAAxee5Mx8DM4tChxNzK1gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANsWO2XbFjtld; newlogin=1; MCITY=-132%3A131%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=39633_39647_39664_39688_39676_39678_39712_39736_39738_39753; BA_HECTOR=21a5aka1al858k8h2l058h0l1ildhde1q; ZFY=877LN7i:Ah37gzwQu42Ih69pLqFAcPNIuRoG8DKEjDrk:C; BAIDUID_BFESS=A412AD29217981C33A7B969011876766:SL=0:NR=10:FG=1; delPer=0; PSINO=2; ab_sr=1.0.1_ZDAxMmRiYTBiODBmMTFlNmQ3MjE2ZjAxZWQwMzg3ZTk1OWI4ZmY5OGM1N2MwZWY1MWUzM2M2ODcyNWJlODFkMWVmNWEwNmM3ODFkYjkxYjJlMmQ5MmJlMWJiOTEzOGVjNGU3NmEzNDE0MDc1YWUwOTdiMDNjYjc3OTEwZjcwNGIyNDI2OTYzZDRjYzM0NmIyNWI0NmRkYmI5NDAzMDk1MzE2MWY0YmZiZGU1NThmODBlNTI1ODYyMzg4NjVhMWQ3; RT='z=1&dm=baidu.com&si=271667d6-810f-4d97-a708-498924d57601&ss=lp1ys7d4&sl=1&tt=6fv&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=78p&ul=7xd&hd=7xx'; BCLID=7669815110825854193; BCLID_BFESS=7669815110825854193; BDSFRCVID=E0_OJeC62mZvLfcqousbKwLlyTUNiXvTH6ao36BEy_tFhGAHAEACEG0PFx8g0KubVwkKogKK0mOTHv-F_2uxOjjg8UtVJeC6EG0Ptf8g0x5; "
                          "BDSFRCVID_BFESS=E0_OJeC62mZvLfcqousbKwLlyTUNiXvTH6ao36BEy_tFhGAHAEACEG0PFx8g0KubVwkKogKK0mOTHv-F_2uxOjjg8UtVJeC6EG0Ptf8g0x5; "
                          "H_BDCLCKID_SF=tbC8VCDKJKD3H48k-4QEbbQH-UnLq5Q33gOZ04n-ah058UcSXnQoBpFpypJr2ncbBDrP0Pom3UTKsq76Wh35K5tTQP6rLf5eLRc4KKJxbP8aKJbH5tK-M6JQhUJiB5OLBan7LDnIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC-we5L-DjbbeUQja45yMPo2WbCQMnOr8pcNLTDKMttZQh7yb4RyQmJiLhRsMlrEMJR-hlO1j4_eyM6e0x6q5IO-bx72BbT-Kq5jDh3Jb6ksD-RtWljBaa6y0hvctn6cShnCeMjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t225QhDNDJtTK8JRPs34JVHJvhHJTgMjL2DKCShUFs0M3RB2Q-5KL-2RQH8MOPKtnhXU_U5PvQhxc2JGQD_MbdJJjoJbnVyPPBW4InQP7fBtRE3gTxoUJM5DnJhhvGXfO83xIebPRiJPr9QgbqslQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0M5DK0hDPxjT8MDToM5pJfetnbaD5KW5rJabC3sDJ3XU6qLT5XhJ6qWP52-COtQbocbhRSJfbaX4ri5l0njxQyJ55G365dLpQS3hj1Eq5qLUonDh8z2a7MJUntKHcfBhvO5hvvhb6O3M7-qfKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQ2a_E5bj2qRPD_DLK3f; H_BDCLCKID_SF_BFESS=tbC8VCDKJKD3H48k-4QEbbQH-UnLq5Q33gOZ04n-ah058UcSXnQoBpFpypJr2ncbBDrP0Pom3UTKsq76Wh35K5tTQP6rLf5eLRc4KKJxbP8aKJbH5tK-M6JQhUJiB5OLBan7LDnIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC-we5L-DjbbeUQja45yMPo2WbCQMnOr8pcNLTDKMttZQh7yb4RyQmJiLhRsMlrEMJR-hlO1j4_eyM6e0x6q5IO-bx72BbT-Kq5jDh3Jb6ksD-RtWljBaa6y0hvctn6cShnCeMjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t225QhDNDJtTK8JRPs34JVHJvhHJTgMjL2DKCShUFs0M3RB2Q-5KL-2RQH8MOPKtnhXU_U5PvQhxc2JGQD_MbdJJjoJbnVyPPBW4InQP7fBtRE3gTxoUJM5DnJhhvGXfO83xIebPRiJPr9QgbqslQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0M5DK0hDPxjT8MDToM5pJfetnbaD5KW5rJabC3sDJ3XU6qLT5XhJ6qWP52-COtQbocbhRSJfbaX4ri5l0njxQyJ55G365dLpQS3hj1Eq5qLUonDh8z2a7MJUntKHcfBhvO5hvvhb6O3M7-qfKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQ2a_E5bj2qRPD_DLK3f",
            }
            url = f"https://alayn.baidu.com/express/appdetail/get_com?num={dh}&cb=jsonp_{str(timestamp).replace('.', '_')}"
            request = requests.get(url=url, headers=params)
            gs = re1.findall(request.text)[0]
            return kdbm[gs]
    else:
        return None

def check_field(field):
    """校验字段"""
    field = {"pid": 1, "pdName": "huawei", "purchasePlatform": 0, "buyDate": "2021.1.3", "goonDate": "2023.1.1",
     "expectDate": "2024.1.1", "price": 1999, "sellproce": 2999, "purchaseState": 0}

    re_dic = {"status": 200, "error": "无法处理该请求"}
    re1  = re.compile(r"^\d{5,20}$").fullmatch(field["pid"])
    if re1:
        re_dic["error"] = "pid字段格式错误"
        return re_dic
    if len(field["pdName"]) >30:
        re_dic["error"] = "商品名称超长"
        return re_dic
    elif len(field["pdName"]) == 0:
        re_dic["error"] = "商品名称不能为空"
        return re_dic
    if re_dic["purchasePlatform"]  not in [0,1,2,3]:
        re_dic["error"] = "购买平台错误"
        return re_dic
    re1 = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
    for k,y in {"购买日期":"buyDate","发走日期":"goonDate","预期到达日期":"expectDate"}.items():
        if not re1.fullmatch(field[y]):
            re_dic["error"] = f"{k}格式错误请检查格式"
            return re_dic

