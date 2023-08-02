from django.contrib import admin
from Home.models import User,Problem,Submission,TestCases

admin.site.register(User)
admin.site.register(Problem)
admin.site.register(Submission)
admin.site.register(TestCases)