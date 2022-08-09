from playwright.sync_api import sync_playwright
import time
import os

class Cheater:
    def __init__(self,mode):
        self.mode = mode
        if 'data' not in os.listdir():
            os.mkdir('data')
    def login(self,p,email,password,email_recv):
        p.goto('https://twitter.com/i/flow/login')
        p.wait_for_selector('//input[@name="text"]',timeout=10000)
        p.fill('//input[@name="text"]',email)
        p.click('//div[@role="button"][2]')
        p.wait_for_selector('//input[@name="password"]', timeout=10000)
        p.fill('//input[@name="password"]', password)
        p.click('//div[@role="button"and@data-testid="LoginForm_Login_Button"]')

        try:
            p.wait_for_selector('//input[@data-testid="ocfEnterTextTextInput"]', timeout=3000)
            p.fill('//input[@data-testid="ocfEnterTextTextInput"]', email_recv)
            p.click('//div[@role="button"and@data-testid="ocfEnterTextNextButton"]')
        except:
            pass
    def get_account_cookie(self,email,password,email_recv):
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(channel='msedge',headless=self.mode)
                context = browser.new_context()
                page = context.new_page()
                self.login(page,email,password,email_recv)
                page.wait_for_selector('//div[@data-testid="tweetTextarea_0"]', timeout=10000)
                page.wait_for_timeout(3000)
                context.storage_state(path=f"data/{email}.json")
                context.close()
                page.close()
                return True,email
            except :
                return False,email
    def create_tweet(self,acc_email,post_text='',media_file='',process="all",tweet_type='space'):
        with sync_playwright() as p:
            if tweet_type == 'normal':
                browser = p.chromium.launch(channel='msedge',headless=self.mode)
                context = browser.new_context(storage_state=f"data/{acc_email}.json")
                page = context.new_page()
                page.goto('https://twitter.com')
                if process == 'tweet':
                    page.wait_for_selector('//div[@aria-label="Tweet text"]',timeout=10000)
                    page.fill('//div[@aria-label="Tweet text"]',post_text)
                elif process == 'tweet_media':
                    page.locator('//input[@data-testid="fileInput"]').set_input_files(media_file)
                else:
                    page.wait_for_selector('//div[@aria-label="Tweet text"]', timeout=10000)
                    page.fill('//div[@aria-label="Tweet text"]',post_text)
                    page.locator('//input[@data-testid="fileInput"]').set_input_files(media_file)
                page.wait_for_selector('//div[@data-testid="tweetButtonInline"]', timeout=10000)
                page.click('//div[@data-testid="tweetButtonInline"]')
            else:
                browser = p.chromium.launch(channel='msedge', headless=self.mode)
                context = browser.new_context(storage_state=f"data/{acc_email}.json",user_agent='Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.129 Mobile Safari/537.36')
                page = context.new_page()
                page.goto('https://twitter.com')
                page.wait_for_selector('//a[@data-testid="SideNav_NewTweet_Button"]')
                page.click('//a[@data-testid="SideNav_NewTweet_Button"]')
                if process == 'tweet':
                    page.wait_for_selector('//textarea[@data-testid="tweetTextarea_0"]')
                    page.fill('//textarea[@data-testid="tweetTextarea_0"]',post_text)
                elif process == 'tweet_media':
                    page.locator('//input[@data-testid="fileInput"]').set_input_files(media_file)
                else:
                    page.wait_for_selector('//textarea[@data-testid="tweetTextarea_0"]')
                    page.fill('//textarea[@data-testid="tweetTextarea_0"]', post_text)
                    media_input = page.locator('//input[@data-testid="fileInput"]').first
                    media_input.set_input_files(media_file)
                page.wait_for_selector('//div[@data-testid="tweetButton"]')
                page.click('//div[@data-testid="tweetButton"]')

            page.wait_for_selector('text=Your Tweet was sent',timeout=20000)
            page.click('//article[@data-testid="tweet"]')
            url = page.url.replace('mobile.','')
            context.storage_state(path=f"data/{acc_email}.json")
            context.close()
            page.close()
            return url
    def tweet_activity(self,acc_email,url,comment,process="all"):
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(channel='msedge',headless=self.mode)
                context = browser.new_context(storage_state=f"data/{acc_email}.json")
                page = context.new_page()
                page.goto(url)
                if process == 'comment':
                    page.wait_for_selector('//div[@data-testid="reply"]',timeout=10000)
                    page.click('//div[@data-testid="reply"]')
                    page.wait_for_selector('//div[@data-testid="tweetTextarea_0"]', timeout=10000)
                    page.fill('//div[@data-testid="tweetTextarea_0"]', comment)
                    page.wait_for_selector('//div[@data-testid="tweetButton"]', timeout=10000)
                    page.click('//div[@data-testid="tweetButton"]')
                elif process == 'like':
                    page.wait_for_selector('//div[@data-testid="like"]', timeout=10000)
                    page.click('//div[@data-testid="like"]')
                elif process == 'quote' :
                    page.wait_for_selector('//div[@aria-haspopup="menu"and@role="button"]')
                    page.locator('//div[@aria-haspopup="menu"and@role="button"]').nth(2).click()
                    page.wait_for_selector('//a[@role="menuitem"]', timeout=10000)
                    page.click('//a[@role="menuitem"]')
                    page.wait_for_selector('//div[@role="textbox"]', timeout=10000)
                    page.fill('//div[@role="textbox"]', comment)
                    page.wait_for_selector('//div[@data-testid="tweetButton"]', timeout=10000)
                    page.click('//div[@data-testid="tweetButton"]')
                elif process == 'retweet':
                    page.wait_for_selector('//div[@aria-haspopup="menu"and@role="button"]')
                    page.locator('//div[@aria-haspopup="menu"and@role="button"]').nth(2).click()
                    page.wait_for_selector('//div[@data-testid="retweetConfirm"]', timeout=10000)
                    page.click('//div[@data-testid="retweetConfirm"]')
                else:
                    page.wait_for_selector('//div[@data-testid="reply"]', timeout=10000)
                    page.click('//div[@data-testid="reply"]')
                    page.wait_for_selector('//div[@data-testid="tweetTextarea_0"]', timeout=10000)
                    page.fill('//div[@data-testid="tweetTextarea_0"]', comment)
                    page.wait_for_selector('//div[@data-testid="tweetButton"]', timeout=10000)
                    page.click('//div[@data-testid="tweetButton"]')
                    page.wait_for_timeout(700)
                    page.wait_for_selector('//div[@data-testid="like"]', timeout=10000)
                    page.click('//div[@data-testid="like"]')
                    page.wait_for_timeout(700)
                    page.wait_for_selector('//div[@aria-haspopup="menu"and@role="button"]')
                    page.locator('//div[@aria-haspopup="menu"and@role="button"]').nth(2).click()
                    page.wait_for_selector('//div[@data-testid="retweetConfirm"]', timeout=10000)
                    page.click('//div[@data-testid="retweetConfirm"]')
                    page.wait_for_timeout(700)
                    page.wait_for_selector('//div[@aria-haspopup="menu"and@role="button"]')
                    page.locator('//div[@aria-haspopup="menu"and@role="button"]').nth(2).click()
                    page.wait_for_selector('//a[@role="menuitem"]', timeout=10000)
                    page.click('//a[@role="menuitem"]')
                    page.wait_for_selector('//div[@role="textbox"]', timeout=10000)
                    page.fill('//div[@role="textbox"]', comment)
                    page.wait_for_selector('//div[@data-testid="tweetButton"]', timeout=10000)
                    page.click('//div[@data-testid="tweetButton"]')
                page.wait_for_timeout(500)

                context.storage_state(path=f"data/{acc_email}.json")
                context.close()
                page.close()
                return True, acc_email
            except:
                return False, acc_email


Cheater(False).tweet_activity(f'Nihan25730986','https://twitter.com/hourly_shitpost/status/1551869977510252544','HAHAHA','like')
