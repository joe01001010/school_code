import undetected_chromedriver as uc
import time

def main():
    website_list = [
        'https://www.google.com/search?q=Colorado+Springs+Colorado+USA+weather',
        'https://www.google.com/search?q=Winter+Park+Colorado+USA+weather',
        'https://www.google.com/search?q=Winter+Park+Florida+USA+weather',
        'https://www.google.com/search?q=Alexandria+Virginia+USA+weather',
        'https://www.google.com/search?q=Alexandria+Ontario+Canada+weather',
        'https://www.google.com/search?q=Melbourne+Florida+USA+weather',
        'https://www.google.com/search?q=Melbourne+Victoria+Australia+weather'
    ]
    browser = uc.Chrome()
    for website in website_list:
        browser.get(website)
        time.sleep(2)

    input("Press enter to close browser")
    browser.quit()



if __name__ == '__main__':
    main()