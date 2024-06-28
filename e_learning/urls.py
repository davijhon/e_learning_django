from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    # Allauth
    path('accounts/', include('allauth.urls')),

    # DJango-CKeditor-5
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    
    #Local Apps
    path('', include('courses.urls', namespace='courses')),
    path('students/', include('students.urls', namespace='students')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('payment/', include('payment.urls', namespace='payment')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)