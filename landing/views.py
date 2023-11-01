from django.shortcuts import render, redirect
from .forms import WaitlistForm
from .forms import AIRequestStep1Form, AIRequestStep2Form
from .models import Waitlist
import requests
import json
from django.views.decorators.csrf import csrf_exempt


def index(request):
    if request.method == "POST":
        form = AIRequestStep1Form(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            request.session["phone_number"] = phone_number
            return redirect("landing:try_ai_agent_step2")
    return render(request, "landing/home.html")


def contact(request):
    return render(request, "landing/contact.html")


def join_waitlist(request):
    if request.method == "POST":
        form = WaitlistForm(request.POST)
        if form.is_valid():
            form.save()
            # Render the confirmation page after successful submission
            return render(request, "landing/confirmation.html")
    else:
        form = WaitlistForm()
    return render(request, "landing/join_waitlist.html", {"form": form})


def calling_page(request):
    phone_number = request.session.get("phone_number", "")
    print(f"Retrieved phone_number from session: {phone_number}")
    # Optional: delete the phone number from the session after retrieving it
    if "phone_number" in request.session:
        del request.session["phone_number"]
    return render(request, "landing/calling.html", {"phone_number": phone_number})


def try_ai_agent_step2(request):
    print("try_ai_agent_step2 function called")  # <-- Check if this view function is called at all
    if request.method == "POST":
        print("Request method is POST")  # <-- Check if the method is POST
        form = AIRequestStep2Form(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            phone_number = request.session["phone_number"]

            entry = Waitlist(
                phone_number=phone_number,
                email=email,
                ai_request=True,
            )
            entry.save()

            print("About to make the API call")

            # Make an API call
            response = requests.post(
                "https://callfusion-0c6c4ca2c8e6.herokuapp.com/dispatch_demo_call",
                json={
                    "is_joy" : True,
                    "phone_number": phone_number,
                    "prospect_details": {
                        "email": email,
                    }
                }
            )

            # Optional: Check if the API call was successful
            if response.status_code != 200:
                # Handle error, maybe log it or notify admins
                pass

            # Clear session data or further handle it
            #del request.session["phone_number"]
            return redirect("landing:calling_page")
        else:
            print("Form is not valid")  # <-- See if form validation fails
            print(form.errors)
    else:
        print("Request method is NOT POST")
        form = AIRequestStep2Form()

    return render(request, "landing/try_ai_agent_step2.html", {"form": form})