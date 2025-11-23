# plants/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Plant, Country
from .forms import PlantForm, PlantSearchForm, CommentForm


def plant_list(request):
    """
    صفحة جميع النباتات + تدعم الفلترة بالباراميترات:
      ?search=&category=&is_edible=&country=
    وتعرض شِيبس الدول للانتقال السريع.
    """
    # باراميترات الفلترة من الـ GET
    search       = (request.GET.get("search") or "").strip()
    category     = (request.GET.get("category") or "").strip()
    is_edible    = (request.GET.get("is_edible") or "").strip()  # "true"/"false"/""
    country_name = (request.GET.get("country") or "").strip()

    # كويري أساسي
    plants = Plant.objects.all().prefetch_related("countries").order_by("-created_at")

    # فلترة نصية
    if search:
        plants = plants.filter(
            Q(name__icontains=search) |
            Q(about__icontains=search) |
            Q(used_for__icontains=search)
        )

    # فلترة التصنيف
    if category:
        plants = plants.filter(category=category)

    # فلترة صالح للأكل
    if is_edible == "true":
        plants = plants.filter(is_edible=True)
    elif is_edible == "false":
        plants = plants.filter(is_edible=False)

    # فلترة بالدولة (بالاسم)
    if country_name:
        plants = plants.filter(countries__name__iexact=country_name)

    # نموذج البحث لملء القيم الحالية
    form = PlantSearchForm(initial={
        "search": search,
        "category": category,
        "is_edible": is_edible,
        # بإمكانك تمرير الدولة هنا لو تحب
    })

    countries = Country.objects.all()

    return render(request, "plants/plant_list.html", {
        "plants": plants,
        "form": form,
        "countries": countries,
        "active_country": country_name,
    })


def plants_by_country(request, country_name):
    """مسار مستقل لعرض نباتات دولة معينة."""
    country = get_object_or_404(Country, name__iexact=country_name)
    plants = Plant.objects.filter(countries=country).prefetch_related("countries")
    return render(request, "plants/plants_by_country.html", {
        "country": country,
        "plants": plants
    })


def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    comments = plant.comments.all()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.plant = plant
            new_comment.save()
            return redirect("plants:detail", plant_id=plant.id)
    else:
        form = CommentForm()

    related_plants = Plant.objects.filter(category=plant.category).exclude(id=plant.id)[:4]

    return render(request, "plants/plant_detail.html", {
        "plant": plant,
        "related_plants": related_plants,
        "comments": comments,
        "comment_form": form,
    })


def plant_create(request):
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save(commit=False)  # مهم لحفظ M2M لاحقًا
            plant.save()
            form.save_m2m()                  # حفظ countries
            # روح للتفاصيل بعد الإضافة (أو plants:all لو تحب)
            return redirect("plants:detail", plant_id=plant.id)
    else:
        form = PlantForm()
    return render(request, "plants/plant_form.html", {"form": form, "title": "Add Plant"})


def plant_update(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.save()
            form.save_m2m()  # تحديث الدول المرتبطة
            return redirect("plants:detail", plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)

    return render(request, "plants/plant_form.html", {"form": form, "title": "Update Plant"})


def plant_delete(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    if request.method == "POST":
        plant.delete()
        return redirect("plants:all")
    return render(request, "plants/plant_confirm_delete.html", {"plant": plant})


def plant_search(request):
    """
    صفحة البحث المتقدم باستخدام PlantSearchForm
    حقول: search / category / is_edible / country
    """
    form = PlantSearchForm(request.GET or None)
    plants = Plant.objects.all().prefetch_related("countries")

    if form.is_valid():
        search    = form.cleaned_data.get("search") or ""
        category  = form.cleaned_data.get("category") or ""
        is_edible = form.cleaned_data.get("is_edible") or ""
        country   = form.cleaned_data.get("country")   # ModelChoiceField أو None

        if search:
            plants = plants.filter(
                Q(name__icontains=search) |
                Q(about__icontains=search) |
                Q(used_for__icontains=search)
            )

        if category:
            plants = plants.filter(category=category)

        if is_edible == "true":
            plants = plants.filter(is_edible=True)
        elif is_edible == "false":
            plants = plants.filter(is_edible=False)

        if country:
            plants = plants.filter(countries=country)

    else:
        # لو الفورم غير صالح نرجّع نتيجة فاضية حتى ما نعرض كل شيء بالغلط
        plants = Plant.objects.none()

    return render(request, "plants/plant_search.html", {
        "form": form,
        "plants": plants,
    })
