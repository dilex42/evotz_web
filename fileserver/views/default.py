from pyramid.view import view_config, forbidden_view_config, notfound_view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from ..models import mymodel
from ..forms import CredentialsForm, UploadForm
import mongoengine
from pyramid.response import Response
from pyramid.security import remember, forget
import datetime

def is_latin(s):
    try:
        s.encode("latin-1")
        return True
    except UnicodeEncodeError:
        return False

@view_config(route_name='home', renderer='fileserver:/templates/home.jinja2')
def my_view(request):
    if mymodel.MetaInfo.objects().count() == 0 :
        mymodel.MetaInfo().save()
    meta = mymodel.MetaInfo.objects().first()
    time_now = datetime.datetime.now()
    if time_now >= meta.next_check :
        print('Check expired....')
        expired_files = mymodel.Files.objects(expires_at__lte=time_now)
        for file in expired_files :
            file.file.delete()
            file.delete()
        meta.next_check = meta.next_check+datetime.timedelta(hours=1)
        meta.save()
    form = UploadForm(request.POST)
    form.expires.process_data(datetime.datetime.now()+datetime.timedelta(hours=1))
    return {'username': request.authenticated_userid, 'form':form, 'title' :'Home page'}

@view_config(route_name='upload')
def upload_file(request) :
    form = UploadForm(request.POST)
    if request.method == 'POST' :
        if not form.validate():
            return Response(json={'status':'Error','errors':form.errors})
        file_data = request.POST['file']
        if file_data.bytes_read >26214400 :
            form.file_input.errors.append('File too big. Please select file less than 25MB.')
            return Response(json={'status':'Error','errors':form.errors})
        description = request.POST['description']
        expires = request.POST['expires']
        filename = file_data.filename
        file_name,file_ext = filename.split('.')
        if is_latin(file_name) :
            new_filename = file_name
        else :
            new_filename = 'uploaded_file'
            description = 'Original filename : ' + file_name + '||   Your description : ' + description
        new_filename += '.'+file_ext
        new_file = mymodel.Files()
        new_file.file.put(file_data.file, content_type = file_data.type, file_name = new_filename)
        if description :
            new_file.description = description
        new_file.expires_at = expires
        if request.authenticated_userid :
            user = mymodel.Users.by_name(request.authenticated_userid)
            new_file.user = user
        try:
            new_file.save()
        except Exception as e:
            return Response(json={'status':'Bad'})
        return Response(json={'status':'OK','file_id':str(new_file.id)})
    return HTTPFound(location=request.route_url('home'))

@view_config(route_name='download')
def download_file(request):
    file_id = request.matchdict.get('file_id','no id')
    try:
        my_file = mymodel.Files.objects(id=file_id).first()
    except mongoengine.errors.ValidationError as e:
        raise HTTPNotFound()
    if not my_file :
        raise HTTPNotFound()
    if my_file.expires_at <= datetime.datetime.now() :
        my_file.file.delete()
        my_file.delete()
        raise HTTPNotFound()
    file_body = my_file.file
    return Response(body=file_body.read(),content_type=file_body.content_type,content_disposition='attachment; filename=%s' % (file_body.file_name),charset='utf-8')

@view_config(route_name='preview')
def preview_file(request):
    file_id = request.matchdict.get('file_id','no id')
    try:
        my_file = mymodel.Files.objects(id=file_id).first()
    except mongoengine.errors.ValidationError as e:
        raise HTTPNotFound()
    if not my_file :
        raise HTTPNotFound()
    if my_file.expires_at <= datetime.datetime.now() :
        my_file.file.delete()
        my_file.delete()
        raise HTTPNotFound()
    file_body = my_file.file
    return Response(body=file_body.read(),content_type=file_body.content_type,content_disposition='filename=%s' % (file_body.file_name),charset='utf-8')

@view_config(route_name='login',renderer='fileserver:templates/login.jinja2')
@forbidden_view_config(renderer='fileserver:/templates/login.jinja2')
def login(request):
    if request.authenticated_userid :
        return HTTPFound(location=request.route_url('home'))
    form = CredentialsForm(request.POST)
    if request.method == 'POST' and form.validate():
        u = mymodel.Users.by_name(form.username.data)
        if u and u.verify_password(form.password.data.encode('utf8')):
            return HTTPFound(location=request.route_url('home'), headers=remember(request,u.username))
        form.username.errors.append('Wrong password or username')
        return {'form' :form,'title' : 'Sign In'}
    return {'form': form,'title' : 'Sign In'}

@view_config(route_name='register',renderer='fileserver:templates/register.jinja2')
def register(request) :
    if request.authenticated_userid :
        return HTTPFound(location=request.route_url('home'))
    form = CredentialsForm(request.POST)
    if request.method == 'POST' and form.validate():
        u = mymodel.Users(username=form.username.data)
        u.set_password(form.password.data.encode('utf8'))
        try:
            u.save()
        except mongoengine.errors.NotUniqueError as e:
            form.username.errors.append('Username already taken')
            return {'form' : form,'title':'Sign Up'} 
        return HTTPFound(location=request.route_url('home'), headers=remember(request,u.username))
    return {'form' : form,'title':'Sign Up'}

@view_config(route_name='logout',permission='manage')
def log_out(request) :
    return HTTPFound(location=request.route_url('home'), headers=forget(request))

@view_config(route_name='userfiles',permission='manage',renderer='fileserver:templates/userfiles.jinja2')
def user_files(request):
    user = mymodel.Users.by_name(request.authenticated_userid)
    files = mymodel.Files.objects(user=user)
    return {'files':files,'username':request.authenticated_userid,'title':'My files'}


@view_config(route_name='delete',permission='manage')
def delete_file(request):
    file_id = request.matchdict.get('file_id','no id')
    my_file = mymodel.Files.objects(id=file_id).first()
    if not my_file :
        return HTTPFound(location=request.route_url('userfiles'))
    user = mymodel.Users.by_name(request.authenticated_userid)
    if my_file.user != user :
        return Response('No rights')
    my_file.file.delete()
    my_file.delete()
    return HTTPFound(location=request.route_url('userfiles'))

@notfound_view_config(renderer='fileserver:/templates/404.jinja2')
def notfound_view(request):
    request.response.status = 404
    return {'username':request.authenticated_userid}