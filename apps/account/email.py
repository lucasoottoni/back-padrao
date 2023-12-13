from djoser import email 

class PasswordResetEmail(email.PasswordResetEmail):
    template_name='account/email/password_reset.html'