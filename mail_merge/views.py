import pandas as pd
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string

def email_merge_view(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        uploaded_file = request.FILES['excel_file']
        
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            if 'Name' not in df.columns or 'Email' not in df.columns:
                messages.error(request, "ভুল ফরম্যাট! ফাইলে অবশ্যই 'Name' এবং 'Email' কলাম থাকতে হবে।")
                return render(request, 'upload.html')

            success_count = 0
            
            for index, row in df.iterrows():
                name = row['Name']
                email = row['Email']
                
                subject = f"হ্যালো {name}, আপনার জন্য একটি বিশেষ বার্তা!"
                
                plain_message = f"প্রিয় {name},\n\nএটি আমার পার্সোনাল ইমেইল কন্টেন্ট।"
                
                context = {'name': name}
                html_message = render_to_string('email_template.html', context)
                
                from_email = f"Rubayed <{settings.EMAIL_HOST_USER}>"
                
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=from_email,
                    recipient_list=[email],
                    fail_silently=False,
                    html_message=html_message
                )
                success_count += 1
                
            messages.success(request, f"অভিনন্দন! মোট {success_count} টি মেইল সফলভাবে পাঠানো হয়েছে।")
            
        except Exception as e:
            messages.error(request, f"একটি সমস্যা হয়েছে: {str(e)}")
            
    return render(request, 'upload.html')