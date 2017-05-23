from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        print "um"
        return None
    def get_logout_redirect_url(self, request):
        print "dois"
        return None
    def get_email_confirmation_redirect_url(self, request):
        print "tres"
        return None

