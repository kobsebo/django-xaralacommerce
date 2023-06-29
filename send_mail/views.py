from django.core.mail import send_mail
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives


def send_new_order_email(email):
    # on envoie un mail au client (faire de meme pour l'administrateur)
    send_mail(
        "Votre commande sur Xaralacommerce",
        "Nous avons bien reçu votre commande.",
        "contact@xaralacommerce.com",
        [email],
        fail_silently=False,
    )


def send_new_order_email_with_template(email):
    template = get_template("email/new_order.html")
    context = {"email": email}
    from_email = ("Nouvelle commande sur Xaralacommerce")
    body = template.render(context)
    # subject = template.render(context)
    message = EmailMultiAlternatives(body, from_email, [email])
    message.attach_alternative(body, "text/html")
    message.send(fail_silently=False)


def payment_successful_email(email):
    # on envoie un mail au client (faire de meme pour l'administrateur)
    send_mail(
        "Votre commande sur Xaralacommerce",
        "Nous avons bien reçu votre paiement.",
        "contact@xaralacommerce.com",
        [email],
        fail_silently=False,
    )
