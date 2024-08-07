import streamlit as st
from agents import web_summarizer_company, web_summarizer_person, company_linkedin_agent, person_linkedin_agent, image_prompt_agent, tweet_agent 
from tools import scrape_website, post_on_linkedin, generate_image, post_on_twitter

def main():
    st.title('Social Media Content Generator')

    tab1, tab2 = st.tabs(["LinkedIn", "Twitter"])
    with tab1:
        with st.form(key='linkedin_form'):
            topic = st.text_input('Topic')
            url = st.text_input('Website URL')
            mood = st.text_input('Mood')
            post_company = st.checkbox('For Company')
            ai_image = st.checkbox('Add AI Generated Image')

            generate_button = st.form_submit_button(label='Generate Post')

            if generate_button:
                if url:
                    
                    try:
                        scraped_data = scrape_website(url)
                        if scrape_website == '':
                            scraped_data = 'scrape failed'
                    except Exception as e:
                        st.error('unable to scrape website')

                    if scraped_data == 'scrape failed':
                        summary = 'summary not available'
                    else:
                        if post_company:
                            summary = web_summarizer_company(scraped_data)
                        else:
                            print(1111)
                            summary = web_summarizer_person(scraped_data)
                            print(summary)
                    try:
                        summary = summary.content
                    except Exception as e:
                        print(e)
                    print('summary: ' +  summary)

                    if post_company:
                        post_content = company_linkedin_agent(topic, summary, mood)
                    else:
                        post_content = person_linkedin_agent(topic, summary, mood)
                    
                    print(post_content.content)
                    post_content = post_content.content
                    
                    if post_content.endswith(':'):
                        post_content = post_content[:-5]

                    image_path = None
                    if ai_image:
                        prompt = image_prompt_agent(post_content)
                        print(prompt.content)
                        image_path = generate_image(prompt.content)
                        print(image_path)

                    st.session_state.post_content = post_content
                    st.session_state.image_path = image_path
                    st.session_state.post_generated = True

                    st.markdown(f"**Generated Post Content:**\n\n{st.session_state.post_content}")
                    if ai_image:
                        st.image(image_path)

                    # Text area for reviewing generated content
                    # st.text_area('Post Content (for review)', st.session_state.post_content, height=200)

                else:
                    st.error('Something went wrong.')

        # Button to post on LinkedIn outside the form
        if st.session_state.get('post_generated'):
            post_linkedin = st.checkbox('Post on LinkedIn')
            
            if post_linkedin:
                token = st.text_input('LinkedIn Token', type='password')
                post_button = st.button('Post')
                if post_button:
                    image_path = st.session_state.image_path
                    post_on_linkedin(token, 'linkedin post', st.session_state.post_content, image_path)
                    st.success('Post has been successfully published on LinkedIn!')
                    st.session_state.post_generated = False  # Reset state after posting

    with tab2:
        with st.form(key='twitter_form'):
            topic = st.text_input('Topic')
            # url = st.text_input('Website URL')
            instructions = st.text_area('Instructions')
            mood = st.text_input('Mood')
            # post_company = st.checkbox('For Company')
            # ai_image = st.checkbox('Add AI Generated Image')

            generate_button = st.form_submit_button(label='Generate Post')

            if generate_button:
                tweet_content = tweet_agent(topic, instructions, mood)

                st.session_state.tweet_content = tweet_content.content.strip('"')
                st.session_state.tweet_generated = True

                st.markdown(f"**Generated tweet:**\n\n{st.session_state.tweet_content}")

        if st.session_state.get('tweet_generated'):
            post_twitter = st.checkbox('Post on Twitter')
            
            if post_twitter:
                consumer_key        = st.text_input(label='', placeholder='consumer key')
                consumer_secret     = st.text_input(label='', placeholder='consumer secret')
                access_token        = st.text_input(label='', placeholder='access token')
                access_token_secret = st.text_input(label='', placeholder='access token secret')

                post_button = st.button('Post')
                if post_button:
                    # post_on_twitter(token, 'linkedin post', st.session_state.post_content, image_path)
                    if consumer_key and consumer_secret and access_token and access_token_secret:
                        post_on_twitter(st.session_state.tweet_content, consumer_key, consumer_secret, access_token, access_token_secret)
                    else:
                        st.error('Enter credentials!')
                    st.success('Post has been successfully published on Twitter!')
                    st.session_state.post_generated = False  # Reset state after posting


if __name__ == "__main__":
    main()
