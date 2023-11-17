from io import BytesIO

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from StudentExamination.models import admin, test_paper, teacher

from StudentExamination.forms.StudentForm import RegisterModelForm, loginModelForm
from StudentExamination.forms.randimg import check_code
from StudentExamination.forms.MD5 import md5
import requests, datetime, re


# Create your views here.
def register(request):
    """注册界面"""
    form = RegisterModelForm()
    if request.method == "GET":
        data = {
            "form": form
        }
        return render(request, "register.html", data)
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/login/")
    data = {
        "form": form
    }
    return render(request, "register.html", data)


def login(request):
    """登录界面"""
    if request.method == "GET":
        form = loginModelForm()
        data = {
            "form": form
        }
        return render(request, 'login.html', data)
    form = loginModelForm(data=request.POST)
    if form.is_valid():
        # 校验验证码
        img = form.cleaned_data.pop("random_img")
        image_code = request.session.get("image_code")
        if not image_code:
            form.add_error("random_img", "验证码已过期")
            return render(request, "login.html", {"form": form})
        # 将获取的验证码大写
        if img.upper() == image_code.upper():
            # 这个判断是判断为学生还是老师账号  但是账号重复则会出现问题
            if admin.objects.filter(**form.cleaned_data).first():
                request.session['info'] = {"user": form.cleaned_data.get("user"),
                                           "passwd": form.cleaned_data.get("passwd")}
                request.session.set_expiry(60 * 60 * 7)
                return redirect("/index/")
            elif teacher.objects.filter(**form.cleaned_data).first():
                request.session['info'] = {"user": form.cleaned_data.get("user"),
                                           "passwd": form.cleaned_data.get("passwd")}
                request.session.set_expiry(60 * 60 * 7)
                return redirect("/TeacherIndex/")
            else:
                form.add_error("passwd", "账号或密码错误")
        else:
            form.add_error("random_img", "验证码不正确")
        # 校验账号密码
        print(form.errors)
    data = {
        "form": form
    }
    return render(request, "login.html", data)


def index(request):
    """考试主页面"""
    achievement = 0
    if request.method == "GET":
        paper_data = test_paper.objects.all()
        data = {
            "paper_data": paper_data
        }
        return render(request, "index.html", data)
    form = request.POST
    paper_data = test_paper.objects.all().values("answer")
    for i in range(1, len(paper_data) + 1):
        if str(form[f"id{i}"]) == str(paper_data[i - 1]["answer"]):
            achievement += 2
    request.session["achievement"] = achievement
    return redirect("/achievement/")


def teacher_index(request):
    """教师主页面"""
    if request.method == "GET":
        return render(request, "teacher_index.html")
    return render(request, "teacher_index.html")


def achievement(request):
    """查询成绩"""
    return render(request, "achievement.html")


def gtimg(request):
    """验证码获取"""
    img, img_str = check_code()
    # 将验证码正确数子放入session中
    request.session["image_code"] = img_str
    print(img_str)
    # 设置验证码超时时间 10S
    request.session.set_expiry(30)
    # 创建虚拟内存对象并返回前端
    stream = BytesIO()
    # 将获取到的验证码对象放入虚拟内存中
    img.save(stream, 'png')
    # 获取内存中的图片并返回到前端
    return HttpResponse(stream.getvalue())


def exit(request):
    """注销登录"""
    request.session.clear()
    return redirect("/login/")


class JsonResponse(JsonResponse):
    """重新方法使得返回中文"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, json_dumps_params={"ensure_ascii": False})


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
    url = f"https://alayn.baidu.com/express/appdetail/get_com?num={dh}&cb=jsonp_{str(timestamp).replace('.', '_')}"
    request = requests.get(url=url, headers=params)
    gs = re1.findall(request.text)[0]
    url = f"https://alayn.baidu.com/express/appdetail/get_detail?query_from_srcid=51151&tokenV2=tmtMT2ckxiG4xM2MvB9M%2Be9fXkHjFXBjEEYzT2hwVcwDCT%2FtLSnbKEe1jZAUkxOE&appid=4001&nu={dh}&com={gs}&qid=4879176651996235000&ds=&tk=&verifyMode=1&cb=jsonp_jsonp_{str(timestamp).replace('.', '_')}"
    re1 = re.compile(r"\{\"time\".*?\}")
    reque = requests.get(url=url, headers=params)
    return re1.findall(reque.text)


def main_register(request):
    """主页面"""
    json_data = {"status": "", "data": ""}
    if request.method == "POST":
        usename = request.POST.get("username")
        passwd1 = request.POST.get("passwd1")
        passwd2 = request.POST.get("passwd2")
        email_data = request.POST.get("email")
        for i, y in {"用户名": usename, "密码": passwd1, "重复密码": passwd2, "邮箱": email_data}.items():
            if not y:
                return JsonResponse({"status": 200, "error": f"{i}不能为空"})
        if passwd1 != passwd2:
            return JsonResponse({"status": 200, "error": f"两次输入密码不一致"})
        re_s = re.compile(r"^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(.[a-zA-Z0-9]+)+$")
        if not re_s.fullmatch(email_data):
            return JsonResponse({"status": 200, "error": f"邮箱格式错误"})
        if admin.objects.filter(user=usename).first():
            return JsonResponse({"status": 200, "error": f"用户名已存在"})
        passwd1, passwd2 = md5(passwd1), md5(passwd2)
        try:
            admin.objects.create(user=usename, passwd=passwd1, email=email_data)
        except Exception as e:
            return JsonResponse({"status": 200, "error": f"{e}"})
        json_data["status"] = 200
        json_data["data"] = "注册成功"
        return JsonResponse(json_data)
    else:
        json_data["status"] = 502
        json_data["data"] = "不支持的请求方法"
        return JsonResponse(json_data)


def main_login(request):
    """登录界面"""
    json_data = {"status": "", "data": ""}
    if request.method == "POST":
        usename = request.POST.get("username")
        passwd1 = request.POST.get("passwd")
        ima = request.POST.get("image_code")
        for i, y in {"用户名": usename, "密码": passwd1, "验证码": ima}.items():
            if not y:
                return JsonResponse({"status": 200, "error": f"{i}不能为空"})
        passwd1 = md5(passwd1)
        image_code = request.session.get("image_code")
        if not image_code:
            return JsonResponse({"status": 200, "error": "验证码已过期请重新获取!"})
        if image_code.upper() != ima.upper():
            return JsonResponse({"status": 200, "error": "验证码错误!"})
        if admin.objects.filter(user=usename, passwd=passwd1).first():
            request.session['info'] = {"user": usename,
                                       "passwd": passwd1}
            request.session.set_expiry(60 * 60 * 7)
            return JsonResponse({"status": 200, "data": "登录成功！"})
        return JsonResponse({"status": 200, "error": "账号或密码错误"})
    else:
        json_data["status"] = 502
        json_data["data"] = "无法处理该请求"
        return JsonResponse(json_data)

def main_index(request):
    """主页面"""
    if request.method == "GET":
        danhao = request.GET.get("dh")

        print(danhao,type(danhao))
        return JsonResponse({"结果:":get_kd(danhao)})
    else:
        return JsonResponse({"status":502,"data":"无法处理该请求"})
    pass