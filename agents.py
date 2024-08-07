from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

def web_summarizer_company(scraped_data):

    AI71_BASE_URL = "https://api.ai71.ai/v1/"
    AI71_API_KEY = 'ai71-api-f65e97e6-af86-4de9-a667-dc61c1ef8c75'

    llm = ChatOpenAI(
        model="tiiuae/falcon-180b-chat",
        api_key=AI71_API_KEY,
        base_url=AI71_BASE_URL,
        # streaming=True,
    )
    
    summary = llm.invoke(
    [
        SystemMessage(content="You are a Web Data Summarizer. you are skilled at summarizing company webpages into short summaries. "),
        HumanMessage(content=f"provide a neet summary of the company. Do not add up things. \n\n**Scraped Data:** \n\n{scraped_data}"),
    ]
    )

    # summary = llm.invoke("provide a neet summary of the company. "
    #                      f"**Scraped Data from company web page: **{scraped_data} "
    #                      "Do not add up things. ")

    return summary

def web_summarizer_person(scraped_data):

    AI71_BASE_URL = "https://api.ai71.ai/v1/"
    AI71_API_KEY = 'ai71-api-f65e97e6-af86-4de9-a667-dc61c1ef8c75'

    llm = ChatOpenAI(
        model="tiiuae/falcon-180b-chat",
        api_key=AI71_API_KEY,
        base_url=AI71_BASE_URL,
        # streaming=True,
    )
    
    # summary = llm.invoke(
    # [
    #     SystemMessage(content="You are a Web Data Summarizer. you are skilled at summarizing complex webpages into short summaries. "),
    #     HumanMessage(content=f"provide a neet summary of the youself. Do not add up things. \n\n**Scraped Data from your portfolio:** \n\n{scraped_data}"),
    # ]
    # )

    summary = llm.invoke("Given scraped data from your personal website, provide a neet summary of the yourself. "
               f"**Scraped Data: **{scraped_data} \n\n"
               "The output should not contain sentences like 'i am not capable...', 'As an AI language model...', etc. "
               "If unable to provide summary, then output 'summary not available.'")
    return summary

def person_linkedin_agent(topic, summary, mood):

    AI71_BASE_URL = "https://api.ai71.ai/v1/"
    AI71_API_KEY = 'ai71-api-f65e97e6-af86-4de9-a667-dc61c1ef8c75'

    llm = ChatOpenAI(
        model="tiiuae/falcon-180b-chat",
        api_key=AI71_API_KEY,
        base_url=AI71_BASE_URL,
        # streaming=True,
    )

    # blog = llm.invoke(
    # [
    #     SystemMessage(content=f"Your details are given below: \n\n{summary}"),
    #     HumanMessage(content=f"Write a LinkedIn post on the topic: {topic}. Mention your details in the post. Add symbols and emojis to make the post attractive. "),
    # ])

    blog = llm.invoke(f"You are not AI Language Model, you are: {summary}\n "
                      f"Write a {mood} LinkedIn post for youself on the topic: {topic} "
                      "Add symbols and emojis to make the post attractive.")
    return blog

def company_linkedin_agent(topic, summary, mood):

    AI71_BASE_URL = "https://api.ai71.ai/v1/"
    AI71_API_KEY = 'ai71-api-f65e97e6-af86-4de9-a667-dc61c1ef8c75'

    llm = ChatOpenAI(
        model="tiiuae/falcon-180b-chat",
        api_key=AI71_API_KEY,
        base_url=AI71_BASE_URL,
        # streaming=True,
    )

    # blog = llm.invoke(
    # [
    #     SystemMessage(content=f"You are a content Writer. You write content in {mood} way. You also add symbols, emojis to make the content attractive."),
    #     HumanMessage(content=f"Write a LinkedIn post on the topic: {topic}.\n\nThe post is for the company mentioned below.\n\n{summary}"),
    # ])
    blog = llm.invoke(f"You are not AI Language Model, you work for the company: {summary}\n "
                      f"Write a {mood} LinkedIn post on the topic: {topic}. for the company"
                      "Add symbols, emojis to make the post attractive.")

    return blog

def image_prompt_agent(post):

    llm = ChatGroq(model="llama3-70b-8192", api_key='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')
    # AI71_BASE_URL = "https://api.ai71.ai/v1/"
    # AI71_API_KEY = 'ai71-api-f65e97e6-af86-4de9-a667-dc61c1ef8c75'

    # llm = ChatOpenAI(
    #     model="tiiuae/falcon-180b-chat",
    #     api_key=AI71_API_KEY,
    #     base_url=AI71_BASE_URL,
    #     # streaming=True,
    # )

    blog = llm.invoke(f"""write image generation prompt for the below LinkedIn post. 
                      **LinkedIn post**: \n{post} \n
                      Prompt is 'What you wish to see in the output image'. 
                      A descriptive prompt that clearly defines elements, colors, and subjects will lead to better results. 
                      For example: 'The (sky:0.5) was a crisp (blue:0.3) and (green:0.8)' would convey a sky that was blue and green, but more green than blue. The weight applies to all words in the prompt. ,
                      Output only the prompt, no additional text.""")
    return blog

def tweet_agent(topic, instructions, mood):

    AI71_BASE_URL = "https://api.ai71.ai/v1/"
    AI71_API_KEY = 'ai71-api-f65e97e6-af86-4de9-a667-dc61c1ef8c75'

    llm = ChatOpenAI(
        model="tiiuae/falcon-180b-chat",
        api_key=AI71_API_KEY,
        base_url=AI71_BASE_URL,
        # streaming=True,
    )

    tweet = llm.invoke(f"""write a {mood} twitter tweet on the topic: {topic}. 
                        Follow below instructions: \n\n{instructions}""")
    return tweet