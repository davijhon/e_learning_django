from django.contrib import admin


from .models import Order, OrderCourse, Address

class OrderAdmin(admin.ModelAdmin):
	list_display = [
			'user', 
			'ordered', 
			'billing_address',
	]
	list_filter = [
			'user', 
			'ordered', 

	]
	list_display_links = [
			'user', 
			'billing_address',
	]


class AddressAdmin(admin.ModelAdmin):
	list_display = [
		'user',
		'street_address',
		'apartment_address',
		'country',
		'zip_code',
		#'address_type',
		'default',
	]
	list_filter = [
		'default',
		#'address_type',
		'country',
	]
	search_fields = [
		'user',
		'street_address',
		'apartment_address',
		'zip_code',
	]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderCourse)
# admin.site.register(Payment)
admin.site.register(Address, AddressAdmin)
