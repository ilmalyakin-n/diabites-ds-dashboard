import plotly.express as px
import plotly.graph_objects as go


BLUE = "#2563EB"
GREEN = "#22C55E"
TEAL = "#14B8A6"
SKY = "#38BDF8"
AMBER = "#F59E0B"
RED = "#EF4444"
PANEL = "#111827"
TEXT = "#F5F5F5"
SECONDARY = "#D1D5DB"

COLOR_SEQUENCE = [BLUE, GREEN, TEAL, SKY, AMBER, RED]
RECOMMENDATION_COLORS = {
    "Recommended": GREEN,
    "Caution": AMBER,
    "Not Recommended": RED,
}


def apply_theme(fig: go.Figure, height: int = 380) -> go.Figure:
    """Apply the shared dark Plotly theme with high-contrast labels and axes."""
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font={"family": "Inter, Segoe UI, sans-serif", "color": TEXT, "size": 14},
        title={"font": {"color": "#FFFFFF", "size": 18}, "x": 0.01, "xanchor": "left"},
        margin={"l": 44, "r": 28, "t": 64, "b": 44},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
            "font": {"color": SECONDARY, "size": 13},
        },
        hoverlabel={"bgcolor": "#F9FAFB", "font_color": "#111827", "font_size": 13},
    )
    fig.update_xaxes(
        title_font={"color": SECONDARY, "size": 13},
        tickfont={"color": SECONDARY, "size": 13},
        gridcolor="rgba(209, 213, 219, 0.10)",
        zeroline=False,
    )
    fig.update_yaxes(
        title_font={"color": SECONDARY, "size": 13},
        tickfont={"color": SECONDARY, "size": 13},
        gridcolor="rgba(209, 213, 219, 0.10)",
        zeroline=False,
    )
    return fig


def bar_chart(df, x, y, title, color=None, height=380, color_map=None, orientation="v", text=None):
    """Create a themed bar chart for categorical summaries."""
    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        color=color,
        orientation=orientation,
        color_discrete_map=color_map,
        color_discrete_sequence=COLOR_SEQUENCE,
        text=text,
    )
    fig.update_traces(marker_line_width=0, textposition="outside", cliponaxis=False)
    return apply_theme(fig, height)


def pie_chart(df, names, values, title, height=380):
    """Create a themed pie chart for category distribution."""
    fig = px.pie(
        df,
        names=names,
        values=values,
        title=title,
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return apply_theme(fig, height)


def histogram_chart(df, x, title, color=None, nbins=32, height=360):
    """Create a themed histogram for numeric nutrition distributions."""
    fig = px.histogram(
        df,
        x=x,
        title=title,
        color=color,
        nbins=nbins,
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    return apply_theme(fig, height)


def scatter_chart(df, x, y, title, color=None, size=None, height=420, color_map=None, hover_name=None, hover_data=None):
    """Create a themed scatter plot for comparing two nutrition dimensions."""
    fig = px.scatter(
        df,
        x=x,
        y=y,
        title=title,
        color=color,
        size=size,
        hover_name=hover_name,
        hover_data=hover_data,
        color_discrete_map=color_map,
        color_discrete_sequence=COLOR_SEQUENCE,
        opacity=0.82,
    )
    fig.update_traces(marker={"line": {"width": 0.6, "color": "#F9FAFB"}})
    return apply_theme(fig, height)


def box_chart(df, x, y, title, color=None, height=400):
    """Create a themed box plot for spread and outlier analysis."""
    fig = px.box(
        df,
        x=x,
        y=y,
        title=title,
        color=color,
        color_discrete_sequence=COLOR_SEQUENCE,
        points="outliers",
    )
    return apply_theme(fig, height)


def nutrition_comparison_bar(df, title, height=390):
    """Create a bar chart comparing nutrition values for one selected product."""
    fig = px.bar(
        df,
        x="nutrient",
        y="value",
        title=title,
        color="nutrient",
        color_discrete_sequence=COLOR_SEQUENCE,
        text="value",
    )
    fig.update_traces(marker_line_width=0, texttemplate="%{text:.1f}", textposition="outside")
    return apply_theme(fig, height)


def heatmap_chart(df, x, y, z, title, height=420):
    """Create a themed heatmap for profile sensitivity matrices."""
    fig = px.imshow(
        df.pivot(index=y, columns=x, values=z).fillna(0),
        title=title,
        text_auto=".1f",
        color_continuous_scale=[RED, AMBER, GREEN],
        aspect="auto",
    )
    fig.update_coloraxes(colorbar={"tickfont": {"color": SECONDARY}, "title": {"font": {"color": SECONDARY}}})
    return apply_theme(fig, height)


def heatmap_from_crosstab(df, title, height=420):
    """Create a themed heatmap from a pre-pivoted (crosstab) DataFrame."""
    fig = px.imshow(
        df,
        title=title,
        text_auto=True,
        color_continuous_scale=[[0, "#1E293B"], [0.5, "#3B82F6"], [1, "#93C5FD"]],
        aspect="auto",
    )
    fig.update_coloraxes(
        colorbar={"tickfont": {"color": SECONDARY}, "title": {"font": {"color": SECONDARY}}}
    )
    return apply_theme(fig, height)
