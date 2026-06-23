import re

import streamlit as st

from final_pipeline import run_research_pipeline
from comparision import compareReport

from utils.pdfGenerator import generate_pdf

from database.db import create_table

from llms.llm_factory import get_llm , set_llm


from database.operations import *

create_table()  # this will create schema just after streamlit starts


st.set_page_config(
    page_title="MultiAgent Researcher",
    page_icon="\U0001F9E0",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
        :root {
            --bg-1: #07111f;
            --bg-2: #101f35;
            --panel: rgba(8, 18, 33, 0.78);
            --panel-border: rgba(255, 255, 255, 0.08);
            --text-main: #f4f7fb;
            --text-muted: #a8b4c7;
            --accent: #7ce7c5;
            --accent-2: #78a8ff;
            --danger: #ff7d7d;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(124, 231, 197, 0.15), transparent 30%),
                radial-gradient(circle at top right, rgba(120, 168, 255, 0.18), transparent 28%),
                linear-gradient(160deg, var(--bg-1) 0%, var(--bg-2) 100%);
            color: var(--text-main);
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(4, 10, 20, 0.95), rgba(8, 18, 33, 0.92));
            border-right: 1px solid var(--panel-border);
        }

        .hero {
            padding: 1.4rem 1.5rem;
            border: 1px solid var(--panel-border);
            border-radius: 24px;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.06), rgba(255, 255, 255, 0.02));
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.28);
        }

        .eyebrow {
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: var(--accent);
            font-size: 0.78rem;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }

        .title {
            font-size: clamp(2rem, 4vw, 4rem);
            line-height: 1.05;
            margin: 0;
            color: var(--text-main);
        }

        .subtitle {
            color: var(--text-muted);
            font-size: 1rem;
            max-width: 760px;
            margin-top: 0.9rem;
        }

        .metric-card {
            padding: 1rem 1.1rem;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--panel-border);
        }

        .metric-label {
            color: var(--text-muted);
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .metric-value {
            color: var(--text-main);
            font-size: 1.35rem;
            font-weight: 700;
            margin-top: 0.25rem;
        }

        .panel {
            padding: 1rem 1.1rem;
            border-radius: 20px;
            background: var(--panel);
            border: 1px solid var(--panel-border);
            box-shadow: 0 18px 40px rgba(0, 0, 0, 0.25);
        }

        .section-label {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            color: var(--accent);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.8rem;
            margin-bottom: 0.7rem;
        }

        .source-pill {
            display: inline-block;
            padding: 0.35rem 0.65rem;
            margin: 0.2rem 0.35rem 0.2rem 0;
            border-radius: 999px;
            border: 1px solid rgba(124, 231, 197, 0.35);
            background: rgba(124, 231, 197, 0.09);
            color: var(--text-main);
            font-size: 0.82rem;
        }

        .stTextInput input, .stTextArea textarea {
            background: rgba(255, 255, 255, 0.06) !important;
            color: var(--text-main) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 14px !important;
        }

        .stButton button {
            background: linear-gradient(135deg, #7ce7c5, #78a8ff) !important;
            color: #05111d !important;
            border: none !important;
            border-radius: 14px !important;
            font-weight: 800 !important;
            padding: 0.7rem 1rem !important;
        }

        .stButton button:hover {
            transform: translateY(-1px);
            box-shadow: 0 14px 30px rgba(120, 168, 255, 0.2);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def extract_sources(text: str) -> list[str]:
    urls = re.findall(r'https?://[^\s)>"]+', text)
    cleaned = []
    for url in urls:
        url = url.rstrip(".,;]")
        if url not in cleaned:
            cleaned.append(url)
    return cleaned


def render_metric(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Multi-agent research studio</div>
        <h1 class="title">Generate a report, then critique it with a second pass.</h1>
        <p class="subtitle">
            Enter a topic, let the search and reader agents collect evidence, then publish a polished report
            with a separate critic review. The interface is designed to feel more like a command center than a form.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Compare two research topics</div>', unsafe_allow_html=True)
comparison_col_a, comparison_col_b = st.columns(2)
with comparison_col_a:
    topic_a = st.text_input("Topic A", value="Quantum computing in healthcare", key="compare_topic_a")
with comparison_col_b:
    topic_b = st.text_input("Topic B", value="AI agents in scientific research", key="compare_topic_b")

if "comparison_result" not in st.session_state:
    st.session_state.comparison_result = None

compare_button = st.button("Generate comparison report", use_container_width=True)

if compare_button:
    topic_a = topic_a.strip()
    topic_b = topic_b.strip()
    if not topic_a or not topic_b:
        st.error("Please provide both topics to compare.")
    else:
        with st.spinner("Comparing both research reports..."):
            try:
                st.session_state.comparison_result = compareReport(topic_a, topic_b)
            except Exception as exc:
                st.session_state.comparison_result = None
                st.error(f"Comparison failed: {exc}")

if st.session_state.comparison_result:
    st.markdown("### Comparison Output")
    st.write(st.session_state.comparison_result)

st.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown("### Research Controls")
st.sidebar.caption("Tune the input before launching the pipeline.")

default_topic = st.sidebar.text_input("Topic", value="AI agents in scientific research")
llm_model = st.sidebar.selectbox(
    "Model selection",
    ["Mistral", "gemini", "openai"],
    index=0,
)
st.sidebar.info("Please don't select other llm except mistral because I have don't have money to buy api keys of openai and gemini...")
st.session_state.selected_model = llm_model
set_llm(st.session_state.selected_model)
report_focus = st.sidebar.selectbox(
    "Output style",
    ["Balanced", "Executive summary", "Technical deep dive"],
    index=0,
)
show_debug = st.sidebar.toggle("Show raw pipeline output", value=False)

st.sidebar.markdown("---")
st.sidebar.info(
    "This app uses the existing search, reader, writer, and critic steps defined in your pipeline."
)

# frontend logic for showing up all the history research paper

history = get_all_research()

st.sidebar.title("Research History : ")

for item in history: 
    research_id = item[0]
    topic = item[1]
    date = item[2]
    if st.sidebar.button(
        f"{topic}",
        key=research_id
    ):
        st.session_state.selected_report = research_id

if history:
  if st.sidebar.button("🗑 Delete Reports"):
     delete_all_reports()
     st.rerun()    
else:
    st.sidebar.write("No past reports are there....")



if "selected_report" in st.session_state:
    data = get_research_by_id(
        st.session_state.selected_report
    )
    st.header(data[1])
    st.subheader("Research Report")
    st.write(data[2])
    st.subheader("Critic Feedback")
    st.write(data[3])


    pdf_path = data[5]

    with open(pdf_path,"rb") as pdf:

      st.download_button(

         "📄 Download PDF",

         data=pdf,

         file_name=f"{data[1]}.pdf",

         mime="application/pdf"
     )



top_left, top_middle, top_right = st.columns(3)
with top_left:
    render_metric("Pipeline", "Search → Read → Write → Critique")
with top_middle:
    render_metric("Theme", report_focus)
with top_right:
    render_metric("Mode", "Interactive Streamlit")


run_button = st.button("Run research pipeline", use_container_width=True)

if "last_state" not in st.session_state:
    st.session_state.last_state = None

if run_button:
    topic = default_topic.strip()
    if not topic:
        st.error("Please enter a topic before running the pipeline.")
    else:
        with st.spinner("Running the multi-agent workflow..."):
            try:
                
                st.session_state.last_state = run_research_pipeline(topic)

            except Exception as exc:
                st.session_state.last_state = None
                st.error(f"Pipeline failed: {exc}")


state = st.session_state.last_state



if state:
    st.markdown("### Research Output")

    report_col, feedback_col = st.columns([1.4, 1])

    with report_col:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Written report</div>', unsafe_allow_html=True)
        st.markdown(state.get("report", "No report generated yet."))
        st.markdown("</div>", unsafe_allow_html=True)

    with feedback_col:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Critic review</div>', unsafe_allow_html=True)
        st.write(state.get("feedback", "No feedback available."))
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### Evidence Trail")
    evidence_left, evidence_right = st.columns(2)

    with evidence_left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Search results</div>', unsafe_allow_html=True)
        st.write(state.get("search_results", "No search results captured."))
        st.markdown("</div>", unsafe_allow_html=True)

    with evidence_right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Scraped content</div>', unsafe_allow_html=True)
        st.write(state.get("scraped_content", "No scraped content captured."))
        st.markdown("</div>", unsafe_allow_html=True)

    sources = extract_sources(state.get("search_results", "") + "\n" + state.get("report", ""))
    if sources:
        st.markdown("### Sources")
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        for source in sources:
            st.markdown(f'<span class="source-pill">{source}</span>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if show_debug:
        st.markdown("### Raw State")
        st.json(state)

    pdf_path = generate_pdf(
        topic=state['topic'],
        report=state["report"],
        feedback=state["feedback"],
        sources=state["search_results"]
    )
    already_In_history = search_history(state["topic"])
    if not already_In_history:
       research_id = save_research(
         state["topic"],
         state["report"],
         state["feedback"],
         state["search_results"],
         pdf_path
       )
        


    with open(pdf_path, "rb") as pdf_file:

        st.download_button(
            label="📄 Download Research Report",
            data=pdf_file,
            file_name=f"{state['topic']}"+f"_Research_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    
    st.divider()

    st.subheader("💬 Chat with Research Report")

    question = st.text_input(
    "Ask anything about this report"
    )

    if st.button("Ask"):

       if "retriever" not in state:

        st.warning("Generate a report first.")

       else:

         from ragConcepts.rag_pipeline import QuestionAnswer

         answer = QuestionAnswer(
            question,
            state["retriever"]
         )

         st.success(answer)
else:
    st.markdown(
        """
        <div class="panel">
            <div class="section-label">Ready</div>
            <p style="color: var(--text-muted); margin-bottom: 0;">
                Choose a topic in the sidebar and launch the pipeline to populate the report, evidence trail,
                and critic feedback.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
