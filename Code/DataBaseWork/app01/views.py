from django.shortcuts import render, HttpResponse, redirect
import pymysql
from itertools import chain
from django.utils.safestring import mark_safe
from django.http import JsonResponse
con = pymysql.connect(host='localhost',
                      user='root',
                      password='root',
                      db='market',
                      autocommit=True
                      )
cur = con.cursor()


def login(request):
    if (request.method == "GET"):
        return render(request, "login.html")
    if (request.method == "POST"):
        email = request.POST.get("email")
        password = request.POST.get("pswd")
        cur.execute("SELECT email FROM user_info WHERE email='%s'" % (email,))
        e = cur.fetchone()
        cur.execute("SELECT pwd FROM user_info WHERE pwd='%s'" % (password,))
        p = cur.fetchone()
        if (p == None or e == None):
            return render(request, "login.html", {"error_msg": "login failed"})
        if (email == e[0] and password == p[0]):
            return redirect("http://127.0.0.1:8000/index")
        else:
            return render(request, "login.html", {"error_msg": "login failed"})


def index(request):
    page = int(request.GET.get("page", 1))
    if (page < 1):
        page = 1
    start = (page - 1) * 12
    end = page * 12
    cur.execute("SELECT * FROM Goods_Info")
    goods = cur.fetchall()
    page_str_list = []
    length_size = len(goods)
    page_num = length_size / 12
    if (page_num + 2 <= 2 * 5 + 1):
        page_front = 1
        page_back = page_num + 1
    else:
        if (page <= 5):
            page_front = 1
            page_back = 11
        if (page >= int(page_num) - 3):
            page_front = page - 5
            page_back = int(page_num) + 2
        if (page > 5 and page < int(page_num) - 3):
            page_front = page - 5
            page_back = page + 5 + 1
    if (page >= 1):
        prev_page = '<li><a href="?page={}">«</a></li>'.format(page - 1)
    else:
        prev_page = '<li><a href="?page={}">«</a></li>'.format(1)

    page_str_list.append(prev_page)

    for i in range(page_front, page_back):
        if (i == page):
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)
    if (page < int(page_num)):
        next_page = prev_page = '<li><a href="?page={}">»</a></li>'.format(page + 1)
    else:
        next_page = prev_page = '<li><a href="?page={}">»</a></li>'.format(int(page_num) + 1)
    page_str_list.append(prev_page)
    page_string = mark_safe("".join(page_str_list))
    return render(request, "index.html", {"goods": goods[start:end], "page_string": page_string})


def add(request):
    if (request.method == "GET"):
        return render(request, "add.html")
    if (request.method == "POST"):
        spbh = request.POST.get("spbh")
        lb = request.POST.get("lb")
        kcl = request.POST.get("kcl")
        dj = request.POST.get("dj")
        if (int(kcl) <= 0 or int(dj) <= 0):
            return render(request, "add.html", {"error_msg": "非法输入"})
        else:
            _time = request.POST.get("time")
            csbh = request.POST.get("csbh")
            cur.execute(
                "INSERT INTO goods_info (商品编号,商品类别,库存量,单价,进货时间,厂家编号) VALUES ('%s','%s','%s','%s','%s','%s');" % (
                    spbh, lb, kcl, dj, _time, csbh,))
            return render(request, "add.html", {"sucess_msg": "Add Successful!"})


def goods_find(request):
    if (request.method == "GET"):
        return render(request, "goods_find.html")
    if (request.method == "POST"):
        spbh = request.POST.get("spbh")
        cur.execute("SELECT * FROM goods_info WHERE 商品编号='%s'" % (spbh))
        info = cur.fetchall()
        if (info):
            return render(request, "goods_find_result.html", {"info": info})
        else:
            return render(request, "goods_find.html", {"error_msg": "not found!"})


def update(request):
    if (request.method == "GET"):
        return render(request, "update.html")
    if (request.method == "POST"):
        spbh = request.POST.get("spbh")
        lb = request.POST.get("lb")
        kcl = request.POST.get("kcl")
        dj = request.POST.get("dj")
        if (int(kcl) <= 0 or int(dj) <= 0):
            return render(request, "update.html", {"error_msg": "非法输入"})
        else:
            _time = request.POST.get("time")
            csbh = request.POST.get("csbh")
            cur.execute("UPDATE goods_info SET 商品类别='%s', 库存量='%s', 单价='%s', 进货时间='%s', 厂家编号='%s' WHERE 商品编号='%s' " %
                        (lb, kcl, dj, _time, csbh, spbh,))
            return render(request, "update.html", {"sucess_msg": "Sucessfully Update!"})


def delete(request):
    if (request.method == "GET"):
        return render(request, "delete.html")
    if (request.method == "POST"):
        spbh = request.POST.get("spbh")
        cur.execute("SELECT 商品编号 FROM goods_info WHERE 商品编号='%s'" % (spbh))
        is_exit = cur.fetchone()
        if (is_exit):
            cur.execute("DELETE FROM goods_info WHERE 商品编号='%s'" % (spbh))
            return render(request, "delete.html", {"success_msg": "Delete Success!"})
        else:
            return render(request, "delete.html", {"error_msg": "delete failed!"})


def cs_find(request):
    if (request.method == "GET"):
        return render(request, "cs_find.html")
    if (request.method == "POST"):
        csbh = request.POST.get("csbh")
        cur.execute("SELECT 厂家编号 FROM industry_info WHERE 厂家编号='%s'" % (csbh,))
        is_exit = cur.fetchone()
        if (is_exit):
            cur.execute("SELECT * FROM industry_info WHERE 厂家编号='%s'" % (csbh,))
            info = cur.fetchall()
            return render(request, "cs_find_result.html", {"info": info})
        else:
            return render(request, "cs_find.html", {"error_msg": "No Match"})


def lh_find(request):
    if (request.method == "GET"):
        return render(request, "lh_find.html")
    if (request.method == "POST"):
        csbh = request.POST.get("csbh")
        cur.execute("SELECT 厂家编号 FROM industry_info WHERE 厂家编号='%s'" % (csbh,))
        is_exit = cur.fetchone()
        if (is_exit):
            cur.execute(
                "SELECT * FROM goods_info WHERE goods_info.厂家编号 IN (SELECT industry_info.厂家编号 FROM industry_info WHERE industry_info.厂家编号='%s')" % (
                    csbh,))
            info = cur.fetchall()
            return render(request, "lh_find_result.html", {"info": info})
        else:
            return render(request, "lh_find.html", {"error_msg": "No Match"})


def order_find(request):
    if (request.method == "GET"):
        return render(request, "order_find.html")
    if (request.method == "POST"):
        spbh = request.POST.get("spbh")
        cur.execute("SELECT 商品编号 FROM goods_info WHERE 商品编号='%s'" % (spbh))
        info = cur.fetchone()
        if (info):
            cur.execute(
                "SELECT * FROM goods_order WHERE 商品编号 IN (SELECT 商品编号 FROM goods_info WHERE goods_info.商品编号='%s')" % (
                    spbh,))
            info = cur.fetchall()
            return render(request, "order_find_result.html", {"info": info})
        else:
            return render(request, "order_find.html", {"error_msg": "No Match!"})
