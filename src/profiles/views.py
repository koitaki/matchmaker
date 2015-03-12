# Create your views here.

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect
from django.forms.models import modelformset_factory

from questions.matching import points, match_percentage
from matches.models import Match

from .models import Address, Job, UserPicture
from .forms import AddressForm, JobForm, UserPictureForm


def home(request):
    return render_to_response('profiles/home.html', locals(), context_instance=RequestContext(request))


def all(request):
    users = User.objects.filter(is_active=True)
    return render_to_response('profiles/all.html', locals(), context_instance=RequestContext(request))


def single_user(request, username):
    try:
        user = User.objects.get(username=username)
        if user.is_active:
            single_user = user
    except:
        raise Http404
    set_match, created = Match.objects.get_or_create(from_user=request.user, to_user=single_user)
    set_match.percent = round(match_percentage(request.user, single_user), 4)
    set_match.save()

    match = set_match.percent * 100
    return render_to_response('profiles/single_user.html', locals(), context_instance=RequestContext(request))


def edit_profile(request):
    user = request.user
    picture = UserPicture.objects.get(user=user)
    user_picture_form = UserPictureForm(request.POST or None, request.FILES or None, prefix='picture', instance=picture)
    addresses = Address.objects.filter(user=user)
    jobs = Job.objects.filter(user=user)

    AddressFormset = modelformset_factory(Address, form=AddressForm, extra=1)
    formset_a = AddressFormset(queryset=addresses)

    JobFormset = modelformset_factory(Job, form=JobForm, extra=1)
    formset_j = JobFormset(queryset=jobs)

    if user_picture_form.is_valid():
        form3 = user_picture_form.save(commit=False)
        form3.save()

    return render_to_response('profiles/edit_profile.html', locals(), context_instance=RequestContext(request))


def edit_locations(request):
    if request.method == 'POST':
        user = request.user
        addresses = Address.objects.filter(user=user)

        AddressFormset = modelformset_factory(Address, form=AddressForm, extra=1)
        formset_a = AddressFormset(request.POST or None, queryset=addresses)

        if formset_a.is_valid():
            for form in formset_a:
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.save()

            messages.success(request, 'Profile details updated')
        else:
            messages.error(request, 'Profile details failed to update')

        return HttpResponseRedirect('/edit/')

    else:
        return Http404

def edit_jobs(request):
    if request.method == 'POST':
        user = request.user
        jobs = Job.objects.filter(user=user)

        JobFormset = modelformset_factory(Job, form=JobForm, extra=1)
        formset_j = JobFormset(request.POST, queryset=jobs)

        if formset_j.is_valid():
            for form in formset_j:
                new_form = form.save(commit=False)
                new_form.save()

            messages.success(request, 'Profile details updated')
        else:
            messages.error(request, 'Profile details failed to update')

        return HttpResponseRedirect('/edit/')

    else:
        return Http404

