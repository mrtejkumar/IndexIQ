import streamlit as st
import time
from typing import Optional, Callable
from core.openrouter_helper import ask_openrouter_stock_ai

class SearchBarState:
    """Manages session state for the search bar component"""
    
    STATE_KEYS = {
        "show_popup": False,
        "popup_response": "",
        "is_loading": False,
        "current_question": "",
        "search_history": []
    }
    
    @staticmethod
    def initialize():
        """Initialize all session state variables"""
        for key, default_value in SearchBarState.STATE_KEYS.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    @staticmethod
    def reset_popup():
        """Reset popup-related session state"""
        st.session_state.show_popup = False
        st.session_state.popup_response = ""
        st.session_state.is_loading = False
        st.session_state.current_question = ""
    
    @staticmethod
    def start_loading(question: str):
        """Set loading state and question"""
        st.session_state.show_popup = True
        st.session_state.is_loading = True
        st.session_state.current_question = question
        st.session_state.popup_response = ""
    
    @staticmethod
    def finish_loading(response: str):
        """Set response and stop loading"""
        st.session_state.popup_response = response
        st.session_state.is_loading = False
        # Add to history
        if st.session_state.current_question:
            SearchBarState.add_to_history(st.session_state.current_question, response)
        st.session_state.current_question = ""
    
    @staticmethod
    def add_to_history(question: str, response: str):
        """Add question and response to search history"""
        history_item = {
            "question": question,
            "response": response,
            "timestamp": time.time()
        }
        
        # Keep only last 10 items
        if len(st.session_state.search_history) >= 10:
            st.session_state.search_history.pop(0)
        
        st.session_state.search_history.append(history_item)

class ThinkingAnimation:
    """Handles the thinking animation display"""
    
    @staticmethod
    def show_animated_dots(duration: float = 1.2, container=None):
        """Show animated thinking dots"""
        placeholder = container.empty() if container else st.empty()
        cycles = int(duration / 0.3)
        
        for i in range(cycles):
            dots_count = (i % 3) + 1
            dots = "●" * dots_count + "○" * (3 - dots_count)
            placeholder.markdown(
                f"""
                <div style='text-align: center; font-size: 24px; color: #ffd700; 
                           animation: pulse 0.5s ease-in-out infinite alternate;'>
                    {dots}
                </div>
                <style>
                @keyframes pulse {{
                    0% {{ opacity: 0.8; }}
                    100% {{ opacity: 1; }}
                }}
                </style>
                """, 
                unsafe_allow_html=True
            )
            time.sleep(0.3)
        
        placeholder.empty()
    
    @staticmethod
    def show_progress_bar(message: str = "Loading...", duration: float = 2.0):
        """Show a progress bar animation"""
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(int(duration * 10)):
            progress = (i + 1) / (duration * 10)
            progress_bar.progress(progress)
            status_text.text(f"{message} {int(progress * 100)}%")
            time.sleep(0.1)
        
        progress_bar.empty()
        status_text.empty()

@st.dialog("📘 Stock Market Answer")
def show_response_dialog():
    """Display the AI response in a modal dialog"""
    
    if st.session_state.is_loading:
        st.markdown("### 🤖 AI is thinking...")
        
        # Show question being asked
        if st.session_state.current_question:
            st.markdown(f"**Question:** {st.session_state.current_question}")
            st.markdown("---")
        
        # Show thinking animation
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                ThinkingAnimation.show_animated_dots()
        
        # Get AI response
        try:
            response = ask_openrouter_stock_ai(st.session_state.current_question)
            SearchBarState.finish_loading(response)
            st.rerun()
        except Exception as e:
            error_message = f"❌ Failed to get response: {str(e)}"
            SearchBarState.finish_loading(error_message)
            st.rerun()
    
    else:
        # Display the response
        if st.session_state.popup_response:
            st.markdown("### Response:")
            st.markdown(st.session_state.popup_response)
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("📋 Copy", help="Copy response to clipboard"):
                st.write("Response copied to clipboard!")
        
        with col2:
            if st.button("🔄 Ask Again", help="Ask another question"):
                SearchBarState.reset_popup()
                st.rerun()
        
        with col3:
            if st.button("✕ Close", type="primary", help="Close dialog"):
                SearchBarState.reset_popup()
                st.rerun()

def render_sidebar_search(
    placeholder: str = "e.g., What is a bull market?",
    title: str = "🤖 Ask AI",
    show_history: bool = False
):
    """
    Render the search input in the sidebar
    
    Args:
        placeholder (str): Placeholder text for input
        title (str): Title for the search section
        show_history (bool): Whether to show search history
    """
    
    with st.sidebar:
        st.markdown(f"### {title}")
        
        # Search input
        question = st.text_input(
            "Ask stock market question", 
            key="search_input",
            placeholder=placeholder,
            label_visibility="collapsed"
        )
        
        # Ask button with loading state
        button_text = "⏳ Thinking..." if st.session_state.is_loading else "🚀 Ask"
        button_disabled = st.session_state.is_loading or not question.strip()
        
        if st.button(button_text, key="ask_btn", disabled=button_disabled, use_container_width=True):
            SearchBarState.start_loading(question)
            st.rerun()
        
        # Show search history if enabled
        if show_history and st.session_state.search_history:
            st.markdown("---")
            st.markdown("### 📚 Recent Questions")
            
            for i, item in enumerate(reversed(st.session_state.search_history[-5:])):
                with st.expander(f"Q{len(st.session_state.search_history) - i}: {item['question'][:50]}..."):
                    st.markdown(f"**Question:** {item['question']}")
                    st.markdown(f"**Answer:** {item['response'][:200]}...")
                    if st.button(f"View Full Answer", key=f"view_history_{i}"):
                        st.session_state.popup_response = item['response']
                        st.session_state.show_popup = True
                        st.rerun()

def render_inline_search(
    container_width: bool = True,
    show_examples: bool = True
):
    """
    Render the search input inline (not in sidebar)
    
    Args:
        container_width (bool): Whether to use full container width
        show_examples (bool): Whether to show example questions
    """
    
    if show_examples:
        st.markdown("### 💡 Example Questions:")
        examples = [
            "What is the difference between a bull and bear market?",
            "How do IPOs work?",
            "What are the main stock market indices?",
            "Explain options trading basics"
        ]
        
        cols = st.columns(2)
        for i, example in enumerate(examples):
            with cols[i % 2]:
                if st.button(f"📝 {example}", key=f"example_{i}", use_container_width=True):
                    SearchBarState.start_loading(example)
                    st.rerun()
        
        st.markdown("---")
    
    # Search input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        question = st.text_input(
            "Ask your stock market question:",
            key="inline_search_input",
            placeholder="e.g., What is a bull market?"
        )
    
    with col2:
        st.write("")  # Add some space
        button_text = "⏳" if st.session_state.is_loading else "🚀 Ask"
        button_disabled = st.session_state.is_loading or not question.strip()
        
        if st.button(button_text, key="inline_ask_btn", disabled=button_disabled):
            SearchBarState.start_loading(question)
            st.rerun()

def render_search_bar(
    location: str = "sidebar",
    **kwargs
):
    """
    Main function to render the complete search bar component
    
    Args:
        location (str): Where to render - "sidebar" or "inline"
        **kwargs: Additional arguments passed to specific render functions
    """
    
    # Initialize session state
    SearchBarState.initialize()
    
    # Render based on location
    if location == "sidebar":
        render_sidebar_search(**kwargs)
    elif location == "inline":
        render_inline_search(**kwargs)
    else:
        raise ValueError("Location must be 'sidebar' or 'inline'")
    
    # Show dialog when popup is requested
    if st.session_state.show_popup:
        show_response_dialog()

def add_search_bar_styles():
    """Add custom CSS styles for the search bar"""
    st.markdown("""
        <style>
            /* Search input styling */
            .stTextInput > div > div > input {
                border-radius: 8px;
                border: 2px solid #4CAF50;
                padding: 8px 12px;
                font-size: 14px;
            }
            
            .stTextInput > div > div > input:focus {
                border-color: #45a049;
                box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
            }
            
            /* Button styling */
            .stButton > button {
                border-radius: 8px;
                transition: all 0.3s ease;
                font-weight: 600;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
            
            /* Dialog styling */
            .st-dialog {
                max-width: 800px;
            }
            
            /* Animation for thinking dots */
            @keyframes pulse {
                0% { opacity: 0.8; }
                100% { opacity: 1; }
            }
        </style>
    """, unsafe_allow_html=True)

# Convenience function for quick setup
def setup_stock_search_bar(
    location: str = "sidebar",
    add_styles: bool = True,
    **kwargs
):
    """
    Quick setup function for stock search bar
    
    Args:
        location (str): Where to render - "sidebar" or "inline"
        add_styles (bool): Whether to add custom CSS styles
        **kwargs: Additional arguments passed to render_search_bar
    """
    if add_styles:
        add_search_bar_styles()
    
    render_search_bar(location=location, **kwargs)

# Example usage
if __name__ == "__main__":
    setup_stock_search_bar(
        location="sidebar",
        show_history=True,
        title="🤖 Stock Market AI"
    )