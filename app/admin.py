from django.contrib import admin
from .models import *
from .form import SourceTableForm
from django.urls import reverse
from django.utils.html import format_html

class GlobalSearchAdmin(admin.ModelAdmin):
    def global_search_link(self, obj=None):
        url = reverse('global_search')
        return format_html(f'<a href="{url}">Global Search</a>')

    global_search_link.short_description = 'Global Search'

from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['custom_links'] = [
            {
                'name': 'Global Search',
                'url': reverse('global_search'),
            }
        ]
        return super().index(request, extra_context)

admin_site = CustomAdminSite(name='custom_admin')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'session', 'department', 'regNo', 'search_export_link')

    def search_export_link(self, obj):
        url = reverse('search_export')  # The name of the custom URL
        return format_html(f'<a href="{url}">Search & Export</a>')

    search_export_link.short_description = 'Search & Export'

admin.site.register(AddStudents, StudentAdmin)

# Register your models here.
class SearchFilterAdmin(admin.ModelAdmin):
    # Display fields in the admin
    form =SourceTableForm
    list_display = ['name', 'session', 'score']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        session = request.GET.get('session')
        if session:
            qs =qs.filter(session=session)
            return qs
# Define a custom action for moving filtered data
@admin.action(description="Move filtered data to DestinationTable")
def move_to_destination(self, request, queryset):
    for record in queryset:
        DestinationTable.objects.create(
            name=record.name,
            session=record.session,
            score=record.score,
        )
    self.message_user(
        request, f"{queryset.count()} records moved to DestinationTable."
    )

    
class DestinationTableAdmin(admin.ModelAdmin):
    list_display = ('name', 'session', 'score')
class SessionFilter(admin.SimpleListFilter):
    title = 'Session'
    parameter_name = 'session'
    def lookups(self, request, model_admin):
        return SourceTable.lv
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(session=self.value())
        return queryset
class SearchFilterAdmin(admin.ModelAdmin):
    # Display fields in the admin
    form =SourceTableForm
    list_display = ['name', 'session', 'score']
    actions = [move_to_destination]
    list_filter = [SessionFilter]
# Register the admin models
admin.site.register(SourceTable, SearchFilterAdmin)
admin.site.register(DestinationTable, DestinationTableAdmin)

admin.site.register(news)
admin.site.register(TokenUser)
admin.site.register(Payments)
admin.site.register(Customize)
admin.site.register(Courses)
admin.site.register(CourseRegistration) 