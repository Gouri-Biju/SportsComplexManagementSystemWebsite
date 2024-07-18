from django.shortcuts import render
from django.views import View
from SportsComplexManagementSystemWebsite.firebase import firebase_admin_instance,pyrebas_instance

class SignUp(View):
    def get(self,request):
        return render(request,'signup.html')
    def post(self,request):
        try:
            name=request.POST['name']
            email= request.POST['email']
            phone_number= request.POST['phone_number']
            password = request.POST['password']
            firebase_admin_instance.auth.createuser(
                display_name=name
                email=email
                phone_number=phone_number
                password=password
            )
            user_data={
                name=name
                phone_number=phone_number
                email=email
            }
            firebase_admin_instance.db.collection(users).doc(user.uid).set(user_data)
            login=pyrebas_instance.auth.sign_in_with_email_and_password(email,password)
            id_token=login['idToken']
            pyrebas_instance.auth.send_email_verification(id_token)
            print("Email verification has been send")
            return redirect('loginemail')
        except Exception as e:
            print("Failed to create user")
            return render(request,'signup.html'{'error':'Failed to create user.Please try again'})
            print("User Created Successfully")

        return render(request,'home.html')

class SignIn(View):
    try:
        mail=request.POST['email']
        password=request.POST['password']
        user=pyrebas_instance.auth.sign_in_with_email_and_password(email,password)
        id_token=user['idToken']
        request.session['user_id_token']=id_token
        return redirect('home2')
    except Exception as e:
        print(f"error:{e}")
        return render(request,'signin.html',{'error':'Invalid Credentials'})