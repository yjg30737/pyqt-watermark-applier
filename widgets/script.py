import webbrowser

from constants import PAYPAL_URL, BUYMEACOFFEE_URL


def goPayPal():
    webbrowser.open(PAYPAL_URL)

def goBuyMeCoffee():
    webbrowser.open(BUYMEACOFFEE_URL)