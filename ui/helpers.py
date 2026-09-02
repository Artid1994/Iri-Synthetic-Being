MEMORY_TYPE_COLORS = {
    "EPISODIC": "#3b82f6",
    "SEMANTIC": "#22d3ee",
    "WORKING": "#fbbf24",
    "EXPERIENCE": "#a78bfa",
}


def format_uptime(seconds):
    if seconds is None:
        return "—"

    try:
        seconds = int(seconds)
    except (TypeError, ValueError):
        return "—"

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def format_memory_content(content, maximum=24):
    content = str(content).replace("\n", " ").strip()

    if len(content) <= maximum:
        return content

    return content[: maximum - 1] + "…"


def memory_type_color(memory_type):
    return MEMORY_TYPE_COLORS.get(
        str(memory_type).upper(),
        "#a78bfa",
    )
