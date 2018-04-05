from django.shortcuts import render, get_object_or_404, redirect
from main.common import get_navbar_item
from documents.common import PDF_generate, add_empty_document, register_document

from .models import Report_Field, Report_Field_Type
from projects.models import Project, Project_category, Project_type
from contacts.models import Department
from documents.models import Doc_file

from .forms import ReportFieldForm


def view_report(request, project):
    project = get_object_or_404(Project, eng_name=project)

    fields = project.report_field_set.all()
    field_types = project.project_type.report_field_type_set.all().select_related('category')
    last_report = Doc_file.objects. \
        filter(document__in=project.document_set.filter(doc_type__eng_name='org_report')). \
        order_by('date').last()
    result = []
    for ft in field_types:
        try:
            field = fields.get(field_type=ft)
        except:
            field = ''
        result.append({'tp': ft, 'field': field})

    scroll_to = request.GET.get('scroll_to', None)
    if scroll_to:
        request.session['scroll_to'] = scroll_to

    return render(
        request,
        'project_reports/project_report.html',
        {
            'report_fields': result,
            'project': project,
            'nav_menu': [
                get_navbar_item('projects'),
                project.get_navbar_item(),
                get_navbar_item('report')],
            'sec_nav_menu': project.get_sec_nav_menu(active_nav='reports'),
            'last_report': last_report,
        })


def edit_report_field(request, project, field_type):
    project = get_object_or_404(Project, eng_name=project)
    field_type = get_object_or_404(Report_Field_Type, id=field_type)
    try:
        field = project.report_field_set.get(field_type=field_type)
    except:
        field = Report_Field(project=project, field_type=field_type)

    form = ReportFieldForm(request.POST or None, field_type=field_type, instance=field)

    if request.method == "POST" and form.is_valid():
        field = form.save()
        request.session['scroll_to'] = field.id
        return redirect('view_report', project=project.eng_name)
    else:
        return render(
            request,
            'project_reports/report_field_form.html',
            {
                'form': form,
                'form_header': 'Редактирование отчета',
                'nav_menu': [
                    get_navbar_item('projects'),
                    project.get_navbar_item(),
                    get_navbar_item('report')],
            })


def generate_report(request, project):
    project = get_object_or_404(Project, eng_name=project)
    project_current_stage = project.get_current_stage()
    fields = project.report_field_set.filter(field_type__project_types=project.project_type)
    signee = {'user': request.user, 'roles': project.get_user_roles(request.user)}

    document = add_empty_document(doc_type='org_report', objects_list=[project])
    reg = register_document(
        user=request.user,
        document=document,
        department=get_object_or_404(Department, name="Отдел 7910"),
    )

    PDF_generate(
        document=document,
        user=request.user,
        template='project_reports/PDF_project_report.html',
        template_data={
            'project': project,
            'project_current_stage': project_current_stage,
            'reg': reg,
            'fields': fields,
            'signee': signee,
        },
    )

    return redirect(document.get_file_url())


def consolidated_report(request, category=None):
    status = request.GET.getlist('status', ['ACT', 'FUT'])
    projects = Project.objects.filter(status__in=status)
    own_p = False
    all_p = True
    if category:
        category = get_object_or_404(Project_category, eng_name=category)
        projects = projects.filter(project_type__category=category)
        all_p = False
    elif request.resolver_match.url_name == 'own_projects_report':
        user = request.user
        projects = projects.filter(project_user__user=user) | projects.filter(watchers=user)
        projects = projects.distinct()
        own_p = True
        all_p = False

    all_types = set(projects.values_list('project_type', flat=True))

    all_field_types = Report_Field_Type.objects.filter(project_types__id__in=all_types, has_status=True).distinct()
    project_fields = []
    for project in projects:
        fields = []
        for ft in all_field_types:
            try:
                field = project.report_field_set.get(field_type=ft)
            except:
                field = None
            fields.append(field)
        project_fields.append({'project': project, 'fields': fields})

    return render(
        request,
        'project_reports/consolidated_report.html',
        {
            'project_fields': project_fields,
            'all_field_types': all_field_types,
            'categories': Project_category.objects.all(),
            'category': category,
            'status': status,
            'own_p': own_p,
            'all_p': all_p,
            'nav_menu': [
                get_navbar_item('projects'),
                get_navbar_item('projects_reports')],
        })
