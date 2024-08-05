from collections import defaultdict

from django.shortcuts import render
from django.views import View

from evaluate.models import Evaluation
from goods.models import DynastySort, Category, Goods, GoodsSize, GoodsStyle


# Create your views here.
class IndexView(View):
    def get(self, request):
        # 获取分类数据并按 DynastySort 分组,右边导航栏
        categorys_list = Category.objects.all().order_by('dynasty_sort', 'cname')
        categories_by_dynasty = defaultdict(list)
        for category in categorys_list:
            categories_by_dynasty[category.dynasty_sort].append(category)
        # 拿取Goods
        goods_list = Goods.objects.all().order_by('id')[:20]
        # print(goods_list)

        # 将分组后的数据传递给模板
        context = {'categories_by_dynasty': dict(categories_by_dynasty), 'goods_list': goods_list}
        # print(dict(categories_by_dynasty))
        # { < DynastySort: DynastySort: 汉朝 >: [ < Category: Category: 袄裙 >, < Category: Category: 襦裙 >], < DynastySort: DynastySort: 魏晋南北朝 >: [ < Category: Category: 战国袍 >, < Category: Category: 间裙 >], < DynastySort: DynastySort: 唐朝 >: [ < Category: Category: 披帛 >, < Category: Category: 襦衫 >, < Category: Category: 长裙 >], < DynastySort: DynastySort: 明清 >: [ < Category: Category: 满褶裙 >, < Category: Category: 马面裙 >], < DynastySort: DynastySort: 民国 >: [ < Category: Category: 中山装 >, < Category: Category: 旗袍 >]}

        return render(request, 'goods/index.html', context)

class CategoryDetailView(View):
    def  get(self, request, cid):
        # 获取分类详情
        categorys = Category.objects.get(id=cid)
        # 获取分类下的商品
        goods_list = Goods.objects.filter(category=categorys)
        # print(goods_list)
        # 将分类详情和商品列表传递给模板
        context = {'categorys': categorys, 'goods_list': goods_list}
        return render(request, 'goods/category_detail.html', context)
class GoodsDetailView(View):
    def get(self, request, gid):
        # 获取商品详情
        goods_html = Goods.objects.get(id=gid)
        #获取商品尺码
        size_list = GoodsSize.objects.all()
        # 获取商品风格图
        style_lists = [style.gstyle for style in GoodsStyle.objects.filter(goods_id=goods_html.id)]
        # 获取喜欢的商品
        categorys_list = Category.objects.all().order_by('dynasty_sort', 'cname')
        categories_by_dynasty = defaultdict(list)
        for category in categorys_list:
            categories_by_dynasty[category.dynasty_sort].append(category)
        # 拿取Goods
        goods_list = Goods.objects.all().order_by('-id')[:3]
        # 将商品详情传递给模板
        context = {'goods_html': goods_html, 'size_list': size_list, 'style_lists': style_lists, 'goods_list': goods_list}
        return render(request, 'goods/detail.html', context)


class CommentView(View):
    def get(self, request, gid):
        # 获取商品详情
        goods_html = Goods.objects.get(id=gid)
        # 获取评论
        comments_list = Evaluation.objects.all()
        # 将评论传递给模板
        context = {'goods_html': goods_html, 'comments_list': comments_list}
        return render(request, 'goods/comment.html', context)