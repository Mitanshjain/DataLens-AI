# ==========================================
# DATALENS AI - PREMIUM HTML REPORT GENERATOR V4
# ==========================================

from pathlib import Path
from html import escape
import re


# ==========================================
# DISPLAY HELPERS
# ==========================================

def clean_title(value):
    """
    Convert internal keys into clean
    presentation titles.
    """

    return (
        str(value)
        .replace("_", " ")
        .strip()
        .title()
    )


def format_value(value):
    """
    Format individual report values.
    """

    if value is None:
        return "N/A"

    if isinstance(value, bool):
        return "Yes" if value else "No"

    if isinstance(value, float):

        if value != value:
            return "Missing"

        return f"{value:,.4f}"

    return escape(str(value))


# ==========================================
# SIMPLE DICTIONARY TABLE
# ==========================================

def dictionary_to_html(data):
    """
    Render scalar dictionary values as a
    two-column summary table.
    """

    if not data:
        return (
            '<p class="empty-message">'
            'No data available.'
            '</p>'
        )

    rows = []

    for key, value in data.items():

        if isinstance(
            value,
            (dict, list, tuple)
        ):
            continue

        rows.append(
            f"""
            <tr>
                <td class="label-cell">
                    {escape(clean_title(key))}
                </td>

                <td>
                    {format_value(value)}
                </td>
            </tr>
            """
        )

    if not rows:
        return ""

    return f"""
    <div class="table-wrapper">
        <table class="summary-table">
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
    </div>
    """


# ==========================================
# RECORD TABLE
# ==========================================

def records_to_html(records):
    """
    Render list-based report data.

    Lists of dictionaries become tables.
    Simple lists become bullet lists.
    """

    if not records:
        return (
            '<p class="empty-message">'
            'No data available.'
            '</p>'
        )

    if not isinstance(records[0], dict):

        items = "".join(
            f"<li>{format_value(item)}</li>"
            for item in records
        )

        return f"""
        <ul class="report-list">
            {items}
        </ul>
        """

    columns = []

    for record in records:

        for column in record.keys():

            if column not in columns:
                columns.append(column)

    header = "".join(
        f"""
        <th>
            {escape(clean_title(column))}
        </th>
        """
        for column in columns
    )

    body_rows = []

    for record in records:

        cells = []

        for column in columns:

            value = record.get(
                column,
                ""
            )

            if isinstance(
                value,
                (dict, list, tuple)
            ):

                display_value = render_section(
                    value,
                    level=6
                )

            else:

                display_value = format_value(
                    value
                )

            cells.append(
                f"""
                <td>
                    {display_value}
                </td>
                """
            )

        body_rows.append(
            f"""
            <tr>
                {''.join(cells)}
            </tr>
            """
        )

    return f"""
    <div class="table-wrapper">

        <table class="data-table">

            <thead>
                <tr>
                    {header}
                </tr>
            </thead>

            <tbody>
                {''.join(body_rows)}
            </tbody>

        </table>

    </div>
    """


# ==========================================
# RECURSIVE REPORT RENDERER
# ==========================================

def render_section(
    data,
    level=3
):
    """
    Recursively render nested report data.
    """

    if data is None:
        return (
            '<p class="empty-message">'
            'No data available.'
            '</p>'
        )

    if isinstance(
        data,
        dict
    ):

        parts = []

        simple_values = {
            key: value
            for key, value in data.items()
            if not isinstance(
                value,
                (dict, list, tuple)
            )
        }

        if simple_values:

            parts.append(
                dictionary_to_html(
                    simple_values
                )
            )

        for key, value in data.items():

            if not isinstance(
                value,
                (dict, list, tuple)
            ):
                continue

            heading_level = min(
                level,
                6
            )

            title = clean_title(
                key
            )

            parts.append(
                f"""
                <h{heading_level}
                    class="subheading"
                >
                    {escape(title)}
                </h{heading_level}>
                """
            )

            if isinstance(
                value,
                list
            ):

                parts.append(
                    records_to_html(
                        value
                    )
                )

            else:

                parts.append(
                    render_section(
                        value,
                        level=heading_level + 1
                    )
                )

        return "".join(parts)

    if isinstance(
        data,
        list
    ):

        return records_to_html(
            data
        )

    return (
        f"<p>{format_value(data)}</p>"
    )


# ==========================================
# INLINE AI MARKDOWN
# ==========================================

def render_inline_markdown(text):
    """
    Render a small safe subset of inline
    Markdown used by the AI Analyst.
    """

    safe_text = escape(
        str(text)
    )

    safe_text = re.sub(
        r"`([^`]+)`",
        r"<code>\1</code>",
        safe_text
    )

    safe_text = re.sub(
        r"\*\*(.+?)\*\*",
        r"<strong>\1</strong>",
        safe_text
    )

    return safe_text


# ==========================================
# MARKDOWN TABLE
# ==========================================

def markdown_table_to_html(lines):
    """
    Convert a simple Markdown table into HTML.
    """

    rows = []

    for line in lines:

        clean_line = (
            line.strip()
            .strip("|")
        )

        cells = [
            cell.strip()
            for cell
            in clean_line.split("|")
        ]

        rows.append(cells)

    if len(rows) < 2:
        return ""

    headers = rows[0]
    data_rows = rows[2:]

    header_html = "".join(
        f"""
        <th>
            {render_inline_markdown(cell)}
        </th>
        """
        for cell in headers
    )

    body_html = []

    for row in data_rows:

        cells = "".join(
            f"""
            <td>
                {render_inline_markdown(cell)}
            </td>
            """
            for cell in row
        )

        body_html.append(
            f"<tr>{cells}</tr>"
        )

    return f"""
    <div class="table-wrapper">

        <table class="data-table ai-table">

            <thead>
                <tr>
                    {header_html}
                </tr>
            </thead>

            <tbody>
                {''.join(body_html)}
            </tbody>

        </table>

    </div>
    """


# ==========================================
# AI MARKDOWN RENDERER
# ==========================================

def markdown_to_html(markdown_text):
    """
    Render the Markdown subset normally
    returned by the DataLens AI Analyst.
    """

    if not markdown_text:
        return (
            '<p class="empty-message">'
            'No AI analysis available.'
            '</p>'
        )

    lines = (
        str(markdown_text)
        .replace("\r\n", "\n")
        .split("\n")
    )

    html_parts = []
    index = 0

    while index < len(lines):

        line = lines[index].strip()

        if not line:
            index += 1
            continue

        if line in {
            "---",
            "***",
            "___"
        }:

            html_parts.append(
                '<hr class="ai-divider">'
            )

            index += 1
            continue

        heading_match = re.match(
            r"^(#{1,6})\s+(.+)$",
            line
        )

        if heading_match:

            markdown_level = len(
                heading_match.group(1)
            )

            html_level = min(
                markdown_level + 2,
                6
            )

            heading_text = (
                heading_match.group(2)
            )

            html_parts.append(
                f"""
                <h{html_level}
                    class="ai-heading"
                >
                    {
                        render_inline_markdown(
                            heading_text
                        )
                    }
                </h{html_level}>
                """
            )

            index += 1
            continue

        if line.startswith("|"):

            table_lines = []

            while (
                index < len(lines)
                and lines[index]
                .strip()
                .startswith("|")
            ):

                table_lines.append(
                    lines[index].strip()
                )

                index += 1

            html_parts.append(
                markdown_table_to_html(
                    table_lines
                )
            )

            continue

        if re.match(
            r"^[-*]\s+",
            line
        ):

            items = []

            while index < len(lines):

                current = (
                    lines[index]
                    .strip()
                )

                match = re.match(
                    r"^[-*]\s+(.+)$",
                    current
                )

                if not match:
                    break

                items.append(
                    match.group(1)
                )

                index += 1

            list_html = "".join(
                f"""
                <li>
                    {
                        render_inline_markdown(
                            item
                        )
                    }
                </li>
                """
                for item in items
            )

            html_parts.append(
                f"""
                <ul class="ai-list">
                    {list_html}
                </ul>
                """
            )

            continue

        if re.match(
            r"^\d+\.\s+",
            line
        ):

            items = []

            while index < len(lines):

                current = (
                    lines[index]
                    .strip()
                )

                match = re.match(
                    r"^\d+\.\s+(.+)$",
                    current
                )

                if not match:
                    break

                items.append(
                    match.group(1)
                )

                index += 1

            list_html = "".join(
                f"""
                <li>
                    {
                        render_inline_markdown(
                            item
                        )
                    }
                </li>
                """
                for item in items
            )

            html_parts.append(
                f"""
                <ol class="ai-list">
                    {list_html}
                </ol>
                """
            )

            continue

        paragraph_lines = [
            line
        ]

        index += 1

        while index < len(lines):

            next_line = (
                lines[index]
                .strip()
            )

            if not next_line:
                break

            if re.match(
                r"^(#{1,6})\s+",
                next_line
            ):
                break

            if next_line.startswith("|"):
                break

            if re.match(
                r"^[-*]\s+",
                next_line
            ):
                break

            if re.match(
                r"^\d+\.\s+",
                next_line
            ):
                break

            if next_line in {
                "---",
                "***",
                "___"
            }:
                break

            paragraph_lines.append(
                next_line
            )

            index += 1

        paragraph = " ".join(
            paragraph_lines
        )

        html_parts.append(
            f"""
            <p class="ai-paragraph">
                {
                    render_inline_markdown(
                        paragraph
                    )
                }
            </p>
            """
        )

    return "".join(
        html_parts
    )


# ==========================================
# AI ANALYST SECTION
# ==========================================

def render_ai_analysis(
    ai_results
):
    """
    Render the final AI Analyst response.
    """

    if not ai_results:
        return (
            '<p class="empty-message">'
            'No AI analysis available.'
            '</p>'
        )

    analysis = ai_results.get(
        "analysis"
    )

    if not analysis:
        return (
            '<p class="empty-message">'
            'No AI analysis available.'
            '</p>'
        )

    return f"""
    <div class="ai-report">
        {
            markdown_to_html(
                analysis
            )
        }
    </div>
    """


# ==========================================
# DATASET SUMMARY CARDS
# ==========================================

def render_dataset_cards(
    dataset
):
    """
    Create high-level report cards.
    """

    cards = [
        (
            "Records",
            dataset.get(
                "total_records",
                "N/A"
            ),
            "Dataset volume",
            "01"
        ),
        (
            "Columns",
            dataset.get(
                "total_columns",
                "N/A"
            ),
            "Available variables",
            "02"
        ),
        (
            "Missing Values",
            dataset.get(
                "missing_values",
                "N/A"
            ),
            "Data completeness",
            "03"
        ),
        (
            "Duplicates",
            dataset.get(
                "duplicate_rows",
                "N/A"
            ),
            "Repeated records",
            "04"
        )
    ]

    card_html = "".join(
        f"""
        <article class="metric-card">

            <div class="metric-card-top">
                <span class="metric-index">
                    {escape(index)}
                </span>

                <span class="metric-status-dot"></span>
            </div>

            <strong class="metric-value">
                {format_value(value)}
            </strong>

            <span class="metric-label">
                {escape(str(label))}
            </span>

            <span class="metric-description">
                {escape(description)}
            </span>

        </article>
        """
        for label, value, description, index in cards
    )

    return f"""
    <div class="metric-grid">
        {card_html}
    </div>
    """


# ==========================================
# DECISION INSIGHT HELPERS
# ==========================================

def _priority_class(priority):
    """
    Convert Decision Engine priority into a
    safe CSS class.
    """

    normalized = str(
        priority or "info"
    ).lower()

    if normalized not in {
        "high",
        "medium",
        "low",
        "info"
    }:
        normalized = "info"

    return normalized


def render_decision_summary(summary):
    """
    Render Decision Engine summary counters.
    """

    if not isinstance(
        summary,
        dict
    ):
        return ""

    cards = [
        (
            "Total Insights",
            summary.get(
                "total_insights",
                0
            ),
            "total"
        ),
        (
            "High Priority",
            summary.get(
                "high_priority",
                0
            ),
            "high"
        ),
        (
            "Medium Priority",
            summary.get(
                "medium_priority",
                0
            ),
            "medium"
        ),
        (
            "Low Priority",
            summary.get(
                "low_priority",
                0
            ),
            "low"
        ),
        (
            "Informational",
            summary.get(
                "informational",
                0
            ),
            "info"
        )
    ]

    cards_html = "".join(
        f"""
        <div class="decision-summary-card {css_class}">

            <span class="decision-summary-label">
                {escape(label)}
            </span>

            <strong class="decision-summary-value">
                {format_value(value)}
            </strong>

        </div>
        """
        for label, value, css_class
        in cards
    )

    return f"""
    <div class="decision-summary-grid">
        {cards_html}
    </div>
    """


def render_decision_insight_card(
    insight
):
    """
    Render one structured Decision Engine
    insight.
    """

    if not isinstance(
        insight,
        dict
    ):
        return ""

    priority = str(
        insight.get(
            "priority",
            "info"
        )
    ).lower()

    css_class = _priority_class(
        priority
    )

    title = (
        insight.get(
            "title"
        )
        or insight.get(
            "name"
        )
        or insight.get(
            "category"
        )
        or "Decision Insight"
    )

    observation = (
        insight.get(
            "observation"
        )
        or insight.get(
            "insight"
        )
        or insight.get(
            "message"
        )
        or insight.get(
            "description"
        )
    )

    recommendation = (
        insight.get(
            "recommendation"
        )
        or insight.get(
            "suggestion"
        )
        or insight.get(
            "next_step"
        )
    )

    category = insight.get(
        "category"
    )

    evidence = insight.get(
        "evidence"
    )

    category_html = ""

    if category:

        category_html = f"""
        <span class="decision-category">
            {escape(clean_title(category))}
        </span>
        """

    observation_html = ""

    if observation:

        observation_html = f"""
        <p class="decision-observation">
            {escape(str(observation))}
        </p>
        """

    evidence_html = ""

    if evidence is not None:

        evidence_html = f"""
        <div class="decision-detail">

            <div class="decision-detail-label">
                Evidence
            </div>

            {render_section(evidence, level=6)}

        </div>
        """

    recommendation_html = ""

    if recommendation:

        recommendation_html = f"""
        <div class="decision-recommendation">

            <span class="recommendation-icon">
                →
            </span>

            <div>
                <strong>Possible next step</strong>
                <p>
                    {escape(str(recommendation))}
                </p>
            </div>

        </div>
        """

    return f"""
    <article class="decision-card {css_class}">

        <div class="decision-card-header">

            <div>
                {category_html}

                <h4 class="decision-card-title">
                    {escape(str(title))}
                </h4>
            </div>

            <span class="priority-badge {css_class}">
                {escape(priority.title())}
            </span>

        </div>

        {observation_html}

        {evidence_html}

        {recommendation_html}

    </article>
    """


def render_decision_group(
    title,
    insights,
    priority
):
    """
    Render one priority group.
    """

    if not insights:
        return ""

    cards = "".join(
        render_decision_insight_card(
            insight
        )
        for insight in insights
    )

    return f"""
    <div class="decision-group {escape(priority)}">

        <div class="decision-group-header">

            <span class="decision-group-dot"></span>

            <h3 class="decision-group-title">
                {escape(title)}
            </h3>

            <span class="decision-group-count">
                {len(insights)}
            </span>

        </div>

        <div class="decision-card-list">
            {cards}
        </div>

    </div>
    """


def render_decision_insights(
    decision_results
):
    """
    Render Decision / Insight Engine results
    without duplicating all internal structures.

    Preferred source:
        priorities

    Fallback source:
        all_insights
    """

    if not decision_results:
        return (
            '<p class="empty-message">'
            'No decision insights available.'
            '</p>'
        )

    summary = (
        decision_results.get(
            "summary",
            {}
        )
    )

    priorities = (
        decision_results.get(
            "priorities",
            {}
        )
    )

    high = []
    medium = []
    low = []
    info = []

    if isinstance(
        priorities,
        dict
    ):

        high = priorities.get(
            "high",
            []
        ) or []

        medium = priorities.get(
            "medium",
            []
        ) or []

        low = priorities.get(
            "low",
            []
        ) or []

        info = priorities.get(
            "info",
            []
        ) or []

    if not any(
        [
            high,
            medium,
            low,
            info
        ]
    ):

        all_insights = (
            decision_results.get(
                "all_insights",
                []
            )
            or []
        )

        for insight in all_insights:

            if not isinstance(
                insight,
                dict
            ):
                continue

            priority = str(
                insight.get(
                    "priority",
                    "info"
                )
            ).lower()

            if priority == "high":
                high.append(insight)

            elif priority == "medium":
                medium.append(insight)

            elif priority == "low":
                low.append(insight)

            else:
                info.append(insight)

    groups = "".join(
        [
            render_decision_group(
                "High Priority",
                high,
                "high"
            ),
            render_decision_group(
                "Medium Priority",
                medium,
                "medium"
            ),
            render_decision_group(
                "Low Priority",
                low,
                "low"
            ),
            render_decision_group(
                "Informational",
                info,
                "info"
            )
        ]
    )

    safety = (
        decision_results.get(
            "safety"
        )
    )

    safety_html = ""

    if isinstance(
        safety,
        dict
    ):

        description = safety.get(
            "description"
        )

        if description:

            safety_html = f"""
            <div class="decision-safety-note">

                <div class="safety-icon">
                    i
                </div>

                <div>
                    <strong>
                        Interpretation note
                    </strong>

                    <p>
                        {escape(str(description))}
                    </p>
                </div>

            </div>
            """

    return f"""
    <div class="decision-report">

        {render_decision_summary(summary)}

        {groups}

        {safety_html}

    </div>
    """


# ==========================================
# GENERATE HTML REPORT
# ==========================================

def generate_html_report(
    report_data,
    output_path=(
        "reports/generated/"
        "datalens_report.html"
    )
):
    """
    Generate the standalone premium
    DataLens AI HTML report.
    """

    print("\n================================")
    print("GENERATING HTML REPORT V4")
    print("================================")

    output_file = Path(
        output_path
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    metadata = report_data.get(
        "metadata",
        {}
    )

    dataset = report_data.get(
        "dataset_overview",
        {}
    )

    ml_results = report_data.get(
        "machine_learning",
        {}
    )

    business_results = report_data.get(
        "business_analytics",
        {}
    )

    decision_results = report_data.get(
        "decision_insights",
        {}
    )

    ai_results = report_data.get(
        "ai_analyst",
        {}
    )

    report_title = metadata.get(
        "report_title",
        "DataLens AI Analysis Report"
    )

    generated_at = metadata.get(
        "generated_at",
        "N/A"
    )

    report_version = metadata.get(
        "report_version",
        "4.0"
    )

    target_column = dataset.get(
        "target_column",
        "N/A"
    )

    problem_type = dataset.get(
        "problem_type",
        "N/A"
    )

    html_content = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<meta
    name="color-scheme"
    content="light"
>

<title>
    {escape(str(report_title))}
</title>

<style>

    /* ==========================================
       DESIGN TOKENS
       ========================================== */

    :root {{
        --canvas: #f7f9fc;
        --canvas-blue: #f2f7ff;
        --surface: #ffffff;
        --surface-soft: #f8fafc;

        --navy-950: #0b1425;
        --navy-900: #111d32;
        --navy-800: #172640;
        --navy-700: #223757;

        --blue-700: #2457a7;
        --blue-600: #2f67bd;
        --blue-500: #4b7fd0;
        --blue-100: #e9f1ff;
        --blue-50: #f5f8ff;

        --slate-900: #172033;
        --slate-700: #3d4b61;
        --slate-600: #5b687c;
        --slate-500: #7a8798;
        --slate-300: #cbd4df;
        --slate-200: #dde4ec;
        --slate-100: #edf1f5;

        --green-700: #157347;
        --green-100: #e9f8f0;

        --red-700: #b42318;
        --red-100: #fff0ee;

        --amber-700: #a15c00;
        --amber-100: #fff6df;

        --radius-xl: 26px;
        --radius-lg: 20px;
        --radius-md: 14px;
        --radius-sm: 10px;

        --shadow-lg:
            0 30px 80px rgba(31, 56, 92, 0.10);

        --shadow-md:
            0 14px 35px rgba(31, 56, 92, 0.07);

        --shadow-sm:
            0 5px 16px rgba(31, 56, 92, 0.05);
    }}


    /* ==========================================
       RESET / BASE
       ========================================== */

    * {{
        box-sizing: border-box;
    }}

    html {{
        scroll-behavior: smooth;
    }}

    body {{
        margin: 0;

        color: var(--slate-900);

        font-family:
            Inter,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            Arial,
            sans-serif;

        line-height: 1.6;

        background:
            radial-gradient(
                circle at 8% 0%,
                rgba(79, 134, 215, 0.12),
                transparent 24%
            ),
            radial-gradient(
                circle at 92% 6%,
                rgba(116, 163, 229, 0.10),
                transparent 22%
            ),
            linear-gradient(
                180deg,
                #fbfdff 0%,
                var(--canvas) 24%,
                #f8fafc 100%
            );

        -webkit-font-smoothing: antialiased;
    }}

    ::selection {{
        background: #d9e8ff;
        color: var(--navy-950);
    }}

    .container {{
        width: min(
            1280px,
            calc(100% - 48px)
        );

        margin: 0 auto;

        padding:
            30px 0 54px;
    }}


    /* ==========================================
       TOP NAV / BRAND
       ========================================== */

    .report-nav {{
        display: flex;

        align-items: center;
        justify-content: space-between;

        gap: 20px;

        margin-bottom: 18px;

        padding:
            11px 4px;
    }}

    .brand {{
        display: flex;
        align-items: center;
        gap: 11px;
    }}

    .brand-mark {{
        display: grid;
        place-items: center;

        width: 38px;
        height: 38px;

        border-radius: 10px;

        background:
            linear-gradient(
                145deg,
                var(--navy-950),
                #244979
            );

        color: white;

        font-size: 13px;
        font-weight: 800;
        letter-spacing: -0.5px;

        box-shadow:
            0 8px 20px
            rgba(20, 46, 83, 0.18);
    }}

    .brand-copy {{
        display: flex;
        flex-direction: column;
    }}

    .brand-name {{
        color: var(--navy-950);

        font-size: 15px;
        font-weight: 800;

        letter-spacing: -0.2px;
    }}

    .brand-subtitle {{
        margin-top: -2px;

        color: var(--slate-500);

        font-size: 10px;
        font-weight: 700;

        letter-spacing: 1.15px;
        text-transform: uppercase;
    }}

    .report-status {{
        display: flex;
        align-items: center;
        gap: 8px;

        color: var(--slate-600);

        font-size: 12px;
        font-weight: 600;
    }}

    .status-dot {{
        width: 7px;
        height: 7px;

        border-radius: 999px;

        background: #20a66a;

        box-shadow:
            0 0 0 4px
            rgba(32, 166, 106, 0.10);
    }}


    /* ==========================================
       PREMIUM REPORT HERO
       ========================================== */

    .report-header {{
        position: relative;

        overflow: hidden;

        min-height: 350px;

        padding:
            48px 50px 42px;

        margin-bottom: 18px;

        border:
            1px solid
            rgba(188, 205, 226, 0.75);

        border-radius:
            var(--radius-xl);

        background:
            linear-gradient(
                135deg,
                rgba(255, 255, 255, 0.98),
                rgba(248, 251, 255, 0.98)
            );

        box-shadow:
            var(--shadow-lg);
    }}

    .report-header::before {{
        content: "";

        position: absolute;

        width: 520px;
        height: 520px;

        top: -330px;
        right: -90px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(70, 127, 209, 0.22),
                rgba(70, 127, 209, 0.02) 58%,
                transparent 72%
            );

        pointer-events: none;
    }}

    .report-header::after {{
        content: "";

        position: absolute;

        width: 300px;
        height: 300px;

        left: -170px;
        bottom: -180px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(103, 154, 225, 0.14),
                transparent 70%
            );

        pointer-events: none;
    }}

    .hero-grid {{
        position: relative;
        z-index: 1;

        display: grid;

        grid-template-columns:
            minmax(0, 1.55fr)
            minmax(300px, 0.7fr);

        gap: 48px;

        align-items: end;
    }}

    .hero-main {{
        min-width: 0;
    }}

    .eyebrow {{
        display: inline-flex;
        align-items: center;
        gap: 9px;

        margin:
            0 0 20px;

        padding:
            7px 11px;

        border:
            1px solid #d9e5f5;

        border-radius: 999px;

        background:
            rgba(246, 250, 255, 0.85);

        color: var(--blue-700);

        font-size: 10px;
        font-weight: 800;

        letter-spacing: 1.25px;
        text-transform: uppercase;
    }}

    .eyebrow-dot {{
        width: 6px;
        height: 6px;

        border-radius: 50%;

        background: var(--blue-600);
    }}

    .report-header h1 {{
        max-width: 780px;

        margin: 0;

        color: var(--navy-950);

        font-size:
            clamp(
                36px,
                5vw,
                60px
            );

        line-height: 1.04;

        letter-spacing: -2.5px;
    }}

    .header-description {{
        max-width: 720px;

        margin:
            22px 0 0;

        color: var(--slate-600);

        font-size: 16px;
        line-height: 1.75;
    }}

    .hero-side {{
        padding:
            21px;

        border:
            1px solid
            rgba(204, 216, 231, 0.9);

        border-radius:
            18px;

        background:
            rgba(255, 255, 255, 0.72);

        box-shadow:
            var(--shadow-sm);
    }}

    .hero-side-label {{
        display: block;

        margin-bottom: 15px;

        color: var(--slate-500);

        font-size: 10px;
        font-weight: 800;

        letter-spacing: 1.2px;
        text-transform: uppercase;
    }}

    .hero-context-row {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;

        gap: 18px;

        padding:
            12px 0;

        border-bottom:
            1px solid var(--slate-100);
    }}

    .hero-context-row:last-child {{
        border-bottom: 0;
        padding-bottom: 0;
    }}

    .hero-context-row:first-of-type {{
        padding-top: 0;
    }}

    .context-label {{
        color: var(--slate-500);

        font-size: 12px;
    }}

    .context-value {{
        max-width: 190px;

        color: var(--navy-900);

        font-size: 12px;
        font-weight: 700;

        text-align: right;
        word-break: break-word;
    }}

    .header-meta {{
        position: relative;
        z-index: 1;

        display: flex;
        flex-wrap: wrap;

        gap: 8px;

        margin-top: 35px;
    }}

    .meta-pill {{
        display: inline-flex;
        align-items: center;

        padding:
            7px 11px;

        border:
            1px solid #dce6f1;

        border-radius: 999px;

        background:
            rgba(255, 255, 255, 0.76);

        color: var(--slate-600);

        font-size: 11px;
        font-weight: 650;
    }}


    /* ==========================================
       REPORT INTRO RAIL
       ========================================== */

    .report-rail {{
        display: grid;

        grid-template-columns:
            repeat(3, minmax(0, 1fr));

        margin-bottom: 18px;

        overflow: hidden;

        border:
            1px solid var(--slate-200);

        border-radius:
            16px;

        background: var(--surface);

        box-shadow:
            var(--shadow-sm);
    }}

    .rail-item {{
        padding:
            18px 20px;

        border-right:
            1px solid var(--slate-100);
    }}

    .rail-item:last-child {{
        border-right: 0;
    }}

    .rail-label {{
        display: block;

        margin-bottom: 4px;

        color: var(--navy-900);

        font-size: 12px;
        font-weight: 750;
    }}

    .rail-copy {{
        color: var(--slate-500);

        font-size: 11px;
    }}


    /* ==========================================
       METRIC CARDS
       ========================================== */

    .metric-grid {{
        display: grid;

        grid-template-columns:
            repeat(
                4,
                minmax(0, 1fr)
            );

        gap: 12px;

        margin-bottom: 18px;
    }}

    .metric-card {{
        position: relative;

        overflow: hidden;

        min-height: 156px;

        padding:
            19px;

        border:
            1px solid var(--slate-200);

        border-radius:
            16px;

        background:
            linear-gradient(
                155deg,
                #ffffff,
                #fbfdff
            );

        box-shadow:
            var(--shadow-sm);
    }}

    .metric-card::after {{
        content: "";

        position: absolute;

        width: 100px;
        height: 100px;

        top: -58px;
        right: -50px;

        border-radius: 50%;

        background:
            rgba(70, 126, 207, 0.07);
    }}

    .metric-card-top {{
        display: flex;
        align-items: center;
        justify-content: space-between;

        margin-bottom: 20px;
    }}

    .metric-index {{
        color: var(--slate-500);

        font-size: 9px;
        font-weight: 800;

        letter-spacing: 1px;
    }}

    .metric-status-dot {{
        width: 6px;
        height: 6px;

        border-radius: 50%;

        background: var(--blue-500);
    }}

    .metric-value {{
        display: block;

        margin-bottom: 4px;

        color: var(--navy-950);

        font-size: 29px;
        font-weight: 780;

        line-height: 1.1;

        letter-spacing: -1px;
    }}

    .metric-label {{
        display: block;

        color: var(--slate-700);

        font-size: 12px;
        font-weight: 700;
    }}

    .metric-description {{
        display: block;

        margin-top: 4px;

        color: var(--slate-500);

        font-size: 10px;
    }}


    /* ==========================================
       SECTION
       ========================================== */

    .section {{
        position: relative;

        margin-bottom: 18px;

        padding:
            34px 36px 38px;

        border:
            1px solid var(--slate-200);

        border-radius:
            var(--radius-lg);

        background:
            rgba(255, 255, 255, 0.98);

        box-shadow:
            var(--shadow-md);
    }}

    .section-header {{
        display: flex;
        align-items: flex-start;

        gap: 18px;

        margin-bottom: 30px;

        padding-bottom: 22px;

        border-bottom:
            1px solid var(--slate-100);
    }}

    .section-number {{
        display: grid;
        place-items: center;

        flex: 0 0 auto;

        width: 38px;
        height: 38px;

        border:
            1px solid #d5e2f2;

        border-radius: 11px;

        background: var(--blue-50);

        color: var(--blue-700);

        font-size: 10px;
        font-weight: 850;

        letter-spacing: 0.7px;
    }}

    .section-heading-copy {{
        min-width: 0;
    }}

    .section-kicker {{
        display: block;

        margin-bottom: 3px;

        color: var(--blue-700);

        font-size: 9px;
        font-weight: 800;

        letter-spacing: 1.2px;
        text-transform: uppercase;
    }}

    .section-title {{
        margin: 0;

        color: var(--navy-950);

        font-size: 24px;
        font-weight: 780;

        line-height: 1.25;

        letter-spacing: -0.7px;
    }}

    .section-description {{
        max-width: 760px;

        margin:
            7px 0 0;

        color: var(--slate-500);

        font-size: 12px;
        line-height: 1.65;
    }}

    .subheading {{
        position: relative;

        margin:
            31px 0 13px;

        color: var(--navy-900);

        line-height: 1.3;

        letter-spacing: -0.25px;
    }}

    h3.subheading {{
        font-size: 18px;
    }}

    h4.subheading {{
        font-size: 16px;
    }}

    h5.subheading,
    h6.subheading {{
        font-size: 14px;
    }}


    /* ==========================================
       TABLES
       ========================================== */

    .table-wrapper {{
        width: 100%;

        overflow-x: auto;

        margin:
            12px 0 24px;

        border:
            1px solid var(--slate-200);

        border-radius:
            13px;

        background: var(--surface);
    }}

    table {{
        width: 100%;

        border-collapse: collapse;

        background: white;

        font-size: 12px;
    }}

    th {{
        padding:
            12px 14px;

        border-bottom:
            1px solid var(--slate-200);

        background:
            linear-gradient(
                180deg,
                #f8fafc,
                #f4f7fa
            );

        color: var(--slate-600);

        font-size: 10px;
        font-weight: 800;

        letter-spacing: 0.45px;

        text-align: left;
        text-transform: uppercase;

        white-space: nowrap;
    }}

    td {{
        padding:
            12px 14px;

        border-bottom:
            1px solid var(--slate-100);

        color: var(--slate-700);

        vertical-align: top;
    }}

    tbody tr:last-child td {{
        border-bottom: none;
    }}

    tbody tr:nth-child(even) {{
        background: #fbfcfe;
    }}

    tbody tr {{
        transition:
            background 0.16s ease;
    }}

    tbody tr:hover {{
        background: #f5f8fc;
    }}

    .summary-table .label-cell {{
        width: 34%;

        background: #fafbfd;

        color: var(--slate-600);

        font-size: 11px;
        font-weight: 700;
    }}

    .summary-table td:last-child {{
        color: var(--navy-900);

        font-weight: 550;
    }}


    /* ==========================================
       LISTS
       ========================================== */

    .report-list,
    .ai-list {{
        margin:
            12px 0 22px;

        padding-left: 21px;
    }}

    .report-list li,
    .ai-list li {{
        margin-bottom: 8px;

        padding-left: 3px;

        color: var(--slate-700);
    }}

    .report-list li::marker,
    .ai-list li::marker {{
        color: var(--blue-600);
    }}


    /* ==========================================
       DECISION INSIGHTS
       ========================================== */

    .decision-report {{
        padding-top: 1px;
    }}

    .decision-summary-grid {{
        display: grid;

        grid-template-columns:
            repeat(
                5,
                minmax(0, 1fr)
            );

        gap: 10px;

        margin-bottom: 34px;
    }}

    .decision-summary-card {{
        position: relative;

        overflow: hidden;

        padding:
            15px 16px;

        border:
            1px solid var(--slate-200);

        border-radius:
            12px;

        background: var(--surface-soft);
    }}

    .decision-summary-card::before {{
        content: "";

        position: absolute;

        left: 0;
        top: 0;
        bottom: 0;

        width: 3px;

        background: var(--slate-300);
    }}

    .decision-summary-label {{
        display: block;

        margin-bottom: 6px;

        color: var(--slate-500);

        font-size: 9px;
        font-weight: 800;

        letter-spacing: 0.45px;
        text-transform: uppercase;
    }}

    .decision-summary-value {{
        display: block;

        color: var(--navy-950);

        font-size: 22px;
        line-height: 1.2;
    }}

    .decision-summary-card.high::before {{
        background: #d92d20;
    }}

    .decision-summary-card.medium::before {{
        background: #d98a12;
    }}

    .decision-summary-card.low::before {{
        background: var(--blue-600);
    }}

    .decision-summary-card.info::before {{
        background: #8995a5;
    }}

    .decision-group {{
        margin-top: 30px;
    }}

    .decision-group-header {{
        display: flex;
        align-items: center;

        gap: 9px;

        margin-bottom: 12px;
    }}

    .decision-group-dot {{
        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: var(--slate-400, #9aa6b5);
    }}

    .decision-group.high
    .decision-group-dot {{
        background: #d92d20;
    }}

    .decision-group.medium
    .decision-group-dot {{
        background: #d98a12;
    }}

    .decision-group.low
    .decision-group-dot {{
        background: var(--blue-600);
    }}

    .decision-group-title {{
        margin: 0;

        color: var(--navy-900);

        font-size: 15px;
        font-weight: 750;
    }}

    .decision-group-count {{
        display: grid;
        place-items: center;

        min-width: 22px;
        height: 22px;

        padding:
            0 6px;

        border:
            1px solid var(--slate-200);

        border-radius: 999px;

        background: var(--surface-soft);

        color: var(--slate-500);

        font-size: 9px;
        font-weight: 800;
    }}

    .decision-card-list {{
        display: grid;
        gap: 10px;
    }}

    .decision-card {{
        position: relative;

        padding:
            20px 20px 18px;

        border:
            1px solid var(--slate-200);

        border-left:
            3px solid #9aa6b5;

        border-radius:
            13px;

        background:
            linear-gradient(
                145deg,
                #ffffff,
                #fcfdff
            );
    }}

    .decision-card.high {{
        border-left-color: #d92d20;
    }}

    .decision-card.medium {{
        border-left-color: #d98a12;
    }}

    .decision-card.low {{
        border-left-color: var(--blue-600);
    }}

    .decision-card.info {{
        border-left-color: #8b97a7;
    }}

    .decision-card-header {{
        display: flex;

        justify-content: space-between;
        align-items: flex-start;

        gap: 16px;
    }}

    .decision-category {{
        display: inline-block;

        margin-bottom: 5px;

        color: var(--slate-500);

        font-size: 9px;
        font-weight: 800;

        letter-spacing: 0.75px;
        text-transform: uppercase;
    }}

    .decision-card-title {{
        margin: 0;

        color: var(--navy-950);

        font-size: 15px;
        font-weight: 750;

        letter-spacing: -0.25px;
    }}

    .priority-badge {{
        flex: 0 0 auto;

        padding:
            5px 9px;

        border-radius: 999px;

        background: var(--slate-100);

        color: var(--slate-700);

        font-size: 9px;
        font-weight: 800;

        letter-spacing: 0.4px;
        text-transform: uppercase;
    }}

    .priority-badge.high {{
        background: var(--red-100);
        color: var(--red-700);
    }}

    .priority-badge.medium {{
        background: var(--amber-100);
        color: var(--amber-700);
    }}

    .priority-badge.low {{
        background: var(--blue-100);
        color: var(--blue-700);
    }}

    .priority-badge.info {{
        background: var(--slate-100);
        color: var(--slate-600);
    }}

    .decision-observation {{
        margin:
            13px 0 0;

        color: var(--slate-700);

        font-size: 12px;
        line-height: 1.7;
    }}

    .decision-detail {{
        margin-top: 15px;

        padding:
            13px 14px;

        border:
            1px solid var(--slate-100);

        border-radius:
            10px;

        background: #fafbfd;
    }}

    .decision-detail-label {{
        margin-bottom: 7px;

        color: var(--slate-500);

        font-size: 9px;
        font-weight: 800;

        letter-spacing: 0.8px;
        text-transform: uppercase;
    }}

    .decision-detail
    .table-wrapper {{
        margin-bottom: 0;
    }}

    .decision-recommendation {{
        display: flex;

        gap: 11px;

        margin-top: 14px;

        padding:
            12px 13px;

        border:
            1px solid #dfe9f6;

        border-radius:
            10px;

        background: var(--blue-50);

        color: var(--slate-700);

        font-size: 11px;
    }}

    .decision-recommendation p {{
        margin:
            2px 0 0;
    }}

    .decision-recommendation strong {{
        color: var(--navy-900);
    }}

    .recommendation-icon {{
        display: grid;
        place-items: center;

        flex: 0 0 auto;

        width: 23px;
        height: 23px;

        border-radius: 7px;

        background: white;

        color: var(--blue-700);

        font-weight: 800;
    }}

    .decision-safety-note {{
        display: flex;

        gap: 12px;

        margin-top: 30px;

        padding:
            14px 16px;

        border:
            1px solid var(--slate-200);

        border-radius:
            12px;

        background: #fafbfd;

        color: var(--slate-600);

        font-size: 11px;
    }}

    .decision-safety-note p {{
        margin:
            3px 0 0;
    }}

    .decision-safety-note strong {{
        color: var(--navy-900);
    }}

    .safety-icon {{
        display: grid;
        place-items: center;

        flex: 0 0 auto;

        width: 24px;
        height: 24px;

        border:
            1px solid var(--slate-200);

        border-radius: 50%;

        background: white;

        color: var(--blue-700);

        font-size: 11px;
        font-weight: 800;
    }}


    /* ==========================================
       AI ANALYST PREMIUM SECTION
       ========================================== */

    .ai-section {{
        overflow: hidden;

        border-color:
            rgba(167, 190, 221, 0.85);

        background:
            linear-gradient(
                145deg,
                #ffffff 0%,
                #fbfdff 52%,
                #f6f9ff 100%
            );
    }}

    .ai-section::after {{
        content: "";

        position: absolute;

        width: 280px;
        height: 280px;

        top: -180px;
        right: -130px;

        border-radius: 50%;

        background:
            rgba(69, 123, 199, 0.08);

        pointer-events: none;
    }}

    .ai-report {{
        position: relative;
        z-index: 1;

        padding:
            2px 2px 0;
    }}

    .ai-heading {{
        margin:
            29px 0 12px;

        color: var(--navy-950);

        line-height: 1.3;

        letter-spacing: -0.25px;
    }}

    .ai-report
    > .ai-heading:first-child {{
        margin-top: 0;
    }}

    .ai-paragraph {{
        margin:
            0 0 15px;

        color: var(--slate-700);

        font-size: 12px;
        line-height: 1.75;
    }}

    .ai-divider {{
        margin:
            27px 0;

        border: 0;

        border-top:
            1px solid var(--slate-200);
    }}

    code {{
        padding:
            2px 5px;

        border:
            1px solid #e1e7ef;

        border-radius:
            5px;

        background: #f3f6fa;

        color: var(--navy-800);

        font-family:
            Consolas,
            "SFMono-Regular",
            monospace;

        font-size: 0.92em;
    }}

    strong {{
        font-weight: 750;
    }}

    .empty-message {{
        margin:
            10px 0;

        padding:
            14px;

        border:
            1px dashed var(--slate-300);

        border-radius:
            10px;

        background: var(--surface-soft);

        color: var(--slate-500);

        font-size: 11px;
        font-style: italic;
    }}


    /* ==========================================
       FOOTER
       ========================================== */

    .footer {{
        display: flex;

        justify-content: space-between;
        align-items: center;

        gap: 20px;

        padding:
            23px 5px 5px;

        color: var(--slate-500);

        font-size: 10px;
    }}

    .footer-brand {{
        display: flex;
        align-items: center;

        gap: 8px;

        color: var(--navy-900);

        font-weight: 750;
    }}

    .footer-mark {{
        display: grid;
        place-items: center;

        width: 25px;
        height: 25px;

        border-radius: 7px;

        background: var(--navy-900);

        color: white;

        font-size: 8px;
        font-weight: 800;
    }}

    .footer-meta {{
        text-align: right;
    }}


    /* ==========================================
       RESPONSIVE
       ========================================== */

    @media (
        max-width: 1050px
    ) {{

        .hero-grid {{
            grid-template-columns:
                1fr;
        }}

        .hero-side {{
            max-width: 650px;
        }}

        .decision-summary-grid {{
            grid-template-columns:
                repeat(
                    3,
                    minmax(0, 1fr)
                );
        }}

    }}


    @media (
        max-width: 860px
    ) {{

        .container {{
            width:
                calc(100% - 30px);
        }}

        .report-header {{
            min-height: auto;

            padding:
                38px 32px;
        }}

        .report-header h1 {{
            letter-spacing: -1.7px;
        }}

        .metric-grid {{
            grid-template-columns:
                repeat(
                    2,
                    minmax(0, 1fr)
                );
        }}

        .report-rail {{
            grid-template-columns:
                1fr;
        }}

        .rail-item {{
            border-right: 0;

            border-bottom:
                1px solid var(--slate-100);
        }}

        .rail-item:last-child {{
            border-bottom: 0;
        }}

        .section {{
            padding:
                28px 25px 30px;
        }}

    }}


    @media (
        max-width: 620px
    ) {{

        .report-nav {{
            align-items: flex-start;
        }}

        .report-status {{
            display: none;
        }}

        .decision-summary-grid {{
            grid-template-columns:
                repeat(
                    2,
                    minmax(0, 1fr)
                );
        }}

        .decision-card-header {{
            flex-direction: column;
        }}

        .footer {{
            flex-direction: column;
            align-items: flex-start;
        }}

        .footer-meta {{
            text-align: left;
        }}

    }}


    @media (
        max-width: 520px
    ) {{

        .container {{
            width:
                calc(100% - 20px);

            padding-top: 13px;
        }}

        .report-header {{
            padding:
                28px 22px;

            border-radius:
                18px;
        }}

        .report-header h1 {{
            font-size: 34px;

            letter-spacing: -1.5px;
        }}

        .header-description {{
            font-size: 14px;
        }}

        .hero-side {{
            padding: 16px;
        }}

        .metric-grid,
        .decision-summary-grid {{
            grid-template-columns:
                1fr;
        }}

        .metric-card {{
            min-height: 140px;
        }}

        .section {{
            padding:
                22px 18px 24px;

            border-radius:
                15px;
        }}

        .section-header {{
            gap: 12px;
        }}

        .section-number {{
            width: 34px;
            height: 34px;
        }}

        .section-title {{
            font-size: 20px;
        }}

        th,
        td {{
            padding:
                10px 11px;
        }}

    }}


    /* ==========================================
       PRINT / PDF
       ========================================== */

    @media print {{

        @page {{
            margin:
                14mm;
        }}

        body {{
            background: white;

            color: #111827;

            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}

        .container {{
            width: 100%;
            max-width: none;

            padding: 0;
        }}

        .report-nav {{
            margin-bottom: 12px;
        }}

        .report-header {{
            min-height: auto;

            padding:
                30px;

            border-radius: 12px;

            box-shadow: none;
        }}

        .report-header h1 {{
            font-size: 34px;
        }}

        .hero-grid {{
            grid-template-columns:
                1.45fr 0.7fr;

            gap: 25px;
        }}

        .metric-grid {{
            grid-template-columns:
                repeat(4, 1fr);

            gap: 7px;
        }}

        .metric-card {{
            min-height: 115px;

            padding: 13px;

            box-shadow: none;
        }}

        .metric-card-top {{
            margin-bottom: 12px;
        }}

        .metric-value {{
            font-size: 22px;
        }}

        .report-rail,
        .section,
        .decision-card {{
            box-shadow: none;
        }}

        .section {{
            padding:
                22px;

            break-inside: auto;
        }}

        .metric-card,
        .decision-card,
        .decision-summary-card,
        table {{
            break-inside: avoid;
        }}

        .decision-card {{
            page-break-inside: avoid;
        }}

        tbody tr:hover {{
            background: inherit;
        }}

        .section-header {{
            margin-bottom: 20px;
        }}

        .footer {{
            padding-top: 15px;
        }}

    }}

</style>

</head>


<body>

<div class="container">


    <!-- ==========================================
         REPORT BRAND NAV
         ========================================== -->

    <nav class="report-nav">

        <div class="brand">

            <div class="brand-mark">
                DL
            </div>

            <div class="brand-copy">

                <span class="brand-name">
                    DataLens AI
                </span>

                <span class="brand-subtitle">
                    Intelligence Workspace
                </span>

            </div>

        </div>


        <div class="report-status">

            <span class="status-dot"></span>

            Analysis report generated

        </div>

    </nav>


    <!-- ==========================================
         PREMIUM REPORT HEADER
         ========================================== -->

    <header class="report-header">

        <div class="hero-grid">


            <div class="hero-main">

                <p class="eyebrow">

                    <span class="eyebrow-dot"></span>

                    Intelligent Analytics Report

                </p>


                <h1>
                    {escape(str(report_title))}
                </h1>


                <p class="header-description">

                    A consolidated analytical view of
                    dataset quality, model evidence,
                    business intelligence, deterministic
                    decision insights and AI-assisted
                    interpretation.

                </p>

            </div>


            <aside class="hero-side">

                <span class="hero-side-label">
                    Analysis Context
                </span>


                <div class="hero-context-row">

                    <span class="context-label">
                        Target variable
                    </span>

                    <span class="context-value">
                        {escape(str(target_column))}
                    </span>

                </div>


                <div class="hero-context-row">

                    <span class="context-label">
                        Problem type
                    </span>

                    <span class="context-value">
                        {escape(str(problem_type))}
                    </span>

                </div>


                <div class="hero-context-row">

                    <span class="context-label">
                        Report version
                    </span>

                    <span class="context-value">
                        {escape(str(report_version))}
                    </span>

                </div>


                <div class="hero-context-row">

                    <span class="context-label">
                        Generated
                    </span>

                    <span class="context-value">
                        {escape(str(generated_at))}
                    </span>

                </div>

            </aside>

        </div>


        <div class="header-meta">

            <span class="meta-pill">
                Automated profiling
            </span>

            <span class="meta-pill">
                Machine learning
            </span>

            <span class="meta-pill">
                Explainability
            </span>

            <span class="meta-pill">
                Business intelligence
            </span>

            <span class="meta-pill">
                Decision evidence
            </span>

        </div>

    </header>


    <!-- ==========================================
         REPORT PRINCIPLES
         ========================================== -->

    <div class="report-rail">

        <div class="rail-item">

            <span class="rail-label">
                Evidence first
            </span>

            <span class="rail-copy">
                Analytical metrics are computed by
                the DataLens pipeline.
            </span>

        </div>


        <div class="rail-item">

            <span class="rail-label">
                Explainable analysis
            </span>

            <span class="rail-copy">
                Model evidence is surfaced before
                business interpretation.
            </span>

        </div>


        <div class="rail-item">

            <span class="rail-label">
                Decision ready
            </span>

            <span class="rail-copy">
                Deterministic insights precede
                AI-assisted explanation.
            </span>

        </div>

    </div>


    <!-- ==========================================
         EXECUTIVE DATASET METRICS
         ========================================== -->

    {
        render_dataset_cards(
            dataset
        )
    }


    <!-- ==========================================
         01 DATASET OVERVIEW
         ========================================== -->

    <section class="section">

        <div class="section-header">

            <div class="section-number">
                01
            </div>

            <div class="section-heading-copy">

                <span class="section-kicker">
                    Data Foundation
                </span>

                <h2 class="section-title">
                    Dataset Overview
                </h2>

                <p class="section-description">
                    Structural profile of the source
                    dataset, target configuration and
                    data-quality characteristics used
                    throughout this analysis.
                </p>

            </div>

        </div>

        {
            render_section(
                dataset
            )
        }

    </section>


    <!-- ==========================================
         02 MACHINE LEARNING
         ========================================== -->

    <section class="section">

        <div class="section-header">

            <div class="section-number">
                02
            </div>

            <div class="section-heading-copy">

                <span class="section-kicker">
                    Model Evidence
                </span>

                <h2 class="section-title">
                    Machine Learning Analysis
                </h2>

                <p class="section-description">
                    Model evaluation, comparison,
                    validation, diagnostics and
                    explainability evidence produced
                    by the analytical pipeline.
                </p>

            </div>

        </div>

        {
            render_section(
                ml_results
            )
        }

    </section>


    <!-- ==========================================
         03 BUSINESS ANALYTICS
         ========================================== -->

    <section class="section">

        <div class="section-header">

            <div class="section-number">
                03
            </div>

            <div class="section-heading-copy">

                <span class="section-kicker">
                    Business Intelligence
                </span>

                <h2 class="section-title">
                    Business Analytics
                </h2>

                <p class="section-description">
                    Evidence-backed KPIs, segment
                    observations and factual findings
                    derived directly from the dataset.
                </p>

            </div>

        </div>

        {
            render_section(
                business_results
            )
        }

    </section>


    <!-- ==========================================
         04 DECISION INSIGHTS
         ========================================== -->

    <section class="section">

        <div class="section-header">

            <div class="section-number">
                04
            </div>

            <div class="section-heading-copy">

                <span class="section-kicker">
                    Decision Intelligence
                </span>

                <h2 class="section-title">
                    Decision Insights
                </h2>

                <p class="section-description">
                    Structured, deterministic
                    observations prioritized from
                    analytical evidence before
                    AI interpretation.
                </p>

            </div>

        </div>

        {
            render_decision_insights(
                decision_results
            )
        }

    </section>


    <!-- ==========================================
         05 AI ANALYST
         ========================================== -->

    <section class="section ai-section">

        <div class="section-header">

            <div class="section-number">
                05
            </div>

            <div class="section-heading-copy">

                <span class="section-kicker">
                    AI-Assisted Interpretation
                </span>

                <h2 class="section-title">
                    AI Analyst Briefing
                </h2>

                <p class="section-description">
                    A contextual interpretation of
                    validated analytical evidence,
                    designed to make the findings
                    easier to understand and act on.
                </p>

            </div>

        </div>

        {
            render_ai_analysis(
                ai_results
            )
        }

    </section>


    <!-- ==========================================
         FOOTER
         ========================================== -->

    <footer class="footer">

        <div class="footer-brand">

            <span class="footer-mark">
                DL
            </span>

            DataLens AI

        </div>


        <div class="footer-meta">

            Generated by DataLens AI
            &nbsp;·&nbsp;
            Report Version
            {escape(str(report_version))}

        </div>

    </footer>


</div>

</body>

</html>
"""

    output_file.write_text(
        html_content,
        encoding="utf-8"
    )

    print(
        "✓ Premium HTML report generated."
    )

    print(
        "✓ Dataset overview rendered."
    )

    print(
        "✓ Machine Learning analysis rendered."
    )

    print(
        "✓ Business Analytics rendered."
    )

    print(
        "✓ Decision Insights section rendered."
    )

    print(
        "✓ AI Analyst Markdown rendered."
    )

    print(
        "✓ Premium responsive layout applied."
    )

    print(
        "✓ Print-friendly styling applied."
    )

    print(
        f"✓ Report saved to: {output_file}"
    )

    return str(
        output_file
    )