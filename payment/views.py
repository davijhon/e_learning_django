import json
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    TemplateView, View 
)
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from .models import OrderCourse, Order, Address, Payment
from .forms import CheckoutForm
from courses.models import Course




class CartPageView(View):

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order,
            }
            return render(self.request, 'pages/cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


class CheckoutView(View):

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )

            return render(self.request, "pages/checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have an active order')
            return redirect("payment:cart")
    
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address= form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip_code = form.cleaned_data.get('zip_code')

                payment_option = form.cleaned_data.get('payment_option')

                billing_address = Address(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip_code=zip_code,
                    address_type='B'
                )

                billing_address.save()
                order.billing_address = billing_address
                order.payment_option = payment_option
                order.save()

                if payment_option == 'S':
                    return redirect('payment:payment', payment_option="PayPal")
                elif payment_option == 'P':
                    return redirect('payment:payment', payment_option='PayPal')
                else:
                    messages.warning(self.request, 'Invalid payment option')
                    return redirect('payment:checkout')
        
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an active order')
            return redirect("payment:cart")


class PaymentView(View):

    def get(self, *args, payment_option, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order,
            'payment_option': payment_option,
        }
        return render(self.request, 'pages/payment.html', context)


def payment_complete(request):
    body = json.loads(request.body)
    user = request.user
    order = Order.objects.get(
        user=user, ordered=False, id=body['orderID']
    )
    if order:
        payment = Payment(
            user=user,
            charge_id=body['payID'],
            amount=order.get_total()
        )
        payment.save()

        #Assign the paymet to the order
        order_items = order.items.all()
        order_items.update(ordered=True)

        for item in order_items:
        # Add user to courses
            course = Course.objects.get(id=item.id)
            course.students.add(user)
            item.save()
        
        order.ordered = True
        order.payment = payment
        order.save()

        messages.info(request, "The payment was successfull")
        return redirect('students:student_course_list')
    else:
        messages.info(request, "A serius error accourred. We have been notified")
        return redirect('/')

@login_required
def add_to_cart(request, slug):
    course = get_object_or_404(Course, slug=slug)
    
    # Evaluated if user is already enrolled for this course.
    user_in = Course.objects.filter(id=course.id, students=request.user)
    if user_in.exists():
        messages.info(request, "You are already enrolled for this package")
        return redirect("courses:index")

    order_item, created = OrderCourse.objects.get_or_create(
                                                            course=course,
                                                            user=request.user,
                                                            ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(course__slug=course.slug).exists():
            # order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("payment:cart")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("payment:cart")
    else:
        order = Order.objects.create(
            user=request.user,
        )
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("payment:cart")

@login_required
def remove_from_cart(request, slug):
    course = get_object_or_404(Course, slug=slug)
    order_qs = Order.objects.filter(
                                    user=request.user,
                                    ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(course__slug=course.slug).exists():
            order_item = OrderCourse.objects.filter(
                                                    course=course,
                                                    user=request.user,
                                                    ordered=False,
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("payment:cart")
        else:
            messages.info(request, "This item not in your cart.")
            return redirect("courses:course_detail", slug=slug)
    else:
        messages.info(request, "You do not have an activate order.")
        return redirect("courses:course_detail", slug=slug)