from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render, redirect

from StudentExamination.models import admin, test_paper, teacher

from StudentExamination.forms.StudentForm import RegisterModelForm, loginModelForm
from StudentExamination.forms.randimg import check_code


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
                return render(request, "teacher_login.html")
            else:
                form.add_error("passwd", "账号或密码错误")
        else:
            form.add_error("random_img", "验证码不正确")
        # 校验账号密码
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


def achievement(request):
    return render(request, "achievement.html")


def gtimg(request):
    """验证码获取"""
    img, img_str = check_code()
    # 将验证码正确数子放入session中
    request.session["image_code"] = img_str
    # 设置验证码超时时间 20S
    request.session.set_expiry(20)
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

    return None
