from allauth.account.adapter import DefaultAccountAdapter

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class AccountAdapter(DefaultAccountAdapter):
    pass
    #def get_login_redirect_url(self, request):
    #    print "um"
    #    return "/"
    #def get_logout_redirect_url(self, request):
    #    print "dois"
    #    return None
    #def get_email_confirmation_redirect_url(self, request):
    #    print "tres"
    #    return None



class SocialAccountAdapter(DefaultSocialAccountAdapter):
    pass
    #def get_login_redirect_url(self, request):
    #    return "/"
    #def get_logout_redirect_url(self, request):
    #    print "dois"
    #    return None
    #def get_email_confirmation_redirect_url(self, request):
    #    print "tres"
    #    return None
