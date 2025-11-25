from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Contact
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string  # تصحيح اسم الدالة

def contact_page(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # حفظ البيانات في قاعدة البيانات
            contact = form.save()

            # تجهيز محتوى الإيميل من قالب HTML
            content_html = render_to_string("main/mail/confirmation.html", {
                'contact': contact
            })

            # البريد المستقبل
            send_to = contact.email

            # إنشاء رسالة البريد
            email_message = EmailMessage(
                subject="Confirmation",               # عنوان الرسالة
                body=content_html,                   # محتوى الرسالة HTML
                from_email=settings.EMAIL_HOST_USER, # البريد المرسل
                to=[send_to]                         # المستقبل
            )
            email_message.content_subtype = "html"   # تحديد نوع المحتوى HTML

            # إرسال البريد
            try:
                email_message.send(fail_silently=False)
                print("Email sent successfully ✅")
            except Exception as e:
                print("Failed to send email ❌:", e)

            return redirect('contact_success')

    return render(request, 'contact/contact.html', {'form': form})


def contact_success(request):
    return render(request, 'contact/success.html')


def contact_messages(request):
    messages = Contact.objects.all().order_by('-created_at')
    return render(request, 'contact/messages.html', {'messages': messages})
