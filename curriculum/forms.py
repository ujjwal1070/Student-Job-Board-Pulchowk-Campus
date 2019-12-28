from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import widgets
from django.contrib.staticfiles.templatetags.staticfiles import static
from curriculum import models


class ResumeExportForm(forms.Form):
    hide_image = forms.BooleanField(required=False)
    hide_resume = forms.BooleanField(required=False)

    hide_phone = forms.BooleanField(required=False)
    hide_city = forms.BooleanField(required=False)
    hide_country = forms.BooleanField(required=False)
    

    hide_email = forms.BooleanField(required=False)
    hide_website = forms.BooleanField(required=False)
    hide_skype = forms.BooleanField(required=False)
    hide_stackoverflow = forms.BooleanField(required=False)
    hide_github = forms.BooleanField(required=False)
    hide_experience_description = forms.BooleanField(required=False)
    hide_experience_environment = forms.BooleanField(required=False)
    hide_certification_description = forms.BooleanField(required=False)
    hide_training_description = forms.BooleanField(required=False)
   
    hide_project_url = forms.BooleanField(required=False)

    class Media:
        css = {'all': (static('admin/css/widgets.css'),), }

    def __init__(self, instance, *args, **kwargs):
        super(ResumeExportForm, self).__init__(*args, **kwargs)
        self.instance = instance
        self.fields['experiences'] = forms.ModelMultipleChoiceField(
            queryset=instance.experiences.all(),
            initial=instance.experiences.all(),
            widget=widgets.FilteredSelectMultiple(_("experiences"), is_stacked=False,
                    attrs={'size': 5, 'style': 'height: unset'}))
        self.fields['projects'] = forms.ModelMultipleChoiceField(
            queryset=instance.projects.all(),
            initial=instance.projects.all(),
            widget=widgets.FilteredSelectMultiple(_("projects"), is_stacked=False,
                    attrs={'size': 5, 'style': 'height: unset'}))
        self.fields['skills'] = forms.ModelMultipleChoiceField(
            queryset=instance.skills.order_by('skill__name'),
            initial=instance.skills.all(),
            widget=widgets.FilteredSelectMultiple(_("skills"), is_stacked=False,
                    attrs={'size': 5, 'style': 'height: unset'}))
        self.fields['certifications'] = forms.ModelMultipleChoiceField(
            queryset=instance.certifications.all(),
            initial=instance.certifications.all(),
            widget=widgets.FilteredSelectMultiple(_("certifications"), is_stacked=False,
                    attrs={'size': 5, 'style': 'height: unset'}))
        self.fields['trainings'] = forms.ModelMultipleChoiceField(
            queryset=instance.trainings.all(),
            initial=instance.trainings.all(),
            widget=widgets.FilteredSelectMultiple(_("trainings"), is_stacked=False,
                    attrs={'size': 3, 'style': 'height: unset'}))
        self.fields['languages'] = forms.ModelMultipleChoiceField(
            queryset=instance.languages.all(),
            initial=instance.languages.all(),
            widget=widgets.FilteredSelectMultiple(_("languages"), is_stacked=False,
                    attrs={'size': 4, 'style': 'height: unset'}))


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = models.Experience
        exclude = ()

    def clean(self):
        cleaned_data = super(ExperienceForm, self).clean()
        if cleaned_data.get('end_month') and not cleaned_data.get('end_year'):
            raise forms.ValidationError(_(
                "You must specify an end year with end month."))
        if cleaned_data.get('end_year'):
            if cleaned_data.get('end_year') < cleaned_data.get('start_year'):
                raise forms.ValidationError(_("End year is lower than start."))
        if cleaned_data.get('end_year') == cleaned_data.get('start_year'):
            if cleaned_data.get('end_month') < cleaned_data.get('start_month'):
                raise forms.ValidationError(_("End month is lower than start."))

    def clean_end_year(self):
        data = self.cleaned_data['end_year']
        if not self.cleaned_data['still'] and not data:
            raise forms.ValidationError(_(
                "You must specify an end year if experience is finished."))
        return data

class LanguageForm(forms.ModelForm):
    class Meta:
        model=models.Language
        fields=[
            'name', 
        ]

class LanguageItemForm(forms.ModelForm):
    class Meta:
        model=models.LanguageItem
        fields=[
             'level','language'
        ]

class ResumeForm(forms.ModelForm):
    class Meta:
        model=models.Resume
        fields = '__all__'
        exclude = ('user','firstname','lastname',)

class SkillForm(forms.ModelForm):
    class Meta:
        model=models.Skill
        fields = '__all__'


class SkillItemForm(forms.ModelForm):
    class Meta:
        model=models.SkillItem
        fields = '__all__'
        exclude = ('user','resume',)

class CertificationForm(forms.ModelForm):
    class Meta:
        model=models.Certification
        fields = '__all__'

class CertificationItemForm(forms.ModelForm):
    class Meta:
        model=models.CertificationItem
        fields = '__all__'
        exclude = ('user','resume',)

class ExperienceForm(forms.ModelForm):
    class Meta:
        model=models.Experience
        fields = '__all__'
        exclude = ('user','resume',)

class ProjectForm(forms.ModelForm):
    class Meta:
        model=models.Project
        fields = '__all__'

class ProjectItemForm(forms.ModelForm):
    class Meta:
        model=models.ProjectItem
        fields = '__all__'
        exclude = ('user','resume',)

class TrainingForm(forms.ModelForm):
    class Meta:
        model=models.Training
        fields = '__all__'
        exclude = ('user','resume',)

