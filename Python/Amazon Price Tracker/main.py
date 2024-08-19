import requests
from bs4 import BeautifulSoup
import smtplib
import os
import dotenv

dotenv.load_dotenv()

#Instapot item on Amazon

URL = ("https://www.amazon.com/Bose-QuietComfort-Cancelling-Headphones-Bluetooth/dp/B0CCZ26B5V/ref=sr_1_10?crid"
       "=2GJVN1BCGVS6P&dib=eyJ2IjoiMSJ9"
       ".RMA5ihmlCzcuJy8k6E88yCEBOGh0T9Dl3w78rHtfLpXBLG2Gu0c61PA5WeNO_cYj2HMhdgRTSsfgRT1bc1XQJCO6EnYpDdoF"
       "-tsGlg_lAo5TRtjdnajyNxSf6Cd-mYShWh_MDwISHiyHfhrkTz7BMf61jPnCdK7sv"
       "-5HLnXejH_jZKUFUh9T_oKuIWEZU0LNTtfdLpH32AN4IKRufbFIs0Q7AxWJK_oFlA9veK7saPU.HJtsDmto5BxjN"
       "-jHHGPXYfDOwHSzfvB7VXHpgUkiSNk&dib_tag=se&keywords=noise%2Bcancelling%2Bheadphones&qid=1723231839&sprefix"
       "=noise%2Bcancel%2Caps%2C156&sr=8-10&th=1")

response = requests.get(URL, headers={"Accept-Language": "en-US",
                                      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 "
                                                    "Safari/537.36",
                                      })
insta_pot_web = response.text

soup = BeautifulSoup(insta_pot_web, "html.parser")

price_whole = soup.find(name="span", class_="a-price-whole")
price_fraction = soup.find(name="span", class_="a-price-fraction")
product = soup.find(name="span", class_="a-size-large product-title-word-break").getText()
product = ' '.join(product.split())

total_price = float(price_whole.getText() + price_fraction.getText())

print(soup.prettify())

# Send Email if price drops below $300

if total_price < 300:
    my_email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    with smtplib.SMTP(os.getenv("SMTP_ADDRESS"), port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="brian.avrit@verkada.com",
            msg=f"Subject:Price Alert\n\n {product} is now ${total_price} \n\n {URL}".encode("utf-8")
        )

