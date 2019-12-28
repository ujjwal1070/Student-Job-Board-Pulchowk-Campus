from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.core.files.storage import get_storage_class
from django.utils.six import BytesIO
import qrcode
from qrcode.image.pure import PymagingImage
from django.conf import settings

CURRICLUM_USER = getattr(settings, 'CURRICULUM_USER', '')


@python_2_unicode_compatible
class Resume(models.Model):
    firstname = models.CharField(max_length=150, verbose_name=_("First name"))
    lastname = models.CharField(max_length=150, verbose_name=_("Last name"))
    user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='resumes',on_delete=models.CASCADE,default=None)
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Title"))
    resume = models.TextField(max_length=3000, blank=True, null=True, verbose_name=_("resume"), help_text=_("Short profile's description"))
    image = models.ImageField(upload_to='user_images', blank=True, null=True, verbose_name=_("image"))

    phone = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("phone"))
    website = models.URLField(max_length=300, blank=True, null=True, verbose_name=_("website"))
    email = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("email"))
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("city"))
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("country"))
   
    
    
    hobbies = models.TextField(max_length=1000, blank=True, null=True, verbose_name=_("hobbies"))
    skype = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Skype ID"))
    stackoverflow = models.IntegerField(blank=True, null=True, verbose_name=_("StackOverflow ID"))
    github = models.CharField(max_length=300, blank=True, null=True, verbose_name=_("GitHub ID"))
    

    class Meta:
        app_label = 'curriculum'
        verbose_name = _("resume")

    def __str__(self):
        return "%s %s - %s" % (self.firstname, self.lastname, self.title)

    def create_website_qrcode(self):
        storage = get_storage_class(settings.DEFAULT_FILE_STORAGE)()
        img_name = '%s-webite-qrcode.png' % self.id
        img_file = BytesIO()
        img = qrcode.make(self.website, image_factory=PymagingImage)
        img.save(img_file)
        storage.save(img_name, img_file)

    def website_qrcode(self):
        storage = get_storage_class(settings.DEFAULT_FILE_STORAGE)()
        img_name = '%s-webite-qrcode.png' % self.id
        if not storage.exists(img_name):
            self.create_website_qrcode()
        return storage.url('%s-webite-qrcode.png' % self.id)
    


@python_2_unicode_compatible
class AbstractUserResumes(models.Model):
    user = models.ForeignKey(CURRICLUM_USER, unique=True, verbose_name=_("user"),
                             help_text=_("User associated with resume."),on_delete=models.CASCADE)
    resumes = models.ManyToManyField(Resume)

    class Meta:
        abstract = True

    def __str__(self):
        return '%s resume(s)' % self.user
