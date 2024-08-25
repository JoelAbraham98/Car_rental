from django.contrib import admin
from.models import UserProfile
from.models import Car,Booking
from.models import CarCategory

# Register your models here.
class CarCategoryAdmin(admin.ModelAdmin):
     list_display = ['name']

# class CarImageAdmin(admin.ModelAdmin):
#      list_display = ['car','image']

class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'registration_number', 'daily_rental_rate', 'display_availability', 'stock')
    search_fields = ('make', 'model', 'registration_number')
    list_filter = ('make', 'year', 'category', 'transmission', 'fueltype', 'seats')

    fieldsets = (
        (None, {
            'fields': ('user', 'make', 'model', 'year', 'registration_number', 'daily_rental_rate', 'image', 'category', 'transmission', 'fueltype', 'seats', 'mileage', 'stock')
        }),
    )

    def display_availability(self, obj):
        return obj.availability
    display_availability.short_description = 'Availability'
    display_availability.boolean = True





class BookingAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'start_date', 'end_date', 'status')
    actions = ['mark_as_completed']

    def mark_as_completed(self, request, queryset):
        for booking in queryset:
            booking.mark_as_completed()
        self.message_user(request, "Selected bookings have been marked as completed.")
    mark_as_completed.short_description = "Mark selected bookings as completed"

admin.site.register(Booking, BookingAdmin)


admin.site.register(Car,CarAdmin)
admin.site.register(CarCategory,CarCategoryAdmin)
# admin.site.register(CarImage,CarImageAdmin)



admin.site.register(UserProfile)