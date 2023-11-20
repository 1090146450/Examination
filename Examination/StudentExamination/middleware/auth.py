from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class LoginSeesion(MiddlewareMixin):
    """校验登录的session是否相同"""

    def process_request(self, request):
        if request.path_info in ["/login/", "/api/gtimg/", "/register/",
                                 "/api/test/","/api/testlogin/","/api/testmain/",
                                 "/api/getxx/",]:
            pass
        else:
            if request.session.get("info"):
                pass
            else:
                return redirect("/login/")
