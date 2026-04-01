import streamlit as st
import time
from utils.document_parser import parse_document
from agents.research_agent import run_research_agent
from agents.copywriter_agent import run_copywriter_agent
from agents.editor_agent import run_editor_agent
from utils.exporter import export_campaign

st.set_page_config(
    page_title="Autonomous Content Factory",
    page_icon="🏭",
    layout="wide"
)

# --- Animated Agent Card CSS ---
st.markdown("""
<style>
@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.4; }
    100% { opacity: 1; }
}
@keyframes slideIn {
    from { transform: translateX(-10px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
.agent-card {
    border-radius: 16px;
    padding: 20px;
    margin: 8px 0;
    display: flex;
    align-items: center;
    gap: 16px;
    font-size: 15px;
    animation: slideIn 0.4s ease;
    border: 2px solid transparent;
}
.agent-idle {
    background: #f8f9fa;
    border-color: #dee2e6;
    color: #868e96;
}
.agent-thinking {
    background: #fff3cd;
    border-color: #ffc107;
    color: #856404;
    animation: pulse 1.2s infinite, slideIn 0.4s ease;
}
.agent-typing {
    background: #cff4fc;
    border-color: #0dcaf0;
    color: #055160;
    animation: pulse 1s infinite, slideIn 0.4s ease;
}
.agent-done {
    background: #d1e7dd;
    border-color: #198754;
    color: #0f5132;
    animation: slideIn 0.4s ease;
}
.agent-icon {
    font-size: 36px;
    min-width: 44px;
    text-align: center;
}
.agent-name {
    font-weight: 700;
    font-size: 16px;
}
.agent-status {
    font-size: 13px;
    margin-top: 2px;
}
.chat-log {
    background: #1e1e2e;
    color: #cdd6f4;
    border-radius: 12px;
    padding: 16px;
    font-family: monospace;
    font-size: 13px;
    max-height: 220px;
    overflow-y: auto;
    margin-top: 12px;
}
.chat-line {
    padding: 3px 0;
    border-bottom: 1px solid #313244;
    animation: slideIn 0.3s ease;
}
</style>
""", unsafe_allow_html=True)

# --- Session State Init ---
if "fact_sheet" not in st.session_state:
    st.session_state.fact_sheet = None
if "content" not in st.session_state:
    st.session_state.content = None
if "review" not in st.session_state:
    st.session_state.review = None
if "raw_text" not in st.session_state:
    st.session_state.raw_text = None
if "logs" not in st.session_state:
    st.session_state.logs = []
if "agent_states" not in st.session_state:
    st.session_state.agent_states = {
        "research": "idle",
        "copywriter": "idle",
        "editor": "idle"
    }

# --- Agent Card Renderer ---
def render_agent_room(states, logs):
    agents = [
        {
            "key": "research",
            "icon": "🧠",
            "name": "Research Agent",
            "idle": "Waiting for document...",
            "thinking": "Thinking... Reading source document",
            "typing": "Typing... Building Fact-Sheet",
            "done": "✅ Fact-Sheet created!"
        },
        {
            "key": "copywriter",
            "icon": "✍️",
            "name": "Copywriter Agent",
            "idle": "Waiting for Fact-Sheet...",
            "thinking": "Thinking... Planning content strategy",
            "typing": "Typing... Writing Blog, Social & Email",
            "done": "✅ All content generated!"
        },
        {
            "key": "editor",
            "icon": "🎩",
            "name": "Editor-in-Chief Agent",
            "idle": "Waiting for content...",
            "thinking": "Thinking... Reviewing all content",
            "typing": "Typing... Checking tone & facts",
            "done": "✅ Review complete!"
        }
    ]

    cols = st.columns(3)
    for i, agent in enumerate(agents):
        state = states.get(agent["key"], "idle")
        css_class = f"agent-{state}"
        status_text = agent[state]
        with cols[i]:
            st.markdown(f"""
            <div class="agent-card {css_class}">
                <div class="agent-icon">{agent['icon']}</div>
                <div>
                    <div class="agent-name">{agent['name']}</div>
                    <div class="agent-status">{status_text}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Chat log
    if logs:
        log_html = "".join([f'<div class="chat-line">> {log}</div>' for log in logs])
        st.markdown(f'<div class="chat-log">{log_html}</div>', unsafe_allow_html=True)


# --- Header ---
st.title("🏭 Autonomous Content Factory")
st.markdown("*Drop a source document. Get a full marketing campaign instantly.*")
st.divider()

# --- STEP 1: Upload ---
st.header("📂 Step 1: Upload Your Source Document")

input_type = st.radio("Choose input type:", ["Upload File (PDF/TXT)", "Paste URL", "Paste Text"])

raw_text = None

if input_type == "Upload File (PDF/TXT)":
    uploaded_file = st.file_uploader("Upload your document", type=["pdf", "txt"])
    if uploaded_file:
        with st.spinner("Parsing document..."):
            raw_text = parse_document(file=uploaded_file)
        st.success("✅ Document parsed successfully!")
        with st.expander("Preview extracted text"):
            st.write(raw_text[:1000] + "..." if len(raw_text) > 1000 else raw_text)

elif input_type == "Paste URL":
    url = st.text_input("Enter URL:")
    if url and st.button("Fetch URL"):
        with st.spinner("Fetching URL content..."):
            raw_text = parse_document(url=url)
        st.success("✅ URL content fetched!")
        with st.expander("Preview extracted text"):
            st.write(raw_text[:1000] + "..." if len(raw_text) > 1000 else raw_text)

elif input_type == "Paste Text":
    raw_text = st.text_area("Paste your source text here:", height=200)
    if raw_text:
        st.success("✅ Text ready!")

if raw_text:
    st.session_state.raw_text = raw_text

st.divider()

# --- STEP 2: Agent Room + Pipeline ---
st.header("🎙️ Agent Room")
st.caption("Watch your agents collaborate in real time")

agent_room_placeholder = st.empty()

# Show current agent states
with agent_room_placeholder.container():
    render_agent_room(st.session_state.agent_states, st.session_state.logs)

st.divider()

st.header("🤖 Step 2: Run the Agent Pipeline")

if st.session_state.raw_text:
    if st.button("🚀 Generate Campaign", type="primary", use_container_width=True):
        st.session_state.logs = []
        st.session_state.agent_states = {"research": "idle", "copywriter": "idle", "editor": "idle"}

        # --- Agent 1: Research ---
        st.session_state.agent_states["research"] = "thinking"
        st.session_state.logs.append("🧠 Research Agent: Reading source document...")
        with agent_room_placeholder.container():
            render_agent_room(st.session_state.agent_states, st.session_state.logs)
        time.sleep(0.8)

        st.session_state.agent_states["research"] = "typing"
        st.session_state.logs.append("🧠 Research Agent: Extracting features, audience & value proposition...")
        with agent_room_placeholder.container():
            render_agent_room(st.session_state.agent_states, st.session_state.logs)

        fact_sheet = run_research_agent(st.session_state.raw_text)
        st.session_state.fact_sheet = fact_sheet

        st.session_state.agent_states["research"] = "done"
        st.session_state.logs.append("✅ Research Agent: Fact-Sheet ready! Passing to Copywriter...")
        with agent_room_placeholder.container():
            render_agent_room(st.session_state.agent_states, st.session_state.logs)
        time.sleep(0.5)

        # --- Agent 2: Copywriter ---
        st.session_state.agent_states["copywriter"] = "thinking"
        st.session_state.logs.append("✍️ Copywriter Agent: Received Fact-Sheet. Planning content...")
        with agent_room_placeholder.container():
            render_agent_room(st.session_state.agent_states, st.session_state.logs)
        time.sleep(0.8)

        st.session_state.agent_states["copywriter"] = "typing"
        st.session_state.logs.append("✍️ Copywriter Agent: Writing 500-word Blog Post...")
        st.session_state.logs.append("✍️ Copywriter Agent: Writing 5-post Social Media Thread...")
        st.session_state.logs.append("✍️ Copywriter Agent: Writing Email Teaser...")
        with agent_room_placeholder.container():
            render_agent_room(st.session_state.agent_states, st.session_state.logs)

        content = run_copywriter_agent(fact_sheet)
        st.session_state.content = content

        st.session_state.agent_states["copywriter"] = "done"
        st.session_state.logs.append("✅ Copywriter Agent: All 3 pieces done! Passing to Editor...")
        with agent_room_placeholder.container():
            render_agent_room(st.session_state.agent_states, st.session_state.logs)
        time.sleep(0.5)

        # --- Agent 3: Editor ---
        st.session_state.agent_states["editor"] = "thinking"
        st.session_state.logs.append("🎩 Editor Agent: Received content. Checking for hallucinations...")
        with agent_room_placeholder.container():
            render_agent_room(st.session_state.agent_states, st.session_state.logs)
        time.sleep(0.8)

        st.session_state.agent_states["editor"] = "typing"
        st.session_state.logs.append("🎩 Editor Agent: Auditing tone across all 3 pieces...")
        st.session_state.logs.append("🎩 Editor Agent: Verifying facts against Fact-Sheet...")
        with agent_room_placeholder.container():
            render_agent_room(st.session_state.agent_states, st.session_state.logs)

        review = run_editor_agent(fact_sheet, content)
        st.session_state.review = review

        st.session_state.agent_states["editor"] = "done"
        st.session_state.logs.append("✅ Editor Agent: Review complete! Campaign is ready.")
        with agent_room_placeholder.container():
            render_agent_room(st.session_state.agent_states, st.session_state.logs)

        st.success("🎉 Campaign generated successfully!")
else:
    st.info("Please upload a document or paste text above to get started.")

st.divider()

# --- STEP 4: Final Review ---
if st.session_state.content and st.session_state.review:
    st.header("📋 Step 3: Review & Export Campaign")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📄 Original Source (Preview)")
        st.write(st.session_state.raw_text[:500] + "...")

    with col2:
        st.subheader("🗂️ Fact Sheet — Source of Truth")
        fs = st.session_state.fact_sheet
        import json as _json
        st.code(_json.dumps(fs, indent=2), language="json")
        st.download_button(
            label="⬇️ Download Fact Sheet (JSON)",
            data=_json.dumps(fs, indent=2),
            file_name="fact_sheet.json",
            mime="application/json"
        )
        if fs.get('ambiguous_statements'):
            st.warning(f"⚠️ Ambiguous: {', '.join(fs['ambiguous_statements'])}")

    st.divider()

    content = st.session_state.content
    review = st.session_state.review

    # Blog Post
    st.subheader("📝 Blog Post")
    blog_status = review.get("blog", {}).get("status", "Approved")
    blog_note = review.get("blog", {}).get("note", "")
    if blog_status == "Approved":
        st.success("✅ Approved by Editor")
    else:
        st.error(f"❌ Rejected: {blog_note}")
    st.text_area("Blog Post", value=content.get("blog", ""), height=200, key="blog_out")
    if st.button("🔄 Regenerate Blog"):
        with st.spinner("Regenerating..."):
            new_content = run_copywriter_agent(st.session_state.fact_sheet, regenerate="blog", note=blog_note)
            st.session_state.content["blog"] = new_content["blog"]
            st.rerun()

    st.divider()

    # Social Media
    st.subheader("📱 Social Media Thread")
    social_status = review.get("social", {}).get("status", "Approved")
    social_note = review.get("social", {}).get("note", "")
    if social_status == "Approved":
        st.success("✅ Approved by Editor")
    else:
        st.error(f"❌ Rejected: {social_note}")

    # Toggle mobile/desktop preview
    preview_mode = st.toggle("📱 Mobile Preview Mode")
    if preview_mode:
        for i, post in enumerate(content.get("social", "").split("\n\n")):
            if post.strip():
                st.markdown(f"""
                <div style='background:#f0f2f5; padding:12px; border-radius:12px;
                max-width:320px; margin:8px auto; font-size:14px;'>
                {post}
                </div>""", unsafe_allow_html=True)
    else:
        st.text_area("Social Thread", value=content.get("social", ""), height=150, key="social_out")

    if st.button("🔄 Regenerate Social"):
        with st.spinner("Regenerating..."):
            new_content = run_copywriter_agent(st.session_state.fact_sheet, regenerate="social", note=social_note)
            st.session_state.content["social"] = new_content["social"]
            st.rerun()

    st.divider()

    # Email
    st.subheader("📧 Email Teaser")
    email_status = review.get("email", {}).get("status", "Approved")
    email_note = review.get("email", {}).get("note", "")
    if email_status == "Approved":
        st.success("✅ Approved by Editor")
    else:
        st.error(f"❌ Rejected: {email_note}")
    st.text_area("Email Teaser", value=content.get("email", ""), height=100, key="email_out")
    if st.button("🔄 Regenerate Email"):
        with st.spinner("Regenerating..."):
            new_content = run_copywriter_agent(st.session_state.fact_sheet, regenerate="email", note=email_note)
            st.session_state.content["email"] = new_content["email"]
            st.rerun()

    st.divider()

    # Export
    st.header("📦 Export Campaign Kit")
    if st.button("⬇️ Download Campaign as ZIP", type="primary", use_container_width=True):
        zip_path = export_campaign(st.session_state.content, st.session_state.fact_sheet)
        with open(zip_path, "rb") as f:
            st.download_button(
                label="📥 Click to Download ZIP",
                data=f,
                file_name="campaign_kit.zip",
                mime="application/zip"
            )