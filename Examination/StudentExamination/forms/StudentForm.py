from django import forms
from django.core.exceptions import ValidationError

from StudentExamination import models

from StudentExamination.forms.MD5 import md5


class StudentModelForm(forms.ModelForm):
    """通用模板"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    "placeholder": field.label
                }


class RegisterModelForm(StudentModelForm):
    """注册modelform"""
    # 密码
    passwd = forms.CharField(max_length=100, label="密码", widget=forms.PasswordInput(render_value=True))
    # 重复密码
    repeat_passwd = forms.CharField(max_length=100, label="重复密码", widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.admin
        fields = "__all__"

    def clean_user(self):
        """判断数据库是否存在相同数据"""
        user = self.cleaned_data.get("user")
        if not models.admin.objects.filter(user=user).first():
            return user
        raise ValidationError("用户名已存在")

    def clean_passwd(self):
        """规则密码并使用MD5加密"""
        passwd = self.cleaned_data.get("passwd")
        return md5(passwd)

    def clean_repeat_passwd(self):
        """查看重复密码是否相同"""
        repeat_passwd = self.cleaned_data.get("repeat_passwd")
        if md5(repeat_passwd) == self.cleaned_data.get("passwd"):
            return md5(repeat_passwd)
        else:
            raise ValidationError("密码输入不一致")


class loginModelForm(StudentModelForm):
    """登录页面"""
    random_img = forms.CharField(max_length=5, label="验证码",
                                 widget=forms.TextInput(attrs={'class': "e e1"}))
    passwd = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True, attrs={"class": "e"}))
    user = forms.CharField(label="用户名",
                           widget=forms.TextInput(attrs={'class': "e"}))

    class Meta:
        model = models.admin
        fields = ["user", "passwd"]

    def clean_passwd(self):
        return md5(self.cleaned_data.get("passwd"))


class AddPaperModelForm(StudentModelForm):
    """新增题目"""

    class Meta:
        model = models.test_paper
        exclude = []
