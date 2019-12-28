from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import F,Value, CharField
from django.db.models.functions import Concat

from jobsapp.forms import ApplyJobForm
from jobsapp.models import Job, Applicant
from accounts.models import User
from curriculum.models import Resume,ProjectItem,SkillItem,CertificationItem,Training,Experience,LanguageItem,Language,Skill
from django.shortcuts import get_object_or_404
from curriculum.models import *


class HomeView(ListView):
    model = Job
    template_name = 'home.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return self.model.objects.all()[:6]
        

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        # if self.request.user.is_authenticated and self.request.user.role == 'employee':
            
        #     context['recommendations'] = self.model.objects.filter()[:3]
        if self.request.user.is_authenticated and self.request.user.role == 'employee' and self.request.user.skills.exists() :
            current_user= Resume.objects.get(user=self.request.user)
            skillset= Skill.objects.filter(items__resume=current_user).values_list('name',flat=True)
            for skill in skillset:
                if self.model.objects.filter(description__icontains=skill).exists():
                    context['recommendations'] = self.model.objects.filter(description__icontains=skill).distinct()            
        else:
            #context['trendings'] = self.model.objects.filter(created_at__month=timezone.now().month)[:3]
            context['trendings'] = self.model.objects.filter()[:3]
        return context


class SearchView(ListView):
    model = Job
    template_name = 'jobs/search.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return self.model.objects.filter(location__icontains=self.request.GET['location'],
                                         title__icontains=self.request.GET['position'])
class CandidateSearchView(ListView):
    model = Resume
    template_name = 'jobs/candidate_search.html'
    context_object_name = 'candidates'

    def get_queryset(self):
        # return self.model.objects.all().annotate(
        #                                          YOE=F('experiences__end_year')-F('experiences__start_year')
        #                                         ).filter(title__contains=self.request.GET['position'],
        #                                                  skills__skill__name__contains=self.request.GET['skill'],
        #                                                  YOE__gte=self.request.GET['experience']
        #                                                  ).distinct()

        resume_modified = self.model.objects.annotate(YOE=F('experiences__end_year')-F('experiences__start_year'),QUAL=Concat(F('trainings__degree'), Value('in'), F('trainings__field_of_study'), output_field=CharField()))
        returned_users=resume_modified.values('user').filter(title__icontains=self.request.GET['position'],
                                      skills__skill__name__icontains=self.request.GET['skill'],
                                      YOE__gte=self.request.GET['experience'],
                                      QUAL__icontains=self.request.GET['qualification']).distinct()
        return self.model.objects.filter(user__in=returned_users)                                                 
                                                         

                                         

class JobListView(ListView):
    model = Job
    template_name = 'jobs/jobs.html'
    context_object_name = 'jobs'
    paginate_by = 5

def applicant_profile(request,id):
    user = User.objects.get(id=id)
    resume = get_object_or_404(Resume.objects.filter(user=user))
    context = {
        'pagesize': 'a4',
        'resume': resume,
        'skills': user.skills.order_by('category', '-weight'),
        'projects': user.projects.order_by('-weight'),
        'experiences': user.experiences.order_by('-start_year'),
        'trainings': user.trainings.order_by('-start_year', '-start_month'),
        'certifications': user.certifications.order_by('-end_year', '-end_month'),
    }
   # return get_template('curriculum/test1.html').render(context)
    return render(request,'curriculum/cvpreview.html',context)



class JobDetailsView(DetailView):
    model = Job
    template_name = 'jobs/details.html'
    context_object_name = 'job'
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        obj = super(JobDetailsView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # redirect here
            raise Http404("Job doesn't exists")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ApplyJobView(CreateView):
    model = Applicant
    form_class = ApplyJobForm
    slug_field = 'job_id'
    slug_url_kwarg = 'job_id'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.info(self.request, 'Successfully applied for the job!')
            return self.form_valid(form)
        else:
            return HttpResponseRedirect(reverse_lazy('jobs:home'))

    def get_success_url(self):
        return reverse_lazy('jobs:jobs-detail', kwargs={'id': self.kwargs['job_id']})

    # def get_form_kwargs(self):
    #     kwargs = super(ApplyJobView, self).get_form_kwargs()
    #     print(kwargs)
    #     kwargs['job'] = 1
    #     return kwargs

    def form_valid(self, form):
        # check if user already applied
        applicant = Applicant.objects.filter(user_id=self.request.user.id, job_id=self.kwargs['job_id'])
        if applicant:
            messages.info(self.request, 'You already applied for this job')
            return HttpResponseRedirect(self.get_success_url())
        # save applicant
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

