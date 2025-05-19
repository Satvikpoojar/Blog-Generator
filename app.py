import streamlit as st
import os
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

st.set_page_config(page_title="Blog Generator", layout="wide")
st.title("✨ Blog Generator")
st.subheader("Create professional blog posts")

# Sidebar for API key and settings
with st.sidebar:
    st.header("Settings")
    groq_api_key = st.text_input("Groq API Key", type="password")
    
    # st.subheader("Model Selection")
    # model_name = st.selectbox(
    #     "Select Model",
    #     ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma-7b-it"],
    #     index=0
    # )
    
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
    
    # Temperature setting
    temperature = st.slider("Temperature (Creativity)", 0.0, 1.0, 0.7, 0.1)
    
    generate_button = st.button("Generate Blog", type="primary")

# Function to generate blog content
def generate_blog(topic, tone, word_count, include_sections, target_audience, keywords, model, temp, title=""):
    if not groq_api_key:
        st.error("Please enter your Groq API Key in the sidebar")
        return None
    
    os.environ["GROQ_API_KEY"] = groq_api_key
    
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
    
    llm = ChatGroq(model=model, temperature=temp)
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
            # model_name,
            temperature,
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
                
                # Copy to clipboard button
                st.button("Copy to Clipboard", 
                          help="Copy blog content to clipboard",
                          on_click=lambda: st.write('<script>navigator.clipboard.writeText(`' + 
                                                  blog_content.replace('`', '\\`') + 
                                                  '`);</script>', unsafe_allow_html=True))
elif generate_button:
    st.warning("Please enter a blog topic to generate content")

# Add footer with information
st.markdown("---")
st.markdown("### About this Blog Generator")
st.markdown("""
This application uses Groq's API to generate blog content. Groq provides fast inference for various open-source models.
Key features:
- Choose from multiple AI models (Llama 3, Mixtral, Gemma)
- Adjust temperature to control creativity
- Customize blog sections
- Download or copy your generated content
""")