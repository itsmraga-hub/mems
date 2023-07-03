from django.http import HttpResponse

import json
import uuid

from .models import Product, ProductCategory


class SaveProduct:
    def __init__(self):
        pass

    def save_new_product(name, description, price, image, quantity, brand, category_ids):
        try:
            p_code = str(uuid.uuid4())
            product = Product.objects.create(
                p_code=p_code,
                name=name,
                description=description,
                price=price,
                image=image,
                quantity=quantity,
                brand=brand
            )
            product.categories.set(category_ids)
            # print(product.categories)
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
