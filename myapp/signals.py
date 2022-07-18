from django.contrib.auth.signals import user_logged_in, user_logged_out, \
    user_login_failed
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_init, pre_save, pre_delete, \
    post_init, post_save, post_delete
from django.core.signals import request_started, request_finished, got_request_exception
from django.core.cache import cache

# # signals start block --------------*************************
# @receiver(user_logged_in, sender=User)
# def login_success(sender, request, user, **kwargs):
#
#     # when user logs in below data is printed in terminal
#     print("------------------------")
#     print("login signal..... ")
#     print("sender:", sender)
#     print("request:", request)
#     print("user:", user)
#     print("user-password:", user.password)
#     print(f'kwargs: {kwargs}')
#
#
# # user_logged_in.connect(login_success, sender=User)


# @receiver(user_logged_out, sender=User)
# def log_out(sender, request, user, **kwargs):
#
#     # when user logs in below data is printed in terminal
#     print("------------------------")
#     print("logout signal..... ")
#     print("sender:", sender)
#     print("request:", request)
#     print("user:", user)
#     print(f'kwargs: {kwargs}')
#
#
# # user_logged_out.connect(log_out, sender=User)


# @receiver(user_login_failed, sender=User)
# def login_failed(sender, credentials, request, **kwargs):
#
#     # when user logs in below data is printed in terminal
#     print("------------------------")
#     print("login Failed signal..... ")
#     print("sender:", sender)
#     print("credentials:", credentials)
#     print("request:", request)
#     print(f'kwargs: {kwargs}')
#
#
# # user_login_failed.connect(login_failed, sender=User)

# ----------------------------------------------------------------------------

# @receiver(pre_save, sender=User)
# def at_beginning_save(sender, instance, **kwargs):
#     print("------------------------")
#     print("Pre Save Signal..... ")
#     print("sender:", sender)
#     print("instance:", instance)
#     print(f'kwargs: {kwargs}')

# ----------------------------------------------------------------------------

# @receiver(post_save, sender=User)
# def at_ending_save(sender, instance, created, **kwargs):
#     if created:
#         print("------------------------")
#         print("Post Save Signal..... ")
#         print("New Record-----")
#         print("sender:", sender)
#         print("instance:", instance)
#         print("created:", created)
#         print(f'kwargs: {kwargs}')
#     else:
#         print("------------------------")
#         print("Post Save Signal..... ")
#         print("UPDATED---- ")
#         print("sender:", sender)
#         print("instance:", instance)
#         print("created:", created)
#         print(f'kwargs: {kwargs}')

# ----------------------------------------------------------------------------

# @receiver(pre_delete, sender=User)
# def at_begining_delete(sender, instance, **kwargs):
#     print("------------------------")
#     print("Pre Delete Signal ---- ")
#     print("sender:", sender)
#     print("instance:", instance)
#     print(f'kwargs: {kwargs}')
#
#
# @receiver(post_delete, sender=User)
# def at_ending_delete(sender, instance, **kwargs):
#     print("------------------------")
#     print("Post Delete Signal ---- ")
#     print("sender:", sender)
#     print("instance:", instance)
#     print(f'kwargs: {kwargs}')

# ----------------------------------------------------------------------------

# @receiver(pre_init, sender=User)
# def at_beginning_delete(sender, *args, **kwargs):
#     print("------------------------")
#     print("at Pre Init Signal---- ")
#     print("sender:", sender)
#     print(f'args: {args}')
#     print(f'kwargs: {kwargs}')
#
#
# @receiver(post_init, sender=User)
# def at_ending_delete(sender, *args, **kwargs):
#     print("------------------------")
#     print("at Post Init Signal ---- ")
#     print("sender:", sender)
#     print(f'args: {args}')
#     print(f'kwargs: {kwargs}')

# ----------------------------------------------------------------------------

# @receiver(request_started)
# def at_beginning_request(sender, environ, **kwargs):
#     print("------------------------")
#     print("at Beginning Request ---- ")
#     print("sender:", sender)
#     print("Environ:", environ)
#     print(f'kwargs: {kwargs}')


# @receiver(request_finished)
# def at_ending_request(sender, **kwargs):
#     print("------------------------")
#     print("at Ending Request ---- ")
#     print("sender:", sender)
#     print(f'kwargs: {kwargs}')


# @receiver(got_request_exception)
# def at_request_exception(sender, request, **kwargs):
#     print("------------------------")
#     print("at Beginning Request ---- ")
#     print("sender:", sender)
#     print("Request:", request)
#     print(f'kwargs: {kwargs}')

# # signals end block --------------*************************
# ----------------------------------------------------------------------------

# # session to get user ip address:

@receiver(user_logged_in, sender=User)
def login_user_ip(sender, request, user, **kwargs):
    # print("--------")
    # print("Logged in signal:")
    ip = request.META.get('REMOTE_ADDR')
    # print("client IP:", ip)
    request.session['ip'] = ip

# # session end;
# ----------------------------------------------------------------------------

# # get user count :


@receiver(user_logged_in, sender=User)
def login_count(sender, request, user, **kwargs):
    count = cache.get('count', 0, version=user.pk)
    newcount = count + 1
    cache.set('count', newcount, 60*60*24, version=user.pk)
    print(user.pk)

