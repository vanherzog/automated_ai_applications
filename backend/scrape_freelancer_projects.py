import os
import time
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
from docx import Document
from kafka import KafkaProducer
import json
from apikey import apikey

# Set up Selenium WebDriver with Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run browser in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Disable sandbox for Chrome

# In your producer script, update the bootstrap_servers to:
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',  # Use internal Docker network address
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)



def scrape_and_create_application():
    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Define the URL and headers
    url = "https://www.freelancermap.de/project/search/ajax?remoteInPercent%5B0%5D=100&query=AI&countries%5B%5D=1&sort=2&pagenr=1"
    headers = {
        "Host": "www.freelancermap.de",
        "Cookie": "PHPSESSID=ee51l2engi5ujret31rpv932fd; _gcl_au=1.1.1129049897.1731054686; OptanonAlertBoxClosed=2024-11-08T08:31:28.401Z; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Nov+08+2024+09%3A31%3A28+GMT%2B0100+(Mitteleurop%C3%A4ische+Normalzeit)&version=6.26.0&isIABGlobal=false&hosts=&consentId=284516b9-86c8-409b-8d05-548dd84539b6&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1; _ga_XJ51KBMEP2=GS1.1.1731054688.1.0.1731054688.60.0.0; _ga_KB8J09DXVB=GS1.1.1731054688.1.0.1731054688.0.0.0; _ga=GA1.2.967664699.1731054689; _gid=GA1.2.1634529130.1731054689; _gat=1; _fbp=fb.1.1731054689059.363034928859188081; _hjSessionUser_1122021=eyJpZCI6ImYzZDYxYmQ2LTJkNDMtNTlkZi05YTYyLTVlOWMyMjM3MTIxZCIsImNyZWF0ZWQiOjE3MzEwNTQ2ODk1NDUsImV4aXN0aW5nIjpmYWxzZX0=; _hjSession_1122021=eyJpZCI6ImVmYzhlODI3LWExMDYtNDQyNC04NTdhLWJhNjUxNGZhMTlmMyIsImMiOjE3MzEwNTQ2ODk1NDcsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\"",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Accept-Language": "de-DE",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://www.freelancermap.de",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.freelancermap.de/projektboerse.html?remoteInPercent%5B0%5D=100&query=ki&sort=2&pagenr=1",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=1, i"
    }

    # Define the JSON payload
    payload = {
        "changed": ["query", "sort"]
    }

    # Load the CV and project details from data.wordx file
    def read_docx(file_path):
        try:
            document = Document(file_path)
            text = ""
            for para in document.paragraphs:
                text += para.text + "\n"
            return text.strip()
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return "Default CV and project details text."

    # cv_and_projects_text = read_docx("Skills_data.docx")

    cv_file_path = os.path.join(os.path.dirname(__file__), 'Skills_data.docx')
    cv_and_projects_text = read_docx(cv_file_path)

    # Make the POST request
    response = requests.post(url, headers=headers, json=payload)

    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        projects = data.get("projects", [])

        # Extract and print required fields
        project_details = []
        for project in projects:
            slug = project.get("slug")
            title = project.get("title")
            description = project.get("description")

            project_details.append({
                "slug": slug,
                "title": title,
                "description": description
            })

        # Display the extracted project details and generate applications
        for proj in project_details:
            print(f"Project: {proj['title']}")
            url = f"https://www.freelancermap.de/projekt/{proj['slug']}"

            # Use Selenium to load the page and find the content
            driver.get(url)
            time.sleep(3)  # Allow some time for the page to load

            try:
                # Find the content div using Selenium's find_element method
                content_div = driver.find_element(By.CSS_SELECTOR, "div.content:not(.keywords-container.content)")
                content_text = content_div.get_attribute('innerText').strip()

                # Combine the project description and content_text with CV information
                prompt = f"""
                You are an AI assistant helping to write a job application.

                Here is the job description:
                {content_text}

                Here is the applicant's CV and project details:
                {cv_and_projects_text}

                Write a professional job application based on the job description and the applicant's CV. The application should highlight relevant experience, skills, and reasons why the applicant is a good fit for the job.
                Try to write the application fitting to the used language in the job description. If its written not that formal, write also more chill.
                """

                # Initialize OpenAI client
                client = OpenAI(api_key=apikey)

                # Call the GPT-4 API to generate the job application
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="gpt-4",  # Adjust to the model you are using
                    max_tokens=800,  # Adjust based on the desired length
                    temperature=0.7,  # Adjust creativity
                )

                # Print the generated job application
                job_application = chat_completion.choices[0].message.content
                print("Generated Job Application:\n", job_application)

                # Send project and job application to Kafka
                message = {
                    "project_title": proj['title'],
                    "project_slug": proj['slug'],
                    "project_description": proj['description'],
                    "job_application": job_application
                }

                # Send the message to Kafka (Topic: 'job-applications')
                producer.send('job-applications', message)

                print("-" * 50)
            except Exception as e:
                print("Error fetching content:", e)

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

    # Close the browser after scraping
    driver.quit()


def main():
    scrape_and_create_application()


if __name__ == "__main__":
    main()
