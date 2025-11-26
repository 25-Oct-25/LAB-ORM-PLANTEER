from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.http import Http404
from .models import Plant, Comment, Country
from .forms import PlantForm, CommentForm
from django.contrib import messages


class PlantListView(ListView):
    model = Plant
    template_name = 'plants/plant_list.html'
    context_object_name = 'plants'
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        category_filter = self.request.GET.get('category')
        edible_filter = self.request.GET.get('is_edible')

        if category_filter:
            queryset = queryset.filter(category=category_filter)
        
        if edible_filter in ['True', 'False']:
            queryset = queryset.filter(is_edible=(edible_filter == 'True'))
        
        country_name = self.request.GET.get('country')
        if country_name:
            queryset = queryset.filter(countries__name=country_name)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_choices'] = Plant.CategoryChoices.choices 
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_edible'] = self.request.GET.get('is_edible', '')
        context['page_title'] = 'all plants'
        context['all_countries'] = Country.objects.all() 
        context['selected_country'] = self.request.GET.get('country')
        return context

plant_list_view = PlantListView.as_view()

def plant_detail_view(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(pk=plant.pk).order_by('?')[:4] 
    reviews = Comment.objects.filter(plant=plant).order_by('-created_at') 
    context = {
        'plant': plant,
        'comment_form': CommentForm(),
        'reviews': reviews,
        'related_plants': related_plants,
        'page_title': plant.name,
    }
    return render(request, 'plants/plant_detail.html', context)


@login_required(login_url='/accounts/login/') 
def plants_add_view(request):
    
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, 'You do not have permission to add new plants.')
        return redirect('plants:plant_list')
        
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            new_plant = form.save(commit=False)
            new_plant.creator = request.user 
            new_plant.save()
            form.save_m2m() 
            return redirect('plants:plant_list') 
    else:
        form = PlantForm()
    context = {
        'form': form,
        'page_title': 'Add New Plant'
    }
    return render(request, 'plants/add_plant.html', context)


@login_required(login_url='/accounts/login/') 
def plant_update_view(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    if plant.creator != request.user and not request.user.is_superuser:
        raise Http404("You are not authorized to edit this plant.") 
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('plants:plant_detail', pk=plant.pk)
    else:
        form = PlantForm(instance=plant)
    context = {'form': form, 'plant': plant, 'page_title': f'Update {plant.name}'}
    return render(request, 'plants/plant_update.html', context)


@login_required(login_url='/accounts/login/') 
def plant_delete_view(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    if plant.creator != request.user and not request.user.is_superuser:
        raise Http404("You are not authorized to delete this plant.") 
    if request.method == 'POST':
        plant.delete()
        return redirect('plants:plant_list')
    context = {'plant': plant, 'page_title': f'Delete {plant.name}'}
    return render(request, 'plants/plant_delete.html', context)


def plant_search_view(request):
    query = request.GET.get('q')
    results = Plant.objects.none()

    if query:
        results = Plant.objects.filter(
            Q(name__icontains=query) |
            Q(about__icontains=query) |
            Q(used_for__icontains=query)
        ).distinct().order_by('name')

    context = {
        'query': query,
        'results': results,
        'page_title': f'نتائج البحث لـ "{query}"',
    }
    return render(request, 'plants/plant_search.html', context)


@login_required(login_url='/accounts/login/') 
def add_review_view(request, plant_id):
    plant_object = get_object_or_404(Plant, pk=plant_id)
    
    if request.method == "POST":
        form = CommentForm(request.POST) 
        
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.plant = plant_object 
            
            if request.user.is_authenticated:
                new_review.user = request.user 
                new_review.full_name = request.user.username
                new_review.email = request.user.email
                new_review.save()
            messages.success(request, 'Review added successfully!')
            return redirect("plants:plant_detail", pk=plant_id)
        
        reviews = Comment.objects.filter(plant=plant_object).order_by('-created_at')
        related_plants = Plant.objects.filter(
            category=plant_object.category
        ).exclude(pk=plant_object.pk).order_by('?')[:4] 
        
        context = {
            'plant': plant_object, 
            'comment_form': form, 
            'reviews': reviews,
            'related_plants': related_plants,
            'page_title': plant_object.name,
        }
        return render(request, 'plants/plant_detail.html', context)
    return redirect("plants:plant_detail", pk=plant_id)