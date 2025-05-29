import streamlit as st
import requests
import json
import time
from datetime import datetime

# Page config with custom styling
st.set_page_config(
    page_title="AI Blog Generator ", 
    page_icon="✨", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.7rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .blog-output {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin-top: 1rem;
    }
    
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .success-message {
        background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .warning-message {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>✨ AI Blog Generator </h1>
    <p>Create stunning, professional blog posts with AI-powered content generation</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with enhanced styling
with st.sidebar:
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.header("🔧 Configuration")
    
    # API Configuration
    st.subheader("🔑 API Settings")
    api_provider = st.selectbox(
        "Choose AI Provider",
        ["OpenAI", "Groq", "Anthropic", "Local API"],
        help="Select your preferred AI service provider"
    )
    
    api_key = st.text_input(f"{api_provider} API Key", type="password")
    
    if api_provider == "OpenAI":
        api_url = "https://api.openai.com/v1/chat/completions"
        model_options = ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"]
    elif api_provider == "Groq":
        api_url = "https://api.groq.com/openai/v1/chat/completions"
        model_options = ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma-7b-it"]
    elif api_provider == "Anthropic":
        api_url = "https://api.anthropic.com/v1/messages"
        model_options = ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"]
    else:
        api_url = st.text_input("Custom API URL", "http://localhost:11434/v1/chat/completions")
        model_options = ["llama2", "mistral", "codellama"]
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Model Selection
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.subheader("🤖 Model Settings")
    model_name = st.selectbox("Select Model", model_options, index=0)
    temperature = st.slider("🎯 Creativity Level", 0.0, 1.0, 0.7, 0.1, 
                           help="Lower values = more focused, Higher values = more creative")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Blog Configuration
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.subheader("📝 Blog Settings")
    blog_tone = st.selectbox(
        "Writing Tone",
        ["Professional", "Casual", "Technical", "Enthusiastic", "Educational", "Conversational", "Formal"],
        help="Choose the tone that matches your brand voice"
    )
    
    word_count = st.slider("📏 Word Count", 300, 3000, 800, 100)
    
    include_sections = st.multiselect(
        "📋 Blog Sections",
        ["Executive Summary", "Introduction", "Main Content", "Key Takeaways", "Conclusion", "FAQ", "Call to Action", "References"],
        ["Introduction", "Main Content", "Conclusion"],
        help="Select which sections to include in your blog"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Main content area with two columns
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("📋 Blog Content Details")
    
    blog_title = st.text_input("📌 Blog Title", 
                              placeholder="Leave empty to auto-generate a compelling title",
                              help="Provide a specific title or let AI create one for you")
    
    blog_topic = st.text_area("🎯 Blog Topic/Description", 
                             height=120,
                             placeholder="Describe what you want to write about...",
                             help="Be as detailed as possible for better results")
    
    target_audience = st.text_input("👥 Target Audience", 
                                   value="General readers",
                                   help="Who is your primary audience?")
    
    keywords = st.text_input("🔍 SEO Keywords", 
                            placeholder="keyword1, keyword2, keyword3",
                            help="Comma-separated keywords for SEO optimization")
    
    # Advanced options in an expander
    with st.expander("🔧 Advanced Options"):
        writing_style = st.selectbox(
            "Writing Style",
            ["Blog Post", "Article", "Tutorial", "Review", "News Report", "Opinion Piece"]
        )
        
        include_images = st.checkbox("📸 Include Image Suggestions", value=True)
        include_meta = st.checkbox("📊 Include Meta Description", value=True)
        include_tags = st.checkbox("🏷️ Generate Tags", value=True)
    
    # Generate button with enhanced styling
    st.markdown("<br>", unsafe_allow_html=True)
    generate_button = st.button("🚀 Generate Amazing Blog", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Enhanced blog generation function
def generate_blog_content(topic, tone, word_count, sections, audience, keywords, model, temp, title, style, provider, api_key, api_url):
    if not api_key:
        st.error("🔑 Please enter your API key in the sidebar")
        return None
    
    sections_str = ", ".join(sections)
    keywords_str = keywords if keywords else "none specified"
    title_instruction = f"Use this title: '{title}'" if title else "Generate an engaging, SEO-friendly title"
    
    # Enhanced prompt template
    prompt = f"""
    Create a comprehensive {style.lower()} about: {topic}

    REQUIREMENTS:
    - {title_instruction}
    - Writing tone: {tone.lower()}
    - Target audience: {audience}
    - Approximate word count: {word_count} words
    - Include sections: {sections_str}
    - SEO keywords to incorporate naturally: {keywords_str}
    
    FORMAT REQUIREMENTS:
    - Use proper markdown formatting with headers (##, ###)
    - Include engaging subheadings
    - Add bullet points and numbered lists where appropriate
    - Use bold and italic text for emphasis
    - Create scannable content with short paragraphs
    
    CONTENT QUALITY:
    - Write compelling, original content
    - Include actionable insights
    - Add relevant examples where possible
    - Ensure the content provides real value to readers
    - Make it engaging and easy to read
    
    Please format the entire response in clean markdown.
    """
    
    # Prepare API request based on provider
    headers = {"Content-Type": "application/json"}
    
    if provider == "OpenAI" or provider == "Groq":
        headers["Authorization"] = f"Bearer {api_key}"
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temp,
            "max_tokens": word_count * 2
        }
    elif provider == "Anthropic":
        headers["x-api-key"] = api_key
        headers["anthropic-version"] = "2023-06-01"
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temp,
            "max_tokens": word_count * 2
        }
    else:  # Local API
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temp
        }
    
    try:
        response = requests.post(api_url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        
        if provider == "Anthropic":
            content = result.get("content", [{}])[0].get("text", "")
        else:
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        return content
    
    except requests.exceptions.RequestException as e:
        st.error(f"🚨 API Error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"🚨 Error generating blog: {str(e)}")
        return None

# Blog generation and display
if generate_button and blog_topic:
    with col2:
        with st.spinner("🎨 Crafting your amazing blog post..."):
            # Progress bar for better UX
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            blog_content = generate_blog_content(
                blog_topic, blog_tone, word_count, include_sections,
                target_audience, keywords, model_name, temperature,
                blog_title, writing_style, api_provider, api_key, api_url
            )
            
            progress_bar.empty()
            
            if blog_content:
                st.markdown("""
                <div class="success-message">
                    ✅ Your blog post has been generated successfully!
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown('<div class="blog-output">', unsafe_allow_html=True)
                st.markdown("### 📝 Generated Blog Post")
                st.markdown(blog_content)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Enhanced download options
                col_download1, col_download2, col_download3 = st.columns(3)
                
                with col_download1:
                    st.download_button(
                        label="📥 Download Markdown",
                        data=blog_content,
                        file_name=f"blog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                
                with col_download2:
                    # Convert to HTML for download
                    html_content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <title>Generated Blog Post</title>
                        <style>
                            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
                            h1, h2, h3 {{ color: #333; }}
                            p {{ line-height: 1.6; }}
                        </style>
                    </head>
                    <body>
                        {blog_content.replace('**', '<strong>').replace('**', '</strong>')}
                    </body>
                    </html>
                    """
                    st.download_button(
                        label="🌐 Download HTML",
                        data=html_content,
                        file_name=f"blog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                        mime="text/html",
                        use_container_width=True
                    )
                
                with col_download3:
                    # Copy to clipboard functionality
                    st.code(blog_content, language="markdown")
                
                # Blog analytics
                word_count_actual = len(blog_content.split())
                char_count = len(blog_content)
                
                st.markdown("### 📊 Blog Statistics")
                col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
                
                with col_stats1:
                    st.metric("Word Count", word_count_actual)
                with col_stats2:
                    st.metric("Characters", char_count)
                with col_stats3:
                    st.metric("Estimated Reading Time", f"{word_count_actual // 200} min")
                with col_stats4:
                    st.metric("Sections", len(include_sections))

elif generate_button:
    with col2:
        st.markdown("""
        <div class="warning-message">
            ⚠️ Please enter a blog topic to generate content
        </div>
        """, unsafe_allow_html=True)

# Enhanced footer
st.markdown("---")
st.markdown("""
<div class="feature-card">
    <h3>🚀 About AI Blog Generator </h3>
    <p>This enhanced blog generator supports multiple AI providers and creates professional, SEO-optimized content. 
    Choose from OpenAI, Groq, Anthropic, or your local AI models for maximum flexibility.</p>
  
</div>
""", unsafe_allow_html=True)
