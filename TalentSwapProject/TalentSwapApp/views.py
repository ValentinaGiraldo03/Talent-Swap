from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
import os
from django.http import HttpResponse

from . forms import  LoginForm, CommentForm, ApplicationForm
#Forms es un archivo nuevo donde se guardan los formularios
from django.contrib.auth.decorators import login_required

#Modelos y funciones de autenticación
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

#Almacenar y gestionar archivos 
from django.core.files.storage import FileSystemStorage

from .forms import VacancyForm
from .models import Vacancy, Application

from .forms import UserTypeForm, CompanyRegistrationForm, EmployeeRegistrationForm
from django.contrib.auth.models import User
from .models import User, Company, Employee
from django.contrib import messages

def homepage(request):

    return render(request, 'TalentSwapApp/home.html') # Home de verdad


def register(request):
    if request.method == 'POST':
        user_type_form = UserTypeForm(request.POST)
        if user_type_form.is_valid():
            user_type = user_type_form.cleaned_data['user_type']
            if user_type == 'company':
                return redirect('register_company')
            elif user_type == 'employee':
                return redirect('register_employee')
    else:
        user_type_form = UserTypeForm()
    return render(request, 'TalentSwapApp/register.html', {'user_type_form': user_type_form})

def register_employee(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            employee_name = form.cleaned_data['employee_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            information = form.cleaned_data['information']
            interests = form.cleaned_data['interests']
            work_experience = form.cleaned_data['work_experience']
            user = Employee.objects.create_user(username=email, email=email, password=password, information=information)
            user.employee_name = employee_name
            user.interests = interests
            user.work_experience = work_experience
            user.save()
            messages.success(request, '¡Empleado registrado correctamente!')
            return redirect('dashboard_employee')  # Redirigir a la página de dashboard del empleado
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'TalentSwapApp/register_employee.html', {'form': form})

def register_company(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data['company_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            information = form.cleaned_data['information']
            company_type = form.cleaned_data['company_type']
            user = Company.objects.create_user(username=email, email=email, password=password, information=information)
            user.company_name = company_name
            user.company_type = company_type
            user.save()
            messages.success(request, '¡Compañía registrada correctamente!')
            return redirect('dashboard_company')  # Redirigir a la página de dashboard de la compañía
    else:
        form = CompanyRegistrationForm()
    return render(request, 'TalentSwapApp/register_company.html', {'form': form})




def dashboard_employee(request):
    # Lógica para mostrar el dashboard del empleado
    return render(request, 'TalentSwapApp/dashboard_employee.html')



def dashboard_company(request):
    # Lógica para mostrar el dashboard de la compañia
    return render(request, 'TalentSwapApp/dashboard_company.html')




def login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            
            if user is not None:

                auth.login(request, user)

                if Company.objects.filter(id = user.id):  # Verifica si es una compañía
                    return redirect('dashboard_company')
                else:
                    return redirect('dashboard_employee')

            
        
    context = {'loginform': form}
    
    return render(request, 'TalentSwapApp/login.html', context=context) 


def logout(request):

    auth.logout(request)

    return redirect('home') # Redirige a la página de inicio



# @login_required(login_url='login')
# def dashboard(request):
    
#     return render(request, 'TalentSwapApp/dashboard.html') 


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)

def vacancy_listemployee(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'TalentSwapApp/vacancy_listemployee.html',{
        'vacancies' : vacancies
    })

def vacancy_listcompany(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'TalentSwapApp/vacancy_listcompany.html',{
        'vacancies' : vacancies
    })

def upload_vacancy(request):
        if request.method == "POST":
            form = VacancyForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('vacancy_listcompany')
        else:
            form = VacancyForm()
        return render(request, 'TalentSwapApp/upload_vacancy.html', {'form': form})
    


def vacancy_detailemployee(request, id):
    template_name = 'TalentSwapApp/vacancy_detailsemployee.html'
    vacancy = get_object_or_404(Vacancy, id=id)
    print(vacancy.title)
    print(vacancy.description)
    print(vacancy.created_on)
    comments = vacancy.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.vacancy = vacancy
            new_comment.save()
    else:
        comment_form = CommentForm()


    current_user = request.user

    new_application = None
    if request.method == 'POST':
        application_form = ApplicationForm(data=request.POST)
        if application_form.is_valid():
            new_application = application_form.save(commit=False)
            new_application.vacancy = vacancy
            new_application.user = current_user
            new_application.save()
    else:
        application_form = ApplicationForm()

    return render(request, template_name, {'vacancy': vacancy,
                                        'new_application': new_application, 
                                        'application_form': application_form,
                                        'comments': comments,
                                        'new_comment': new_comment,
                                        'comment_form': comment_form})

def vacancy_detailcompany(request, id):
    template_name = 'TalentSwapApp/vacancy_detailscompany.html'
    vacancy = get_object_or_404(Vacancy, id=id)
    print(vacancy.title)
    print(vacancy.description)
    print(vacancy.created_on)
    comments = vacancy.comments.filter(active=True)
    applications = vacancy.applications.filter(status='pending')
    return render(request, template_name, {'vacancy': vacancy,
                                        'comments': comments,
                                        'applications': applications}
                                        )

def download_file(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'vacancies', 'GUÍA DE CONTRATO E INFORMACIÓN PERTINENTE.pdf')

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    else:
        return HttpResponse("El archivo no existe", status=404)
        
def matched_vacancies(request):
    
    if request.user.is_authenticated :
        user_id = request.user.id
        user = Employee.objects.filter(id=user_id)[0] #obtener el usuario de tipo empleado y no el general
        if hasattr(user, 'interests'):
            matched_vacancies = [] # creo la lista donde van a estar las vacantes del match
            interests = set(user.interests.split()) # Convertir los intereses del usuario en un conjunto de palabras
            for vacancy in Vacancy.objects.all():
                vacancy_description_words = set(vacancy.description.split())  # Convertir la descripción de la vacante en un conjunto de palabras
                    # Verificar si hay alguna intersección entre los intereses del usuario y las palabras en la descripción de la vacante
                if interests.intersection(vacancy_description_words): 
                        matched_vacancies.append(vacancy)
    else:
        return redirect('login')

    
    return render(request, 'TalentSwapApp/matched_vacancies.html', {'matched_vacancies': matched_vacancies})

def confirm_vacancy(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    if request.method == 'POST':
        # Cambiar el estado de la vacante a "no disponible" (status=False)
        vacancy.status = False
        vacancy.save()
        return redirect('vacancy_listemployee')
    return render(request, 'confirm_vacancy.html', {'vacancy': vacancy}) 

def reopen_vacancy_company(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    if request.method == 'POST':
        # Cambiar el estado de la vacante a "disponible" (status=True)
        vacancy.status = True
        vacancy.save()
        return redirect('dashboard_company')
    return render(request, 'reopen_vacancy_company.html', {'vacancy': vacancy})   

def statistics(request):
    # Obtener todos los empleados ordenados por experiencia laboral en meses
    employees = Employee.objects.order_by('work_experience')

    # Pasar los empleados a la plantilla
    return render(request, 'TalentSwapApp/statistics.html', {'employees': employees})

    

def applied_to_vacancy(request):
    # Obtener todas las aplicaciones de un usuario
    user = request.user
    applications = Application.objects.filter(user=user)
    return render(request, 'TalentSwapApp/applied_to_vacancy.html', {'applications': applications})
