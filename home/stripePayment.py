import stripe


stripe.api_key = 'sk_test_qm2rPelkovVnEUg34sFSIi7s00ZTj68bMF'

stripe.PaymentIntent.create(
  amount=1099,
  currency='inr',
  payment_method_types=['card'],
)
