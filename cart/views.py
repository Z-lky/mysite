from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from cart.cartmanager import getCartManger


# Create your views here.
# class AddCartView(View):
#     def get(self, request):
#         return render(request, 'carts/cart.html')
class AddCartView(View):
    def post(self, request):
        #多级字典，要手动设置，实时存入session
        request.session.modified = True
        flag = request.POST.get('type')
        if flag == 'add':
            #获取对象
            cartManager = getCartManger(request)
            # 进行操作，加入购物车
            cartManager.add(**request.POST.dict())
        elif flag == 'plus':
            cartManager = getCartManger(request)
            cartManager.update(step=1, **request.POST.dict())
        elif flag =='minus':
            cartManager = getCartManger(request)
            cartManager.update(step=-1, **request.POST.dict())
        elif flag == 'delete':
            cartManager = getCartManger(request)
            #逻辑删除，true 1表示删除，false 0表示不删除
            cartManager.delete(**request.POST.dict())
            print('删除成功')

        return HttpResponseRedirect('/cart/cartList/')

class CartListView(View):
    def get(self, request):
        #判断用户是否登录，如果登录，则显示登录用户的购物车，否则显示空购物车
        if not request.session.get('user'):
            return HttpResponseRedirect('/users/login/')  # 未登录跳转到登录页面
        else:
            cartManager = getCartManger(request)
            #查询当前登录用户的购物车商品
            cart_list = cartManager.queryAll()
            return render(request, 'carts/cart.html', {'cart_list': cart_list})
