from flask import Flask, request, render_template, url_for, redirect, session, flash
import stripe
import os
from forms import DonateForm


app = Flask(__name__)

STRIPE_KEYS={'sk':os.environ.get('STRIPE_SK'),
             'pk':os.environ.get('STRIPE_PK')}

stripe.api_key = STRIPE_KEYS['sk']
app.secret_key = os.environ.get('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/donate', methods = ['POST', 'GET'])
def donate():
    form = DonateForm()
    if form.validate_on_submit():
        amount = form.amount.data
        email = form.email.data
        amount = str(amount)
        if ".0" in amount[-2:]:
            amount = int(float(amount))
            session['amount_cents'] = amount*100 #int(amount+"00")
            session['amount_display'] = "{}.00".format(amount)
        else:
            a,b = str(amount).split('.')
            b = b[:2]
            session['amount_cents'] = int(a+b)
            session['amount_display'] = "{}.{}".format(a,b)
        session['email'] = email
        return redirect(url_for('confirm'))
    return render_template('donate.html', form = form)


@app.route('/confirm')
def confirm():
    key = STRIPE_KEYS['pk']
    return render_template('confirm.html', amount_cents = session['amount_cents'],
                           amount_display=session['amount_display'],
                           key =key,
                           email=session['email'])


@app.route('/pay', methods=['POST'])
def pay():
    try:
        if request.form['stripeTokenType'] == 'bitcoin_receiver':
            customer = stripe.Customer.create(
                email=session['email'],
                source=request.form['stripeToken']
            )

        else:
            customer = stripe.Customer.create(
                email=session['email'],
                card=request.form['stripeToken'],  # having errors getting stripe token
            )
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=session['amount_cents'],
            currency='usd',
            description=customer.email
            )

        session.pop('email',0)
        session.pop('amount_cents',0)
        session.pop('amount_display',0)

    except stripe.error.CardError as e:
        flash("There seems to have been a problem charging your card...")
        return render_template('error.html')
    except stripe.error.StripeError:
        flash("Ooops something went wrong! Not quite sure what...")
        return render_template('error.html')

    return render_template('thanks.html')

if __name__ == '__main__':
    app.run()  #debug=True
