from io import BytesIO

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from StudentExamination.models import admin, test_paper, teacher

from StudentExamination.forms.StudentForm import RegisterModelForm, loginModelForm
from StudentExamination.forms.randimg import check_code
from StudentExamination.forms.MD5 import md5
import re

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
    # 设置验证码超时时间 10S
    request.session.set_expiry(10)
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


def main_index(request):
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
