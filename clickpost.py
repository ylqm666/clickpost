import argparse
from re import template
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


# python clickpost.py --username='username' --password='password' --cvv=9999 --template_path='template_path'

driver = webdriver.Chrome(ChromeDriverManager().install())
parser = argparse.ArgumentParser()
parser.add_argument('--username', required=True)
parser.add_argument('--password', required=True)
parser.add_argument('--cvv', required=True)
parser.add_argument('--template_path', required=True)
args = parser.parse_args()

username = args.username
password = args.password
cvv = args.cvv
template_path = args.template_path


def login(username, password):
    driver.get('https://clickpost.jp/auth/yconnect')
    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id("btnNext").click()
    # ヤフーのログイン画面はIDを入力した後にJSのイベントが走るので、念の為2秒"待ち"
    time.sleep(1)
    driver.find_element_by_id("passwd").send_keys(password)
    driver.find_element_by_id("btnSubmit").click()
    try:
        # 同意して利用するボタン
        driver.find_element_by_id('.save').click()
    except Exception:
        pass


def logout():
    driver.get("https://login.yahoo.co.jp/config/login?logout=1")


def batch_applocate():
    # まとめ申込
    driver.execute_script("javascript:Turbolinks.visit('/labels/multiple_upload');")
    time.sleep(1)
    csv_file = driver.find_element_by_id('file')
    csv_file.send_keys(template_path)
    time.sleep(1)
    driver.find_element_by_name('commit').click()
    time.sleep(1)
    if driver.find_element_by_id('multi_error_message'):
        print('テンプレートが不正です')
        exit()
    driver.find_element_by_name('create').click()


def pay_agreement(wallet_btn):
    wallet_btn.click()
    driver.find_element_by_name('agreement').click()
    cvv_form = driver.find_element_by_id('cvv')
    cvv_form.send_keys(cvv)
    cvv_form.submit()
    driver.find_element_by_name('continue').click()


def main():
    print('開始します')

    login(username, password)
    time.sleep(1)
    batch_applocate()

    while True:
        try:
            wallet_btn = driver.find_element_by_xpath('//*[@id="send_history"]/span/table/tbody/tr[1]/td[5]/input')
        except Exception:
            print(False)
            print('完了しました')
            break
        if wallet_btn:
            print(True)
            pay_agreement(wallet_btn)
    time.sleep(2)
    logout()
    time.sleep(2)
    driver.close()


if __name__ == '__main__':
    main()
