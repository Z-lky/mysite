import json
import uuid

import jsonpickle
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from cart.cartmanager import getCartManger
from cart.models import CartItem
from mysite.settings import alipay
from order.models import Order, OrderItem
from usersapp.models import Address

import datetime as datatime


# Create your views here.
class AddOrderView(View):
    def get(self, request):
        # 获取商品信息
        cartitems = request.GET.get('cartitems', '')
        return HttpResponseRedirect('/order/order.html?cartitems=' + cartitems)


class OrderView(View):
    def get(self, request):
        cartitems = request.GET.get('cartitems', '')
        # print(cartitems)
        print('OrderView(View):get()----------cartitems=' + cartitems)

        # 将 JSON 字符串转换成 python 对象（字典）列表
        # [{goodsid:1, colorid:1, sizeid:1},{goodsid:2, colorid:2, sizeid:2}]
        cartitem_list = jsonpickle.loads(cartitems)
        print(cartitem_list)
        cartitem_dicts = [json.loads(item) for item in cartitem_list if item]

        # 现在 cartitem_dicts 是一个包含字典的列表，每个字典都有 'goodsid' 和 'sizeid' 键
        cartitem_obj_list = []
        for item_dict in cartitem_dicts:
            # 直接从字典中获取 goods_id 和 size_id，并传递给 get_cartitems
            cart_item = getCartManger(request).get_cartitems(goodsid=item_dict['goodsid'], sizeid=item_dict['sizeid'])
            cartitem_obj_list.append(cart_item)
            # 将 python 对象列表转换成 Cartitem 对象列表
        # cartitem_obj_list = [getCartManger(request).get_cartitems(**item) for item in cartitem_list if item]
        print(cartitem_obj_list)
        # 获取用户的默认收货地址
        address = request.session.get('user').address_set.get(isdefault=True)
        # 获取结算总金额
        totalPrice = 0
        for cip in cartitem_obj_list:
            totalPrice += cip.getTotalPrice()
        return render(request, 'orders/order.html',
                      {'cartitem_obj_list': cartitem_obj_list, 'address': address, 'totalPrice': totalPrice})

#
# class OrderPayView(View):
#     def post(self, request):
#         user = request.session.get('user').uname
#         print(user)
#         # 获取总价信息
#         total = request.POST.get('totalPrice')
#         print(total)
#         # 导入alipay对象,并调用统一收单下单并支付页面接口
#         # 参考文档：https://opendocs.alipay.com/apis/api_1/alipay.trade.page.pay
#         # python的uuid模块提供UUID类和函数uuid1(), uuid3(), uuid4(), uuid5() 来生成1, 3, 4, 5各个版本的UUID
#         # 1基于时间戳；3基于名字的MD5散列值；4基于随机数；5基于名字的SHA-1散列值
#         order_param = alipay.api_alipay_trade_page_pay(
#             # 商户订单号
#             # 由商家自定义，64个字符以内，仅支持字母、数字、下划线且需保证在商户端不重复。
#             out_trade_no=str(uuid.uuid4()),
#             # 订单总金额
#             total_amount=total,
#             # 订单标题
#             # 注意：不可使用特殊字符，如 /，=，& 等。
#             # subject=user + '的个人商品',
#             subject=user + '的个人商品',
#             # 回调地址
#             return_url='http://127.0.0.1:8080/cart/cartList/'  # 当支付成功后，支付宝沙箱回调给服务端该url指向的get请求
#         )
#         # 拼接支付地址：支付宝网关 + 订单参数
#         pay_url = 'https://openapi-sandbox.dl.alipaydev.com/gateway.do?' + order_param
#         return JsonResponse({'url': pay_url}, status=200)


class ToPayView(View):
    def get(self, request):
        aid = request.GET.get('address', -1)
        # print(aid)
        payway = request.GET.get('payway', -1)
        # print(payway)
        cartitems = request.GET.get('cartitems', '')
        # print(cartitems)
        # 反序列化cartitems
        cartitem_list = jsonpickle.loads(cartitems)
        # print(cartitem_list)
        # 添加order表信息
        params = {
            # uuid.uuid4() 生成一个随机的唯一标识符
            'out_trade_num': str(uuid.uuid4()),
            # 订单号
            'order_num': datatime.datetime.today().strftime('%Y%m%d%H%M%S'),
            'payway': payway,
            'address_id': aid,
            'user_id': request.session.get('user').id,
        }
        orderObj = Order.objects.create(**params)

        orderItemObjs = [OrderItem.objects.create(order=orderObj, **ci) for ci in cartitem_list if ci]
        # 获取总金额
        total = request.GET.get('totalPrice')
        # 获取用户信息
        user = request.session.get('user').uname
        order_param = alipay.api_alipay_trade_page_pay(
            # 商户订单号
            # 由商家自定义，64个字符以内，仅支持字母、数字、下划线且需保证在商户端不重复。
            out_trade_no=orderObj.out_trade_num,
            # 订单总金额
            total_amount=total,
            # 订单标题
            # 注意：不可使用特殊字符，如 /，=，& 等。
            # subject=user + '的个人商品',
            subject=user + '的个人商品',
            # 回调地址
            return_url='http://127.0.0.1:8088/order/checkPay/'  # 当支付成功后，支付宝沙箱回调给服务端该url指向的get请求
        )
        pay_url = 'https://openapi-sandbox.dl.alipaydev.com/gateway.do?' + order_param
        # 订单创建成功后，删除购物车中已结算的商品
        for ci in cartitem_list:
            if ci:
                CartItem.objects.filter(goodsid=ci['goodsid'], sizeid=ci['sizeid']).delete()

        return HttpResponseRedirect(pay_url)


def checkPay(request):
    params = request.GET.dict()
    print(params)
    # 验证签名
    sign = params.pop('sign')
    if not alipay.verify(params, sign):
        return HttpResponse('支付失败！')
    else:
        # 支付成功，修改订单状态
        out_trade_num = params.get('out_trade_no')
        orderObj = Order.objects.get(out_trade_num=out_trade_num)
        orderObj.status = '已支付'
        orderObj.save()
        return HttpResponseRedirect('/order/orderList/')


class OrderListView(View):
    def get(self, request):
        # 获取订单列表
        order_list = Order.objects.filter(user_id=request.session.get('user').id)
        print(order_list)
        context = {
            'order_list': order_list,
        }


        return render(request, 'orders/orderList.html', context)


class LogisticsView(View):
    def get(self, request):
        order_list = Order.objects.filter(user_id=request.session.get('user').id)
        print(order_list)
        context = {
            'order_list': order_list,
        }
        return render(request, 'orders/logistics.html', context)