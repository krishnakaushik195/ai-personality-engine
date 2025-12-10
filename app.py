import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from memory import MemoryModule
from persona import PersonalityEngine

# --- 1. SETUP & SECURITY ---
# Load environment variables from .env file (for local use)
load_dotenv()

st.set_page_config(page_title="🧠 Companion AI Engine", layout="wide")

# --- SECURE KEY RETRIEVAL LOGIC (FIXED) ---
# 1. Try getting key from .env (Local) FIRST to avoid crashing
api_key = os.getenv("GEMINI_API_KEY")

# 2. If not found in .env, try Streamlit Secrets (Cloud)
if not api_key:
    try:
        # We wrap this in a try-block because accessing st.secrets 
        # crashes the app if secrets.toml doesn't exist locally.
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

# 3. Fallback: If still no key, stop the app
if not api_key:
    st.error("🚨 No API Key found! Please check your .env file or Streamlit Secrets.")
    st.stop()

# Configure global settings with the secure key
genai.configure(api_key=api_key)

# --- 2. MAIN INTERFACE ---
st.title("🧠 AI Memory & Personality Engine")
st.markdown("Transforms raw chat logs into a structured personality matrix.")

# Input Section
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1️⃣ Input Data")
    default_logs = """[10:03 AM] Sarah (Lead): Ops channel is open. Who is on point for the payment gateway?
[10:04 AM] Alex (Dev): I'm here. Why? Dashboards look green.
[10:05 AM] Sarah (Lead): Users are reporting 504 Gateway Timeouts on checkout.
[10:06 AM] Marcus (Junior): Uh, I just merged PR #402 ten minutes ago. Could that be it?
[10:06 AM] Alex (Dev): #402 was just a UI color tweak, Marcus. It shouldn't touch the backend.
[10:07 AM] Sarah (Lead): Error rate just spiked to 15%. We are losing money.
[10:08 AM] David (DBA): Database CPU is hitting 99%. Something is hammering the 'Orders' table.
[10:09 AM] Alex (Dev): I'm looking at the logs. It's not the UI. It's an N+1 query issue.
[10:09 AM] Marcus (Junior): I... might have added a "related products" loop to the checkout page in that PR.
[10:10 AM] Alex (Dev): Marcus! You said it was CSS only!
[10:11 AM] Sarah (Lead): Stop the blame. Fix the bleeding. David, can we kill the slow queries?
[10:12 AM] David (DBA): I can, but they'll just respawn. We need to rollback the deploy.
[10:13 AM] Alex (Dev): Rollback initiated. CI/CD is slow today though.
[10:14 AM] Marcus (Junior): I feel sick. I'm so sorry guys.
[10:15 AM] Sarah (Lead): Deep breaths, Marcus. We review process later. Focus on status now.
[10:16 AM] David (DBA): DB load is still 90%. Is the rollback live?
[10:17 AM] Alex (Dev): GitHub Actions is queuing. Estimated 5 mins. This is a nightmare.
[10:18 AM] Sarah (Lead): I'm notifying the VP. David, throttle traffic to 50% to save the DB.
[10:19 AM] David (DBA): Throttling applied. User experience will degrade but we won't crash hard.
[10:20 AM] Alex (Dev): Rollback deployed to Staging. Verifying... looks clean.
[10:21 AM] Alex (Dev): Pushing to Prod now.
[10:22 AM] Marcus (Junior): Should I draft the incident report?
[10:23 AM] Sarah (Lead): Yes. Be honest about the PR scope creep.
[10:24 AM] David (DBA): CPU dropping. 80%... 60%... we are stabilizing.
[10:25 AM] Alex (Dev): Rollback complete. 504s are gone.
[10:26 AM] Sarah (Lead): Okay, lift the throttle, David.
[10:27 AM] Sarah (Lead): Everyone take 5. We do a post-mortem at 11:00.
[10:28 AM] Alex (Dev): I need a whiskey. It's 10 AM but I don't care.
[10:29 AM] Marcus (Junior): I'm going to go hide in the server room.
[10:30 AM] Sarah (Lead): Good save team. But we are never deploying on Fridays again.."""
    
    raw_logs = st.text_area("Paste Chat Logs (Raw Text)", value=default_logs, height=300)
    
    # We define the extraction button
    if st.button("Extract Memory", type="primary"):
        with st.spinner("Mining conversation for patterns..."):
            # Uses the secure 'api_key' variable defined at the top
            extractor = MemoryModule(api_key)
            st.session_state['memory'] = extractor.extract_memory(raw_logs)
            st.success("Extraction Complete!")

with col2:
    st.subheader("2️⃣ The Brain (Memory State)")
    
    # --- DYNAMIC PERSONA LOADER ---
    # This retrieves the list directly from the class keys in persona.py
    available_personas = list(PersonalityEngine.PERSONAS.keys())
    
    selected_persona = st.selectbox(
        "Select Active Persona", 
        available_personas
    )
    st.divider()

    if 'memory' in st.session_state:
        # Displaying the structured data beautifully
        mem = st.session_state['memory']
        with st.expander("📂 User Facts", expanded=True):
            for fact in mem.facts: st.info(f"📌 {fact}")
        with st.expander("❤️ Preferences", expanded=True):
            for pref in mem.preferences: st.success(f"👍 {pref}")
        with st.expander("🧠 Emotional Patterns", expanded=True):
            for pattern in mem.emotional_patterns: st.warning(f"⚠️ {pattern}")
    else:
        st.info("Waiting for extraction...")

# --- 3. THE TURING TEST (BEFORE VS AFTER) ---
st.divider()
st.subheader("3️⃣ The Turing Test: Before vs After")

test_input = st.text_input("User's New Message", "Steve is back in the office and asking for the logs.")

if st.button("Generate Responses") and 'memory' in st.session_state:
    
    # Init Gemini Client for the Chat generation
    # Using 'gemini-1.5-flash' for stability
    chat_model = genai.GenerativeModel("gemini-2.5-flash")
    
    engine = PersonalityEngine(st.session_state['memory'])
    system_prompt = engine.construct_system_prompt(selected_persona)

    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("### 🤖 Generic AI (Before)")
        with st.spinner("Generating..."):
            # Standard prompt without memory
            resp = chat_model.generate_content(f"User said: {test_input}. Respond helpfully.")
            st.write(resp.text)
            
    with col_b:
        st.markdown(f"### ✨ {selected_persona} (After)")
        with st.spinner("Thinking with Personality..."):
            # The "Top 1%" Prompt
            full_prompt = f"{system_prompt}\n\nUSER INPUT: {test_input}"
            resp = chat_model.generate_content(full_prompt)
            st.write(resp.text)