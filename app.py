import streamlit as st
import os
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

st.set_page_config(page_title="Blog Generator", layout="wide")

st.title("✨ Blog Generator")
st.subheader("Create professional blog posts with the power of Gemini AI")

# Sidebar for API key and settings
with st.sidebar:
    st.header("Settings")
    google_api_key = st.text_input("Google API Key", type="password")
    
    st.subheader("Blog Settings")
    blog_tone = st.selectbox(
        "Blog Tone",
        ["Professional", "Casual", "Technical", "Enthusiastic", "Educational"]
    )
    
    word_count = st.slider("Approximate Word Count", 300, 2000, 800, 100)
    
    include_sections = st.multiselect(
        "Include Sections",
        ["Introduction", "Main Content", "Conclusion", "FAQ", "Call to Action"],
        ["Introduction", "Main Content", "Conclusion"]
    )

# Main area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Blog Details")
    blog_title = st.text_input("Blog Title (Leave empty to generate one)", "")
    blog_topic = st.text_area("Blog Topic/Description", height=100)
    target_audience = st.text_input("Target Audience", "General readers")
    
    keywords = st.text_input("Keywords (comma separated)", "")
    
    generate_button = st.button("Generate Blog", type="primary")

# Function to generate blog content
def generate_blog(topic, tone, word_count, include_sections, target_audience, keywords, title=""):
    if not google_api_key:
        st.error("Please enter your Google API Key in the sidebar")
        return None
    
    os.environ["GOOGLE_API_KEY"] = google_api_key
    
    sections_str = ", ".join(include_sections)
    keywords_str = keywords if keywords else "none specified"
    title_instruction = f"Use this title: {title}" if title else "Generate an engaging title"
    
    prompt_template = f"""
    Write a {tone.lower()} blog post about: {topic}
    
    {title_instruction}
    
    Guidelines:
    - Target audience: {target_audience}
    - Approximate word count: {word_count}
    - Include these sections: {sections_str}
    - Incorporate these keywords where natural: {keywords_str}
    - Write in a {tone.lower()} tone
    - Format the blog using markdown with appropriate headers, subheaders, and formatting
    - Create content that is informative, engaging, and valuable to readers
    
    The blog post should be well-structured, with a compelling introduction, 
    substantive body content, and a strong conclusion if requested.
    """
    
    prompt = PromptTemplate(
        input_variables=["topic"],
        template=prompt_template
    )
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.7)
    chain = LLMChain(llm=llm, prompt=prompt)
    
    try:
        result = chain.run(topic=topic)
        return result
    except Exception as e:
        st.error(f"Error generating blog: {str(e)}")
        return None

# Generate and display blog
if generate_button and blog_topic:
    with st.spinner("Generating your blog post..."):
        blog_content = generate_blog(
            blog_topic,
            blog_tone,
            word_count,
            include_sections,
            target_audience,
            keywords,
            blog_title
        )
        
        if blog_content:
            with col2:
                st.subheader("Generated Blog")
                st.markdown(blog_content)
                
                st.download_button(
                    label="Download Blog",
                    data=blog_content,
                    file_name="generated_blog.md",
                    mime="text/markdown"
                )
elif generate_button:
    st.warning("Please enter a blog topic to generate content")