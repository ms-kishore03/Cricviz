import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_groq import ChatGroq
from utilities import scraper

load_dotenv()
api_key = os.getenv("Groq_API_Key")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3
)

print("Fetching all live match details..........")
live_matches_data = scraper.get_live_match_links()
for idx, match in enumerate(live_matches_data):
    print(f"{idx}) {match['series_name']}")

user_input = input("\nWhat do you want to know about these matches?\n"
                   "You can either get information about all the ongoing matches or a specific match from the list:\n")


def get_specific_match_detail(series_name):
    for match in live_matches_data:
        if match['series_name'].lower() == series_name.lower():
            return scraper.get_match_details(match)
    return "No data found for the series name asked."


def linkedin_formatter(match_data):
    prompt = f"Format the following cricket match data for a LinkedIn post:\n\n{match_data}"
    return llm.invoke([{"role": "user", "content": prompt}]).content


def x_formatter(match_data):
    prompt = f"Create an engaging Twitter thread based on this cricket match data:\n\n{match_data}"
    return llm.invoke([{"role": "user", "content": prompt}]).content


fetcher_tools = [
    Tool(
        name="All_Match_Details",
        func=scraper.scrape_all_match_data,
        description="Use this to get info about all live matches. Input: 'Get all live matches.'"
    ),
    Tool(
        name="Get_Specific_Match_Details",
        func=lambda x: get_specific_match_detail(x),
        description="Use this to get info about a specific match. Input should be the series name."
    )
]

formatter_tools = [
    Tool(
        name="LinkedIn_Style",
        func=lambda x: linkedin_formatter(x),
        description="Use this to format match data as a LinkedIn post."
    ),
    Tool(
        name="TwitterX_Style",
        func=lambda x: x_formatter(x),
        description="Use this to format match data as a Twitter/X thread."
    )
]

fetcher_agent = initialize_agent(
    fetcher_tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

formatter_agent = initialize_agent(
    formatter_tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Step 1: Get data
data = fetcher_agent.run(user_input)

# Step 2: Ask if formatting is needed
while True:
    format_decision = input("Do you want to format the data for social media? (yes/no): ").strip().lower()
    if format_decision == "yes":
        format_type = input("Choose format: 'twitter' or 'linkedin': ").strip().lower()
        if format_type == "linkedin":
            print("\nGenerating LinkedIn post...\n")
            linkedin_post = formatter_agent.run(data)
            print(linkedin_post)
        elif format_type == "twitter":
            print("\nGenerating Twitter thread...\n")
            twitter_post = formatter_agent.run(data)
            print(twitter_post)
        else:
            print("Invalid format option.")
    else:
        break
