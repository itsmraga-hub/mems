from django.http import HttpResponse

import json
import uuid

from .models import Product, ProductCategory, Expense, ExpenseCategory


class SaveProduct:
    def __init__(self):
        pass

    def save_new_product(name, description, buy_price, price, image, quantity, brand, category_ids, user):
        try:
            p_code = str(uuid.uuid4())
            product = Product.objects.create(
                p_code=p_code,
                name=name,
                description=description,
                buy_price=buy_price,
                price=price,
                image=image,
                quantity=quantity,
                brand=brand,
            )
            if product is not None:
                e_category = ExpenseCategory.objects.get(name='Purchases')
                total = float(product.price) * float(product.quantity)
                date = product.date.strftime("%D")
                description = f"Purchase of {product.quantity} - {product.name} on {date} worth {total}"                
               
                e_code = str(uuid.uuid4())
                print(e_code)
                try:
                    expense = Expense.objects.create(
                        product=product,
                        e_code=e_code,
                        description=description,
                        staff=user,
                        amount=total,
                        category=e_category
                    )
                except Exception as e:
                    return HttpResponse(json.dumps({"status": "fail", "data": {"message": str(e)}}))
            product.save()
            return HttpResponse(json.dumps({"status": "success", "data": {"message": p_code}}))
        except Exception as e:
            return HttpResponse(json.dumps({"status": "fail", "data": {"message": str(e)}}))

    def update_product_price_quantity(product, quantity, price):
        product.quantity = quantity
        product.price = price
        product.save()

    def update_product_full(product):
        pass

    def create_product_category(name):
        pc_code = str(uuid.uuid4)
        p_category = ProductCategory.objects.filter(name=name).exists()
        if not p_category:
            ProductCategory.objects.create(
                name=name,
                pc_code=pc_code
            )
            return {'success': 'Category added successfully'}
        return {'failed': 'Category not added because it exists'}
