from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

 # this functions helps to run signals in signals.py
    def ready(self):
        import accounts.signals