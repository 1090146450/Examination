from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
import re

class LoginSeesion(MiddlewareMixin):
    """校验登录的session是否相同"""

    def process_request(self, request):
        try:
            re_d = re.compile(r"\/api\/.?").findall(request.path_info)
            print(re_d)
        except Exception as e:
            print(str(e))
            re_d = None
        if request.path_info in ["/login/", "/register/",] and re_d:
            pass
        else:
            if request.session.get("info"):
                pass
            else:
                return redirect("/login/")
