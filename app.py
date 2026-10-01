import os
import streamlit as st
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool


# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="AI Research Studio",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# API SECRETS
# =========================================================
def get_secret(name: str) -> str:
    """Read a secret from Streamlit Secrets or environment variables."""
    try:
        value = st.secrets.get(name, "")
    except Exception:
        value = ""

    return value or os.getenv(name, "")


# =========================================================
# PROFESSIONAL UI / CSS
# =========================================================
st.markdown(
    """
    <style>

    /* Main application background */
    .stApp,
    [data-testid="stAppViewContainer"] {
        background-color: #0B1020 !important;
        color: #E5E7EB !important;
    }

    [data-testid="stHeader"] {
        background-color: #0B1020 !important;
    }

    /* Main content typography */
    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stAppViewContainer"] h4,
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] li,
    [data-testid="stAppViewContainer"] label,
    [data-testid="stAppViewContainer"] [data-testid="stCaptionContainer"],
    [data-testid="stAppViewContainer"] [data-testid="stWidgetLabel"],
    [data-testid="stAppViewContainer"] .stMarkdown {
        color: #E5E7EB !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111A2E !important;
        border-right: 1px solid #25324B;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #E5E7EB !important;
    }

    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #A9B7D0 !important;
    }

    /* Hero banner */
    .hero {
        padding: 34px 36px;
        border-radius: 22px;
        background: linear-gradient(
            120deg,
            #172554 0%,
            #312E81 52%,
            #5B21B6 100%
        );
        border: 1px solid #45418D;
        margin-bottom: 26px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.18);
    }

    .hero h1 {
        color: #FFFFFF !important;
        font-size: 2.35rem;
        font-weight: 800;
        margin: 0 0 12px 0;
    }

    .hero p {
        color: #E0E7FF !important;
        font-size: 1.05rem;
        line-height: 1.7;
        margin: 0;
    }

    .hero-badge {
        display: inline-block;
        color: #E0E7FF !important;
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.20);
        border-radius: 30px;
        padding: 5px 12px;
        font-size: 0.8rem;
        margin-bottom: 14px;
    }

    /* Feature cards */
    .metric-card {
        padding: 22px;
        border-radius: 16px;
        background: #111A2E;
        border: 1px solid #293752;
        min-height: 142px;
        height: 100%;
        box-sizing: border-box;
    }

    .metric-card h3 {
        color: #C4B5FD !important;
        font-size: 1.05rem;
        margin: 0 0 12px 0;
    }

    .metric-card p {
        color: #D1D9E8 !important;
        font-size: 0.94rem;
        line-height: 1.65;
        margin: 0;
    }

    /* Text input */
    [data-testid="stTextInput"] input {
        background-color: #F9FAFB !important;
        color: #111827 !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
        min-height: 46px;
    }

    [data-testid="stTextInput"] input::placeholder {
        color: #6B7280 !important;
        opacity: 1;
    }

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button {
        background: linear-gradient(
            90deg,
            #6366F1,
            #7C3AED
        ) !important;

        color: #FFFFFF !important;
        border: 1px solid #7774F5 !important;
        border-radius: 10px !important;
        min-height: 45px;
        font-weight: 650 !important;
        transition: all 0.2s ease;
    }

    .stButton > button p,
    .stDownloadButton > button p {
        color: #FFFFFF !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        border-color: #C4B5FD !important;
        filter: brightness(1.12);
    }

    /* Expander */
    [data-testid="stExpander"] {
        background-color: #111A2E !important;
        border: 1px solid #293752 !important;
        border-radius: 12px !important;
    }

    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary p {
        color: #E5E7EB !important;
    }

    /* Tabs */
    [data-testid="stTabs"] button {
        color: #CBD5E1 !important;
    }

    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #C4B5FD !important;
    }

    /* Code blocks */
    [data-testid="stCode"] {
        border: 1px solid #293752;
        border-radius: 10px;
    }

    /* Section labels */
    .section-label {
        color: #A5B4FC !important;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 1.4px;
        text-transform: uppercase;
    }

    /* Footer */
    .footer-text {
        color: #94A3B8 !important;
        font-size: 0.83rem;
        text-align: center;
        line-height: 1.7;
    }

    hr {
        border-color: #293752 !important;
    }

    /* Mobile */
    @media (max-width: 768px) {

        .hero {
            padding: 24px 20px;
        }

        .hero h1 {
            font-size: 1.75rem;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.markdown("## 🔎 Research Studio")
    st.caption("CREWAI MULTI-AGENT WORKSPACE")

    st.divider()

    st.markdown("### ⚡ How it works")

    st.markdown(
        """
        1. Enter your research topic.
        2. Research Agent gathers information.
        3. Content Writer prepares the blog.
        4. Review and download your results.
        """
    )

    st.divider()

    st.markdown("### 🤖 AI Agents")

    st.markdown(
        """
        - 🧠 Senior Research Analyst
        - ✍️ Content Writer
        """
    )

    st.divider()

    st.markdown("### 🔐 Security")

    st.caption(
        "API keys are loaded from Streamlit Secrets. "
        "Never publish credentials in your source code."
    )


# =========================================================
# HERO SECTION
# =========================================================
st.markdown(
    """
    <div class="hero">

        <div class="hero-badge">
            ✦ AI-POWERED RESEARCH PLATFORM
        </div>

        <h1>AI Research Studio</h1>

        <p>
            Research smarter. Transform reliable findings into
            structured research reports and professional,
            source-linked blog content using CrewAI.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# FEATURE CARDS
# =========================================================
col1, col2, col3 = st.columns(3, gap="medium")


with col1:

    st.markdown(
        """
        <div class="metric-card">

            <h3>🧠 Research Agent</h3>

            <p>
                Searches for relevant information, evaluates sources,
                and organizes key findings into a research brief.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


with col2:

    st.markdown(
        """
        <div class="metric-card">

            <h3>✍️ Content Writer</h3>

            <p>
                Converts research findings into a readable,
                structured blog with headings and references.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


with col3:

    st.markdown(
        """
        <div class="metric-card">

            <h3>🔗 Source-aware</h3>

            <p>
                Requests source titles and URLs so readers can
                review the original information.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# RESEARCH INPUT
# =========================================================
st.write("")

st.markdown(
    '<p class="section-label">WORKSPACE</p>',
    unsafe_allow_html=True
)

st.header("Create a research report")

st.write(
    "Enter a topic to start your multi-agent research workflow."
)


topic = st.text_input(
    "Research topic",
    placeholder="e.g., Applications of AI in healthcare",
    help="A specific topic generally produces a more focused result.",
)


# =========================================================
# ADVANCED SETTINGS
# =========================================================
with st.expander("⚙️ Advanced settings"):

    model_name = st.text_input(
        "xAI Grok model",
        value="grok-4.6",
        help="xAI Grok model used by the CrewAI workflow.",
    )


# =========================================================
# GENERATE BUTTON
# =========================================================
generate = st.button(
    "✨ Generate Research & Blog",
    type="primary",
    use_container_width=True,
)


# =========================================================
# RUN CREWAI WORKFLOW
# =========================================================
if generate:

    # -----------------------------------------------------
    # Validate topic
    # -----------------------------------------------------
    if not topic.strip():

        st.warning(
            "Please enter a research topic first."
        )

        st.stop()


    # -----------------------------------------------------
    # Load xAI + Serper keys
    # -----------------------------------------------------
    xai_key = get_secret("XAI_API_KEY")

    serper_key = get_secret("SERPER_API_KEY")


    # -----------------------------------------------------
    # Validate API keys
    # -----------------------------------------------------
    if not xai_key:

        st.error(
            "Missing XAI_API_KEY. "
            "Please add it in Streamlit Cloud → Settings → Secrets."
        )

        st.stop()


    if not serper_key:

        st.error(
            "Missing SERPER_API_KEY. "
            "Please add it in Streamlit Cloud → Settings → Secrets."
        )

        st.stop()


    # -----------------------------------------------------
    # Environment variables
    # -----------------------------------------------------
    os.environ["XAI_API_KEY"] = xai_key

    os.environ["SERPER_API_KEY"] = serper_key


    # -----------------------------------------------------
    # Validate model
    # -----------------------------------------------------
    if not model_name.strip():

        st.warning(
            "Please enter a valid xAI Grok model name."
        )

        st.stop()


    # =====================================================
    # START WORKFLOW
    # =====================================================
    try:

        with st.spinner(
            "🔍 Researching your topic and preparing the blog. "
            "This may take a few minutes..."
        ):

            # -------------------------------------------------
            # xAI Grok LLM
            # -------------------------------------------------
            llm = LLM(
                model=model_name.strip(),
                api_key=xai_key,
                base_url="https://api.x.ai/v1",
                temperature=0.3,
            )


            # -------------------------------------------------
            # Serper Search Tool
            # -------------------------------------------------
            search_tool = SerperDevTool(
                n=5
            )


            # =================================================
            # RESEARCH AGENT
            # =================================================
            researcher = Agent(

                role="Senior Research Analyst",

                goal=(
                    f"Research, analyze, and synthesize reliable "
                    f"information about {topic.strip()}."
                ),

                backstory=(
                    "You are an experienced research analyst. "
                    "Evaluate source credibility, cross-check facts, "
                    "distinguish evidence from interpretation, and "
                    "provide source URLs for important claims."
                ),

                tools=[
                    search_tool
                ],

                llm=llm,

                verbose=False,
            )


            # =================================================
            # CONTENT WRITER
            # =================================================
            writer = Agent(

                role="Professional Content Writer",

                goal=(
                    "Turn the research brief into an accurate, "
                    "engaging, well-structured professional blog post."
                ),

                backstory=(
                    "You write clear and professional content based "
                    "strictly on research findings. Preserve factual "
                    "nuance, avoid unsupported claims, and include "
                    "source links and references."
                ),

                llm=llm,

                verbose=False,
            )


            # =================================================
            # RESEARCH TASK
            # =================================================
            research_task = Task(

                description=(

                    f"Research the topic: {topic.strip()}.\n\n"

                    "Cover the following:\n"

                    "1. Introduction and background.\n"
                    "2. Key concepts.\n"
                    "3. Current developments.\n"
                    "4. Industry trends.\n"
                    "5. Important statistics where verifiable.\n"
                    "6. Benefits and applications.\n"
                    "7. Challenges and limitations.\n"
                    "8. Different viewpoints where relevant.\n"
                    "9. Supporting evidence.\n"
                    "10. Reliable source URLs.\n\n"

                    "Assess source credibility carefully.\n"

                    "Do not invent facts, statistics, "
                    "citations, or URLs.\n"

                    "Clearly identify uncertainty and limitations."
                ),

                expected_output=(

                    "A structured research brief containing:\n"

                    "- Executive summary\n"
                    "- Key findings\n"
                    "- Supporting evidence\n"
                    "- Important statistics\n"
                    "- Benefits\n"
                    "- Challenges\n"
                    "- Limitations\n"
                    "- Source titles\n"
                    "- Direct source URLs"
                ),

                agent=researcher,
            )


            # =================================================
            # WRITING TASK
            # =================================================
            writing_task = Task(

                description=(

                    "Use the completed research brief to write "
                    "a professional blog post.\n\n"

                    "Include:\n"

                    "1. Clear title\n"
                    "2. Introduction\n"
                    "3. Descriptive headings\n"
                    "4. Well-structured paragraphs\n"
                    "5. Important findings\n"
                    "6. Benefits and challenges\n"
                    "7. Conclusion\n"
                    "8. Inline source links\n"
                    "9. References section\n\n"

                    "Do not introduce unsupported claims.\n"

                    "Do not invent citations or URLs."
                ),

                expected_output=(

                    "A polished Markdown blog post containing "
                    "a title, introduction, headings, conclusion, "
                    "inline source links, and a References section."
                ),

                agent=writer,

                context=[
                    research_task
                ],
            )


            # =================================================
            # CREW
            # =================================================
            crew = Crew(

                agents=[
                    researcher,
                    writer
                ],

                tasks=[
                    research_task,
                    writing_task
                ],

                verbose=False,
            )


            # =================================================
            # EXECUTE
            # =================================================
            result = crew.kickoff()


        # =====================================================
        # SAVE OUTPUT
        # =====================================================
        output = (
            getattr(result, "raw", None)
            or str(result)
        )


        st.session_state["research_output"] = output

        st.session_state["research_topic"] = topic.strip()

        st.session_state["research_model"] = model_name.strip()


        st.success(
            "Research and blog generation completed successfully! 🎉"
        )


    # =====================================================
    # ERROR HANDLING
    # =====================================================
    except Exception as e:

        st.error(
            "The workflow could not be completed."
        )

        st.warning(
            "Please check your xAI API key, Serper API key, "
            "model name, API quota, package versions, "
            "and Streamlit Cloud logs."
        )

        with st.expander("Technical error details"):

            st.code(
                str(e)
            )


# =========================================================
# DISPLAY RESULTS
# =========================================================
if st.session_state.get("research_output"):

    output = st.session_state["research_output"]

    result_topic = st.session_state.get(
        "research_topic",
        "Research report"
    )


    st.divider()


    st.markdown(
        '<p class="section-label">COMPLETED OUTPUT</p>',
        unsafe_allow_html=True,
    )


    st.header(
        "Your research results"
    )


    st.caption(
        f"Topic: {result_topic}"
    )


    # =====================================================
    # TABS
    # =====================================================
    tab_report, tab_blog = st.tabs(
        [
            "📚 Research & Blog Output",
            "📝 Markdown Preview"
        ]
    )


    with tab_report:

        st.markdown(
            output
        )


    with tab_blog:

        st.markdown(
            "Review the generated Markdown content below."
        )

        st.code(
            output,
            language="markdown"
        )


    st.write("")


    # =====================================================
    # DOWNLOAD BUTTONS
    # =====================================================
    download_col1, download_col2 = st.columns(2)


    with download_col1:

        st.download_button(

            label="⬇️ Download Report (.md)",

            data=output,

            file_name="ai_research_report.md",

            mime="text/markdown",

            use_container_width=True,
        )


    with download_col2:

        st.download_button(

            label="⬇️ Download Report (.txt)",

            data=output,

            file_name="ai_research_report.txt",

            mime="text/plain",

            use_container_width=True,
        )


    st.caption(
        "Please verify important facts, source URLs, and citations "
        "before using or publishing AI-generated content."
    )


# =========================================================
# FOOTER
# =========================================================
st.divider()


st.markdown(
    """
    <div class="footer-text">

        <strong>AI Research Studio</strong><br>

        Powered by CrewAI · xAI Grok · Serper<br>

        Research responsibly. Verify sources before publication.

    </div>
    """,
    unsafe_allow_html=True,
)
