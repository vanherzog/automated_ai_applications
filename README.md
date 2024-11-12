# 🧑‍💻 Freelance Application Bot 🤖

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/) [![GPT-4 Powered](https://img.shields.io/badge/GPT--4-powered-yellowgreen)](https://openai.com/) [![Docker](https://img.shields.io/badge/Docker-Containerized-blue)](https://www.docker.com/)  

## 🌟 Overview

This bot automates the process of **sending job applications to Freelancermap.de** using **GPT-4 for crafting tailored cover letters** and **Selenium for web interactions**. It comes with a **React-based interface** for managing job details and sending applications, and uses **Snowflake** as a database solution to store job logs, application history, and configuration.

> **Why Automate?**  
> Manual job applications can be repetitive and time-consuming. This bot leverages AI and automation to apply to jobs for you, ensuring each application is unique and professionally written.

---

## ⚙️ Key Features

- **📝 Custom Application Writing**: GPT-4 crafts professional and context-aware job applications based on your CV and the job description.
- **🌐 Web Automation with Selenium**: Uses Selenium to navigate Freelancermap.de, locate jobs, and apply on your behalf.
- **💻 User-Friendly Frontend**: A React-based interface displays job details, generated applications, and allows easy navigation and control.
- **📦 Docker Integration**: Easily deployable with Docker, ensuring smooth operation across environments.
- **📊 Database Integration with Snowflake**: Stores application history, job logs, and other important data for tracking and analysis.

---

## 🏗️ Tech Stack

- **Backend**: Python, GPT-4 (via OpenAI API), Selenium
- **Frontend**: React
- **Database**: Snowflake
- **Containerization**: Docker

---

## 🚀 Getting Started

### Prerequisites

Ensure the following are installed:

- **Python 3.x**
- **Docker**
- **Node.js & npm** (for frontend setup)
- **Snowflake Account** (for database setup)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/freelance-application-bot.git
cd freelance-application-bot
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory with the following variables:

```bash
OPENAI_API_KEY=your_openai_api_key
SNOWFLAKE_USER=your_snowflake_username
SNOWFLAKE_PASSWORD=your_snowflake_password
SNOWFLAKE_ACCOUNT=your_snowflake_account
```

### 3. Build and Run with Docker

To build and run the bot using Docker, simply use the following commands:

```bash
docker-compose build
docker-compose up
```

The bot will now be accessible at `http://localhost:3000` for frontend interaction.

### 4. Launch Without Docker (For Development)

#### Backend

```bash
# Install backend dependencies
pip install -r requirements.txt

# Start the backend
python app.py
```

#### Frontend

```bash
cd frontend
npm install
npm start
```

### 5. Running Selenium WebDriver

Ensure **ChromeDriver** is installed and configured (or use `webdriver_manager` for auto-setup in code).

---

## 🎨 Frontend Overview

The React-based interface includes:

- **Job Description Panel**: View job details pulled from Freelancermap.de.
- **Application Panel**: Review or edit the GPT-4 generated application.
- **Control Buttons**: Choose to skip, edit, or submit applications directly from the UI.

![Frontend Screenshot](screenshot.png)

---

## 📊 Database: Snowflake

All job logs and application history are stored in Snowflake, allowing for easy data analysis and tracking of past applications.

---

## 🤖 How It Works

1. **Scraping Jobs**: Uses Selenium to scrape job listings based on criteria from Freelancermap.de.
2. **Generating Applications**: Each job’s description is fed into GPT-4, along with your resume details, to create a tailored cover letter.
3. **Automated Submission**: The bot automatically submits the application via Selenium.
4. **Logging to Snowflake**: Each application is logged for reference.

---

## ⚠️ Disclaimer

This bot is for **educational purposes only**. Ensure compliance with **Freelancermap.de's terms of service** before using.

---

## 👨‍💻 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 📞 Support

For any issues or questions, please open an issue on GitHub or reach out via email at support@yourdomain.com.

--- 

Happy automating! 🚀
