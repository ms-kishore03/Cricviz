# Cricviz
## Overview

An intelligent command-line tool that scrapes live cricket match data from Cricbuzz and uses a Large Language Model (LLM) via Groq and LangChain to automatically generate engaging social media posts for Twitter/X and LinkedIn.

## Features

- **Live Data Scraping:** Fetches real-time scores and details for all ongoing cricket matches from Cricbuzz using Selenium.
- **Natural Language Queries:** Simply ask what you want to know in plain English (e.g., "Tell me about the T20 Blast match" or "Get all live matches").
- **Intelligent Agent System:** Uses LangChain agents to understand your query and decide whether to scrape data for a specific match or all of them.
- **AI-Powered Content Creation:** Leverages the power of llama-3.1-8b-instant model to generate a short story that can be posted on social media platforms.
- **Multi-Platform Formatting:** Automatically generates tailored content for:
  - **LinkedIn:** Creates professional, well-structured posts.
  - **Twitter/X:** Crafts engaging, multi-part threads.
- **Interactive CLI:** A user-friendly command-line interface guides you through the process.

## Technologies Used

- **Python:** The primary programming language.
- **Selenium:** For web scraping.
- **Langchain-Groq:** For interacting with the Groq's Llama model.

## Approach

1. User is shown a list of live match series names

2. User chooses to fetch all matches or a specific match

3. fetcher_agent (LangChain agent with scraping tools) retrieves data

4. If the user chooses, formatter_agent formats it for LinkedIn or Twitter using LLM prompts
## Setup
### Prerequisites

- Python 3.8 or above
- [ChromeDriver](https://developer.chrome.com/docs/chromedriver/downloads) that matches your Chrome version. (Make sure the chromedriver executable is in your system's PATH.)
- A GroqAPI key that can be obtained from [Groq](https://groq.com/)

### Installation
1. **Install the required dependencies:** All dependencies are listed in the `requirements.txt` file.  You can install them using pip:

```bash
pip install -r requirements.txt
```
2. **set up your environment variables:** Create a file named .env in the root of the project directory and add your Groq API key.

## Run

Run the main script from the terminal
```bash
python main.py
```

## Improvements

- Add memory support for ongoing interaction
- Export formatted posts to **.txt** files
- Add support for other social platforms (Instagram, Threads, etc.)




