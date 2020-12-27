from utils import SimpleLogger
import requests, json, bs4, time, random, os, threading
from bs4 import BeautifulSoup, SoupStrainer
from discord_webhook import DiscordEmbed, DiscordWebhook

os.system("cls")

logger = SimpleLogger()

class Monitor:
    def __init__(self):
        self.session = requests.Session()
        self.delay = 3.5
        self.userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        self.discordWebhook = "YOUR_DISCORD_WEBHOOK"
        self.profile = {
            "firstAndMiddleName": "YOUR_FIRST_AND_MIDDLE_NAME",
            "lastName": "YOUR_LAST_NAME",
            "birthDay": "YOUR_BIRTH_DAY",
            "birthMonth": "YOUR_BIRTH_MONTH",
            "birthYear": "YOUR_BIRTH_YEAR",
            "licenseNumber": "YOUR_LICENSE_NUMBER"
        }
        logger.yellow("Starting Monitor...")
        self.login()

    def login(self):

        logger.yellow("Logging into DVLA...")

        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Host": "wsr.theorytest.dvsa.gov.uk",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.userAgent
        }

        logger.yellow("Getting Login Page...")

        while True:
            try:
                resp = self.session.get("https://wsr.theorytest.dvsa.gov.uk/testtaker/signin/SignInPage/DSA?locale=en_GB", headers=self.headers)
                soup = BeautifulSoup(resp.text, 'lxml')
                componentRoot = soup.find('input', {'name': 'componentRoot'})['value']
                viewState = soup.find('input', {'name': 'javax.faces.ViewState'})['value']
                logger.blue("Successfully Parsed Login Form!")
                break
            except Exception as e:
                logger.red(f"Get Login Page: Exception Occured => {type(e).__name__} - Retrying...")
                time.sleep(self.delay)

        logger.yellow("Attempting to Login...")

        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "wsr.theorytest.dvsa.gov.uk",
            "Origin": "https://wsr.theorytest.dvsa.gov.uk",
            "Referer": "https://wsr.theorytest.dvsa.gov.uk/testtaker/signin/SignInPage/DSA?locale=en_GB",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.userAgent
        }

        self.data = {
            "inputFIRST_NAME": self.profile['firstAndMiddleName'],
            "inputLAST_NAME": self.profile['lastName'],
            "inputCLIENT_CANDIDATE_ID": self.profile['licenseNumber'],
            "inputQUESTION1967.day": self.profile['birthDay'],
            "inputQUESTION1967.month": self.profile['birthMonth'],
            "inputQUESTION1967.year": self.profile['birthYear'],
            "componentRoot": componentRoot,
            "submitButton": "Log in",
            "SignInForm_SUBMIT": "1",
            "javax.faces.ViewState": viewState
        }

        while True:
            try:
                resp = self.session.post("https://wsr.theorytest.dvsa.gov.uk/testtaker/signin/SignInPage/DSA", headers=self.headers, data=self.data)
                if resp.status_code == 200 and "/Dashboard" in resp.url:
                    soup = BeautifulSoup(resp.text, 'lxml')
                    actionCol = soup.find('td', {'class': 'actionCol'})
                    self.examRescheduleName = actionCol.find('input', {'value': 'Change test'})['name']
                    self.viewState = soup.find('input', {'name': 'javax.faces.ViewState'})['value']
                    logger.green("Successfully Logged In!")
                    return self.changeTest()
                else:
                    logger.red(f"Login: An Error Occured => Status Code: {resp.status_code} - Retrying...")
                    time.sleep(self.delay)
            except Exception as e:
                logger.red(f"Login: Exception Occured => {type(e).__name__} - Retrying...")
                time.sleep(self.delay)

    def changeTest(self):

        logger.yellow("Going to 'Change Test' page...")

        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "wsr.theorytest.dvsa.gov.uk",
            "Origin": "https://wsr.theorytest.dvsa.gov.uk",
            "Referer": "https://wsr.theorytest.dvsa.gov.uk/testtaker/registration/custom/Dashboard/DSA",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.userAgent
        }

        self.data = {
            self.examRescheduleName: "Change test",
            "DashBoardForm_SUBMIT": "1",
            "javax.faces.ViewState": self.viewState
        }

        while True:
            try:
                resp = self.session.post("https://wsr.theorytest.dvsa.gov.uk/testtaker/registration/custom/Dashboard/DSA", headers=self.headers, data=self.data)
                if resp.status_code == 200 and "/CalendarAppointmentSearchPage" in resp.url:
                    logger.green("Reached 'Change Test' Page!")
                    soup = BeautifulSoup(resp.text, 'lxml')
                    self.viewState = soup.find('input', {'name': 'javax.faces.ViewState'})['value']
                    self.monitorUrl = f"https://wsr.theorytest.dvsa.gov.uk{soup.find('form', {'name': 'toggleForm'})['action']}"
                    logger.blue("Successfully Parsed Necessary Objects!")
                    return self.monitor()
                else:
                    logger.red(f"Change Test: An Error Occured => Status Code: {resp.status_code} - Retrying...")
                    time.sleep(self.delay)
            except Exception as e:
                logger.red(f"Change Test: Exception Occured => {type(e).__name__} - Retrying...")
                time.sleep(self.delay)

    def monitor(self):
        
        logger.yellow("Initializing Monitor...")

        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Faces-Request": "partial/ajax",
            "Host": "wsr.theorytest.dvsa.gov.uk",
            "Origin": "https://wsr.theorytest.dvsa.gov.uk",
            "Referer": "https://wsr.theorytest.dvsa.gov.uk/testtaker/registration/CalendarAppointmentSearchPage/DSA?conversationId=660698",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": self.userAgent
        }

        self.data = {
            "selectedAppointmentId": "",
            "calendarForm_SUBMIT": "1",
            "javax.faces.ViewState": self.viewState,
            "year": "2021",
            "month": "1",
            "org.richfaces.ajax.component": "j_id_4l",
            "j_id_4l": "j_id_4l",
            "rfExt": "null",
            "AJAX:EVENTS_COUNT": "1",
            "javax.faces.partial.event": "undefined",
            "javax.faces.source": "j_id_4l",
            "javax.faces.partial.ajax": "true",
            "javax.faces.partial.execute": "@component",
            "javax.faces.partial.render": "@component",
            "calendarForm": "calendarForm"
        }

        while True:
            try:
                month = random.choice(["1", "2"])
                self.data['month'] = month
                resp = self.session.post(self.monitorUrl, headers=self.headers, data=self.data)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'xml')
                    jsonResponse = json.loads(str(json.loads(str(soup.find('changes').find('data').text.strip()))))
                    if len(jsonResponse['availableDates']) == 0:
                        logger.yellow(f"No available theory test dates found in month: {month} - Monitoring...")
                        try:
                            logger.blue(f"DVLA response: {jsonResponse['errorMessages']}")
                        except:
                            pass
                        time.sleep(self.delay)
                    else:
                        logger.green(f"Available Dates Found: {jsonResponse['availableDates']} - Gogogogogo!")
                        self.availableDates = jsonResponse['availableDates']
                        return self.sendDiscordWebhook()
                else:
                    logger.red(f"Monitor: An Error Occured => Status Code: {resp.status_code} - Retrying...")
                    time.sleep(self.delay)
            except Exception as e:
                logger.red(f"Monitor: Exception Occured => {type(e).__name__} - Retrying...")
                time.sleep(self.delay)

    def sendDiscordWebhook(self):
        logger.yellow("Sending Discord Webhook...")
        webhook = DiscordWebhook(url=self.discordWebhook, username="New Theory Test Dates Found", content="@everyone")
        embed = DiscordEmbed(title="New Theory Test Dates Found!", color=0x00FF00)
        embed.add_embed_field(name="Available Dates", value=str(self.availableDates))
        embed.set_timestamp()
        webhook.add_embed(embed)
        webhook.execute()
        logger.green("Webhook Sent!")

if __name__  == '__main__':
    threadCount = input("Enter Thread Count: ")
    os.system("cls")
    for i in range(int(threadCount)):
        threading.Thread(target=Monitor).start()