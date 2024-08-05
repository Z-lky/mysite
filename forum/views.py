from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View

from forum.models import Writings
from usersapp.models import UserInfo

# Create your views here.
class EssayListView(View):
    def get(self, request):
        #获取文章列表
        writing_list = Writings.objects.all()
        return render(request, 'forums/essay_list.html', {'writing_list': writing_list})


class EssayWriteView(View):
    def get(self, request):
        #判断用户是否登录
        user = request.session.get('user')
        if not user:
            return HttpResponseRedirect('/users/login/')
        #渲染文章写作页面
        return render(request, 'forums/essay_write.html')


class EssayEditView(View):
    def post(self, request):
        #获取用户信息
        user = request.session.get('user')
        #获取文章标题
        title = request.POST.get('title')
        #获取文章内容
        content = request.POST.get('content')
        #获取作者id
        user_id = user.id
        #插入数据库中
        Writings.objects.create(title=title, content=content, user_id=user_id)
        #渲染文章编辑成功重定向到文章列表页面
        return HttpResponseRedirect('/forum/essay/')


class ConsultationListView(View):
    def get(self, request):
        #获取用户信息
        user_id = request.session.get('user').id
        #获取信息列表
        consultation_list = Writings.objects.filter(user_id=user_id)
        return render(request, 'forums/consultation_list.html', {'consultation_list': consultation_list})


class ConsultationDeleteView(View):
    def post(self, request):
        #获取文章id
        writing_id = request.POST.get('essay_id',)
        #根据文章id删除文章
        Writings.objects.filter(id=writing_id).delete()
        #渲染文章删除成功返回json值ture
        return JsonResponse({'flag': 'true'})