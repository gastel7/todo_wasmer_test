from django.db import connection
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Task


def index(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        if title:
            Task.objects.create(title=title[:200])
        return redirect("index")
    return render(request, "tasks/index.html", {"tasks": Task.objects.all()})


@require_POST
def toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.done = not task.done
    task.save(update_fields=["done"])
    return redirect("index")


@require_POST
def delete(request, pk):
    get_object_or_404(Task, pk=pk).delete()
    return redirect("index")


def health(request):
    """Page de diagnostic : /health/ -> prouve que Django ET la base répondent."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return JsonResponse(
            {"status": "ok", "db_vendor": connection.vendor, "tasks": Task.objects.count()}
        )
    except Exception as exc:  # noqa: BLE001
        return JsonResponse(
            {"status": "error", "db_vendor": connection.vendor, "error": f"{type(exc).__name__}: {exc}"},
            status=500,
        )
