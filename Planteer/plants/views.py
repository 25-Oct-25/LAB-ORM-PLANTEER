from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Plant, Comment
from .forms import PlantForm, CommentForm


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
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_choices'] = Plant.CategoryChoices.choices 
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_edible'] = self.request.GET.get('is_edible', '')
        context['page_title'] = 'all plantes'
        return context
        
plant_list_view = PlantListView.as_view()


def plant_detail_view(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
   
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.plant = plant 
            new_comment.save()
            return redirect('plants:plant_detail', pk=plant.pk)
    else:
        comment_form = CommentForm()

    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(pk=plant.pk).order_by('?')[:4] 

    context = {
        'plant': plant,
        'comment_form': comment_form,
        'comments': plant.comments.all().order_by('-created_at'),
        'related_plants': related_plants,
        'page_title': plant.name,
    }
    return render(request, 'plants/plant_detail.html', context)


class PlantCreateView(CreateView):
    model = Plant
    form_class = PlantForm
    template_name = 'plants/plant_form.html'
    
    def get_success_url(self):
        return reverse_lazy('plants:plant_detail', kwargs={'pk': self.object.pk})

plant_create_view = PlantCreateView.as_view()


class PlantUpdateView(UpdateView):
    model = Plant
    form_class = PlantForm
    template_name = 'plants/plant_form.html'
    
    def get_success_url(self):
        return reverse_lazy('plants:plant_detail', kwargs={'pk': self.object.pk})
        
plant_update_view = PlantUpdateView.as_view()


class PlantDeleteView(DeleteView):
    model = Plant
    template_name = 'plants/plant_confirm_delete.html'
    success_url = reverse_lazy('plants:plant_list') 
    
plant_delete_view = PlantDeleteView.as_view()


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