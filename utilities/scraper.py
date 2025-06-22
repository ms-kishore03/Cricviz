import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

def get_live_match_links():
    driver.get("https://www.cricbuzz.com/cricket-match/live-scores")
    time.sleep(3)

    series_data = []

    for j in range(2, 10):
        try:
            series_name = driver.find_element(By.XPATH, f'//*[@id="page-wrapper"]/div[5]/div[2]/div/div[{j}]/h2').text
            teams = driver.find_element(By.XPATH, f'//*[@id="page-wrapper"]/div[5]/div[2]/div/div[{j}]/div/div[1]/div/h3').text
            match_no = driver.find_element(By.XPATH, f'//*[@id="page-wrapper"]/div[5]/div[2]/div/div[{j}]/div/div[1]/div/span').text
            time_venue = driver.find_element(By.XPATH, f'//*[@id="page-wrapper"]/div[5]/div[2]/div/div[{j}]/div/div[1]/div/div').text
            commentary_link = driver.find_element(By.XPATH, f'//*[@id="page-wrapper"]/div[5]/div[2]/div/div[{j}]/div/div[2]/a').get_attribute("href")

            driver.get(commentary_link)
            time.sleep(2)

            try:
                scorecard_link = driver.find_element(By.XPATH, '//*[@id="matchCenter"]/div[2]/nav/a[2]').get_attribute("href")
            except Exception:
                continue


            series_data.append({
                "series_name": series_name,
                "teams": teams,
                "match_no": match_no,
                "time_and_venue": time_venue,
                "commentary_link": commentary_link,
                "scorecard_link": scorecard_link
            })

            driver.back()
            time.sleep(1)

        except Exception:
            continue

    return series_data



def get_match_details(match_info):
    driver.get(match_info["commentary_link"])
    time.sleep(2)

    try:
        score = driver.find_element(By.XPATH,'//*[@id="matchCenter"]/div[3]/div[2]/div[1]/div[1]/div[1]').text

        driver.get(match_info["scorecard_link"])
        time.sleep(2)

        match_details=[]

        for inn in range(1, 5):
            for sec in range(1, 5):
                try:
                    detail = driver.find_element(By.XPATH, f'//*[@id="innings_{inn}"]/div[{sec}]').text
                    match_details.append(detail.strip().split("\n"))
                except Exception:
                    continue

        return {
            **match_info,
            "score": score,
            "match_details":match_details
        }
    except Exception:
        return None


def scrape_all_match_data():

    final_data = {}

    try:
        match_list = get_live_match_links()

        for match in match_list:
            details = get_match_details(match)
            if details:
                key = f"{details['series_name']} - {details['teams']} ({details['match_no']})"
                final_data[key] = details
    finally:
        driver.quit()

    return final_data

