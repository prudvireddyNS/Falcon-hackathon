from fns import extract_content

content = extract_content('https://docs.crewai.com/')


for item in content:
        print(f"URL: {item['url']}")
        print()
        print(f"Content: {item['content'][:500]}")  # Print first 500 characters of content
        print()
        print('-' * 80)
        print()