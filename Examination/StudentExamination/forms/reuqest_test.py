import json

import requests
import datetime,re
def get_kd(dh):
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
    url = f"https://alayn.baidu.com/express/appdetail/get_com?num={dh}&cb=jsonp_{str(timestamp).replace('.','_')}"
    request = requests.get(url=url, headers=params)
    gs = re1.findall(request.text)[0]
    url = f"https://alayn.baidu.com/express/appdetail/get_detail?query_from_srcid=51151&tokenV2=tmtMT2ckxiG4xM2MvB9M%2Be9fXkHjFXBjEEYzT2hwVcwDCT%2FtLSnbKEe1jZAUkxOE&appid=4001&nu={dh}&com={gs}&qid=4879176651996235000&ds=&tk=&verifyMode=1&cb=jsonp_jsonp_{str(timestamp).replace('.','_')}"
    re1 = re.compile(r"\{\"time\".*?\}")
    reque = requests.get(url=url, headers=params)
    return re1.findall(reque.text)
print(get_kd("777178512616535"))