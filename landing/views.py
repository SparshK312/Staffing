from django.shortcuts import render, redirect
from .forms import WaitlistForm
from .forms import AIRequestStep1Form, AIRequestStep2Form
from .models import Waitlist
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime 
import os
import pytz
from pytz import timezone
from django.utils import timezone as django_timezone
from datetime import timedelta
from django.utils import timezone
from .models import DemoUsage
from requests.auth import HTTPBasicAuth


# Function to initialize Google Sheets client
def init_gsheets_client():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    # Try to get credentials from environment variable
    creds_json = os.getenv('GOOGLE_SHEETS_CREDS')
    if creds_json:
        print("The google creds were found")  
        creds_dict = json.loads(creds_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    else:
        # Fallback to using a local file for credentials
        print("Environment variable not set, using local JSON file for credentials.")
        # Define the path to the local JSON credentials file
        creds_file_path = r'C:\Users\spars\OneDrive\Desktop\Staffing Website\call-fusion-auth-e2e882f33c5f.json'
        # Ensure the file exists
        if not os.path.exists(creds_file_path):
            raise FileNotFoundError(f"Credentials file not found at path: {creds_file_path}")
        # Create credentials from the JSON file
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file_path, scope)

    client = gspread.authorize(creds)
    return client

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
    print(
        "try_ai_agent_step2 function called"
    )  # <-- Check if this view function is called at all

    if request.method == "POST":
        print("Request method is POST")  # <-- Check if the method is POST
        form = AIRequestStep2Form(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            phone_number = request.session["phone_number"]

            print("About to make the API call")

            # Make the API call
            response = requests.post("https://dispatcher.callfusion-bcknd-1630.com/dispatch_live_agent", json = {"prospect_phone_number" : phone_number, "agent_id" : "joiy", "additional_args" : {"prospect_name" : ""}}, auth = HTTPBasicAuth("callfusionadmin", "callfusiontothemoon123")) 

            # Check if the API call was successful
            if response.status_code == 200:
                # Log usage
                DemoUsage.objects.create(phone_number=phone_number)

                # Save the details in the database
                entry = Waitlist.objects.create(**form.cleaned_data, phone_number=phone_number, ai_request=True)
                print("Saved Entry Company Name:", entry.company_name)

                # Set timezone to EST
                est = pytz.timezone('America/New_York')
                current_datetime = timezone.now().astimezone(est)

                date_str = current_datetime.strftime("%B %dth, %Y")  # e.g., "November 16th, 2023"
                time_str = current_datetime.strftime("%I:%M:%S %p")  # e.g., "10:53:32 PM"

                # Prepare the row data
                row_data = [
                entry.email,
                entry.phone_number,
                date_str,
                time_str
                ]

                # If successful, append data to Google Sheet
                client = init_gsheets_client()
                sheet = client.open("Landing Page Database").worksheet("ActivateStaff")
                sheet.append_row(row_data)

                return redirect("landing:calling_page")
            else:
                # If the call was not successful, show an error
                print(f"API call failed: {response.text}")
                return render(request, "landing/error.html", {"message": "There was an error with the AI agent call."})
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        print("Request method is NOT POST")
        form = AIRequestStep2Form()

    return render(request, "landing/try_ai_agent_step2.html", {"form": form})
