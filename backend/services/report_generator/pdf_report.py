from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from pathlib import Path
from datetime import datetime
from backend.config import settings


def build_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="CustomTitle",
        fontSize=22,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1a1a2e"),
        alignment=TA_CENTER,
        spaceAfter=12,
    ))
    styles.add(ParagraphStyle(
        name="SectionHeader",
        fontSize=14,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#16213e"),
        spaceBefore=16,
        spaceAfter=6,
        borderPad=4,
    ))
    styles.add(ParagraphStyle(
        name="BodyText2",
        fontSize=10,
        fontName="Helvetica",
        textColor=colors.HexColor("#333333"),
        spaceAfter=6,
        leading=16,
        alignment=TA_JUSTIFY,
    ))
    styles.add(ParagraphStyle(
        name="MetaText",
        fontSize=9,
        fontName="Helvetica-Oblique",
        textColor=colors.HexColor("#666666"),
        alignment=TA_CENTER,
        spaceAfter=4,
    ))

    return styles


def generate_experiment_report(experiment_data: dict, output_filename: str = None) -> str:
    reports_dir = Path(settings.REPORTS_DIR)
    reports_dir.mkdir(parents=True, exist_ok=True)

    if not output_filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"report_{timestamp}.pdf"

    output_path = reports_dir / output_filename
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=0.8*inch,
        leftMargin=0.8*inch,
        topMargin=1*inch,
        bottomMargin=0.8*inch
    )

    styles = build_styles()
    story = []

    # ── Title page ──────────────────────────────────────────
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("AI Research Scientist Assistant", styles["CustomTitle"]))
    story.append(Paragraph("Automated ML Experiment Report", styles["MetaText"]))
    story.append(Spacer(1, 0.1*inch))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#4C9BE8")))
    story.append(Spacer(1, 0.2*inch))

    generated_at = datetime.now().strftime("%B %d, %Y at %H:%M")
    story.append(Paragraph(f"Generated: {generated_at}", styles["MetaText"]))
    story.append(Spacer(1, 0.3*inch))

    # ── Abstract ────────────────────────────────────────────
    story.append(Paragraph("Abstract", styles["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 0.1*inch))

    exp_name = experiment_data.get("experiment_name", "Unnamed Experiment")
    problem_type = experiment_data.get("problem_type", "unknown")
    best_model = experiment_data.get("best_model", "N/A")
    best_score = experiment_data.get("best_score", 0)
    dataset_name = experiment_data.get("dataset_name", "uploaded dataset")

    abstract_text = (
        f"This report presents the results of an automated machine learning experiment titled "
        f"'{exp_name}'. The experiment was conducted on the dataset '{dataset_name}', "
        f"which was identified as a {problem_type} problem. Multiple machine learning models "
        f"were trained and evaluated. The best performing model was {best_model} "
        f"with a score of {round(best_score, 4)}. "
        f"This report includes dataset analysis, methodology, model comparison, "
        f"feature importance analysis, and recommendations for future work."
    )
    story.append(Paragraph(abstract_text, styles["BodyText2"]))
    story.append(Spacer(1, 0.2*inch))

    # ── Problem Statement ────────────────────────────────────
    story.append(Paragraph("1. Problem Statement", styles["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 0.1*inch))

    problem_text = (
        f"The objective of this experiment was to build and evaluate machine learning models "
        f"for a {problem_type} task. The dataset contains "
        f"{experiment_data.get('dataset_profile', {}).get('rows', 'N/A')} rows and "
        f"{experiment_data.get('dataset_profile', {}).get('columns', 'N/A')} features. "
        f"The goal was to identify the most effective algorithm and provide "
        f"interpretable insights through feature importance analysis."
    )
    story.append(Paragraph(problem_text, styles["BodyText2"]))
    story.append(Spacer(1, 0.2*inch))

    # ── Dataset Analysis ─────────────────────────────────────
    story.append(Paragraph("2. Dataset Analysis", styles["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 0.1*inch))

    profile = experiment_data.get("dataset_profile", {})
    if profile:
        summary_data = [
            ["Metric", "Value"],
            ["Total Rows", str(profile.get("rows", "N/A"))],
            ["Total Columns", str(profile.get("columns", "N/A"))],
            ["Duplicate Rows", str(profile.get("duplicate_rows", "N/A"))],
            ["Numeric Columns", str(len(profile.get("numeric_columns", [])))],
            ["Categorical Columns", str(len(profile.get("categorical_columns", [])))],
        ]

        table = Table(summary_data, colWidths=[3*inch, 3*inch])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4C9BE8")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.2*inch))

    # ── Methodology ──────────────────────────────────────────
    story.append(Paragraph("3. Methodology", styles["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 0.1*inch))

    methodology_text = (
        "The following pipeline was applied: "
        "(1) Data cleaning — missing values handled using median/mode imputation, "
        "duplicate rows removed. "
        "(2) Feature encoding — categorical variables encoded using Label Encoding. "
        "(3) Feature scaling — numeric features normalized using StandardScaler. "
        "(4) Feature selection — top features selected using statistical scoring. "
        "(5) Model training — multiple algorithms trained using 80/20 train-test split. "
        "(6) Hyperparameter defaults used for initial run; Optuna optimization available separately."
    )
    story.append(Paragraph(methodology_text, styles["BodyText2"]))
    story.append(Spacer(1, 0.2*inch))

    # ── Results ──────────────────────────────────────────────
    story.append(Paragraph("4. Experiment Results", styles["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 0.1*inch))

    all_results = experiment_data.get("all_results", {})
    if all_results:
        # build results table
        rows = [["Model", "Score", "Train Time (s)"]]
        for model_name, metrics in all_results.items():
            if "error" not in metrics:
                if problem_type == "classification":
                    score = metrics.get("f1_score", metrics.get("accuracy", 0))
                elif problem_type == "regression":
                    score = metrics.get("r2_score", 0)
                else:
                    score = metrics.get("silhouette_score", 0)

                rows.append([
                    model_name,
                    str(round(score, 4)),
                    str(metrics.get("train_time_seconds", "N/A"))
                ])

        results_table = Table(rows, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        results_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#16213e")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f4ff")]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(results_table)
        story.append(Spacer(1, 0.2*inch))

    # ── Feature Importance ───────────────────────────────────
    fi = experiment_data.get("feature_importance", {})
    if fi:
        story.append(Paragraph("5. Feature Importance (SHAP Analysis)", styles["SectionHeader"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
        story.append(Spacer(1, 0.1*inch))

        fi_rows = [["Feature", "Importance Score"]]
        for feature, score in list(fi.items())[:10]:
            fi_rows.append([feature, str(round(score, 4))])

        fi_table = Table(fi_rows, colWidths=[3.5*inch, 2.5*inch])
        fi_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4CE87A")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0fff4")]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(fi_table)
        story.append(Spacer(1, 0.2*inch))

    # ── Conclusions ──────────────────────────────────────────
    story.append(Paragraph("6. Conclusions", styles["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 0.1*inch))

    conclusion_text = (
        f"The experiment evaluated {len(all_results)} machine learning models on the "
        f"{problem_type} task. {best_model} achieved the best performance with a score of "
        f"{round(best_score, 4)}. "
        f"Feature importance analysis identified the most influential predictors. "
        f"The automated pipeline demonstrates reliable model selection and evaluation."
    )
    story.append(Paragraph(conclusion_text, styles["BodyText2"]))
    story.append(Spacer(1, 0.2*inch))

    # ── Future Work ──────────────────────────────────────────
    story.append(Paragraph("7. Future Work", styles["SectionHeader"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
    story.append(Spacer(1, 0.1*inch))

    future_text = (
        "Recommended next steps: "
        "(1) Run Optuna hyperparameter optimization for the best model. "
        "(2) Explore deep learning architectures for improved performance. "
        "(3) Apply cross-validation for more robust evaluation. "
        "(4) Investigate ensemble methods combining top models. "
        "(5) Collect more data to address potential class imbalance."
    )
    story.append(Paragraph(future_text, styles["BodyText2"]))

    doc.build(story)
    print(f"report saved: {output_path}")
    return str(output_path)