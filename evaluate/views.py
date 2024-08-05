from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View

from evaluate.models import Evaluation

# Create your views here.

class ToAccess(View):
    def get(self, request):
        return render(request, 'evaluates/to_access.html')

class AddCommentOver(View):
    def post(self, request):
        # 获取用户信息
        user = request.session.get('user')
        # 获取评论内容
        content = request.POST.get('content')
        # 获取评论用户id
        user_id = user.id
        # 插入数据库中
        Evaluation.objects.create(content=content, user_id=user_id,)
        # 重定向到我的评论页面
        return HttpResponseRedirect('/evaluate/my_comments/')


class MyComments(View):
    def get(self, request):
        # 获取用户信息
        user = request.session.get('user')
        # 获取用户id
        user_id = user.id
        # 获取用户评论
        evaluations = Evaluation.objects.filter(user_id=user_id)
        # 渲染评论页面
        return render(request, 'evaluates/my_comments.html', {'evaluations': evaluations})


class DelComments(View):
    def post(self, request):
        # 获取评论id
        comment_id = request.POST.get('comment_id')
        # 删除评论
        Evaluation.objects.filter(id=comment_id).delete()
        # 返回json数据
        return JsonResponse({'flag': 'true'})