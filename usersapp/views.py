from django.core.serializers import serialize
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View

from goods.models import Goods
from . import service
from .models import UserInfo, Address, Area, ImprovePersonal
from utils.code import *
# Create your views here.

class RegisterView(View):
    def get(self, request):
        return render(request, 'users/register.html')

    def post(self, request):
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')

        #插入数据库操作
        user = UserInfo.objects.create(uname=uname, pwd=pwd)

        #判断是否注册成功
        if user:
            request.session['user'] = user  # 登录成功后设置session

            return HttpResponseRedirect('/users/login/')  # 注册成功跳转到个人中心页面

        return HttpResponseRedirect('/users/register/')  # 注册失败跳转到注册页面


class CheckUnameView(View):
    def get(self, request):
        #获取用户名
        uname = request.GET.get('uname', '')
        #查询数据库,get和filter的区别是,数据库中没有这个数据，get会报错,filter会返回一个空的QuerySet
        user_list = UserInfo.objects.filter(uname=uname)
        flag = False
        if user_list:
            flag = True
        return JsonResponse({'flag': flag})

class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        #给每个字段判断，为空就提示用户
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')

        #查询数据库
        user_list = UserInfo.objects.filter(uname=uname, pwd=pwd)
        if user_list:
            user = user_list[0]
            request.session['user'] = user  # 登录成功后设置session
            return HttpResponseRedirect('/')  # 登录成功跳转到个人中心页面
        else:
            return HttpResponseRedirect('/users/login/')  # 登录失败跳转到登录页面


class CenterView(View):
    def get(self, request):
        # 判断用户是否登录
        if not request.session.get('user'):
            return HttpResponseRedirect('/users/login/')  # 未登录跳转到登录页面
        else:
            # 获取用户信息
            user = request.session.get('user')
            # 获取用户信息完善信息
            improve_personal = user.improvepersonal_set.all()
            if improve_personal:
                uqqemail = improve_personal[0].uqqemail
                uphone = improve_personal[0].uphone
                ubirthday = improve_personal[0].ubirthday
                usex = improve_personal[0].usex
                utag = improve_personal[0].utag
                address = improve_personal[0].getDefaultAddress()
            else:
                uqqemail = ''
                uphone = ''
                ubirthday = ''
                usex = ''
                utag = ''
                address = ''
            # 返回个人中心页面
            return render(request, 'users/users_center.html', {'address': address, 'uqqemail': uqqemail, 'uphone': uphone, 'ubirthday': ubirthday, 'usex': usex, 'utag': utag})

class LogoutView(View):
    def post(self, request):
        if 'user' in request.session:
            del request.session['user']
        return JsonResponse({'flag': True})


class LoadCodeView(View):
    def get(self, request):
        img, str = gene_code()
        # 将验证码字符串保存到session中
        request.session['session_code'] = str
        # 返回验证码图片
        return HttpResponse(img, content_type='image/png')  # 设置MIME类型为image/png


class CheckCodeView(View):
    def get(self, request):
        # 获取get数据
        code = request.GET.get('code')
        # 获取session中的验证码
        session_code = request.session.get('session_code')
        # 比较验证码,==优先级高于=
        flag = code == session_code
        # 返回结果
        return JsonResponse({'flag': flag})


class EditPersonalView(View):
    def get(self, request):
        # 判断用户是否登录
        if not request.session.get('user'):
            return HttpResponseRedirect('/users/login/')  # 未登录跳转到登录页面
        else:
            return render(request, 'users/edit_personal.html')

    def post(self, request):
        # 获取用户信息
        user = request.session.get('user')
        # 获取post数据
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        # 更新数据库
        UserInfo.objects.filter(id=user.id).update(uname=uname, email=email, phone=phone)
        # 更新session中的用户信息
        request.session['user'] = UserInfo.objects.get(id=user.id)
        # 跳转到个人中心页面
        return HttpResponseRedirect('/users/center/')


class AddressView(View):
    def get(self, request):
        user = request.session.get('user')
        address_list = user.address_set.all()
        return render(request, 'users/address.html', {'address_list': address_list})

    def post(self, request):
        # 获取表单数据
        aname = request.POST.get('aname', '')
        aphone = request.POST.get('aphone', '')
        addr = request.POST.get('addr', '')
        user = request.session.get('user')

        # 插入数据库
        Address.objects.create(aname=aname, aphone=aphone, addr=addr, userinfo=user,
                               isdefault=(lambda count: True if count == 0 else False)(user.address_set.all().count()))

        # 返回结果
        return HttpResponseRedirect('/users/address/')


class LoadAreaView(View):
    def get(self, request):
        # 获取省份id
        pid = request.GET.get('pid', -1)
        pid = int(pid)
        # 查询数据库
        area_list = Area.objects.filter(parentid=pid)
        # 序列化，构造json数据
        area_list_json = serialize('json', area_list)

        return JsonResponse({'area_list_json': area_list_json})

class AddressEditView(View):
    def get(self, request, aid):
        #获取对应user的地址数据，查询数据库
        user = request.session.get('user')
        address_list = Address.objects.filter(id=aid, userinfo=user)
        print(address_list[0].isdefault)

        if address_list:
            aname = address_list[0].aname
            aphone = address_list[0].aphone
            addr = address_list[0].addr
            isdefault = address_list[0].isdefault
            return render(request, 'users/address_edit.html', {'aname': aname, 'aphone': aphone, 'addr': addr, 'isdefault': isdefault, 'aid': aid})

    #表单数据
    def post(self, request, aid):
        # 获取表单数据
        aname = request.POST.get('aname', '')
        aphone = request.POST.get('aphone', '')
        addr = request.POST.get('addr', '')
        user = request.session.get('user')

        # 更新数据库
        Address.objects.filter(id=aid, userinfo=user).update(userinfo=user, aname=aname, aphone=aphone, addr=addr)
        if Address.objects.filter(id=aid, userinfo=user):
            return JsonResponse({'flag': True})
        else:
            return JsonResponse({'flag': False})



class AddressDeleteView(View):
    def get(self, request, aid):
        # 查询数据库
        address = Address.objects.get(id=aid)
        if address:
            # 删除该条地址数据
            address.delete()
            # 返回结果
            return HttpResponseRedirect('/users/address/')


class ImprovePersonalView(View):
    def post(self, request):
        # 获取用户信息
        user = request.session.get('user')
        # 获取post数据
        uqqemail = request.POST.get('uqqemail')
        uphone = request.POST.get('uphone')
        ubirthday = request.POST.get('ubirthday')
        usex = request.POST.get('sex')
        utag = request.POST.get('utag')
        user_id = user.id
        #如果没有数据，插入数据库，否则更新数据库
        if not ImprovePersonal.objects.filter(user_id=user_id):
            ImprovePersonal.objects.create(uqqemail=uqqemail, uphone=uphone, ubirthday=ubirthday, usex=usex, utag=utag, user_id=user_id)
        else:
            ImprovePersonal.objects.filter(user_id=user_id).update(uqqemail=uqqemail, uphone=uphone, ubirthday=ubirthday, usex=usex, utag=utag)
        # 更新session中的用户信息
        request.session['user'] = UserInfo.objects.get(id=user_id)
        # 更新数据库
        # 跳转到个人中心页面
        return HttpResponseRedirect('/users/center/')


class SearchFucView(View):
    def post(self, request):
        #获取表单中input的值，也就是搜索的关键字
        keyword = request.POST.get('q')
        print(keyword)
        #查询数据库,icontains表示模糊查询
        #__icontains表示忽略大小写
        user_list = Goods.objects.filter(gname__icontains=keyword)
        print(user_list)
        if user_list:
            return render(request, 'goods/search_result.html', {'user_list': user_list, 'keyword': keyword})
        else:
            #返回没有查询到商品的页面
            return render(request, 'goods/search_result_error.html', {'msg': '没有查询到相关商品','keyword': keyword})


class ServiceView(View):
    def get(self, request):
        return render(request, 'users/service.html')




# 获取邮箱
def email_code(request):
    email = request.GET.get('e')
    print(email)
    # 验证邮件地址格式
    ef = service.verify_email(email)
    if not ef:
        return JsonResponse({'flag': 'flase'})
    # pf:邮件是否发生成功
    pf = service.post_email(email)
    if not pf:
        return JsonResponse({'flag': 'flase'})
    print("发生验证码成功：", email)
    return JsonResponse({'flag': 'true'})

#检查邮箱是否被注册或者可用
class CheckEmailView(View):
    def get(self, request):
        # 获取邮箱
        email = request.GET.get('email')
        # 查询数据库邮箱是否存在
        user_list = ImprovePersonal.objects.filter(uqqemail=email)
        if user_list:
            return JsonResponse({'flag': True})
        else:
            return JsonResponse({'flag': False})


class checkEcode(View):
    def get(self, request):
        # 获取验证码
        code = request.GET.get('code')
        # 获取session中的验证码
        session_code = request.session.get('session_code')
        # 比较验证码,==优先级高于=
        flag = code == session_code
        # 返回结果
        return JsonResponse({'flag': flag})

