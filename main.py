import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import re

# Set up the WebDriver
driver = webdriver.Chrome()

# List of URLs to scrape for credit cards from different banks
base_url = "https://www.soulwallet.com/credit-cards-uae/"
bank_urls = [
    "emirates-nbd-credit-cards", "adcb-credit-cards", "dubai-islamic-bank-dib-credit-cards", "abu-dhabi-islamic-bank-adib-credit-cards", "american-express-amex-credit-cards", "commercial-bank-international-cbi-credit-cards", "deem-credit-cards", "first-abu-dhabi-bank-fab-credit-cards", "najm-credit-cards", "rakbank-credit-cards", "standard-chartered-bank-scb-credit-cards", "united-arab-bank-uab-credit-cards", "emirates-islamic-bank-eib-credit-cards", "mashreq-bank-credit-cards", "al-masraf-credit-cards", "citibank-credit-cards", "commercial-bank-dubai-cbd-credit-cards", "finance-house-credit-cards", "hsbc-credit-cards", "noor-bank-credit-cards", "simplylife-credit-cards", "union-national-bank-unb-credit-cards", "dubai-first-credit-cards"
     
    # Add more bank URLs as needed...
]

# Data storage
cards_data = []

def find_optional_element_and_get_text_content(driver_or_element, by, locator):
    try:
        return driver_or_element.find_element(by, locator).get_attribute('textContent')
    except NoSuchElementException:
        return None

# Function to scrape credit card details from a bank page
def scrape_bank_cards(bank_url):
    driver.get(bank_url)
    # time.sleep(3)  # Wait for the page to load

    # load_more_buttons = driver.find_elements(By.LINK_TEXT, 'LOAD MORE')
    # for button in load_more_buttons:
    #     driver.execute_script('arguments[0].click()', button)
    #     driver.implicitly_wait(10)
    #     load_more_buttons.extend(driver.find_elements(By.LINK_TEXT, 'LOAD MORE'))
    
    # Locate the card elements (adjust XPath based on actual structure)
    card_elements = driver.find_elements(By.XPATH, "//div[@class='tocc_card']")
    
    for card in card_elements:
        try:
            # ActionChains(driver, 0).scroll_to_element(card).perform()
            card_id_string = card.find_element(By.XPATH, "./div[@class='row'][1]").get_attribute('id')
            card_id = int(re.search(r'card-(?P<id>\d+)', card_id_string).group('id'))
            print(card_id)
            # quick_view_button = card.find_element(By.XPATH, f".//*[@id='d_accordion{card_id}']/div/div[1]/h5/button")
            # driver.execute_script('arguments[0].click()', quick_view_button)
            bank_name = find_optional_element_and_get_text_content(card, By.XPATH, f".//*[@id='bank-name-{card_id}']")
            print(bank_name)
            card_name = find_optional_element_and_get_text_content(card, By.XPATH, f".//*[@id='card-name-{card_id}']")
            print(card_name)
            min_salary = find_optional_element_and_get_text_content(card, By.XPATH, f".//*[@id='card-ms-{card_id}']")
            print(min_salary)
            interest_rate = find_optional_element_and_get_text_content(card, By.XPATH, f".//*[@id='card-rate-{card_id}']")
            print(interest_rate)
            annual_fee = find_optional_element_and_get_text_content(card, By.XPATH, f".//*[@id='card-af-{card_id}']")
            print(annual_fee)
            non_aed_transaction_fee = find_optional_element_and_get_text_content(card, By.XPATH, f".//*[@id='d_{card_id}1']/div[@class='card-body']/div[@class='row'][1]/div/p[.='Non AED Transaction Fee']/following-sibling::*[1]")
            print(non_aed_transaction_fee)
            cash_advance_fee = find_optional_element_and_get_text_content(card, By.XPATH, f".//*[@id='d_{card_id}1']/div[@class='card-body']/div[@class='row'][1]/div/p[.='Cash Advance Fee']/following-sibling::*[1]")
            print(cash_advance_fee)
            joining_offer = find_optional_element_and_get_text_content(card, By.XPATH, f".//*[@id='d_{card_id}1']/div[@class='card-body']/div[@class='row'][1]/div/p[.='Joining Offers']/following-sibling::*[1]")
            print(joining_offer)
            key_features = find_optional_element_and_get_text_content(card, By.XPATH, f".//*[@id='d_{card_id}1']/div[@class='card-body']/div[@class='row'][2]/div/p[.='Key Features']/following-sibling::*[1]")
            print(key_features)
            reward_features = find_optional_element_and_get_text_content(card, By.XPATH, f".//*[@id='d_{card_id}1']/div[@class='card-body']/div[@class='row'][2]/div/p[.='Reward Features']/following-sibling::*[1]")
            print(reward_features)
            things_to_be_aware_of = find_optional_element_and_get_text_content(card, By.XPATH, f".//*[@id='d_{card_id}1']/div[@class='card-body']/div[@class='row'][2]/div/p[.='Things To Be Aware Of']/following-sibling::*[1]")
            print(things_to_be_aware_of)
            other_key_benefits = find_optional_element_and_get_text_content(card, By.XPATH, f".//*[@id='card-ob-{card_id}']")
            print(other_key_benefits)
            top_reason_to_choose = find_optional_element_and_get_text_content(card, By.XPATH, f".//*[@id='card-trc-{card_id}']")
            print(top_reason_to_choose)

            cards_data.append({
                'Bank Name': bank_name,
                'Card Name': card_name,
                'Minimum Salary': min_salary,
                'Interest Rate': interest_rate,
                'Annual Fee': annual_fee,
                'Non AED Transaction Fee': non_aed_transaction_fee,
                'Cash Advance Fee': cash_advance_fee,
                'Joining Offers' : joining_offer,
                'Key Features' : key_features,
                'Reward Features': reward_features,
                'Things To Be Aware Of': things_to_be_aware_of,
                'Other Key Benefits' : other_key_benefits,
                'Top Reasons To Choose' : top_reason_to_choose



            })
        except Exception as e:
            print(f"Error scraping card: {e}")
            continue

# Loop through each bank URL and scrape the card data
for bank_url in bank_urls:
    full_url = base_url + bank_url
    scrape_bank_cards(full_url)

# Close the WebDriver
driver.quit()

# Create a DataFrame and save it to Excel
df = pd.DataFrame(cards_data)
df.to_excel(r"D://UAE//sat1_cc_uae.xlsx", index=False)

print("Data scraping completed and saved to sat1_cc_uae.xlsx")
