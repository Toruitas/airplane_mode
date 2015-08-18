from flask import Flask, request, render_template, url_for, redirect, session
import stripe
import os
from forms import DonateForm


app = Flask(__name__)

STRIPE_KEYS={'sk':os.environ.get('STRIPE_SK'),
             'pk':os.environ.get('STRIPE_PK')}

stripe.api_key = STRIPE_KEYS['sk']
app.secret_key = os.environ.get('SECRET_KEY')

def stream():
    while True:
        yield ('Content-Type: audio/mp4')
    stream()


@app.route('/')
def index():
    """
    http://www.techairlines.com/useful-youtube-url-tricks/
    Hidden youtube for now hahahahahaha.
    :return:
    """
    return render_template('index.html')


@app.route('/donate', methods = ['POST', 'GET'])
def donate():
    form = DonateForm()
    if form.validate_on_submit():
        amount = form.amount.data
        email = form.email.data
        amount_cents = amount * 100
        amount_cents = int(amount_cents)  # to account for this shit being in cents yo
        session['email'] = email
        session['amount_cents'] = amount_cents
        session['amount_display'] = amount
        #return "{}".format(session['amount_cents'])
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
    """
    On confirmation, send email to Admins if it is a new Pot, or just directly allow. Or text.
    Enter the test number 4242 4242 4242 4242, a three digit CVC and any expiry date in the future.
    Submitting the form should bring up our successful charge page.

    Having trouble getting stripe token: C:\Windows\System32\drivers\etc
    http://stackoverflow.com/questions/6180720/how-to-fix-socket-gaierror-11004-getaddrinfo-failed-error-in-gae
    :param amount:
    :param pot:
    :param first:
    :return:
    """
    customer = stripe.Customer.create(
        email=session['email'],
        card=request.form['stripeToken']  # having errors getting stripe token
    )

    try:
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=session['amount_cents'],
            currency='usd',
            description='donation to focused flight'
        )
        session.pop('email',0)
        session.pop('amount_cents',0)
        session.pop('amount_display',0)

    except stripe.CardError:
        pass

    return render_template('thanks.html')

if __name__ == '__main__':
    app.run(debug=True)
