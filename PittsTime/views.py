from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, logout
from PittsTime.forms import *
from django.contrib.auth import authenticate
from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse, Http404, JsonResponse
from PittsTime.spotifyModel import app_Authorization, user_Authorization, Track_Data, Button_src, Profile_Data
import json
import re
import bleach
from taggit.models import Tag
from django.core import serializers
from django.db.models import Count
from PittsTime.yelpModel import Get_Info

# Create your views here.
@login_required
def home_page(request):
    context = {}
    blogs = Blog.objects.annotate(number_of_comment=Count('comment')).order_by('create_time').reverse()
    context['blogs'] =blogs
    context['interest'] = [t for t in Tag.objects.all()]
    recent_four_blogs = Blog.objects.order_by('-id')[:4]
    recent_four_blogs_ascending = reversed(recent_four_blogs)
    context['recentblogs'] = recent_four_blogs_ascending
    picture  = Picture.objects.order_by('-id')[:9]
    context['pictures']=picture
    # print(request.user)
    return render(request, "PittsTime/home.html", context)

def login_action(request):
    context = {}
    context['interest'] = [t for t in Tag.objects.all()]
        # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'PittsTime/login.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form
    # Validates the form.
    if not form.is_valid():
        return render(request, 'PittsTime/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))

def spotify_login(request):
    # print(request.user)
    if not request.user.first_name  or not request.user.last_name or not request.user.first_name.strip() or not request.user.last_name.strip:
        return redirect(reverse('spotify_addUserInfo'))
    if not request.user.is_staff:
        request.user.is_staff= True;
        request.user.save()
        profile = Profile(user = request.user)
        profile.save()
    return redirect(reverse('home'))


def spotify_addUserInfo(request):
    context={}
    if request.method == 'GET':
        name = request.user.first_name
        context['name']= name
        return render(request, 'PittsTime/spotify_addUserInfo.html', context)
    if (request.POST['first_name']=='' or request.POST['last_name']==''):
        context['message']='the fields cannot be empty'
    request.user.first_name = request.POST['first_name']
    request.user.last_name = request.POST['last_name']
    request.user.is_staff = True;
    request.user.save()
    profile = Profile(user=request.user)
    profile.save()
    return redirect(reverse('home'))

@login_required
def logout_action(request):
    logout(request)
    return redirect(reverse('login'))


def register_action(request):
    context = {}
    context['interest'] = [t for t in Tag.objects.all()]
    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'PittsTime/register.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    # need detail design in html, maybe a checkbox

    # print(interests)
    # print('end')
    # print(type(interests))
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'PittsTime/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        is_staff = True
                                        )


    new_user.save()
    new_profile = Profile(user=new_user)
    new_profile.save()
    # Interest objects not initialized yet
    # uncomment following code when Interests has been init
    # for interest in interests:
    #     Interest.objects.filter(Interest_name=interest).last().users.add(new_user)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('login'))

@login_required
def myprofile(request):
    context={}
    context['interest'] = [t for t in Tag.objects.all()]
    profile = Profile.objects.get(user=request.user)
    print(profile.bio_picture)
    # context['form'].fields["bio_text"]= profile.bio_text
    context['profile']= profile
    context['form']=ProfileForm(instance = profile)
    #context['form']=ProfileForm()
    interests = Profile.objects.get(user=request.user).interest.all()
    context['following'] = interests
    return render(request,'PittsTime/myprofile.html',context)

@login_required
def updateProfile(request):
    if request.method == 'GET':
        return redirect(reverse('myprofile'))
    context={}
    profile = Profile.objects.get(user=request.user)
    if ('bio_picture' not in request.FILES) or (not request.FILES['bio_picture']):
        request.FILES['bio_picture']=[]
        # request.FILES['bio_picture']= (Profile.objects.get(user=request.user)).picture
    form = ProfileForm(request.POST,request.FILES,instance=profile)
    if not form.is_valid():
        print(form.errors)
        context['form']=form
    else:
        context={}
        profile = Profile.objects.get(user=request.user)
        # if ('bio_picture' not in request.FILES) or (not request.FILES['bio_picture']):
        #     request.FILES['bio_picture']= (Profile.objects.get(user=request.user)).picture

        form = ProfileForm(request.POST,request.FILES,instance=profile)

        if not form.is_valid():
            print(form.errors)
            context['form']=form
            context['profile']= profile
            interests = Profile.objects.get(user=request.user).interest.all()
            context['following'] = interests
            return render(request,'PittsTime/myprofile.html',context)
        else:
            pic = form.cleaned_data['bio_picture']
            #print(pic)
            is_pic = form.clean_picture()
            #print(is_pic)
            if is_pic == 'You must upload a picture!' or is_pic == 'File type is not image!' or is_pic == 'File too big!':
                context['message'] = is_pic
                context['form']=form
                context['profile']= profile
                #print(profile.bio_picture)
                interests = Profile.objects.get(user=request.user).interest.all()
                context['following'] = interests
                return render(request,'PittsTime/myprofile.html',context)
            #profile.content_type = form.cleaned_data['bio_picture'].content_type
            #print("++++++hihihi",form.cleaned_data['bio_text'])
            form.save()
        #     context['form']=form
        # context['profile']=profile
        return redirect(reverse('myprofile'))

@login_required
def other_profile(request,id):
    context={}
    try:
        int(id)
        ClickedUser = User.objects.get(id=id)
    except:
        context['error'] = 'parameter in the url is not validate'
        context['interest'] = [t for t in Tag.objects.all()]
        return render(request,"PittsTime/error.html", context)
    ClickedUser = User.objects.get(id=id)
    if (ClickedUser == request.user):
        return redirect(reverse('myprofile'))
    context['user'] = request.user
    profile = Profile.objects.get(user=ClickedUser)
    context['profile'] = profile
    interests = Profile.objects.get(user=ClickedUser).interest.all()
    context['following'] = interests
    return render(request,'PittsTime/other_profile.html',context)

@login_required
def get_photo(request,id):
    profile =get_object_or_404(Profile,id=id)
    print('Picture #{} fetched from db: {} (type={})'.format(id, profile.bio_picture, type(profile.bio_picture)))
    if not profile.bio_picture:
        raise Http404
    return HttpResponse(profile.bio_picture)


@login_required
def createBlog_action(request):
    context = {}
    context['interest'] = [t for t in Tag.objects.all()]
    pictures = []
    if request.method == 'GET':
        context['form'] = BlogForm()
        return render(request,"PittsTime/createBlog.html",context)
    else:
        time = timezone.now()
        blog = Blog(user=request.user, create_time=time)
        blog_form = BlogForm(request.POST, instance=blog)

        print(blog_form['tags'].data)
#         #print(blog_form['tags'])
#         if blog_form.is_valid():
#             tags = blog_form['tags'].data
#             #print(tags)
#             # if ',' not in tags:
#             #     blog_form['tags'] = '<input type=\"text\" name=\"tags\" value=\"'+tags+',\" required id=\"id_tags\">'
#             #extracted_tags = re.findall(r'value="([^"]+)',tags)
#             #print(blog_form['tags'].data)
#             #print(extracted_tags)
#             blog_temp = blog_form.save(commit=False)
#             print(blog_temp.tags)
#         # new_blog = blog_form.save(commit=False)
#         # new_blog.blog_content = bleach.clean()
#         #blog_form.save_m2m()

#     return redirect(reverse('spotify'))

        # print(blog_form['tags'])
        print(blog_form['Blog_content'].data)
        # string = repr(blog_form['Blog_content'])
        # print(string)
        # print(len(string))
        if len(blog_form['Blog_content'].data)==0:
            context['error'] = "please enter blog content"
            context['form'] = BlogForm()
            return render(request,"PittsTime/createBlog.html",context)
        else:
            if blog_form.is_valid():
                #print(blog_form['Blog_content'])
                tags = blog_form.cleaned_data['tags']
                #print(tags)
                #cleaned_tags = re.findall(r'<input [^>]*value="([^"]+)',tags)
                # new_tag = blog_form.save(commit=False)
                # print(new_tag.tags)
                blog_form.save()
                return redirect(reverse('spotify'))

@login_required
def manageBlog_action(request):
    context={}
    context['interest'] = [t for t in Tag.objects.all()]
    photo_album = []
    pictures = []
    blog = Blog.objects.filter(user=request.user).order_by('create_time').reverse()
    # interests = Interest.objects.filter(users=request.user)
    context['blog']=blog
    context['tags']=[]
    #print(blog)
    for b in blog:
        tags = b.tags.all()
        for t in tags:
            print(t.name)
            if t.name not in context['tags']:
                context['tags'].append(t.name)
    #print(context['tags'])
    return render(request,"pittsTime/manageBlog.html",context)

@login_required
def blog_delete_action(request,id):
    # picture model uses blog as ForeignKey, to delete blog needs to delete pictures first
    context = {}
    try:
        int(id)
        blog = Blog.objects.get(id=id)
    except:
        context['error'] = 'parameter in the url is not validate'
        context['interest'] = [t for t in Tag.objects.all()]
        return render(request,"PittsTime/error.html", context)
    context['interest'] = [t for t in Tag.objects.all()]
    blog = Blog.objects.get(id=id)
    Picture.objects.filter(blog=blog).delete()
    Comment.objects.filter(blog=blog).delete()
    blog.delete()
    for t in Tag.objects.all():
        name = [t.name]
        blogs = [b for b in Blog.objects.filter(tags__name__in=name)]
        if len(blogs) == 0:
            t.delete()
    photo_album = []
    pictures = []
    blog = Blog.objects.filter(user=request.user)
    context['interest'] = [t for t in Tag.objects.all()]
    context['blog']=blog
    print(blog)
    tags = set()
    for b in blog:
        photo_album = Picture.objects.filter(blog=b)
        for t in b.tags.all():
            tags.add(t)
        print(photo_album)
        pictures.extend(photo_album)
    print(pictures)
    for p in pictures:
        print(p.picture_link)
    context['picture'] = pictures
    context['tags'] = tags
    return render(request,"pittsTime/manageBlog.html",context)

@login_required
def blog_edit_action(request,id):
    context = {}
    try:
        int(id)
        blog = Blog.objects.get(id=id)
    except:
        context['error'] = 'parameter in the url is not validate'
        context['interest'] = [t for t in Tag.objects.all()]
        return render(request, "PittsTime/error.html", context)
    pictures = []
    context['interest'] = [t for t in Tag.objects.all()]
    tags = Blog.objects.get(id=id).tags.all()
    print(tags)
    context['tags'] = []
    for t in tags:
        context['tags'].append(t.name)
    if request.method == 'GET':
        title = Blog.objects.get(id=id).title
        Blog_content = Blog.objects.get(id=id).Blog_content
        tags = Blog.objects.get(id=id).tags.all()
        print(tags)
        context['tags'] = []
        for t in tags:
            context['tags'].append(t.name)
        print(context['tags'])
        blog_form = BlogForm()
        context['form'] =blog_form
        context['title'] = title
        context['blog_content'] = Blog_content
        return render(request,"PittsTime/editBlog.html",context)
    else:
        blog = Blog.objects.get(id=id)
        blog_form = BlogForm(request.POST, instance=blog)
        # string = repr(blog_form['Blog_content'])
        # print(len(string))
        # print(blog_form['Blog_content'].data)
        if len(blog_form['Blog_content'].data)==0:
            context['error'] = "please enter blog content"
            title = Blog.objects.get(id=id).title
            Blog_content = Blog.objects.get(id=id).Blog_content
            tags = Blog.objects.get(id=id).tags.all()
            print(tags)
            context['tags'] = []
            for t in tags:
                context['tags'].append(t.name)
            print(context['tags'])
            blog_form = BlogForm()
            context['form'] =blog_form
            context['title'] = title
            context['blog_content'] = Blog_content
            return render(request,"PittsTime/editBlog.html",context)
        if blog_form.is_valid():
            blog_form.save()

        blog = Blog.objects.filter(user=request.user)
        context['interest'] = [t for t in Tag.objects.all()]
        context['blog']=blog
    return render(request,"pittsTime/manageBlog.html",context)

@login_required
def my_timeline_action(request):
    context = {}
    context['interest'] = [t for t in Tag.objects.all()]
    blog = Blog.objects.filter(user=request.user).order_by("-create_time")
    context['blog'] = blog
    print(context['blog'])
    if not blog:
        context['error'] = "You haven't create any blog yet, come back later"
    return render(request,"pittsTime/timeLine.html",context)

# @login_required
# def my_gallery_action(request):
#     context = {}
#     return render(request,"pittsTime/gallery.html",context)

@login_required
def myinterest_action(request):
    context={}
    context['interest'] = [t for t in Tag.objects.all()]
    profile = Profile.objects.get(user=request.user)
    my_interest = [m for m in profile.interest.all()]
    context['myinterest'] = my_interest
    context['myinterest_empty'] = len(my_interest) == 0
    name = [t.name for t in my_interest]
    blog = Blog.objects.filter(tags__name__in=name)
    context['blog'] = blog
    #blog = Blog.objects.get()
    return render(request,"PittsTime/interest.html", context)

@login_required
def next_action(request):
    context={}
    context['interest'] = [t for t in Tag.objects.all()]
    return render(request, "PittsTime/blognext.html", context)

@login_required
def blog_detail_action(request,id):
    context = {}
    try:
        int(id)
        blog = Blog.objects.get(id=id)
    except:
        context['error'] = 'parameter in the url is not validate'
        context['interest'] = [t for t in Tag.objects.all()]
        return render(request,"PittsTime/error.html", context)
    context['interest'] = [t for t in Tag.objects.all()]
    # print(id)
    blog = Blog.objects.get(id=id)
    # print(blog)
    context['blog']=blog
    profile = Profile.objects.get(user=blog.user)
    context['profile'] = profile
    context['tags'] = blog.tags.all()
    context['comments'] = Comment.objects.filter(blog=blog)
    recent_four_blogs = Blog.objects.order_by('-id')[:4]
    recent_four_blogs_ascending = reversed(recent_four_blogs)
    context['recentblogs'] = recent_four_blogs_ascending
    print(blog.location)
    print(len(blog.location))
    if blog.location is not None and blog.location !='' and len(blog.location) != 0:
        yelpName = blog.location.split(',')[0]
        yelpLocation = blog.location
        # print(yelpName,yelpLocation)
        yelpInfo = Get_Info(yelpName,yelpLocation)
        context['yelpInfo'] = yelpInfo
    try:
        profile = Profile.objects.get(user=blog.user)
    except Profile.DoesNotExist:
        profile = Profile(user = blog.user)
        profile.save()
    context['profile']=profile

    return render(request,"PittsTime/blog-detail.html", context)


@login_required
def add_location(request):
    pictures = []
    blog = Blog.objects.filter(user=request.user).order_by('create_time').reverse()
    target = blog[0]
    if request.method == 'GET':
        target.save()
        return redirect(reverse('home'))
    print(request.POST['location'])
    target.location = request.POST['location']
    target.save()
    response_text = "{\"success\": \"success\", \"url\": \"/PittsTime/home\"}"

    # scrape all pictures in blog into picture models
    blog_content = blog[0].Blog_content
    photo_album = re.findall(r'<img [^>]*src="([^"]+)',blog_content)
    for photo in photo_album:
        print(photo)
        if photo.find("png")!=-1 or photo.find("jpeg")!=-1 or photo.find("jpg")!=-1:
            pictures.append(photo)
    for p in pictures:
        print(p)
        new_picture = Picture(picture_link=p,blog=blog[0])
        new_picture.save()

    #return redirect(reverse('home'))
    return HttpResponse(response_text, content_type='application/json')

@login_required
def add_comment(request):
    if request.method != 'POST':
        raise Http404

    if not 'postID' in request.POST or not 'comment_text' in request.POST or not request.POST['comment_text']:
        context = {}
        context['error'] = 'You must provide valid parameters'
        context['interest'] = [t for t in Tag.objects.all()]
        return render(request, "PittsTime/error.html", context)

    new_comment = Comment(blog=Blog.objects.get(id=request.POST.get('postID',0)),comment_text=request.POST['comment_text'],user=request.user,create_time=timezone.now()) # Other fields to add
    new_comment.save()
    #response_text = json.dumps(new_comment)
    response_text = "{" +"\"comment\":" + serializers.serialize('json', [ new_comment, ])+","+"\"user\":" + serializers.serialize('json', [ new_comment.user, ])+"}"
    #response_text = serializers.serialize('json', [ new_comment, ])
    print(response_text)

    return HttpResponse(response_text, content_type='application/json')

@login_required
def spotify(request):
    context={}
    context['interest'] = [t for t in Tag.objects.all()]
    context['redirectURL'] = app_Authorization()
    return render(request,"PittsTime/searchTrack.html",context)

@login_required
def spotify_callback(request):
    context={}
    context['interest'] = [t for t in Tag.objects.all()]
    if request.GET['code']:
        context['code'] = request.GET['code']
    else:
        context['redirectURL'] = app_Authorization()
    return render(request,"PittsTime/searchTrack.html",context)

@login_required
def search_track(request):
    context = {}
    track_name = request.GET['track_name']
    if not track_name or len(track_name) == 0:
        context['error'] = 'Please try again with validate information'
        context['interest'] = [t for t in Tag.objects.all()]
        auth_token = request.GET['code']
        if (request.GET['authorization_header']):
            authorization_header = json.loads(request.GET['authorization_header'].replace("\'", "\""))
        else:
            try:
                authorization_header = user_Authorization(auth_token)
            except:
                context['error'] = 'You change the code in the hidden field'
                return render(request, "PittsTime/error.html", context)
        context['authorization_header'] = authorization_header
        context['code'] = auth_token
    else:
        auth_token = request.GET['code']

        context['interest'] = [t for t in Tag.objects.all()]

        context['track_name'] = track_name
        if(request.GET['authorization_header']):
            try:
                authorization_header = json.loads(request.GET['authorization_header'].replace("\'", "\""))
            except:
                context['error'] = 'You change the code in the hidden field'
                return render(request, "PittsTime/error.html", context)
        else:
            try:
                authorization_header = user_Authorization(auth_token)
            except:
                context['error'] = 'You change the code in the hidden field'
                return render(request, "PittsTime/error.html", context)
        context['authorization_header'] = authorization_header
        # spotify_profile = Profile_Data(authorization_header)
        srcs = []
        try:
            track_uris = Track_Data(authorization_header,track_name)
            for track_uri in track_uris:
                srcs.append(Button_src(track_uri))
        except:
            context['error'] = 'You change the code in the hidden field'
            return render(request, "PittsTime/error.html", context)
        if len(srcs) == 0:
            context['error'] = 'Please try again with validate information'
        else:
            context['srcs'] = srcs
        context['code'] = auth_token
    return render(request, "PittsTime/searchTrack.html", context)

@login_required
def add_track(request):
    if request.method != 'POST':
        return Http404

    track_src = request.POST['track_src']
    track_name = request.POST['track_name']
    blog = Blog.objects.filter(user=request.user).order_by('create_time').reverse()
    target = blog[0]
    target.song_name = track_name
    target.song_src = track_src
    target.save()
    return redirect(reverse('createBlog_next'))

@login_required
def one_interest(request, id):
    context = {}
    try:
        int(id)
        t = Tag.objects.get(id=id)
    except:
        context['error'] = 'parameter in the url is not validate'
        context['interest'] = [t for t in Tag.objects.all()]
        return render(request, "PittsTime/error.html", context)
    context['interest'] = [t for t in Tag.objects.all()]
    interests = Profile.objects.get(user=request.user).interest.all()
    if 'myinterest' in request.path:
        context['myinterest'] = interests
    else:
        context['following'] = interests

    t = Tag.objects.get(id=id)
    name = []
    photo_album = []
    pictures = []
    name.append(t.name)
    blog = Blog.objects.filter(tags__name__in=name)
    context['blog'] = blog
    for b in blog:
        photo_album = Picture.objects.filter(blog=b)
        #print(photo_album)
        pictures.extend(photo_album)
    #print(pictures)
    #for p in pictures:
        #print(p.picture_link)
    context['picture'] = pictures
    return render(request,"PittsTime/interest.html", context)

@login_required
def add_interest(request, id):
    try:
        int(id)
        t = Tag.objects.get(id=id)
    except:
        context = {}
        context['error'] = 'parameter in the url is not validate'
        context['interest'] = [t for t in Tag.objects.all()]
        return render(request, "PittsTime/error.html", context)
    profile = Profile.objects.get(user=request.user)
    t = Tag.objects.get(id=id)
    profile.interest.add(t)
    profile.save()
    #print(request.path)
    if 'profile' in request.path:
        return redirect(reverse('myprofile'))
    elif 'myinterest' in request.path:
        return redirect(reverse('interest'))
    else:
        return redirect(reverse('tag', kwargs={'id': id}))

@login_required
def delete_interest(request, id):
    try:
        int(id)
        t = Tag.objects.get(id=id)
    except:
        context = {}
        context['error'] = 'parameter in the url is not validate'
        context['interest'] = [t for t in Tag.objects.all()]
        return render(request, "PittsTime/error.html", context)
    profile = Profile.objects.get(user=request.user)
    t = Tag.objects.get(id=id)
    profile.interest.remove(t)
    profile.save()
    print(request.path)
    if 'profile' in request.path:
        return redirect(reverse('myprofile'))
    elif 'myinterest' in request.path:
        return redirect(reverse('interest'))
    else:
        return redirect(reverse('tag', kwargs={'id': id}))
