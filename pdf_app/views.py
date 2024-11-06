from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Document
from django.core.files.storage import default_storage
from .services.nlp_processor import get_answer, InsufficientQuotaError, RateLimitExceededError
import fitz  # PyMuPDF for PDF processing

def home(request):
    return render(request, "home.html")  # Main page with upload form

def upload_pdf(request):
    if request.method == "POST" and request.FILES.get("file"):
        pdf_file = request.FILES["file"]
        file_path = default_storage.save(f"uploads/{pdf_file.name}", pdf_file)
        document_text = extract_text_from_pdf(file_path)

        # Save the document details in the database
        Document.objects.create(
            filename=pdf_file.name,
            content=document_text
        )

        # Store document_text in the session to access it in the next view
        request.session['document_text'] = document_text

        # Redirect to the successful upload page
        return redirect("successful_upload")
    return JsonResponse({"error": "Invalid request"}, status=400)

def successful_upload(request):
    # Access the document_text from the session
    document_text = request.session.get('document_text', '')
    return render(request, "successful_upload.html", {"document_text": document_text})

def ask_question(request):
    if request.method == "POST":
        # Get the question from the POST request
        question = request.POST.get("question")
        
        # Retrieve the document_text from the session
        document_text = request.session.get('document_text', '')

        if not document_text:
            return JsonResponse({"error": "No document text available for the question"}, status=400)

        try:
            # Get the answer from the nlp_processor
            answer = get_answer(document_text, question)
            return render(request, "home.html", {"document_text": document_text, "answer": answer})
        except InsufficientQuotaError:
            return redirect("insufficient_quota")
        except RateLimitExceededError:
            return redirect("rate_limit_exceeded")
    return redirect("home")

def insufficient_quota(request):
    return render(request, "insufficient_quota.html")

def rate_limit_exceeded(request):
    return render(request, "rate_limit_exceeded.html")

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text
