from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages

from .models import Pet, PetType
from .forms import PetForm
from owners.models import Owner

class PetDetailView(DetailView):
    """View for displaying pet details"""
    model = Pet
    template_name = 'pets/pet_detail.html'
    context_object_name = 'pet'

class PetCreateView(CreateView):
    """View for creating a new pet"""
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet_form.html'

    def get_form_kwargs(self):
        """Pass owner_id to the form if provided in URL"""
        kwargs = super().get_form_kwargs()
        if 'owner_id' in self.kwargs:
            kwargs['owner_id'] = self.kwargs['owner_id']
        return kwargs

    def get_context_data(self, **kwargs):
        """Add owner to context if owner_id is provided"""
        context = super().get_context_data(**kwargs)
        if 'owner_id' in self.kwargs:
            context['owner'] = get_object_or_404(Owner, pk=self.kwargs['owner_id'])
        return context

    def form_valid(self, form):
        """Ensure owner is set on the pet if owner_id is provided"""
        if 'owner_id' in self.kwargs and not form.instance.owner_id:
            form.instance.owner = get_object_or_404(Owner, pk=self.kwargs['owner_id'])
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to owner detail page if pet was created from there"""
        if self.object.owner:
            return reverse('owners:owner-detail', kwargs={'pk': self.object.owner.pk})
        return reverse('pets:pet-detail', kwargs={'pk': self.object.pk})

class PetUpdateView(UpdateView):
    """View for updating an existing pet"""
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet_form.html'

    def get_success_url(self):
        """Return to the pet's detail page after successful update"""
        return reverse('pets:pet-detail', kwargs={'pk': self.object.pk})
