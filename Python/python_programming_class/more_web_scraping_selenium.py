import undetected_chromedriver as uc

def main():
    browser = uc.Chrome()
    browser.get('https://www.google.com/search?q=Colorado+Springs+Colorado+USA+weather')

    input("Press enter to close browser")
    browser.quit()



if __name__ == '__main__':
    main()