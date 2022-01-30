from django.shortcuts import HttpResponse
import requests, json, sys
from django.conf import settings

test_url = settings.ALLOWED_HOSTS[-1]
test_url_full = 'https://' + test_url

class PaddlePayment:
    def __init__(self, price, product_name, product_id):
        self.product_name = product_name
        self.price = price
        self.p_id = product_id


    def checkoutrequest(self):
        try:
            url = 'https://sandbox-vendors.paddle.com/api/2.0/product/generate_pay_link'
            vendor_id = 3972
            auth_code = '5df6310a143137c3feda13b3f498373c9151f4d10c475f2d62'
            custom_message = f'Thanks for purchasing {self.product_name}'
            price = ['USD:' + str(self.price)]
            wh_url = test_url_full + '/webhook'
            receipt = 'https://sandbox-my.paddle.com/invoice/ + order_id(from webhook endpoint) + / + checkout_id'

            payload = json.dumps(
                {"vendor_id":vendor_id,
                "vendor_auth_code":auth_code,
                "title":self.product_name,
                "prices":price,
                'webhook_url': wh_url,
                "custom_message":custom_message,
                "image_url":"https://s3.envato.com/files/309606114/80x80-logo-tortoizthemes.jpg",
                "return_url":test_url_full + "/products/order-details?checkout_id={checkout_hash}",
                "quantity_variable":0,
                "quantity":1,
                "p_id":self.p_id,
                "marketing_consent":0,
                "is_recoverable":0}
            )

            headers = {'content-type': 'application/json'}
            response = requests.request("POST", url, data=payload, headers=headers)
            return response.text

        except:
            # e = sys.exc_info()[0]
            # print('An unexpected error occurred %s' %e)
            error = {'url': 'Check your internet connection and try again'}
            return error