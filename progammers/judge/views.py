from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from judge import models
# Create your views here.

from django.core.exceptions import *
from django.db import *
from django.db.models import *

from django import forms
from django.core.urlresolvers import reverse
from subprocess import Popen, PIPE
import time
import threading

LANG = {
    'py2': "Python 2",
    'py3': "Python 3",
    'cpp': "C++"
}


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class Command(object):
    def __init__(self, cmd, input=None):
        self.cmd = cmd
        self.input = input
        self.process = None
        self.output = None

    def run(self, timeout):
        def target():
            print 'Thread started'
            if self.input is not None:
                self.process = Popen(self.cmd, stdin=self.input, stdout=PIPE)
                self.output = self.process.communicate()[0]
            else:
                self.process = Popen(self.cmd, stdout=PIPE)
                self.output = self.process.communicate()[0]
            print 'Thread finished'


        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            print 'Terminating process'
            self.process.terminate()
            thread.join()
        return self.process.returncode, self.output


def login(request):
    try:
        print "Trying to Log In"
        m = models.User.objects.get(emailid=request.POST['username'])
        if m.password == request.POST['password']:
            request.session['email'] = m.emailid
            return request
        else:
            return False
    except KeyError:
        return request
    except Exception:
        return False


def index(request):

    login_result = login(request)
    template = loader.get_template('judge/index.html')
    logged = False
    credentials = False
    user = None
    if login_result:
        request = login_result
        try:
            user = request.session['email']
        except KeyError:
            pass
        if user:
            logged = True
    else:
        credentials = True

    context = RequestContext(request, {
            'form': LoginForm,
            'logged': logged,
            'incorrect_credentials': credentials,
            'email': user
        })
    return HttpResponse(template.render(context))


def logout(request):

    try:
        del request.session['email']
    except KeyError:
        pass

    template = loader.get_template('judge/index.html')
    logged = False
    credentials = False
    user = None

    context = RequestContext(request, {
            'form': LoginForm,
            'logged': logged,
            'incorrect_credentials': credentials,
            'email': user
        })
    return HttpResponse(template.render(context))


def css(request):
    template = loader.get_template('judge/styles.css')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))


def questions(request):
    login_result = login(request)
    template = loader.get_template('judge/questions.html')
    logged = False
    credentials = False
    user = None
    if login_result:
        request = login_result
        try:
            user = request.session['email']
        except KeyError:
            pass
        if user:
            logged = True
    else:
        credentials = True

    try:
        all_questions = models.Question.objects.all()

    except KeyError:
        pass

    context = RequestContext(request, {
            'form': LoginForm,
            'logged': logged,
            'incorrect_credentials': credentials,
            'email': user,
            'questions': all_questions
        })
    return HttpResponse(template.render(context))


def submit(request):
    login_result = login(request)
    template = loader.get_template('judge/submit.html')
    logged = False
    credentials = False
    user = None
    if login_result:
        request = login_result
        try:
            user = request.session['email']
        except KeyError:
            pass
        if user:
            logged = True
    else:
        credentials = True

    all_questions = models.Question.objects.all()

    if not request.POST:
        context = RequestContext(request, {
            'form': LoginForm,
            'logged': logged,
            'incorrect_credentials': credentials,
            'email': user,
            'questions': all_questions
        })
        return HttpResponse(template.render(context))

    print "Code Submitted"

    try:
        m = models.Submission.objects.all().aggregate(Max('s_id'))

        if m['s_id__max'] is None:
            m['s_id__max'] = 0


        qid = request.POST['question']
        code = request.POST['code']
        q = models.Question.objects.filter(id=qid)
        u = models.User.objects.filter(emailid=user)
        question = q[0].question.split(".")[0]

        print 'Submitting for question', question

        output_text = open("judge/data/Output/"+question+".out").read()

        lang = request.POST['lang']
        print  "Language Used", lang

        if lang == "py2" or lang =="py3":
            file_name = "judge/data/Codes/"+str(m['s_id__max'])+".py"
            with open(file_name, "w") as myfile:
                myfile.write(code)

            if lang == "py2":
                command = Command(
                    ["python", file_name],
                    open("judge/data/Input/"+question+".in")
                )
            if lang == "py3":
                command = Command(
                    ["python3", file_name],
                    open("judge/data/Input/"+question+".in")
                )
            retval, output = command.run(5)

            if retval == 0:
                if output == output_text:
                    result = 4
                else:
                    result = 1
            elif retval == 1:
                result = 0
            elif retval < 0:
                result = 2

        elif lang == "cpp":
            file_name = "judge/data/Codes/"+str(m['s_id__max'])+".cpp"
            with open(file_name, "w") as myfile:
                myfile.write(code)

            command = Command(
                ["g++", file_name],
            )
            retval, output = command.run(5)
            if retval == 1:
                result = 0
            else:
                command = Command(
                    ["./a.out"],
                    open("judge/data/Input/"+question+".in")
                )
                retval, output = command.run(5)
                if retval == 1:
                    result = 3
                elif retval == 0:
                    if output == output_text:
                        result = 4
                    else:
                        result = 1
                elif retval < 0:
                    result = 2

        sub = models.Submission(
            s_id=m['s_id__max']+1,
            q_id=q[0],
            status=result,
            u_id=u[0],
            lang=LANG[lang]
        )

        sub.save(force_insert=True)

    except KeyError:
        pass

    context = RequestContext(request, {
            'form': LoginForm,
            'logged': logged,
            'incorrect_credentials': credentials,
            'email': user,
            'questions': all_questions,
            'result': result
        })                                                                                                                                                                                                                                                                                                                                                                                                                                                              
    return HttpResponse(template.render(context))


def display_question(request, question):
    login_result = login(request)
    template = loader.get_template('judge/display_question.html')
    logged = False
    credentials = False
    user = None
    if login_result:
        request = login_result
        try:
            user = request.session['email']
        except KeyError:
            pass
        if user:
            logged = True
    else:
        credentials = True

    try:

        with open("judge/data//Questions/"+question) as myfile:
            text = myfile.read()
    except KeyError:
        pass

    context = RequestContext(request, {
            'form': LoginForm,
            'logged': logged,
            'incorrect_credentials': credentials,
            'email': user,
            'question': text
        })
    return HttpResponse(template.render(context))


def all_submissions(request):
    login_result = login(request)
    template = loader.get_template('judge/submissions.html')
    logged = False
    credentials = False
    user = None
    if login_result:
        request = login_result
        try:
            user = request.session['email']
        except KeyError:
            pass
        if user:
            logged = True
    else:
        credentials = True

    try:
        all_submissions = \
            models.Submission.objects.select_related().all().order_by('-s_id')

    except KeyError:
        pass

    context = RequestContext(request, {
            'form': LoginForm,
            'logged': logged,
            'incorrect_credentials': credentials,
            'email': user,
            'submissions': all_submissions
        })
    return HttpResponse(template.render(context))


def ranks(request):
    login_result = login(request)
    template = loader.get_template('judge/ranks.html')
    logged = False
    credentials = False
    user = None
    if login_result:
        request = login_result
        try:
            user = request.session['email']
        except KeyError:
            pass
        if user:
            logged = True
    else:
        credentials = True

    context = RequestContext(request, {
            'form': LoginForm,
            'logged': logged,
            'incorrect_credentials': credentials,
            'email': user
        })
    return HttpResponse(template.render(context))


def register(request):

    template = loader.get_template('judge/register.html')
    if not request.POST:
        context = RequestContext(request, {
            'form': LoginForm,
            'successfull': "0"
        })
        return HttpResponse(template.render(context))

    print "Registering New User", request.POST['name']


    user = models.User(name=request.POST['name'],
                       password=request.POST['password'],
                       emailid=request.POST['email'])

    try:
        user.save(force_insert=True)
        successfull = '1'
    except IntegrityError:
        successfull = '2'

    context = RequestContext(request, {
        'form': LoginForm,
        'successfull': successfull,
    })
    return HttpResponse(template.render(context))