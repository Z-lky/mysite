# @时间 2024/7/22 20:20
# @Author：郑摇2021210510
# @File : mycontextprocessors.py

def getUserInfo(request):
    return {'suser': request.session.get('user')}
