import os
import streamlit as st
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

st.set_page_config(
    page_title="AI Research Studio",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Read secrets from Streamlit Cloud Secrets or environment variables.
def get_secret(name: str) -> str:
    try:
        value = st.secrets.get(name, "")
    except Exception:
        value = ""
    return value or os.getenv(name, "")

st.markdown("""
<style>
    .stApp { background: #0b1020; color: #edf2ff; }
    [data-testid="stSidebar"] { background: #111a2e; }
    .hero {
        padding: 1.5rem 1.7rem; border-radius: 20px;
        background: linear-gradient(120deg, #172554 0%, #312e81 55%, #4c1d95 100%);
        border: 1px solid rgba(255,255,255,.12); margin-bottom: 1.4rem;
    }
    .hero h1 { color: white; margin-bottom: .35rem; font-size: 2.2rem; }
    .hero p { color: #dbeafe; margin-bottom: 0; }
    .metric-card {
        padding: 1rem; border-radius: 14px; background: #111a2e;
        border: 1px solid #263451; min-height: 100px;
    }
    .metric-card h3 { margin: 0 0 .35rem 0; color: #a5b4fc; font-size: 1rem; }
    .metric-card p { margin: 0; color: #e5e7eb; font-size: .9rem; }
    .stButton > button {
        border: 0; border-radius: 10px; min-height: 2.8rem;
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white; font-weight: 650;
    }
    .stButton > button:hover { border: 1px solid #c4b5fd; color: white; }
    [data-testid="stTextInput"] input { border-radius: 10px; }
    .small-muted { color: #9ca3af; font-size: .85rem; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🔎 Research Studio")
    st.caption("CrewAI multi-agent research workspace")
    st.divider()
    st.markdown("### How it works")
    st.markdown("1. Enter a research topic\n2. Research Agent gathers information\n3. Writer Agent creates a cited blog")
    st.divider()
    st.markdown("**Agents**")
    st.markdown("- 🧠 Senior Research Analyst\n- ✍️ Content Writer")
    st.caption("Keep API keys in app Secrets. Never publish them in code.")

st.markdown("""
<div class="hero">
  <h1>AI Research Studio</h1>
  <p>Research smarter. Turn reliable findings into clear, source-linked content with CrewAI.</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="metric-card"><h3>🧠 Research Agent</h3><p>Finds and organizes relevant information.</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="metric-card"><h3>✍️ Content Agent</h3><p>Transforms findings into a readable blog.</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="metric-card"><h3>🔗 Source-aware</h3><p>Designed to preserve source URLs and references.</p></div>', unsafe_allow_html=True)

st.write("")
st.subheader("Create a research report")
topic = st.text_input(
    "Research topic",
    placeholder="e.g., Applications of AI in healthcare",
    help="Use a specific topic to get more focused research.",
)
with st.expander("Advanced settings"):
    model_name = st.text_input(
        "Gemini model identifier",
        value="gemini/gemini-2.5-flash",
        help="Change this to a model identifier supported by your Gemini API account and CrewAI/LiteLLM.",
    )

generate = st.button("✨ Generate research & blog", type="primary", use_container_width=True)

if generate:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
        st.stop()

    gemini_key = get_secret("GEMINI_API_KEY")
    serper_key = get_secret("SERPER_API_KEY")
    if not gemini_key or not serper_key:
        st.error("API keys are missing. Add GEMINI_API_KEY and SERPER_API_KEY in Streamlit app Secrets.")
        st.info("In Streamlit Cloud: your app → Settings → Secrets. Do not paste API keys into this file.")
        st.stop()

    os.environ["GEMINI_API_KEY"] = gemini_key
    os.environ["SERPER_API_KEY"] = serper_key

    try:
        with st.spinner("The research agent and content writer are working. This can take a few minutes..."):
            llm = LLM(model=model_name.strip(), api_key=gemini_key, temperature=0.3)
            search_tool = SerperDevTool(n=5)

            researcher = Agent(
                role="Senior Research Analyst",
                goal=f"Research, analyze, and synthesize reliable information about {topic}",
                backstory=(
                    "You are an expert web research analyst. Evaluate source credibility, "
                    "cross-check facts, distinguish evidence from interpretation, and include "
                    "source URLs for important claims."
                ),
                tools=[search_tool],
                llm=llm,
                verbose=False,
            )

            writer = Agent(
                role="Content Writer",
                goal="Turn the research brief into an accurate, engaging, well-structured blog post",
                backstory=(
                    "You write accessible, professional content from technical research. "
                    "Preserve factual nuance and include citations and a references section."
                ),
                llm=llm,
                verbose=False,
            )

            research_task = Task(
                description=(
                    f"Research the topic: {topic}. Cover key concepts, recent developments, "
                    "industry trends, useful statistics where verifiable, and differing viewpoints. "
                    "Assess source credibility. Do not invent statistics or citations. Include "
                    "source titles and direct URLs, and clearly mark uncertainty."
                ),
                expected_output=(
                    "A structured research brief with an executive summary, key findings, "
                    "evidence, limitations, and a list of source URLs."
                ),
                agent=researcher,
            )

            writing_task = Task(
                description=(
                    "Using the research brief from the previous task, write a polished blog post. "
                    "Use a clear title, introduction, descriptive headings, conclusion, inline "
                    "source links, and a References section. Do not add unsupported claims."
                ),
                expected_output="A Markdown blog post with inline links and a References section.",
                agent=writer,
                context=[research_task],
            )

            crew = Crew(
                agents=[researcher, writer],
                tasks=[research_task, writing_task],
                verbose=False,
            )
            result = crew.kickoff()

        output = getattr(result, "raw", None) or str(result)
        st.session_state["research_output"] = output
        st.session_state["research_topic"] = topic.strip()
        st.success("Your report is ready.")
    except Exception as exc:
        st.error("The run did not complete. Check your API keys, model name, API quotas, and package compatibility.")
        with st.expander("Technical error details"):
            st.code(str(exc))

if st.session_state.get("research_output"):
    st.divider()
    st.subheader(f"Generated report: {st.session_state.get('research_topic', '')}")
    st.markdown(st.session_state["research_output"])
    st.download_button(
        "⬇️ Download report (.md)",
        data=st.session_state["research_output"],
        file_name="ai_research_report.md",
        mime="text/markdown",
        use_container_width=True,
    )
    st.caption("AI-generated content can contain errors. Verify important claims and citations before publishing.")
