# Modern Light Theme Conversion Prompt for Streamlit Projects

You are a Streamlit UI/UX specialist tasked with converting an existing Streamlit application to a modern light theme. Follow these guidelines precisely.

## Core Objectives

1. Configure Streamlit's `.streamlit/config.toml` with modern light theme colors
2. Apply custom CSS via `st.markdown()` with `<style>` tags for enhanced styling
3. Maintain all existing Streamlit functionality and layout
4. Improve visual hierarchy and spacing throughout the app
5. Ensure accessibility and readability
6. Enhance component appearance (buttons, cards, inputs, etc.)

## Modern Light Theme Specification

### Color Palette (Use these exact hex values)

**Base Colors:**
- Page Background: `#f5f5f7`
- Surface/Card Background: `#ffffff`
- Primary Brand: `#4f46e5` (Indigo)
- Primary Soft Background: `#eef2ff`
- Secondary: `#6366f1`

**Text Colors:**
- Primary Text: `#111827` (Near-black)
- Secondary Text: `#6b7280` (Medium gray)
- Muted Text: `#9ca3af` (Light gray)
- Text on Primary: `#ffffff` (White)

**Utility Colors:**
- Success: `#22c55e` (Green)
- Warning: `#f59e0b` (Amber)
- Danger/Error: `#ef4444` (Red)
- Info: `#06b6d4` (Cyan)

**Borders & Dividers:**
- Subtle Border: `#e5e7eb` (Light gray)
- Strong Border: `#d1d5db` (Medium gray)
- Hover Border: `#bfdbfe` (Light blue)

## Streamlit Configuration (config.toml)

Create or update `.streamlit/config.toml` with these settings:

```toml
[theme]
primaryColor = "#4f46e5"
backgroundColor = "#f5f5f7"
secondaryBackgroundColor = "#ffffff"
textColor = "#111827"
font = "sans serif"

[client]
toolbarMode = "minimal"

[logger]
level = "info"
```

## Custom CSS for Enhanced Styling

Add this CSS to your Streamlit app using `st.markdown()` at the beginning of your script:

```html
<style>
    :root {
        --bg-page: #f5f5f7;
        --bg-surface: #ffffff;
        --text-primary: #111827;
        --text-secondary: #6b7280;
        --text-muted: #9ca3af;
        --accent: #4f46e5;
        --accent-soft: #eef2ff;
        --border: #e5e7eb;
        --success: #22c55e;
        --error: #ef4444;
        --warning: #f59e0b;
        --info: #06b6d4;
    }

    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: var(--text-primary);
        background-color: var(--bg-page);
        line-height: 1.6;
    }

    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary);
        font-weight: 600;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }

    h1 { font-size: 28px; margin-bottom: 16px; }
    h2 { font-size: 22px; margin-bottom: 12px; margin-top: 20px; }
    h3 { font-size: 18px; margin-bottom: 12px; }

    p { color: var(--text-secondary); margin-bottom: 12px; }

    /* Buttons */
    .stButton > button {
        background-color: var(--accent);
        color: #ffffff;
        border: none;
        border-radius: 999px;
        padding: 8px 20px;
        font-weight: 500;
        transition: all 0.18s ease;
    }

    .stButton > button:hover {
        background-color: #4338ca;
        box-shadow: 0 4px 6px rgba(79, 70, 229, 0.2);
    }

    .stButton > button:focus {
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.4);
    }

    /* Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        background-color: var(--bg-surface);
        color: var(--text-primary);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 14px;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent);
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        outline: none;
    }

    .stTextInput > div > div > input::placeholder,
    .stNumberInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: var(--text-muted);
    }

    /* Containers (Cards) */
    [data-testid="stContainer"] {
        background-color: var(--bg-surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    [data-testid="stContainer"]:hover {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
    }

    /* Metrics */
    [data-testid="stMetricContainer"] {
        background-color: var(--bg-surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid var(--border);
    }

    .stTabs [data-baseweb="tab"] {
        color: var(--text-secondary);
        border-radius: 8px 8px 0 0;
        padding: 10px 16px;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        color: var(--accent);
        border-bottom: 3px solid var(--accent);
    }

    /* Expanders */
    [data-testid="stExpander"] {
        background-color: var(--bg-surface);
        border: 1px solid var(--border);
        border-radius: 8px;
    }

    [data-testid="stExpander"] details {
        border: none;
    }

    /* Alerts & Status Messages */
    .stAlert {
        border-radius: 8px;
        padding: 12px 16px;
    }

    .stSuccess {
        background-color: rgba(34, 197, 94, 0.1);
        border: 1px solid var(--success);
        color: #166534;
    }

    .stError {
        background-color: rgba(239, 68, 68, 0.1);
        border: 1px solid var(--error);
        color: #991b1b;
    }

    .stWarning {
        background-color: rgba(245, 158, 11, 0.1);
        border: 1px solid var(--warning);
        color: #92400e;
    }

    .stInfo {
        background-color: rgba(6, 182, 212, 0.1);
        border: 1px solid var(--info);
        color: #164e63;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--bg-surface);
        border-right: 1px solid var(--border);
    }

    /* Code Blocks */
    code {
        background-color: var(--accent-soft);
        color: var(--accent);
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 14px;
    }

    [data-testid="stCodeBlock"] {
        background-color: var(--bg-surface);
        border: 1px solid var(--border);
        border-radius: 8px;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 8px;
    }

    /* Charts */
    [data-testid="stPlotlyContainer"] {
        background-color: var(--bg-surface);
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    /* Divider */
    hr { border-color: var(--border); margin: 20px 0; }

    /* Links */
    a {
        color: var(--accent);
        text-decoration: none;
    }

    a:hover {
        color: #4338ca;
        text-decoration: underline;
    }

    /* Labels */
    label {
        color: var(--text-primary);
        font-weight: 500;
    }

    /* Checkboxes & Radio */
    .stCheckbox > label, .stRadio > label {
        color: var(--text-primary);
    }
</style>
```

## Implementation Steps for Streamlit

### Step 1: Create/Update config.toml
- Location: Create `.streamlit/config.toml` in your project root
- Add the theme configuration with modern light colors from above
- Restart Streamlit to apply changes

### Step 2: Add Custom CSS to Your Main Script
- Import and define custom CSS string (or load from file)
- Call `st.markdown(custom_css, unsafe_allow_html=True)` at the very beginning of your app
- This should be done BEFORE any other Streamlit components

### Step 3: Update Page Configuration
```python
import streamlit as st

st.set_page_config(
    page_title="Your App",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

### Step 4: Refactor Component Styling
- Replace `st.write()` headings with `st.title()`, `st.header()`, `st.subheader()`
- Use `st.container()` for card-like layouts with proper spacing
- Apply consistent padding using dividers (`st.markdown("---")`)
- Use `st.columns()` for side-by-side layouts

### Step 5: Improve Layout Structure
Example of modern card layout:

```python
with st.container():
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.metric(label="Metric 1", value="100", delta="+5%")
    
    with col2:
        st.metric(label="Metric 2", value="200", delta="+12%")
    
    with col3:
        st.metric(label="Metric 3", value="300", delta="-2%")

st.markdown("---")
```

### Step 6: Sidebar Enhancement
```python
with st.sidebar:
    st.markdown("### Navigation")
    page = st.radio("Select Page", ["Home", "Analysis", "Settings"])
    
    st.markdown("---")
    st.markdown("**Quick Links**")
    with st.expander("Documentation"):
        st.write("Add links here...")
```

### Step 7: Form Styling
```python
with st.form("my_form"):
    st.write("### Settings Form")
    
    name = st.text_input("Full Name", placeholder="Enter your name")
    email = st.text_input("Email", placeholder="Enter your email")
    category = st.selectbox("Category", ["Option 1", "Option 2", "Option 3"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.form_submit_button("Submit", use_container_width=True)
    with col2:
        st.form_submit_button("Reset", use_container_width=True)
```

### Step 8: Add Status Message Styling
Use built-in Streamlit status functions with updated colors:

```python
st.success("✅ Operation completed successfully!")
st.error("❌ An error occurred. Please try again.")
st.warning("⚠️ Warning: Please review your inputs.")
st.info("ℹ️ Additional information for the user.")
```

## Quality Checklist

- [ ] `.streamlit/config.toml` created with modern light colors
- [ ] Custom CSS added to main script and applied correctly
- [ ] All Streamlit components styled (buttons, inputs, containers, etc.)
- [ ] Text colors updated to modern palette
- [ ] Button hover and focus states working
- [ ] Input fields have proper styling and focus effects
- [ ] Sidebar properly styled with light background
- [ ] Cards have subtle borders and shadows
- [ ] Status messages display correct colors
- [ ] Typography hierarchy is clear
- [ ] Spacing is consistent throughout
- [ ] No dark mode or old color values remain
- [ ] All elements have sufficient contrast (4.5:1 minimum)
- [ ] Charts and plots display with proper backgrounds

## Common Streamlit Patterns with Modern Theme

### Dashboard Layout
```python
st.title("📊 Analytics Dashboard")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Users", "1,234", "+5%")
col2.metric("Revenue", "$45K", "+12%")
col3.metric("Conversion", "3.21%", "-0.5%")
col4.metric("Avg Order", "$125", "+2%")

st.markdown("---")

with st.container():
    st.subheader("Charts")
    col1, col2 = st.columns(2)
    with col1:
        st.line_chart({"data": [1, 2, 3, 4, 5]})
    with col2:
        st.bar_chart({"data": [3, 1, 4, 1, 5]})
```

### Form with Sections
```python
with st.form("settings_form"):
    st.markdown("### User Settings")
    
    st.write("**Account Information**")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("First Name")
    with col2:
        st.text_input("Last Name")
    
    st.write("**Preferences**")
    st.checkbox("Email Notifications")
    st.selectbox("Theme", ["Light", "Dark", "Auto"])
    
    st.form_submit_button("Save Settings", use_container_width=True)
```

### Multi-Page Navigation
```python
with st.sidebar:
    st.markdown("### Pages")
    page = st.radio("Navigate", [
        "🏠 Home",
        "📊 Dashboard",
        "⚙️ Settings",
        "ℹ️ About"
    ])

if "Home" in page:
    st.title("Welcome Home")
elif "Dashboard" in page:
    st.title("Dashboard View")
# etc...
```

## Additional Streamlit Tips

1. Use `st.cache_data` and `st.cache_resource` for performance
2. Apply `use_container_width=True` on buttons and inputs for responsive design
3. Use `gap="medium"` or `gap="large"` in `st.columns()` for better spacing
4. Use `st.expander()` to reduce cognitive load on long pages
5. Test responsively on different screen sizes
6. Use `st.markdown("---")` for visual separation
7. Organize code with `with st.sidebar:` blocks
8. Add docstrings to functions for maintainability

---

## How to Use This Prompt

1. Copy this entire prompt
2. Provide it to your AI agent along with your Streamlit project
3. Ask: "Apply this modern light theme specification to my Streamlit app"
4. The agent should:
   - Create/update `.streamlit/config.toml`
   - Inject the custom CSS into your main script
   - Refactor components for consistent styling
   - Update layouts and spacing
5. Test locally: `streamlit run app.py`
6. Make final adjustments as needed

Good luck with your Streamlit theme transformation! 🎨