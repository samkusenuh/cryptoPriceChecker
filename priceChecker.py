#! python
# priceAlert.py - Retrieves the Bitcoin price every hour and checks whether
# that price has risen or fallen by 1 % in 1 hour.

import requests, bs4, time, smtplib

def sendMail(message):

    smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('from e-mail address here', 'from e-mail password here')
    smtpObj.sendmail('from e-mail here', 'to-email address here', 'Subject:' + message)
    smtpObj.quit()

previousPrice = 0.0

while True:
  time.sleep(5)
  res = requests.get('https://www.coinmarketcap.com/currencies/bitcoin/')
  res.raise_for_status()
  soupCoin = bs4.BeautifulSoup(res.text, features="html.parser")
  type(soupCoin)
  rawPrice = soupCoin.select('#quote_price > span.h2.text-semi-bold.details-panel-item--price__value')
  justPrice = (rawPrice[0]).getText()
  justPrice = float(justPrice)

  print('the previous price was ' + str(previousPrice) + '... the current price is ' + str(justPrice))

  if justPrice == previousPrice:
      print('the price has stayed the same')
  if justPrice < previousPrice:
      print('the price has gone down!')
      print ('sending an email notification...')
      sendMail('SELL SELL SELL!')
      print('email has been sent')
  if justPrice > previousPrice:
      print('the price has gone up!')
      print('sending an email notification...')
      sendMail('BUY BUY BUY')
      print('email has been sent')
  previousPrice = justPrice
