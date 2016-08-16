from django.views.generic import \
    ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse

from .models import Equipment, RefuelingStop, Defect
from .forms import EquipmentForm, RefuelingStopForm, DefectForm


class EquipmentListView(ListView):
    model = Equipment
    template_name = "equipment/equipment_list.html"
    ordering = "name"


class EquipmentView(DetailView):
    model = Equipment

    def get_context_data(self, **kwargs):
        context = super(EquipmentView, self).get_context_data(**kwargs)
        context['refueling_stops'] = RefuelingStop.objects.filter(equipment=self.object.id).order_by('-mileage')
        context['defects'] = Defect.objects.filter(equipment=self.object.id).order_by('-mileage')
        return context


class EquipmentCreate(CreateView):
    model = Equipment
    form_class = EquipmentForm
    success_url = reverse_lazy('equipment.list')


class EquipmentUpdate(UpdateView):
    model = Equipment
    form_class = EquipmentForm
    success_url = reverse_lazy('equipment.list')


class EquipmentDelete(DeleteView):
    model = Equipment
    success_url = reverse_lazy('equipment.list')


class RefuelingStopCreate(CreateView):
    model = RefuelingStop
    form_class = RefuelingStopForm
    template_name = 'equipment/equipment_form.html'

    def get_form_kwargs(self):
        kwargs = super(RefuelingStopCreate, self).get_form_kwargs()

        equipment = Equipment(id=int(self.kwargs['pk']))
        kwargs['initial'].update({
            'equipment': equipment,
        })
        return kwargs

    def get_success_url(self):
        return reverse('equipment.view', args=(self.object.equipment.id,))


class RefuelingStopUpdate(UpdateView):
    model = RefuelingStop
    form_class = RefuelingStopForm
    template_name = 'equipment/equipment_form.html'

    def get_form_kwargs(self):
        kwargs = super(RefuelingStopUpdate, self).get_form_kwargs()

        equipment = Equipment(id=int(self.kwargs['equipment_pk']))
        kwargs['initial'].update({
            'equipment': equipment,
        })
        return kwargs

    # an updated Refueling Stop might change something in a younger Refueling Stop
    # this flag is to cascade the save method once to a younger object if present
    def form_valid(self, form):
        form.instance.cascade_save = True
        return super(RefuelingStopUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse('equipment.view', args=(self.object.equipment.id,))


class RefuelingStopDelete(DeleteView):
    model = RefuelingStop
    template_name = 'equipment/equipment_confirm_delete.html'

    def get_success_url(self):
        return reverse('equipment.view', args=(self.object.equipment.id,))


class DefectCreate(CreateView):
    model = Defect
    form_class = DefectForm
    template_name = 'equipment/equipment_form.html'

    def get_form_kwargs(self):
        kwargs = super(DefectCreate, self).get_form_kwargs()

        equipment = Equipment(id=int(self.kwargs['pk']))
        kwargs['initial'].update({
            'equipment': equipment,
        })
        return kwargs

    def get_success_url(self):
        return reverse('equipment.view', args=(self.object.equipment.id,))


class DefectUpdate(UpdateView):
    model = Defect
    form_class = DefectForm
    template_name = 'equipment/equipment_form.html'

    def get_form_kwargs(self):
        kwargs = super(DefectUpdate, self).get_form_kwargs()

        equipment = Equipment(id=int(self.kwargs['equipment_pk']))
        kwargs['initial'].update({
            'equipment': equipment,
        })
        return kwargs

    def get_success_url(self):
        return reverse('equipment.view', args=(self.object.equipment.id,))


class DefectDelete(DeleteView):
    model = Defect
    template_name = 'equipment/equipment_confirm_delete.html'

    def get_success_url(self):
        return reverse('equipment.view', args=(self.object.equipment.id,))
