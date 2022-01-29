from django.shortcuts import render,redirect    #渲染html文件
from django.contrib.auth.decorators import login_required   #限制访问显示装饰器
from django.http import Http404
# from django.shortcuts import HttpResponse      #导入此模块
from .models import Topic,Entry
from .forms import TopicForm,EntryForm
# Create your views here.
#
# user_list = [
#     {"user":"jack","pwd":"abc"},
#     {"user":"sdf","pwd":"ABC"},
# ]
#
# def index(request):   #request参数必须由，名字是类似self的默认规则，可以改，他封装了用户请求的所有内容
#     if request.method == 'POST':
#         username = request.POST.get("username",None)
#         password = request.POST.get("password",None)
#         temp = {"user":username,"pwd":password}
#         user_list.append(temp)
#         # print(username,password)
#     return render(request,"index.html",{"data":user_list})

def index(request):
    #学习笔记的主页
    return render(request,'index.html')

@login_required
def topics(request):
    #显示所有的主题
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    topics = Topic.objects.order_by('date_added')
    context = {'topics':topics}
    return render(request,'topics.html',context)

@login_required
def topic(request,topic_id):
    #显示单个主题及其所有的条目
    topic = Topic.objects.get(id=topic_id)
    #确定请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic,'entries':entries}
    return render(request,'topic.html',context)

@login_required
def new_topic(request):
    #添加新主题
    if request.method != 'POST':
        form = TopicForm()
    else:
        #post提交的数据：对数据进行处理
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('studynote:topics')
    #显示空表单或指出表单数据无效
    context = {'form':form}
    return render(request,'new_topic.html',context)

@login_required
def new_entry(request,topic_id):
    #在特定的主体中添加条目
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('studynote:topic',topic_id=topic_id)

    context = {'topic':topic,'form':form}
    return render(request,'new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
    #编辑既有条目
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('studynote:topic',topic_id=topic.id)
    context = {'entry':entry,'topic':topic,'form':form}
    return render(request,'edit_entry.html',context)
