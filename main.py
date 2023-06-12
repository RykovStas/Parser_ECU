import os
import traceback
import time
import sqlite3
import glob
import xlrd
import schedule
from datetime import timedelta, datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# SETTINGS
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")

    project_directory = os.path.abspath(os.path.dirname(__file__))
    download_directory = os.path.join(project_directory, "")

    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def click_button(driver, button_text):
    button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f"//*[text()='{button_text}']")))
    button.click()


def download_file(driver):
    element = driver.find_element(By.XPATH, '//a/button')
    element.click()
    time.sleep(5)


def process_data():
    project_directory = os.path.abspath(os.path.dirname(__file__))
    data_folder = os.path.join(project_directory, "")

    files = glob.glob(os.path.join(data_folder, 'DAM_*.xls'))
    files.sort(key=os.path.getctime)

    if not files:
        print("No files found in the specified folder.")
        return

    latest_file = files[-1]
    print("Latest file:", latest_file)

    # Load Data to db
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT latest_file FROM LastProcessedFile")
    result = cursor.fetchone()
    last_processed_file = result[0] if result else None

    # VALIDATIONS WITH NEW DATA
    if latest_file == last_processed_file:
        print("The latest file has already been processed.")
        conn.close()
        return

    cursor.execute("CREATE TABLE IF NOT EXISTS Data (Дата TEXT, Година TEXT, Ціна_грн_МВт_год TEXT, Обсяг_продажу_МВт_год TEXT, Обсяг_купівлі_МВт_год TEXT, Заявлений_обсяг_продажу_МВт_год TEXT, Заявлений_обсяг_купівлі_МВт_год TEXT)")

    try:
        workbook = xlrd.open_workbook(latest_file, formatting_info=True, ignore_workbook_corruption=True)
        sheet = workbook.sheet_by_index(0)

        for row in range(1, sheet.nrows):
            row_data = [str(cell.value) for cell in sheet.row(row)]

            next_day = datetime.now() + timedelta(days=1)
            date_str = next_day.strftime("%d.%m.%Y")
            row_data.insert(0, date_str)
            cursor.execute("INSERT INTO Data VALUES (?, ?, ?, ?, ?, ?, ?)", row_data)


        conn.commit()
        print("Data inserted successfully!")

        cursor.execute("INSERT OR REPLACE INTO LastProcessedFile VALUES (?)", (latest_file,))
        conn.commit()
    except Exception as e:
        print("Error occurred while processing data:")
        traceback.print_exc()

    conn.close()


def create_last_processed_file_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS LastProcessedFile (latest_file TEXT)")
    conn.commit()
    conn.close()


def main():
    driver = initialize_driver()
    driver.get("https://www.oree.com.ua/index.php/control/results_mo/DAM")
    button_text = "Погодинні результати на РДН"
    click_button(driver, button_text)
    time.sleep(3)
    download_file(driver)
    process_data()


if __name__ == "__main__":
    create_last_processed_file_table()
    main()
    scheduled_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 12, 30).time()
    schedule.every().day.at(scheduled_time.strftime("%H:%M")).do(main)

    while True:
        schedule.run_pending()
        time.sleep(60)
