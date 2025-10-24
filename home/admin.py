from django.contrib import admin
from .models import UserManager, User,Category, House, PricedHouse, Transaction, VerificationCode, BannedUser

admin.site.register(UserManager)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(House)
admin.site.register(PricedHouse)
admin.site.register(Transaction)
admin.site.register(VerificationCode)
admin.site.register(BannedUser)


