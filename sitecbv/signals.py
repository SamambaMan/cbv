from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def post_save_callback(sender, instance, **kwargs):
    del sender
    from .models import InfosAdicionaisUsuario
    tem_infos = False
    try:
        tem_infos = (instance.infosadicionaisusuario is not None)
    except:
        pass

    if not tem_infos:
        infos = InfosAdicionaisUsuario()
        infos.user = instance
        infos.save()


    