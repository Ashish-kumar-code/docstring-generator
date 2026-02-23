"""Professional Streamlit UI for Python Docstring Generator.

A creative, feature-rich interface for automated docstring generation,
validation, and code enhancement with multiple style support.
"""

import json
import tempfile
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


IMPORT_ERROR = False
_IMPORT_ERROR_TRACE = None
try:
    from docstring_generator import (
        BatchDocstringGenerator,
        DocstringInserter,
        DocstringValidator,
        ErrorDetector,
        parse_file,
    )
except Exception as _e:  
    IMPORT_ERROR = True
    import traceback

    _IMPORT_ERROR_TRACE = traceback.format_exc()

    class BatchDocstringGenerator:  # type: ignore
        def __init__(self, *a, **k):
            raise RuntimeError("docstring_generator not available; see logs")

    class DocstringInserter:  # type: ignore
        def __init__(self, *a, **k):
            raise RuntimeError("docstring_generator not available; see logs")

    class DocstringValidator:  # type: ignore
        def __init__(self, *a, **k):
            raise RuntimeError("docstring_generator not available; see logs")

    class ErrorDetector:  # type: ignore
        def __init__(self, *a, **k):
            raise RuntimeError("docstring_generator not available; see logs")

    def parse_file(*a, **k):  # type: ignore
        raise RuntimeError("docstring_generator not available; see logs")


st.set_page_config(
    page_title="Python Docstring Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


def init_session() -> None:
    s = st.session_state
    defaults = {
        "page": "home",
        "code": "",
        "metadata": None,
        "docstrings": None,
        "selected_docstrings": {},  # Track which docstrings are selected
        "enhanced": None,
        "style": "google",
        "parse_time": 0.0,
        "gen_time": 0.0,
        "insert_time": 0.0,
        "quality_before": None,  # Track quality metrics before generation
        "quality_after": None,   # Track quality metrics after generation
    }
    for k, v in defaults.items():
        if k not in s:
            s[k] = v


def render_page_header(title: str, subtitle: str = "", emoji: str = "") -> None:
    st.markdown(f"## {emoji} {title}")
    if subtitle:
        st.markdown(f"*{subtitle}*")
    st.markdown("---")


def sidebar() -> None:
    init_session()
    s = st.session_state
    with st.sidebar:
        st.markdown("# 📚 Docstring Generator")
        st.markdown("*Automated docstring generation with style support*")
        st.markdown("---")
        
        pages_list = ["home", "analyze", "generate", "compare", "metrics", "validate", "export"]
        page_emojis = ["🏠", "📂", "✨", "👀", "📊", "✅", "📥"]
        page_icons = [f"{e} {p.title()}" for e, p in zip(page_emojis, pages_list)]
        
        selected = st.radio("Navigation", page_icons, index=pages_list.index(s.page))
        s.page = pages_list[page_icons.index(selected)]
        
        st.markdown("---")
        st.markdown("### 🎯 Quick Info")
        if s.metadata:
            funcs = len(getattr(s.metadata, "functions", []) or [])
            st.info(f"✓ Parsed: {funcs} functions")
        if s.enhanced:
            st.success("✓ Docstrings generated")
        st.markdown("---")
        


def page_home() -> None:
    render_page_header("Welcome", "Automated docstring generation for Python", "🏠")
    
    # Hero section
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        ### ✨ Key Features
        
        - 🎨 **Multiple Styles** - Google, NumPy, reST
        - ✅ **Validation** - Quality & PEP 257 compliance
        - 🔍 **Error Detection** - Unused imports, missing hints
        - 💬 **Inline Comments** - Auto-annotate complex code
        - ⚡ **Instant** - Template-based, no API calls
        - 🎯 **Smart** - Preserves existing docstrings
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 Quick Start
        
        **3 Simple Steps:**
        
        1. **Upload** a Python file
        2. **Generate** docstrings in your style
        3. **Download** enhanced code
        
        Choose your docstring style (Google, NumPy, reST) and let the tool handle the rest!
        """)
    
    st.markdown("---")
    
    # Featured styles
    st.markdown("### 📖 Docstring Styles")
    style_cols = st.columns(3)
    
    styles_info = [
        ("Google", "args/returns format", "Most popular, readable"),
        ("NumPy", "Parameters/Returns headers", "Scientific computing"),
        ("reST", ":param: directives", "Sphinx & documentation"),
    ]
    
    for col, (name, fmt, desc) in zip(style_cols, styles_info):
        with col:
            st.markdown(f"""
            **{name}**
            
            {fmt}
            
            *{desc}*
            """)
    
    st.markdown("---")
    st.markdown("""
    ### 📊 Metrics & Export
    
    Generate comprehensive reports with:
    - **Quality Scores** (0-100 scale)
    - **Docstring Coverage** per function
    - **Code Issues** detection
    - **Multi-format Export** (Python, Markdown, JSON, HTML)
    """)


def page_analyze() -> None:
    render_page_header("Analyze", "Upload, enter path, or paste Python code to analyze structure", "📂")
    
    # Tabs for different input methods
    input_tab1, input_tab2, input_tab3 = st.tabs(["📥 Upload File", "📂 Enter Path", "📝 Paste Code"])
    
    with input_tab1:
        st.markdown("### Upload a Python File")
        uploaded = st.file_uploader("Select a .py file to analyze", type=["py"], help="Choose a single Python file", key="file_uploader")
        if uploaded is not None:
            code = uploaded.read().decode("utf-8")
            st.session_state.code = code
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
                f.write(code)
                tmp = f.name
            metadata = parse_file(tmp)
            st.session_state.metadata = metadata
            Path(tmp).unlink(missing_ok=True)
            
            st.success(f"✅ File '{uploaded.name}' parsed successfully!")
            
            # Show statistics
            meta = st.session_state.metadata
            funcs = len(getattr(meta, "functions", []) or [])
            classes = len(getattr(meta, "classes", []) or [])
            lines = len(code.splitlines())
            
            metric_cols = st.columns(3)
            metric_cols[0].metric("📏 Lines of Code", lines)
            metric_cols[1].metric("🔧 Functions", funcs)
            metric_cols[2].metric("📦 Classes", classes)
    
    with input_tab2:
        st.markdown("### Enter File or Directory Path")
        st.info("📌 Enter the full path to a Python file or directory containing Python files")
        
        path_input = st.text_input(
            "File/Directory Path",
            placeholder="/home/user/project/file.py or /home/user/project/src",
            help="Absolute or relative path to a .py file or directory"
        )
        
        if path_input:
            path_obj = Path(path_input)
            
            if not path_obj.exists():
                st.error(f"❌ Path does not exist: {path_input}")
            elif path_obj.is_file():
                if path_obj.suffix == ".py":
                    try:
                        code = path_obj.read_text(encoding="utf-8")
                        st.session_state.code = code
                        metadata = parse_file(str(path_obj))
                        st.session_state.metadata = metadata
                        
                        st.success(f"✅ File '{path_obj.name}' parsed successfully!")
                        
                        # Show statistics
                        meta = st.session_state.metadata
                        funcs = len(getattr(meta, "functions", []) or [])
                        classes = len(getattr(meta, "classes", []) or [])
                        lines = len(code.splitlines())
                        
                        metric_cols = st.columns(3)
                        metric_cols[0].metric("📏 Lines of Code", lines)
                        metric_cols[1].metric("🔧 Functions", funcs)
                        metric_cols[2].metric("📦 Classes", classes)
                    except Exception as e:
                        st.error(f"❌ Error reading file: {str(e)}")
                else:
                    st.error("❌ File is not a Python file (.py)")
            elif path_obj.is_dir():
                # List Python files in directory
                py_files = sorted(path_obj.glob("**/*.py"))
                if not py_files:
                    st.warning("⚠️ No Python files found in directory")
                else:
                    st.success(f"✅ Found {len(py_files)} Python file(s) in directory")
                    st.markdown("### 📋 Python Files Found")
                    selected_file = st.selectbox(
                        "Select a file to analyze",
                        py_files,
                        format_func=lambda f: f"{f.name} ({f.parent.name}/)"
                    )
                    
                    if selected_file:
                        try:
                            code = selected_file.read_text(encoding="utf-8")
                            st.session_state.code = code
                            metadata = parse_file(str(selected_file))
                            st.session_state.metadata = metadata
                            
                            st.success(f"✅ File '{selected_file.name}' parsed successfully!")
                            
                            # Show statistics
                            meta = st.session_state.metadata
                            funcs = len(getattr(meta, "functions", []) or [])
                            classes = len(getattr(meta, "classes", []) or [])
                            lines = len(code.splitlines())
                            
                            metric_cols = st.columns(3)
                            metric_cols[0].metric("📏 Lines of Code", lines)
                            metric_cols[1].metric("🔧 Functions", funcs)
                            metric_cols[2].metric("📦 Classes", classes)
                        except Exception as e:
                            st.error(f"❌ Error reading file: {str(e)}")
    
    with input_tab3:
        st.markdown("### Paste Python Code")
        code_input = st.text_area(
            "Python code",
            height=300,
            placeholder="def my_function(x):\n    return x * 2",
            key="code_input"
        )
        
        if code_input:
            st.session_state.code = code_input
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
                f.write(code_input)
                tmp = f.name
            try:
                metadata = parse_file(tmp)
                st.session_state.metadata = metadata
                
                st.success("✅ Code parsed successfully!")
                
                # Show statistics
                meta = st.session_state.metadata
                funcs = len(getattr(meta, "functions", []) or [])
                classes = len(getattr(meta, "classes", []) or [])
                lines = len(code_input.splitlines())
                
                metric_cols = st.columns(3)
                metric_cols[0].metric("📏 Lines of Code", lines)
                metric_cols[1].metric("🔧 Functions", funcs)
                metric_cols[2].metric("📦 Classes", classes)
            except Exception as e:
                st.error(f"❌ Error parsing code: {str(e)}")
            finally:
                Path(tmp).unlink(missing_ok=True)
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("""
    - **Upload**: Select a single file via file browser
    - **Path**: Enter file path (e.g., `/home/user/file.py`) or directory path to browse available files
    - **Paste**: Copy and paste code directly for quick analysis
    - Check for existing docstrings
    - Review class/method structure
    """)
    
    st.markdown("---")
    
    if st.session_state.code:
        st.markdown("### 👀 Code Preview")
        code = st.session_state.code
        st.code(code[:500] + ("\n..." if len(code) > 500 else ""), language="python")


def apply_selected_docstrings(code: str, docstrings_map: dict, selected: dict, metadata) -> str:
    """Apply only the selected docstrings to the code.
    
    Args:
        code: Original source code
        docstrings_map: All generated docstrings {name -> GeneratedDocstring}
        selected: Selected docstrings {name -> bool}
        metadata: File metadata
    
    Returns:
        Code with only selected docstrings inserted
    """
    filtered_docstrings = {
        name: docstring 
        for name, docstring in docstrings_map.items() 
        if selected.get(name, False)
    }
    
    if not filtered_docstrings:
        return code
    
    return DocstringInserter(code).insert_docstrings(filtered_docstrings)


def page_generate() -> None:
    render_page_header("Generate", "Create docstrings for parsed functions and classes", "✨")
    
    if not st.session_state.metadata:
        st.warning("⚠️ No parsed file found. Please use the Analyze page first.", icon="🔄")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎨 Select Docstring Style")
        style_descriptions = {
            "google": "Popular, readable format with Args/Returns sections",
            "numpy": "Scientific style with Parameters/Returns headers",
            "rest": "Sphinx-compatible reStructuredText format"
        }
        style = st.radio(
            "Style",
            ["google", "numpy", "rest"],
            index=["google", "numpy", "rest"].index(st.session_state.style),
            help="Choose the docstring format",
            horizontal=True
        )
        st.session_state.style = style
        st.info(f"**{style.upper()}**: {style_descriptions[style]}")
    
    with col2:
        st.markdown("### 📊 Preview")
        example = """def calculate(x: int) -> int:
    \"\"\"Calculate value.
    
    Args:
        x: Input value
    
    Returns:
        Computed result
    \"\"\"
    return x * 2"""
        st.code(example if style == "google" else "See generated output →", language="python")
    
    st.markdown("---")
    
    if st.button("🚀 Generate Docstrings", use_container_width=True):
        with st.spinner("⏳ Calculating initial quality metrics..."):
            # Calculate quality BEFORE generation
            s = st.session_state
            s.quality_before = calculate_quality_score(s.code, s.metadata)
        
        with st.spinner("⏳ Generating docstrings..."):
            gen = BatchDocstringGenerator(style=style)
            s = st.session_state
            s.docstrings = gen.generate_all(s.metadata)
            # Initialize all as selected by default
            s.selected_docstrings = {name: True for name in s.docstrings.keys()}
            s.enhanced = DocstringInserter(s.code).insert_docstrings(s.docstrings)
        
        st.success("✅ Docstrings generated!")
    
    # Show review and selection interface once docstrings are generated
    if st.session_state.docstrings:
        st.markdown("---")
        st.markdown("### 🔍 Selective Review & Acceptance")
        st.markdown("Review generated docstrings and select which ones to apply:")
        
        # Create tabs for functions and classes
        col_func, col_class = st.columns(2)
        
        with col_func:
            st.markdown("#### 🔧 Functions")
            functions = getattr(st.session_state.metadata, 'functions', []) or []
            func_names = [f.name for f in functions]
            func_docstrings = {k: v for k, v in st.session_state.docstrings.items() if k in func_names}
            
            if func_docstrings:
                for name, doc_obj in func_docstrings.items():
                    col_check, col_preview = st.columns([1, 3])
                    with col_check:
                        st.session_state.selected_docstrings[name] = st.checkbox(
                            name,
                            value=st.session_state.selected_docstrings.get(name, True),
                            key=f"func_{name}"
                        )
                    with col_preview:
                        with st.expander(f"Preview {name}", expanded=False):
                            st.code(doc_obj.content if hasattr(doc_obj, 'content') else str(doc_obj), language="python")
            else:
                st.info("No function docstrings generated")
        
        with col_class:
            st.markdown("#### 📦 Classes & Methods")
            classes = getattr(st.session_state.metadata, 'classes', []) or []
            class_names = [c.name for c in classes]
            class_docstrings = {k: v for k, v in st.session_state.docstrings.items() if k in class_names or any(k.startswith(f"{cn}.") for cn in class_names)}
            
            if class_docstrings:
                for name, doc_obj in class_docstrings.items():
                    col_check, col_preview = st.columns([1, 3])
                    with col_check:
                        st.session_state.selected_docstrings[name] = st.checkbox(
                            name,
                            value=st.session_state.selected_docstrings.get(name, True),
                            key=f"class_{name}"
                        )
                    with col_preview:
                        with st.expander(f"Preview {name}", expanded=False):
                            st.code(doc_obj.content if hasattr(doc_obj, 'content') else str(doc_obj), language="python")
            else:
                st.info("No class docstrings generated")
        
        st.markdown("---")
        st.markdown("### 📊 Selection Summary")
        total_selected = sum(1 for v in st.session_state.selected_docstrings.values() if v)
        total_generated = len(st.session_state.docstrings)
        
        summary_col1, summary_col2, summary_col3 = st.columns(3)
        summary_col1.metric("📋 Total Generated", total_generated)
        summary_col2.metric("✅ Selected", total_selected)
        summary_col3.metric("⏭️ To Skip", total_generated - total_selected)
        
        st.markdown("---")
        
        if st.button("💾 Apply Selected Docstrings", use_container_width=True, type="primary"):
            with st.spinner("⏳ Applying selected docstrings..."):
                s = st.session_state
                s.enhanced = apply_selected_docstrings(
                    s.code,
                    s.docstrings,
                    s.selected_docstrings,
                    s.metadata
                )
            st.success(f"✅ Applied {total_selected} docstrings!")
            
            st.markdown("---")
            st.markdown("### 📊 Quality Analysis: Before vs After")
            
            # Calculate quality metrics after applying docstrings
            # For after quality, we need to parse the enhanced code to get updated metadata
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
                f.write(st.session_state.enhanced)
                tmp = f.name
            try:
                enhanced_metadata = parse_file(tmp)
                st.session_state.quality_after = calculate_quality_score(st.session_state.enhanced, enhanced_metadata)
            finally:
                Path(tmp).unlink(missing_ok=True)
            
            # Display before/after comparison
            if st.session_state.quality_before and st.session_state.quality_after:
                before = st.session_state.quality_before
                after = st.session_state.quality_after
                
                # Main metrics comparison
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("#### 📈 Before")
                    st.metric("Quality Score", f"{before['score']}/100")
                    st.metric("Coverage", f"{before['details'].get('doc_coverage', 0):.1f}%")
                
                with col2:
                    st.markdown("#### ✨ After")
                    st.metric("Quality Score", f"{after['score']}/100")
                    st.metric("Coverage", f"{after['details'].get('doc_coverage', 0):.1f}%")
                
                with col3:
                    st.markdown("#### 📊 Improvement")
                    score_diff = after['score'] - before['score']
                    coverage_diff = after['details'].get('doc_coverage', 0) - before['details'].get('doc_coverage', 0)
                    
                    score_color = "🟢" if score_diff > 0 else "🔴" if score_diff < 0 else "⚪"
                    coverage_color = "🟢" if coverage_diff > 0 else "🔴" if coverage_diff < 0 else "⚪"
                    
                    st.markdown(f"`{score_color} Score: {score_diff:+d} pts`")
                    st.markdown(f"`{coverage_color} Coverage: {coverage_diff:+.1f}%`")
            
            st.markdown("---")
            st.markdown("### 📝 Enhanced Code Preview")
            enhanced = st.session_state.enhanced
            st.code(enhanced[:600] + ("\n..." if len(enhanced) > 600 else ""), language="python")


def page_metrics() -> None:
    render_page_header("Metrics", "Quality scores and coverage analysis", "📊")
    
    if not st.session_state.metadata or not st.session_state.code:
        st.warning("⚠️ Please analyze a file first", icon="📂")
        return
    
    metadata = st.session_state.metadata
    loc = len(st.session_state.code.splitlines())
    functions = len(getattr(metadata, "functions", []))
    classes = len(getattr(metadata, "classes", []))
    
    coverage = 0.0
    if functions + classes:
        covered = sum(1 for f in getattr(metadata, "functions", []) if getattr(f, "docstring", None))
        coverage = 100.0 * covered / max(1, functions)
    
    # Key metrics
    st.markdown("### 📈 Key Metrics")
    metric_cols = st.columns(4)
    metric_cols[0].metric("📏 Total Lines", loc, delta="lines of code")
    metric_cols[1].metric("🔧 Functions", functions, delta="to document")
    metric_cols[2].metric("📦 Classes", classes, delta="found")
    metric_cols[3].metric("✅ Coverage", f"{coverage:.1f}%", delta="documented")
    
    st.markdown("---")
    
    # Quality section
    quality = calculate_quality_score(st.session_state.code, metadata)
    
    st.markdown("### 🎯 Quality Analysis")
    col1, col2, col3 = st.columns([1, 2, 2])
    
    with col1:
        score = quality['score']
        score_color = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
        st.metric(f"{score_color} Quality Score", f"{quality['score']}/100")
    
    with col2:
        st.markdown("**Documentation Coverage**")
        doc_cov = quality['details'].get('doc_coverage', 0)
        st.progress(int(doc_cov) / 100)
        st.markdown(f"*{doc_cov:.1f}% of functions documented*")
    
    with col3:
        st.markdown("**Average Function Length**")
        avg_len = quality['details'].get('avg_func_len', 0)
        st.metric("LOC per Function", f"{avg_len:.1f}")
    
    # Breakdown details
    with st.expander("📋 Detailed Breakdown", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Coverage Details**")
            st.write(f"Total Functions: {quality['details'].get('functions', 0)}")
            st.write(f"Documentation: {doc_cov:.1f}%")
        with col2:
            st.markdown("**Size Analysis**")
            st.write(f"Avg Length: {avg_len:.1f} lines")
            st.write(f"Total LOC: {loc}")
    
    st.markdown("---")
    
    # Per-function table
    funcs = getattr(metadata, 'functions', []) or []
    if funcs:
        st.markdown("### 🔍 Per-Function Coverage")
        rows = []
        for f in funcs:
            rows.append({
                '📌 Name': f.name,
                '📍 Line': getattr(f, 'lineno', '?'),
                '🔤 Params': len(getattr(f, 'parameters', []) or []),
                '📝 Documented': "✅" if getattr(f, 'docstring', None) else "❌",
            })
        st.dataframe(rows, use_container_width=True)


def calculate_quality_score(code: str, metadata) -> dict:
    """Return a simple quality score (0-100) and breakdown.

    This is a lightweight heuristic: docs per function, average length,
    and presence of docstrings.
    """
    functions = getattr(metadata, "functions", []) or []
    total = len(functions)
    if total == 0:
        return {"score": 100, "details": {"functions": 0, "doc_coverage": 100.0}}
    documented = sum(1 for f in functions if getattr(f, "docstring", None))
    doc_coverage = 100.0 * documented / total
    avg_len = sum((getattr(f, "end_line", 0) - getattr(f, "start_line", 0)) for f in functions) / max(1, total)
    score = int(0.6 * doc_coverage + 0.4 * max(0, 100 - avg_len))
    return {"score": max(0, min(100, score)), "details": {"functions": total, "doc_coverage": doc_coverage, "avg_func_len": avg_len}}


def calculate_coverage_metrics(code: str, metadata) -> dict:
    """Return simple coverage estimates for docstrings in functions/classes."""
    functions = getattr(metadata, "functions", []) or []
    total = len(functions)
    if total == 0:
        return {"coverage_percent": 100.0, "total": 0, "documented": 0}
    documented = sum(1 for f in functions if getattr(f, "docstring", None))
    coverage = 100.0 * documented / total
    return {"coverage_percent": coverage, "total": total, "documented": documented}


def page_compare() -> None:
    render_page_header("Compare", "Side-by-side comparison of original and enhanced code", "👀")
    
    if not st.session_state.code:
        st.warning("⚠️ Please analyze a file first", icon="📂")
        return
    
    if not st.session_state.enhanced:
        st.info("ℹ️ Generate docstrings first to see the comparison", icon="✨")
        return
    
    original = st.session_state.code
    enhanced = st.session_state.enhanced
    
    st.markdown("### 📄 Side-by-Side Comparison")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📄 Original Code")
        st.code(original[:450] + ("\n..." if len(original) > 450 else ""), language="python")
    
    with col2:
        st.markdown("#### ✨ Enhanced Code (with Docstrings)")
        st.code(enhanced[:450] + ("\n..." if len(enhanced) > 450 else ""), language="python")
    
    st.markdown("---")
    
    if st.button("📊 Show Unified Diff", use_container_width=True):
        import difflib
        diff_lines = list(difflib.unified_diff(
            original.splitlines(keepends=True),
            enhanced.splitlines(keepends=True),
            fromfile="original.py",
            tofile="enhanced.py",
            lineterm=""
        ))
        
        if diff_lines:
            st.markdown("#### 🔀 Unified Diff")
            diff_text = "".join(diff_lines)
            st.code(diff_text, language="diff")
        else:
            st.info("No differences found")


def page_validate() -> None:
    render_page_header("Validate", "Check docstring quality and detect code issues", "✅")
    
    if not st.session_state.enhanced:
        st.warning("⚠️ Generate docstrings first", icon="✨")
        return
    
    st.markdown("### 🔍 Validation Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ✅ Docstring Validation")
        validator = DocstringValidator()
        validation_result = validator.validate_all(st.session_state.enhanced) if hasattr(validator, "validate_all") else {}
        
        val_count = len(validation_result) if isinstance(validation_result, dict) else 0
        st.metric("📋 Items Validated", val_count)
        
        if validation_result:
            with st.expander("Details", expanded=False):
                for name, result in (validation_result.items() if isinstance(validation_result, dict) else []):
                    st.write(f"- {name}: {result}")
    
    with col2:
        st.markdown("#### 🐛 Code Issues")
        ed = ErrorDetector(st.session_state.metadata)
        code_issues = ed.detect_all() if hasattr(ed, "detect_all") else []
        
        issue_count = len(code_issues) if isinstance(code_issues, list) else 0
        issue_color = "🟢" if issue_count == 0 else "🟡" if issue_count < 5 else "🔴"
        st.metric(f"{issue_color} Issues Found", issue_count)
        
        if code_issues:
            with st.expander("Issue Details", expanded=False):
                for issue in code_issues:
                    if hasattr(issue, 'message'):
                        st.write(f"- {issue.message}")
                    else:
                        st.write(f"- {issue}")


def page_export() -> None:
    render_page_header("Export", "Download enhanced code and generate reports", "📥")
    
    if not st.session_state.enhanced:
        st.warning("⚠️ Generate docstrings first", icon="✨")
        return
    
    st.markdown("### 📥 Download Enhanced Code")
    st.download_button(
        label="📄 Download Python File",
        data=st.session_state.enhanced,
        file_name=f"enhanced_{st.session_state.style}.py",
        mime="text/plain",
        use_container_width=True
    )
    
    st.markdown("---")
    
    metadata = st.session_state.metadata
    quality = calculate_quality_score(st.session_state.code, metadata)
    coverage = calculate_coverage_metrics(st.session_state.code, metadata)
    
    st.markdown("### 📊 Generate Reports")
    
    # Report tabs
    rep_col1, rep_col2, rep_col3, rep_col4 = st.columns(4)
    
    # Markdown Report
    md_lines = [
        "# Docstring Generation Report",
        "",
        f"**Generated with:** Python Docstring Generator",
        f"**Style:** `{st.session_state.style}`",
        f"**Quality Score:** {quality['score']}/100",
        f"**Docstring Coverage:** {coverage['coverage_percent']:.1f}%",
        "",
        "## 📊 Statistics",
        f"- **Total Functions:** {coverage['total']}",
        f"- **Documented:** {coverage['documented']}",
        f"- **Missing Docstrings:** {coverage['total'] - coverage['documented']}",
        "",
        "## 🔍 Functions",
    ]
    for f in getattr(metadata, 'functions', []) or []:
        status = "✅ Documented" if getattr(f, 'docstring', None) else "❌ Missing"
        md_lines.append(f"- **{f.name}** (line {getattr(f,'lineno','?')}): {status}")
    md = "\n".join(md_lines)
    
    with rep_col1:
        st.download_button(
            label="📝 Markdown",
            data=md,
            file_name=f"report_{st.session_state.style}.md",
            use_container_width=True
        )
    
    # JSON Report
    json_data = {
        "metadata": {
            "generator": "Python Docstring Generator",
            "style": st.session_state.style,
            "timestamp": str(__import__('datetime').datetime.now())
        },
        "quality": quality,
        "coverage": coverage,
    }
    
    with rep_col2:
        st.download_button(
            label="🔹 JSON",
            data=json.dumps(json_data, indent=2),
            file_name="report_metadata.json",
            use_container_width=True
        )
    
    # CSV-like data
    csv_lines = ["Name,Line,Parameters,Documented"]
    for f in getattr(metadata, 'functions', []) or []:
        csv_lines.append(f"{f.name},{getattr(f,'lineno','?')},{len(getattr(f, 'parameters', []) or [])},{1 if getattr(f, 'docstring', None) else 0}")
    csv_data = "\n".join(csv_lines)
    
    with rep_col3:
        st.download_button(
            label="📋 CSV",
            data=csv_data,
            file_name="report_functions.csv",
            use_container_width=True
        )
    
    # HTML Report
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Docstring Generation Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; min-height: 100vh; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ font-size: 1.1em; opacity: 0.9; }}
        .content {{ padding: 40px; }}
        .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 30px 0; }}
        .metric-card {{ background: #f8f9fa; border-left: 4px solid #667eea; padding: 20px; border-radius: 8px; text-align: center; }}
        .metric-card h3 {{ color: #667eea; font-size: 2em; margin: 10px 0; }}
        .metric-card p {{ color: #666; font-size: 0.9em; }}
        .section {{ margin: 30px 0; }}
        .section h2 {{ color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px; margin-bottom: 20px; }}
        .function-list {{ display: grid; gap: 10px; }}
        .function-item {{ background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #764ba2; }}
        .function-item.documented {{ border-left-color: #28a745; }}
        .function-item.missing {{ border-left-color: #dc3545; }}
        .function-name {{ font-weight: bold; color: #333; }}
        .badge {{ display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 0.85em; margin-left: 10px; }}
        .badge.ok {{ background: #d4edda; color: #155724; }}
        .badge.err {{ background: #f8d7da; color: #721c24; }}
        .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #666; border-top: 1px solid #ddd; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Docstring Generation Report</h1>
            <p>Python Docstring Generator - {st.session_state.style.upper()} Style</p>
        </div>
        <div class="content">
            <div class="metrics">
                <div class="metric-card">
                    <p>Quality Score</p>
                    <h3>{quality['score']}/100</h3>
                </div>
                <div class="metric-card">
                    <p>Coverage</p>
                    <h3>{coverage['coverage_percent']:.1f}%</h3>
                </div>
                <div class="metric-card">
                    <p>Functions</p>
                    <h3>{coverage['total']}</h3>
                </div>
                <div class="metric-card">
                    <p>Documented</p>
                    <h3>{coverage['documented']}</h3>
                </div>
            </div>
            
            <div class="section">
                <h2>📋 Function Coverage</h2>
                <div class="function-list">
"""
    
    for f in getattr(metadata, 'functions', []) or []:
        has_doc = getattr(f, 'docstring', None)
        status_class = "documented" if has_doc else "missing"
        status_text = "✅ Documented" if has_doc else "❌ Missing"
        badge_class = "ok" if has_doc else "err"
        html += f'<div class="function-item {status_class}"><span class="function-name">{f.name}</span> <span class="badge {badge_class}">{status_text}</span></div>'
    
    html += """
                </div>
            </div>
        </div>
        <div class="footer">
            <p>Generated by Python Docstring Generator • www.github.com</p>
        </div>
    </div>
</body>
</html>"""
    
    with rep_col4:
        st.download_button(
            label="🌐 HTML",
            data=html,
            file_name="report.html",
            mime="text/html",
            use_container_width=True
        )
    
    st.markdown("---")
    st.markdown("### 👁️ Report Preview")
    with st.expander("View HTML Report", expanded=False):
        components.html(html, height=600, scrolling=True)


def main() -> None:
    init_session()
    sidebar()
    pages = {
        "home": page_home,
        "analyze": page_analyze,
        "generate": page_generate,
        "compare": page_compare,
        "metrics": page_metrics,
        "validate": page_validate,
        "export": page_export,
    }
    func = pages.get(st.session_state.page, page_home)
    func()


if __name__ == "__main__":
    main()
