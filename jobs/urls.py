from django.contrib import admin
from django.urls import path, include
from curriculum.views import export_classic,export_class

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('jobsapp.urls')),
    path('', include('accounts.urls')),
    path('employee/', include('curriculum.urls')),
    #path('elasticsearch/',include('haystack.urls')),
   ]
