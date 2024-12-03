from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from payments.models import Payments
from .forms import TariffingFilterForm






def es_moderador(user):
    """Verifica si el usuario pertenece al grupo Moderador."""
    return user.groups.filter(name="Moderador").exists()

@user_passes_test(es_moderador)
def consultar_tarifas(request):
    form = TariffingFilterForm(request.GET)
    pagos = Payments.objects.all()

    if form.is_valid():
        fecha_inicio = form.cleaned_data.get("fecha_inicio")
        fecha_fin = form.cleaned_data.get("fecha_fin")
        abogado = form.cleaned_data.get("abogado")
        canal = form.cleaned_data.get("canal")
        

        if fecha_inicio:
            pagos = pagos.filter(fecha_pago__gte=fecha_inicio)
        if fecha_fin:
            pagos = pagos.filter(fecha_pago__lte=fecha_fin)
        if abogado:
            pagos = pagos.filter(cliente__abogado=abogado)
        if canal:
            pagos = pagos.filter(canal_pago=canal)
        

    return render(request, "create_tariff.html", {"form": form, "pagos": pagos})
