# !coding=utf-8
import datetime, re

import re
import plotly.graph_objects as go
import requests
from StudentExamination.models import Express_delivry


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
            if gs:
                return kdbm[gs]
            return None
    else:
        return None


def check_field(field):
    """校验字段"""
    re_dic = {"status": 201, "error": "无法处理该请求"}
    re1 = re.compile(r"^\d{1,}$").fullmatch(str(field["pid"]))
    if not re1:
        re_dic["error"] = "pid字段格式错误"
        return re_dic
    if len(field["pdName"]) > 30:
        re_dic["error"] = "商品名称超长"
        return re_dic
    elif len(field["pdName"]) == 0:
        re_dic["error"] = "商品名称不能为空"
        return re_dic
    try:
        if int(field["purchasePlatform"]) not in [0, 1, 2, 3]:
            re_dic["error"] = "购买平台错误"
            return re_dic
    except Exception as e:
        re_dic["error"] = str(e)
        return re_dic
    re1 = re.compile(r"^\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}$")
    for k, y in {"购买日期": "buyDate", "发走日期": "goonDate", "预期到达日期": "expectDate"}.items():
        if not re1.fullmatch(str(field[y])):
            re_dic["error"] = f"{k}格式错误请检查格式"
            return re_dic
    try:
        int(field["price"])
    except Exception:
        re_dic["error"] = "购买价格式错误"
        return re_dic
    try:
        int(field["sellprice"])
    except Exception:
        re_dic["error"] = "购买价格式错误"
        return re_dic
    try:
        if int(field["purchaseState"]) not in [0, 1]:
            re_dic["error"] = "商品状态格式错误"
            return re_dic
    except Exception as e:
        re_dic["error"] = str(e)
        return re_dic
    return {"status": 200, "data": "添加成功"}


def check_Logistic(dh):
    dh = str(dh)
    gsbm = get_kd(dh)
    if gsbm:
        if Express_delivry.objects.filter(dh=dh).first():
            return {"status": 201, "error": "快递单号已存在"}
        params = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "17token": "6AFA3318BFD3451E0B30D95677C2F430",
        }
        data = [
            {
                'number': f'{dh}',
                "carrier": gsbm,
            }
        ]
        request = requests.post(url=f"https://api.17track.net/track/v2/register", headers=params, json=data)
        Express_delivry.objects.create(dh=dh, expre_data="")
        return {"status": 200, "error": "注册成功"}
    else:
        return {"status": 201, "error": "快递单号错误，自己找找原因"}



def getDimension(ress):
    url = "https://restapi.amap.com/v3/geocode/geo?parameters"
    key = "ff608780d5d18bab2f875a62b9c0c106"
    params = {
        "key": key,
        "address": ress,
    }
    re = requests.get(url=url, params=params)
    re_data = re.json()
    if re_data["status"] == "1":
        return re_data["geocodes"][0]["location"].split(",")
    return f"失败{re_data['infocode']}"

def getMapHtml(kd_date):
    re_ = re.compile(r"已到达【(.*?)】", re.DOTALL)
    sampledata = {"lat": [], "lon": [], "dataname": []}
    kdst = re_.findall(kd_date)
    print(kdst)
    for i in kdst:
        regetDi = getDimension(i)
        if "失败" not in regetDi:
            sampledata["lon"].append(regetDi[0])
            sampledata["lat"].append(regetDi[1])
            sampledata["dataname"].append(i)
        else:
            return regetDi
    # 创建源数据
    basemap_layer = [
        dict(
            below="traces",
            sourcetype="raster",
            sourceattribution="高德地图",
            source=[
                "http://wprd01.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=7"
            ]
        )
    ]
    print(float(sampledata["lat"][0]),float(sampledata["lon"][0]))
    mapbox_kargs = dict(
        zoom=9,  # 这里的zoom代表地图瓦片缩放的等级，可以依次+1、-1试一试
        center=dict(
            lat=float(sampledata["lat"][0]),  # 这里是设置你的地图的中心点，经纬度要设置好
            lon=float(sampledata["lon"][0]),
        ),
        style="white-bg",
        layers=basemap_layer,
    )

    layout_kargs = dict(
        autosize=False,
        width=1000/2,  # 这里设置的是输出的图的宽度和长度。
        height=800/2,
        margin=dict(
            r=0, t=38, l=0, b=0, pad=0
        ),
    )

    layout = go.Layout(
        mapbox=mapbox_kargs,
        **layout_kargs
    )
    fig = go.Figure(
        data=go.Scattermapbox(lat=sampledata["lat"],  # 这里依次传递经纬度给函数
                              lon=sampledata["lon"],
                              mode='lines+markers',
                              text=sampledata["dataname"],
                              ),
        layout=layout
    )
    return fig.to_html(full_html=False)