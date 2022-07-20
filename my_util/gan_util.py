from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.request
import os, time

def animeGAN(src_fname, dst_dir, version):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')   # 화면없이 실행
    options.add_argument('--no-sandbox')
    #options.add_argument('--disable-infobars')
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome('chromedriver', options=options)

    url = 'https://huggingface.co/spaces/akhaliq/AnimeGANv2'
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get(url)
    time.sleep(5)

    # iframe 전환
    driver.switch_to.frame('iFrameResizer0')
    # 이미지 업로드
    upload = driver.find_element(By.CSS_SELECTOR, 'input.hidden-upload.hidden')
    fname = os.path.join(dst_dir, src_fname)        # .replace('/', '\\') in Windows
    upload.send_keys(fname)
    time.sleep(1)
    # 버전 선택
    if version == '1':
        driver.find_element(By.CSS_SELECTOR, 'input.gr-check-radio.gr-radio').click()

    # 제출하기 버튼 클릭
    button = driver.find_element(By.CSS_SELECTOR, 'button.gr-button.gr-button-lg.gr-button-primary.self-start')
    button.click()
    time.sleep(5)

    ani_img = driver.find_element(By.XPATH, '//*[@id="2"]/img')
    img_url = ani_img.get_attribute('src')
    dst_file = os.path.join(dst_dir, "animated_image.jpg")
    urllib.request.urlretrieve(img_url, dst_file)

    driver.close()