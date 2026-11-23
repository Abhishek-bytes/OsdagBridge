"""Central visual theme for generated OsdagBridge design reports.

The module is organized into page/document settings, table and status styling,
header/footer styling, chart defaults, and named LaTeX dimension aliases.
Chapter fragments refer to the aliases defined here rather than owning style
values.  ``build_latex_preamble`` emits the shared LaTeX theme for a report.
"""

import re
from typing import Dict, Tuple


# Page geometry and typography.
PAPER_SIZE = "a4paper"
BASE_FONT_SIZE_PT = 12
PAGE_MARGIN = "1in"
PAGE_HEADHEIGHT = "14pt"
PAGE_HEADSEP = "0.25in"
PAGE_FOOTSKIP = "30pt"
LINE_SPACING = 1.15

# Brand, status, and chart palette.
COLOR_ACCENT = "91B014"
COLOR_PASS = "2E7D32"
COLOR_FAIL = "C62828"
COLOR_WARNING = "1565C0"
COLOR_NEUTRAL = "000000"
CHART_COLOR_PASS = f"#{COLOR_PASS}"
CHART_COLOR_FAIL = f"#{COLOR_FAIL}"
CHART_COLOR_THRESHOLD = f"#{COLOR_FAIL}"
CHART_COLOR_GRID = "#D9DEE5"

# Table theme.
TABLE_CELL_PADDING_PT = 6
TABLE_ARRAY_STRETCH = 1.12
TABLE_RULE_WIDTH_PT = 0.5
TABLE_EXTRA_ROW_HEIGHT_PT = 0.6
LONGTABLE_PRE_SKIP_PT = 0
LONGTABLE_POST_SKIP_PT = 6
TABLE_ROW_BREAK_PT = 6
TABLE_TALL_ROW_BREAK_PT = 8
TABLE_COMPACT_CELL_PADDING_PT = 3
TABLE_DENSE_CELL_PADDING_PT = 4
TABLE_WIDE_CELL_PADDING_PT = 3.5
TABLE_DENSE_ARRAY_STRETCH = 1.25
TABLE_CAPTION_SKIP_PT = 2
TABLE_MIN_REMAINDER_LINES = 5

# Figure/chart defaults.
FIGURE_WIDTH = r"\textwidth"
FIGURE_WIDTH_LARGE = r"\ReportFigureWidthLarge"
FIGURE_WIDTH_MEDIUM = r"\ReportFigureWidth"
FIGURE_WIDTH_DRAWING = r"\ReportFigureWidthDrawing"
FIGURE_PLACEHOLDER_WIDTH = r"\ReportPlaceholderWidth"
FIGURE_CELL_PLACEHOLDER_WIDTH = r"\ReportCellPlaceholderWidth"
FIGURE_CELL_WIDTH = r"\ReportFigureCellWidth"
_FIGURE_WIDTH_MEDIUM_VALUE = r"0.75\textwidth"
_FIGURE_WIDTH_DRAWING_VALUE = r"0.85\textwidth"
_FIGURE_WIDTH_LARGE_VALUE = r"0.9\textwidth"
_FIGURE_PLACEHOLDER_WIDTH_VALUE = r"0.97\textwidth"
_FIGURE_CELL_PLACEHOLDER_WIDTH_VALUE = r"0.95\linewidth"
_FIGURE_CELL_WIDTH_VALUE = r"0.31\textwidth"
CHART_FIGSIZE: Tuple[float, float] = (9.0, 5.0)
CHART_DPI = 200
CHART_FONT_FAMILY = "DejaVu Sans"
CHART_TITLE_SIZE = 13
CHART_LABEL_SIZE = 10
CHART_TICK_SIZE = 9
CHART_VALUE_SIZE = 9
CHART_THRESHOLD_VALUE = 1.0
CHART_THRESHOLD_LINESTYLE = "--"
CHART_THRESHOLD_LINEWIDTH = 1.8
CHART_GRID_ALPHA = 0.55

# Executive-summary table sizing, retained as data-driven layout settings.
SUMMARY_LABEL_COLUMN_CM = 2.8
SUMMARY_AVAILABLE_WIDTH_CM = 15.0
SUMMARY_MIN_COMPONENT_COLUMN_CM = 1.5
SUMMARY_COMPONENT_COLUMN_PRECISION = 1
TITLE_LOGO_WIDTH_RATIO = 0.6
ORGANIZATION_LOGO_WIDTH_RATIO = 0.35

# Shared dimensions used in LaTeX table specs, title/TOC spacing and figure
# placeholders. The aliases are emitted once in the document preamble.
LATEX_DIMENSIONS = (
    "0.3cm", "0.3em", "0.4cm", "0.4em", "0.5cm", "0.5em", "0.5pt",
    "0.6em", "0.6pt", "0.8cm", "0.8em", "0pt", "1.0cm", "1.2cm",
    "1.3cm", "1.4cm", "1.5cm", "1.5em", "1.6cm", "1.7cm", "1.8cm",
    "10.0cm", "10cm", "10pt", "11.5cm", "12pt", "13cm", "15.0cm",
    "1cm", "1em", "1in", "1pt", "2.0cm", "2.1cm", "2.2cm", "2.2em",
    "2.3cm", "2.3em", "2.4cm", "2.5cm", "2.6cm", "2.8cm", "20pt",
    "2cm", "2pt", "3.0cm", "3.1cm", "3.2cm", "3.2em", "3.4cm",
    "3.5cm", "3.5pt", "3.6cm", "3.8cm", "3.8em", "30pt", "3cm", "3pt",
    "4.0cm", "4.1cm", "4.2cm", "4.3cm", "4.5cm", "4.8cm", "4cm",
    "4pt", "5.0cm", "5.2cm", "5.3cm", "5.5cm", "5.6cm", "6pt", "6.5cm",
    "7.0em", "7.2cm", "7cm", "8.0cm", "8.5cm",
    "-30pt", "-20pt", "-8pt", "-0.5em",
)


def latex_dimension_name(value: str) -> str:
    """Return the LaTeX control-sequence name for a registered dimension."""
    match = re.fullmatch(r"(-?)(\d+(?:\.\d+)?)(pt|cm|mm|in|em)", value)
    if not match:
        raise ValueError(f"Unsupported LaTeX dimension: {value}")
    sign, number, unit = match.groups()
    digits = {
        "0": "Zero",
        "1": "One",
        "2": "Two",
        "3": "Three",
        "4": "Four",
        "5": "Five",
        "6": "Six",
        "7": "Seven",
        "8": "Eight",
        "9": "Nine",
    }
    number = "".join(
        "Point" if char == "." else digits[char]
        for char in number
    )
    prefix = "Negative" if sign else ""
    return rf"\ReportDim{prefix}{unit.title()}{number}"


LATEX_DIMENSION_MACROS: Dict[str, str] = {
    dimension: latex_dimension_name(dimension)
    for dimension in LATEX_DIMENSIONS
}


def _dimension_definitions() -> str:
    """Build the named dimension definitions used by report fragments."""
    return "\n".join(
        rf"\newcommand{{{macro}}}{{{dimension}}}"
        for dimension, macro in LATEX_DIMENSION_MACROS.items()
    )


_STYLE_MACROS = r"""
\newcommand{\ReportRowBreak}{\\[@ROW_BREAK@pt]}
\newcommand{\ReportTallRowBreak}{\\[@TALL_ROW_BREAK@pt]}
\newcommand{\ReportFail}[1]{\textcolor{reportFail}{#1}}
\newcommand{\ReportPass}[1]{\textcolor{reportPass}{#1}}
\newcommand{\ReportWarning}[1]{\textcolor{reportWarning}{#1}}
\newcommand{\ReportInfo}[1]{\textcolor{osdagGreen}{#1}}
\newcommand{\ReportCompactTableSpacing}{\setlength{\tabcolsep}{@COMPACT_PADDING@pt}}
\newcommand{\ReportDenseTableSpacing}{\setlength{\tabcolsep}{@DENSE_PADDING@pt}}
\newcommand{\ReportWideTableSpacing}{\setlength{\tabcolsep}{@WIDE_PADDING@pt}}
\newcommand{\ReportDenseTableRows}{\renewcommand{\arraystretch}{@DENSE_STRETCH@}}
\newcommand{\ReportCaptionSpacing}{%
  \setlength{\abovecaptionskip}{@CAPTION_SKIP@pt}%
  \setlength{\belowcaptionskip}{@CAPTION_SKIP@pt}%
}
\newcommand{\ReportFontSmall}{\small}
\newcommand{\ReportFontFootnotesize}{\footnotesize}
\newcommand{\ReportFontLarge}{\Large}
\newcommand{\ReportFontHuge}{\Huge}
\newcommand{\ReportFontLargeText}{\large}
\newcommand{\ReportFontNormal}{\normalsize}
\newcommand{\ReportFigureWidth}{@FIGURE_WIDTH_MEDIUM@}
\newcommand{\ReportFigureWidthDrawing}{@FIGURE_WIDTH_DRAWING@}
\newcommand{\ReportFigureWidthLarge}{@FIGURE_WIDTH_LARGE@}
\newcommand{\ReportPlaceholderWidth}{@FIGURE_PLACEHOLDER_WIDTH@}
\newcommand{\ReportCellPlaceholderWidth}{@FIGURE_CELL_PLACEHOLDER_WIDTH@}
\newcommand{\ReportFigureCellWidth}{@FIGURE_CELL_WIDTH@}
\newcommand{\ReportTitleLogoWidth}{@TITLE_LOGO_WIDTH@\textwidth}
\newcommand{\ReportOrganizationLogoWidth}{@ORG_LOGO_WIDTH@\textwidth}
"""


def _style_macro_definitions() -> str:
    """Build semantic LaTeX commands from the theme's numeric settings."""
    replacements = {
        "@ROW_BREAK@": str(TABLE_ROW_BREAK_PT),
        "@TALL_ROW_BREAK@": str(TABLE_TALL_ROW_BREAK_PT),
        "@COMPACT_PADDING@": str(TABLE_COMPACT_CELL_PADDING_PT),
        "@DENSE_PADDING@": str(TABLE_DENSE_CELL_PADDING_PT),
        "@WIDE_PADDING@": str(TABLE_WIDE_CELL_PADDING_PT),
        "@DENSE_STRETCH@": str(TABLE_DENSE_ARRAY_STRETCH),
        "@CAPTION_SKIP@": str(TABLE_CAPTION_SKIP_PT),
        "@TITLE_LOGO_WIDTH@": str(TITLE_LOGO_WIDTH_RATIO),
        "@ORG_LOGO_WIDTH@": str(ORGANIZATION_LOGO_WIDTH_RATIO),
        "@FIGURE_WIDTH_MEDIUM@": _FIGURE_WIDTH_MEDIUM_VALUE,
        "@FIGURE_WIDTH_DRAWING@": _FIGURE_WIDTH_DRAWING_VALUE,
        "@FIGURE_WIDTH_LARGE@": _FIGURE_WIDTH_LARGE_VALUE,
        "@FIGURE_PLACEHOLDER_WIDTH@": _FIGURE_PLACEHOLDER_WIDTH_VALUE,
        "@FIGURE_CELL_PLACEHOLDER_WIDTH@": _FIGURE_CELL_PLACEHOLDER_WIDTH_VALUE,
        "@FIGURE_CELL_WIDTH@": _FIGURE_CELL_WIDTH_VALUE,
    }
    macros = _STYLE_MACROS
    for placeholder, value in replacements.items():
        macros = macros.replace(placeholder, value)
    return macros


_TOC_STYLE = r"""
% Table-of-contents typography.
\setcounter{tocdepth}{2}
\titlecontents{chapter}[\ReportDimEmOnePointFive]
  {\normalfont\vspace{\ReportDimPtTwo}}
  {\contentslabel{\ReportDimEmOnePointFive}}
  {\hspace*{-\ReportDimEmOnePointFive}}
  {\hfill\contentspage}
\titlecontents{section}[\ReportDimEmThreePointEight]
  {\normalfont}
  {\contentslabel{\ReportDimEmTwoPointThree}}
  {\hspace*{-\ReportDimEmTwoPointThree}}
  {\hfill\contentspage}
\titlecontents{subsection}[\ReportDimEmSevenPointZero]
  {\normalfont}
  {\contentslabel{\ReportDimEmThreePointTwo}}
  {\hspace*{-\ReportDimEmThreePointTwo}}
  {\hfill\contentspage}
\newpage
\renewcommand{\contentsname}{\centering\ReportFontLarge\bfseries Table of Contents}
\tableofcontents
"""


def build_latex_preamble(
    project_name: str,
    job_number: str,
    report_date: str,
    report_version: str,
) -> str:
    """Build the document preamble from the centralized report theme."""
    geometry = (
        f"{PAPER_SIZE}, margin={PAGE_MARGIN}, headheight={PAGE_HEADHEIGHT}, "
        f"headsep={PAGE_HEADSEP}, footskip={PAGE_FOOTSKIP}"
    )
    preamble = r"""
\documentclass[@FONT_SIZE@pt,@PAPER@]{report}
\usepackage[@GEOMETRY@]{geometry}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{booktabs}
\usepackage{array}
\usepackage{tabularx}
\usepackage{float}
\usepackage{fancyhdr}
\usepackage[hidelinks]{hyperref}
\usepackage{xcolor}
\usepackage{setspace}
\usepackage{enumitem}
\usepackage{caption}
\captionsetup{
    labelfont=bf,
    justification=raggedright,
    singlelinecheck=false,
    format=plain
}
\usepackage{subcaption}
\usepackage{multirow}
\usepackage{colortbl}
\usepackage{longtable}
\setlength{\LTleft}{\fill}
\setlength{\LTright}{\fill}
\usepackage{titlesec}
\usepackage{titletoc}
\usepackage{lastpage}
\usepackage{makecell}
\usepackage{etoolbox}
\usepackage{needspace}
\numberwithin{table}{chapter}
\numberwithin{figure}{chapter}
\setlength{\tabcolsep}{@CELL_PADDING@pt}
\renewcommand{\arraystretch}{@ARRAY_STRETCH@}
\setlength{\LTpre}{@LONGTABLE_PRE@pt}
\setlength{\LTpost}{@LONGTABLE_POST@pt}
\setlength{\arrayrulewidth}{@RULE_WIDTH@pt}
\setlength{\extrarowheight}{@EXTRA_ROW_HEIGHT@pt}
\setlength{\abovecaptionskip}{@CAPTION_SKIP@pt}
\setlength{\belowcaptionskip}{@CAPTION_SKIP@pt}
\BeforeBeginEnvironment{table}{\needspace{@TABLE_MIN_REMAINDER_LINES@\baselineskip}}
\BeforeBeginEnvironment{longtable}{\needspace{@TABLE_MIN_REMAINDER_LINES@\baselineskip}}
\definecolor{osdagGreen}{HTML}{@ACCENT@}
\definecolor{reportPass}{HTML}{@PASS@}
\definecolor{reportFail}{HTML}{@FAIL@}
\definecolor{reportWarning}{HTML}{@WARNING@}
\definecolor{reportNeutral}{HTML}{@NEUTRAL@}
@DIMENSIONS@
@STYLE_MACROS@
\titleformat{\chapter}[block]
  {\normalfont\ReportFontLarge\bfseries\centering}{\thechapter}{\ReportDimEmOne}{}
\titlespacing*{\chapter}{\ReportDimPtZero}{\ReportDimNegativePtThreeZero}{\ReportDimPtOneZero}
\fancypagestyle{main}{
  \fancyhf{}
  \fancyhead[L]{@PROJECT@ $|$ @JOB@}
  \fancyhead[R]{@DATE@ $|$ @VERSION@}
  \fancyfoot[L]{Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay}
  \fancyfoot[R]{Page \thepage\ of \pageref{LastPage}}
  \renewcommand{\headrule}{\color{osdagGreen}\hrule width\headwidth height \ReportDimPtOne \vspace{\ReportDimPtTwo}}
  \renewcommand{\footrule}{%
    \ifbool{hasSDonPage}{%
      \vspace{\ReportDimNegativePtTwoZero}%
      \hbox to \headwidth{\textcolor{reportNeutral}{\ReportFontFootnotesize\textit{* Software default value}}\hfil}%
      \vspace{\ReportDimPtFour}%
    }{%
      \vspace{\ReportDimNegativePtEight}%
    }%
    \color{osdagGreen}\hrule width\headwidth height \ReportDimPtOne \vspace{\ReportDimPtSix}%
  }
}
\fancypagestyle{plain}{
  \fancyhf{}
  \fancyhead[L]{@PROJECT@ $|$ @JOB@}
  \fancyhead[R]{@DATE@ $|$ @VERSION@}
  \fancyfoot[L]{Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay}
  \fancyfoot[R]{Page \thepage\ of \pageref{LastPage}}
  \renewcommand{\headrule}{\color{osdagGreen}\hrule width\headwidth height \ReportDimPtOne \vspace{\ReportDimPtTwo}}
  \renewcommand{\footrule}{%
    \ifbool{hasSDonPage}{%
      \vspace{\ReportDimNegativePtTwoZero}%
      \hbox to \headwidth{\textcolor{reportNeutral}{\ReportFontFootnotesize\textit{* Software default value}}\hfil}%
      \vspace{\ReportDimPtFour}%
    }{%
      \vspace{\ReportDimNegativePtEight}%
    }%
    \color{osdagGreen}\hrule width\headwidth height \ReportDimPtOne \vspace{\ReportDimPtSix}%
  }
}
\fancypagestyle{firstpage}{
  \fancyhf{}
  \renewcommand{\headrulewidth}{0pt}
  \fancyfoot[L]{Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay}
  \fancyfoot[R]{Page \thepage\ of \pageref{LastPage}}
  \renewcommand{\footrule}{\vspace{\ReportDimNegativePtEight}\color{osdagGreen}\hrule width\headwidth height \ReportDimPtOne \vspace{\ReportDimPtSix}}
}
\pagestyle{main}
\setstretch{@LINE_SPACING@}
\newcommand{\placeholder}[1]{\textit{\textless #1\textgreater}}
\newcommand{\todo}[1]{\colorbox{yellow}{TODO: #1}}
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}
\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
\newcolumntype{R}[1]{>{\raggedleft\arraybackslash}p{#1}}
\newcommand{\sdstar}{\textsuperscript{*}}
\newbool{hasSDonPage}
\boolfalse{hasSDonPage}
\renewcommand{\sdstar}{\textsuperscript{*}\global\booltrue{hasSDonPage}}
\AddToHook{shipout/before}{\global\boolfalse{hasSDonPage}}
\title{\ReportFontLarge\textbf{OsdagBridge} \\ \ReportFontNormal Open Source Software for Steel Girder Bridge Design \\ \vspace{\ReportDimCmTwo} \ReportFontLargeText Design Report}
\author{}
\date{}
\begin{document}
"""
    replacements = {
        "@FONT_SIZE@": str(BASE_FONT_SIZE_PT),
        "@PAPER@": PAPER_SIZE,
        "@GEOMETRY@": geometry,
        "@ACCENT@": COLOR_ACCENT,
        "@PASS@": COLOR_PASS.lstrip("#"),
        "@FAIL@": COLOR_FAIL.lstrip("#"),
        "@WARNING@": COLOR_WARNING.lstrip("#"),
        "@NEUTRAL@": COLOR_NEUTRAL.lstrip("#"),
        "@DIMENSIONS@": _dimension_definitions(),
        "@STYLE_MACROS@": _style_macro_definitions(),
        "@PROJECT@": project_name,
        "@JOB@": job_number,
        "@DATE@": report_date,
        "@VERSION@": report_version,
        "@LINE_SPACING@": str(LINE_SPACING),
        "@CELL_PADDING@": str(TABLE_CELL_PADDING_PT),
        "@ARRAY_STRETCH@": str(TABLE_ARRAY_STRETCH),
        "@LONGTABLE_PRE@": str(LONGTABLE_PRE_SKIP_PT),
        "@LONGTABLE_POST@": str(LONGTABLE_POST_SKIP_PT),
        "@RULE_WIDTH@": str(TABLE_RULE_WIDTH_PT),
        "@EXTRA_ROW_HEIGHT@": str(TABLE_EXTRA_ROW_HEIGHT_PT),
        "@CAPTION_SKIP@": str(TABLE_CAPTION_SKIP_PT),
        "@TABLE_MIN_REMAINDER_LINES@": str(TABLE_MIN_REMAINDER_LINES),
    }
    for placeholder, value in replacements.items():
        preamble = preamble.replace(placeholder, value)
    return preamble


TOC_LATEX = _TOC_STYLE
