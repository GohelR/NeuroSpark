# app.py - minimal NeuroSpark Streamlit demo
import streamlit as st
import os
import json
from datetime import datetime

# ---------- simple ticket store (file-based for demo) ----------
TICKET_FILE = "data/tickets.json"

if "tickets" not in st.session_state:
    # load file if exists
    try:
        with open(TICKET_FILE, "r") as f:
            st.session_state.tickets = json.load(f)
    except FileNotFoundError:
        st.session_state.tickets = []

st.set_page_config(page_title="NeuroSpark Demo", layout="wide")
st.title("NeuroSpark — Campus AI Agent (Demo)")

col1, col2 = st.columns([2,1])

with col1:
    st.header("Student Chat & Ticketing")
    user_input = st.text_area("Describe your question or complaint", height=120)
    priority = st.selectbox("Priority", ["Low","Medium","High"])
    if st.button("Submit"):
        if not user_input.strip():
            st.warning("Please type your query or complaint")
        else:
            # Very simple heuristic classification: if contains keywords -> ticket
            ticket_keywords = ["wifi","hostel","fee","id card","mess","library"]
            is_ticket = any(k in user_input.lower() for k in ticket_keywords)
            if is_ticket:
                ticket = {
                    "id": len(st.session_state.tickets)+1,
                    "text": user_input,
                    "priority": priority,
                    "dept": "IT" if "wifi" in user_input.lower() else "General",
                    "status": "Open",
                    "created_at": datetime.utcnow().isoformat()
                }
                st.session_state.tickets.append(ticket)
                # persist
                os.makedirs("data", exist_ok=True)
                with open(TICKET_FILE, "w") as f:
                    json.dump(st.session_state.tickets, f, indent=2)
                st.success(f"Ticket created — ID #{ticket['id']} (dept: {ticket['dept']})")
            else:
                # fake FAQ answer using a placeholder
                st.info("FAQ Answer (demo): Please check the campus handbook or contact admin@edu.edu")

with col2:
    st.header("Staff Dashboard (Demo)")
    if st.button("Refresh"):
        pass
    tickets = st.session_state.tickets
    if not tickets:
        st.write("No tickets yet — submit a complaint from the left.")
    else:
        for t in tickets[::-1]:
            with st.expander(f"#{t['id']} — {t['priority']} — {t['status']}"):
                st.write(t['text'])
                st.write("Dept:", t['dept'])
                if st.button(f"Mark Resolved #{t['id']}", key=f"res_{t['id']}"):
                    t['status'] = "Resolved"
                    with open(TICKET_FILE, "w") as f:
                        json.dump(st.session_state.tickets, f, indent=2)
                    st.experimental_rerun()
