import re
from collections import namedtuple

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q, Max
from django.db.models.functions import Length
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from bs4 import BeautifulSoup
import requests

# Create your views here.
from app.models import Module, Parent

Code = namedtuple("Code", "code")


def table(full, codes):
    modules = {1: ["<th>1</th>"], 2: ["<th>2</th>"], 3: ["<th>3</th>"], 34: ["<th>3/4</th>"], 4: ["<th>4</th>"]}
    start = """<table><tr>"""
    for obj in full:
        style = ""
        if obj.code in codes:
            style = " style=\"border: 2px solid black\""
        c = obj.code.replace("/", "")
        print(obj.code)
        code_safe = obj.code.replace("/", "-").lower()
        url = "https://www.dur.ac.uk/mathematical.sciences/teaching/2017modules/"
        modules[obj.year].append(f"<td id=\"{c}\"{style} onClick=\"window.open('{url}{code_safe}/')\">{obj.name}</td>")
    end = "</tr></table>"
    modules = "</tr><tr>".join(["".join(x) for x in modules.values()])
    return start + modules + end


class Home(View):
    def get(self, request):
        return render(request, "index.html", {"all": Module.objects.all()})

    def post(self, request):
        name = request.POST.get("name", "")
        direct = request.POST.get("direct", False)
        if name == "":
            full = set(Module.objects.all())
            searched = Code(code="")
        else:
            modules = Module.objects.filter(name__icontains=name)
            searched = modules[0]
            modules = Module.objects.filter(code=searched.code)
            full = set([searched])
            while len(modules) > 0:
                modules = Module.objects.filter(parent__child__in=modules)
                full = full.union(modules)
                if direct:
                    break
        modules = table(full, [searched.code])
        return JsonResponse({"d": modules})


class Possible(View):
    def get(self, request):
        return render(request, "possible.html", {"url": "possible/", "all": Module.objects.all()})

    def post(self, request):
        codes = request.POST.getlist("modules[]")
        direct = request.POST.get("direct", False)
        if codes:
            modules = list(Module.objects.filter(code__in=codes))
            year = max(modules, key=lambda x: x.year).year
            full = set(modules)
            full = full.union(Module.objects.filter(child__parent__isnull=True, year__gt=year))
            while len(modules) > 0:
                m = Module.objects.filter(child__parent__in=modules, year__gt=year)
                modules = []
                for mod in m:
                    pre = Module.objects.filter(parent__child=mod)
                    if full.issuperset(pre):
                        modules.append(mod)
                full = full.union(modules)
                if direct:
                    break
            modules = table(full, codes)
            return JsonResponse({"d": modules})
        return JsonResponse({})


def get_module(request):
    search = request.POST.get("module")
    if search:
        module = Module.objects.filter(name__icontains=search).first()
        return JsonResponse({"module": {"code": module.code, "name": module.name}})
    return JsonResponse({})


class Leads(View):
    def get(self, request):
        return render(request, "index.html", {"url": "leads/", "all": Module.objects.all()})

    def post(self, request):
        name = request.POST.get("name", "")
        direct = request.POST.get("direct", False)
        if name == "":
            full = set(Module.objects.all())
            searched = Code(code="")
        else:
            modules = Module.objects.filter(name__icontains=name)
            searched = modules[0]
            modules = Module.objects.filter(code=searched.code)
            full = set([modules.first()])
            while len(modules) > 0:
                modules = Module.objects.filter(child__parent__in=modules)
                full = full.union(modules)
                if direct:
                    break

        modules = table(full, [searched.code])
        print(modules)
        return JsonResponse({"d": modules})


class Add(View):
    def get(self, request):
        return render(request, "add.html")

    def post(self, request):
        name = request.POST.get("name", None)
        parent = request.POST.get("parent", None)
        year = request.POST.get("year", 1)
        if isinstance(year, str):
            year = int(year.replace("/", ""))
        x = requests.get("https://www.dur.ac.uk/mathematical.sciences/teaching/2017modules/")
        page = BeautifulSoup(x.content, 'html.parser')
        modules = page.find_all("a", string=re.compile(name, re.I))
        if parent:
            parents = page.find_all("a", string=re.compile(parent, re.I))
            p = parents[0].string.split(" ")[0]
        else:
            p = None
        if modules and name:
            m = modules[0].string
            mult = len(str(year)) + 1
            mod = Module.objects.get_or_create(code=m[:4 * mult], name=m[(4 * mult) + 1:], year=year)[0]
            if parent:
                Parent.objects.create(parent_id=p, child=mod)
                p = Module.objects.get(code=p).name
            else:
                p = ""
            return JsonResponse({"name": m[9:], "parent": p})
        return JsonResponse({"name": "failed"})

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def test(request):
    # for obj in Module.objects.filter(year=34):
    #     obj.code = obj.code + obj.name[:4]
    #     obj.name = obj.name[5:]
    #     obj.save()
    #
    # for obj in Module.objects.filter(year=34, name__regex="^[0-9]{4}.+"):
    #     # new = Module.objects.get(code=obj.code + obj.name[:4])
    #     # Parent.objects.filter(parent__code=obj.code).update(parent=new)
    #     # Parent.objects.filter(child__code=obj.code).update(child=new)
    #     obj.delete()
    # for obj in Module.objects.annotate(code__len=Length("code")).filter(code__len__gt=8):
    #     if "/" in obj.code:
    #         obj.code = obj.code + input(obj.code)
    #     elif len(obj.code) == 12:
    #         obj.code = obj.code[:8] + "/" + obj.code[8:]
    #     obj.save()
    # for obj in Module.objects.annotate(code__len=Length("code")).filter(code__len=12):
    #     obj.delete()
    return JsonResponse({})
