"""
Views that can used by developer for easily export resume as PDF.
"""
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.forms import modelformset_factory

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from curriculum import export
from curriculum.models import Resume,ProjectItem,SkillItem,CertificationItem,Training,Experience,LanguageItem,Language
from accounts.models import User
from django.template.loader import get_template
from curriculum.forms import LanguageForm, LanguageItemForm, ResumeForm, SkillForm, SkillItemForm, CertificationForm, CertificationItemForm, ExperienceForm, ProjectForm, ProjectItemForm, TrainingForm

from django.conf import settings
def export_single_page(request):
    """Get a resume in a single page PDF."""
    #resume = get_object_or_404(Resume.objects.filter(firstname='Vijay'))
    current_user=request.user
    pdf, result = export.export_pdf(current_user, export.single_page)
    raw_pdf = result.getvalue()
    if not pdf.err:
        return HttpResponse(raw_pdf, content_type='application/pdf')
    return HttpResponse('We had some errors.')

def export_classic(request):
    """Get a resume in a PDF with classic format."""
    #resume = get_object_or_404(Resume.objects.filter(id=resume_id))
    #resume = get_object_or_404(Resume.objects.filter(user=request.user))
    current_user=request.user
    pdf, result = export.export_pdf(current_user, export.classic)
    raw_pdf = result.getvalue()
    if not pdf.err:
        return HttpResponse(raw_pdf, content_type='application/pdf')
    return HttpResponse('We had some errors.')

def export_classic1(request):
    """Get a resume in a PDF with classic format."""
    #resume = get_object_or_404(Resume.objects.filter(id=resume_id))
    #resume = get_object_or_404(Resume.objects.filter(firstname='Vijay'))
    current_user=request.user
    pdf, result = export.export_pdf(current_user, export.classic1)
    raw_pdf = result.getvalue()
    if not pdf.err:
        return HttpResponse(raw_pdf, content_type='application/pdf')
    return HttpResponse('We had some errors.')


def export_class(request):
    """
    Create a classic resume in :mod:`xhtml2pdf` format.
    """
    resume = get_object_or_404(Resume.objects.filter(user=request.user))
    #resume=Resume.objects.get(firstname=first_name)
    current_user = request.user
    context = {
        'pagesize': 'a4',
        'resume': resume,
        'skills': current_user.skills.order_by('category', '-weight'),
        'projects': current_user.projects.order_by('-weight'),
        'experiences': current_user.experiences.order_by('-start_year'),
        'trainings': current_user.trainings.order_by('-start_year', '-start_month'),
        'certifications': current_user.certifications.order_by('-end_year', '-end_month'),
    }
   # return get_template('curriculum/test1.html').render(context)
    return render(request,'curriculum/cvpreview.html',context)

"""
def skillitem(request):
    if request.method=="POST":
        form=ExperienceForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect()
            except:
                pass
    else:
        form=ExperienceForm()
    return render(request,"producttemp.html",{'form':form})
"""

def addlanguage(request):
    form=LanguageForm(request.POST or None)
    
    if form.is_valid():
        form.save()

    context={
        'form':form
    }
    return render(request,"curriculum/language.html",context)

def addlanguageitem(request):
    form=LanguageItemForm(request.POST or None)
   
    if form.is_valid():
        instance=form.save(commit=False)
        instance.user=request.user
        instance.resume= Resume.objects.get(user=request.user)
        instance.save()

    context={
        'form':form
    }
    return render(request,"curriculum/languageitem.html",context)

#@login_required(login_url="")
def addresume(request):
    
    form=ResumeForm(request.POST or None, request.FILES)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.user=request.user
        instance.firstname= request.user.first_name
        instance.lastname = request.user.last_name
        instance.save()

    context={
        'form':form
    }
    return render(request,"curriculum/resume.html",context)

def addskill(request):
    form=SkillForm(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()

    context={
        'form':form
    }
    return render(request,"curriculum/skill.html",context)

def addskillitem(request):
    form=SkillItemForm(request.POST or None, request.FILES)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.user=request.user
        instance.resume= Resume.objects.get(user=request.user)
        instance.save()

    context={
        'form':form
    }
    return render(request,"curriculum/skillitem.html",context)

def addcertification(request):
    form=CertificationForm(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()

    context={
        'form':form
    }
    return render(request,"curriculum/certification.html",context)

def addcertificationitem(request):
    form=CertificationItemForm(request.POST or None, request.FILES)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.user=request.user
        instance.resume= Resume.objects.get(user=request.user)
        instance.save()

    context={
        'form':form
    }
    return render(request,"curriculum/certificationitem.html",context)

def addexperience(request):
    form=ExperienceForm(request.POST or None, request.FILES)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.user=request.user
        instance.resume= Resume.objects.get(user=request.user)
        instance.save()

    context={
        'form':form
    }
    return render(request,"curriculum/experience.html",context)

def addproject(request):
    form=ProjectForm(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()

    context={
        'form':form
    }
    return render(request,"curriculum/project.html",context)

def addprojectitem(request):
    form=ProjectItemForm(request.POST or None, request.FILES)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.user=request.user
        instance.resume= Resume.objects.get(user=request.user)
        instance.save()

    context={
        'form':form
    }
    return render(request,"curriculum/projectitem.html",context)

def addtraining(request):
    form=TrainingForm(request.POST or None, request.FILES)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.user=request.user
        instance.resume= Resume.objects.get(user=request.user)
        instance.save()

    context={
        'form':form
    }
    return render(request,"curriculum/training.html",context)

def menulist(request,*args,**kwargs):
    return render(request,"curriculum/menulist.html",{})


