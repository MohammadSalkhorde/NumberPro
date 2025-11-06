from django.shortcuts import render
import requests
from django.http import JsonResponse,HttpResponse
import requests, time
import os
from dotenv import load_dotenv
load_dotenv()

BASE_URL = "https://api.numberland.ir/v2.php/"
API_KEY = os.getenv("API_KEY")

#====================================================================
def services_page(request):
    api_key = "702cbe2c72dcea78e29f944eb16d5f00"
    url = "https://api.numberland.ir/v2.php/"
    params = {
        "apikey": api_key,
        "method": "getservice"
    }

    try:
        response = requests.get(url, params=params)
        services = response.json()
    except Exception as e:
        services = []
        print("Error :", e)

    return render(request, "numbers/numbers_list.html", {
        "services": services,
        "api_key": api_key,
    })
#====================================================================
def get_numbers(request):
    service_id = request.GET.get("service_id")
    if not service_id:
        return JsonResponse({"error": "Service ID is required"}, status=400)

    url = f"https://api.numberland.ir/v2.php/?apikey={API_KEY}&method=getinfo&service={service_id}"
    response = requests.get(url)

    try:
        data = response.json()

        # اگر پاسخ به‌جای لیست، دیکشنری یا چیز دیگری بود:
        if not isinstance(data, list):
            return JsonResponse({"error": "Invalid data format"}, status=500)

        filtered_data = []

        for item in data:
            try:
                count = int(item.get("count", 0))
                if count > 0:
                    amount = int(item.get("amount", 0)) 
                    filtered_data.append({
                        "emoji": item.get("emoji", ""),
                        "cname": item.get("cname", ""),
                        "count": count,
                        "amount": amount,
                        "country": item.get("country", ""),   # آیدی کشور
                        "service": service_id
                    })
            except (ValueError, KeyError):
                continue  # اگر داده مشکل داشت، از آن عبور می‌کنیم

        return JsonResponse({"numbers": filtered_data})
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
#====================================================================
def load_countries():
    try:
        response = requests.get(BASE_URL, params={
            "apikey": API_KEY,
            "method": "getcountry"
        })
        data = response.json()

        return {
            country["id"]: {
                "name": country["name"],
                "name_en": country["name_en"],
                "areacode": country["areacode"],
                "emoji": country["emoji"],
                "image": f"https://api.numberland.ir{country['image']}"
            }
            for country in data if country.get("active") == "1"
        }

    except Exception:
        return {}

COUNTRIES = load_countries()
#====================================================================
def buy_number(request):
    service_id = request.GET.get("service_id")
    country_id = request.GET.get("country_id")

    if not service_id or not country_id:
        return render(request, "numbers/number_purchased.html", {
            "error": "پارامترهای لازم ارسال نشده‌اند."
        })

    try:
        response = requests.get(BASE_URL, params={
            "apikey": API_KEY,
            "method": "getnum",
            "country": country_id,
            "operator": "any",
            "service": service_id
        })
        data = response.json()

        if "ID" not in data:
            return render(request, "numbers/number_purchased.html", {
                "error": "خرید ناموفق بود. لطفاً اعتبار یا اطلاعات را بررسی کنید."
            })

        number_id = data["ID"]
        number = data["NUMBER"]
        area_code = data.get("AREACODE", "")
        country_info = COUNTRIES.get(country_id, {})

        return render(request, "numbers/number_purchased.html", {
            "number_id": number_id,
            "number": number,
            "area_code": area_code,
            "country_name": country_info.get("name", "نامشخص"),
            "country_image": country_info.get("image"),
            "service_id": service_id
        })

    except Exception as e:
        return render(request, "numbers/number_purchased.html", {
            "error": "خطایی در ارتباط با سرور رخ داده است."
        })

#====================================================================
def get_code(request, number_id):
    print(f"\n🚀 دریافت کد تأیید برای شماره با ID: {number_id}")

    try:
        verify_params = {
            "apikey": API_KEY,
            "method": "checkstatus",
            "id": number_id
        }

        start_time = time.time()
        timeout = 330  # 5.5 دقیقه

        while True:
            verify_response = requests.get(BASE_URL, params=verify_params)

            if verify_response.status_code == 200:
                verify_result = verify_response.json()
                print("وضعیت پاسخ:", verify_result)

                if verify_result.get("RESULT") == 1:
                    elapsed_time = time.time() - start_time
                    if elapsed_time > timeout:
                        print("⏳ زمان تمام شد، در حال لغو شماره...")
                        # return cancel_number(request, number_id, timeout_expired=True)
                    else:
                        print("⏳ کد هنوز ارسال نشده. 30 ثانیه صبر...")
                        time.sleep(30)
                        continue

                elif verify_result.get("RESULT") == 2:
                    verification_code = verify_result.get("CODE")
                    print(f"✅ کد تأیید دریافت شده: {verification_code}")
                    return render(request, 'number_verification.html', {
                        'number_id': number_id,
                        'verification_code': verification_code,
                    })

                else:
                    print("⚠️ وضعیت نامشخص:", verify_result)
                    return HttpResponse("خطا در وضعیت کد تایید")

            else:
                print("❌ خطا در پاسخ دریافت کد:", verify_response.status_code)
                return HttpResponse("خطا در اتصال به API برای دریافت کد")

    except Exception as e:
        print("❌ استثنا در دریافت کد:", e)
        return HttpResponse("یک خطای غیرمنتظره رخ داد.")
#====================================================================
def cancel_number_ajax(request, number_id):
    cancel_params = {
        "apikey": API_KEY,
        "method": "cancelnumber",
        "id": number_id
    }

    try:
        while True:
            cancel_response = requests.get(BASE_URL, params=cancel_params)

            if cancel_response.status_code == 200:
                cancel_result = cancel_response.json()

                if str(cancel_result.get("RESULT")) == '3':
                    return JsonResponse({"status": "success", "message": "✅ شماره با موفقیت لغو شد."})

                elif str(cancel_result.get("RESULT")) == '1':
                    time.sleep(30)
                else:
                    return JsonResponse({"status": "error", "message": "❌ خطا در لغو شماره."})
            else:
                return JsonResponse({"status": "error", "message": "❌ خطا در اتصال به سرور."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": "⚠️ یک خطای غیرمنتظره رخ داد."})
#====================================================================
def cancel_wait(request, number_id):
    return render(request, "numbers/cancel_wait.html", {"number_id": number_id})
#====================================================================


# import requests
# import time

# API_KEY = "702cbe2c72dcea78e29f944eb16d5f00"
# BASE_URL = "https://api.numberland.ir/v2.php/"

# # مرحله 1: درخواست خرید شماره
# buy_params = {
#     "apikey": API_KEY,
#     "method": "getnum",
#     "country": 1,      # روسیه
#     "operator": "any",
#     "service": 26      # سرویس اپل
# }

# response = requests.get(BASE_URL, params=buy_params)

# if response.status_code == 200:
#     result = response.json()
#     print("نتیجه خرید شماره:\n", result)

#     if "ID" not in result:
#         print("خطا در دریافت شماره یا اعتبار کافی نیست.")
#     else:
#         number_id = result["ID"]
#         number = result["NUMBER"]
#         print(f"شماره خریداری شده: {number}")

#         # مرحله 2: درخواست ورودی از کاربر برای ادامه یا لغو
#         user_input = input("\nآیا می‌خواهید کد تایید را دریافت کنید؟ (y برای ادامه، n برای لغو): ").strip().lower()

#         if user_input == "y":
#             # ارسال درخواست دریافت کد تایید از API
#             verify_params = {
#                 "apikey": API_KEY,
#                 "method": "checkstatus",
#                 "id": number_id
#             }

#             start_time = time.time()  # زمان شروع درخواست
#             timeout = 330  # 330 ثانیه (5 دقیقه) برای انتظار

#             while True:
#                 verify_response = requests.get(BASE_URL, params=verify_params)

#                 if verify_response.status_code == 200:
#                     verify_result = verify_response.json()
#                     if verify_result.get("RESULT") == 1:  # کد تایید هنوز در انتظار است
#                         elapsed_time = time.time() - start_time
#                         if elapsed_time > timeout:
#                             print("زمان انتظار تمام شد (۵ دقیقه) و کد تایید ارسال نشد. در حال لغو شماره...")
#                             # ارسال درخواست لغو شماره پس از گذشت 330 ثانیه
#                             cancel_params = {
#                                 "apikey": API_KEY,
#                                 "method": "cancelnumber",
#                                 "id": number_id
#                             }
#                             cancel_response = requests.get(BASE_URL, params=cancel_params)

#                             if cancel_response.status_code == 200:
#                                 cancel_result = cancel_response.json()
#                                 if cancel_result.get("RESULT") == '3':  # شماره لغو شد
#                                     print("با موفقیت لغو شد:", cancel_result)
#                                 else:
#                                     print(f"خطا در لغو شماره: {cancel_result}")
#                             break
#                         else:
#                             print("کد تایید در انتظار است، صبر می‌کنیم...")
#                             time.sleep(30)  # صبر 30 ثانیه‌ای
#                     elif verify_result.get("RESULT") == 2:  # کد تایید دریافت شده
#                         verification_code = verify_result.get("CODE")  # کد تایید
#                         print(f"کد تایید دریافت شده: {verification_code}")
                        
#                         # بررسی REPEAT و درخواست کد تایید مجدد اگر لازم باشد
#                         if result.get("REPEAT") == 1:
#                             user_input_repeat = input("\nآیا می‌خواهید کد تایید جدید دریافت کنید؟ (y برای بله، n برای خیر): ").strip().lower()
#                             if user_input_repeat == "y":
#                                 start_time = time.time()  # زمان شروع درخواست مجدد کد تایید
#                                 continue  # حلقه ادامه می‌یابد و دوباره درخواست کد تایید می‌شود
#                         break
#                     else:
#                         print(f"خطا در وضعیت کد تایید: {verify_result}")
#                         break
#                 else:
#                     print("خطا در درخواست دریافت وضعیت کد تایید:", verify_response.status_code)
#                     break

#         elif user_input == "n":
#             print("در حال لغو شماره...")

#             # حلقه لغو تا زمانی که شماره لغو شود
#             cancel_params = {
#                 "apikey": API_KEY,
#                 "method": "cancelnumber",
#                 "id": number_id
#             }

#             while True:
#                 cancel_response = requests.get(BASE_URL, params=cancel_params)

#                 if cancel_response.status_code == 200:
#                     cancel_result = cancel_response.json()
#                     if cancel_result.get("RESULT") == '3' or cancel_result.get("RESULT") == 3 :  # شماره لغو شد
#                         print("با موفقیت لغو شد:", cancel_result)
#                         break
#                     elif cancel_result.get("RESULT") == '1':  # هنوز لغو نشده
#                         print(f"شماره هنوز لغو نشده است، صبر می‌کنیم و دوباره تلاش می‌کنیم... ({number})")
#                         time.sleep(30)  # صبر 30 ثانیه‌ای
#                     else:
#                         print(f"خطا در لغو شماره: {cancel_result}")
#                         break
#                 else:
#                     print("خطا در درخواست لغو:", cancel_response.status_code)
#                     break

#         else:
#             print("ورودی نامعتبر.")
# else:
#     print("خطا در اتصال به API:", response.status_code)
