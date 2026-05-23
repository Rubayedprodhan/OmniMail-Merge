import pandas as pd
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

def email_merge_view(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        uploaded_file = request.FILES['excel_file']
        
        try:
            # ফাইলের এক্সটেনশন অনুযায়ী রিড করা
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # নিশ্চিত হওয়া যে প্রয়োজনীয় কলামগুলো আছে
            if 'Name' not in df.columns or 'Email' not in df.columns:
                messages.error(request, "ভুল ফরম্যাট! ফাইলে অবশ্যই 'Name' এবং 'Email' কলাম থাকতে হবে।")
                return render(request, 'upload.html')

            success_count = 0
            
            # লুপ চালিয়ে মেইল পাঠানো
            for index, row in df.iterrows():
                name = row['Name']
                email = row['Email']
                
                # আপনার ইমেইল কন্টেন্ট
                subject = f"হ্যালো {name}, আপনার জন্য একটি বিশেষ বার্তা!"
                message = f"প্রিয় {name},\n\nএটি আমার পার্সোনাল ইমেইল কন্টেন্ট। আমি ড্যাশবোর্ড থেকে এক্সেল ফাইল আপলোড করে এই মেইলটি পাঠাচ্ছি।\n\nশুভেচ্ছাান্তে,\nমোঃ রুবায়েদ প্রধান"
                
                send_mail(
                    subject, 
                    message, 
                    settings.EMAIL_HOST_USER, 
                    [email], 
                    fail_silently=False
                )
                success_count += 1
                
            messages.success(request, f"অভিনন্দন! মোট {success_count} টি মেইল সফলভাবে পাঠানো হয়েছে।")
            
        except Exception as e:
            messages.error(request, f"একটি সমস্যা হয়েছে: {str(e)}")
            
    return render(request, 'upload.html')