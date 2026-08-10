from app.constants.agent import AgentConfig
from app.agents.risk_rules import RiskRules
from app.schemas.document_analysis import (
    DocumentAnalysis,
    RiskFlag,
)


class RiskEngine:

    """
    Hybrid risk engine.

    Combines:
        1. AI-generated risks
        2. Deterministic document rules
    """

    def analyze(
        self,
        analysis: DocumentAnalysis,
        document: str,
    ) -> list[RiskFlag]:

        risks: list[RiskFlag] = []

        # ==================================================
        # 1. Preserve AI-generated risks
        # ==================================================

        for risk in analysis.risks:

            risk.source = "ai"

            risks.append(risk)

        # ==================================================
        # 2. Apply deterministic rules
        # ==================================================

        risks.extend(
            self._detect_placeholders(
                document
            )
        )

        # ==================================================
        # 3. Remove duplicate / overlapping risks
        # ==================================================

        risks = self._deduplicate(
            risks
        )

        return risks

    # ======================================================
    # Placeholder Rule
    # ======================================================

    def _detect_placeholders(
        self,
        document: str,
    ) -> list[RiskFlag]:

        risks = []

        document_lower = document.lower()

        found_terms = []

        for term in RiskRules.PLACEHOLDER_TERMS:

            if term.lower() in document_lower:

                found_terms.append(term)

        if not found_terms:

            return risks

        # --------------------------------------------------
        # Find useful evidence
        # --------------------------------------------------

        evidence = self._extract_placeholder_evidence(
            document,
            found_terms,
        )

        risks.append(
            RiskFlag(
                title="Incomplete or placeholder information",
                category=RiskRules.PLACEHOLDER_CATEGORY,
                severity=RiskRules.PLACEHOLDER_SEVERITY,
                confidence=RiskRules.PLACEHOLDER_CONFIDENCE,
                explanation=(
                    "The document contains placeholder or "
                    "incomplete fields that may require "
                    "completion before the document is finalized."
                ),
                evidence=evidence,
                source="rule",
            )
        )

        return risks

    # ======================================================
    # Placeholder Evidence Extraction
    # ======================================================

    @staticmethod
    def _extract_placeholder_evidence(
        document: str,
        terms: list[str],
    ) -> str:

        lines = document.splitlines()

        matches = []

        for line in lines:

            line_lower = line.lower()

            if any(
                term.lower() in line_lower
                for term in terms
            ):

                cleaned = line.strip()

                if cleaned and cleaned not in matches:

                    matches.append(cleaned)

                # Keep evidence concise.
                if len(matches) >= 3:
                    break

        if matches:

            return " | ".join(matches)[:1000]

        return ", ".join(terms)

    # ======================================================
    # Risk Deduplication
    # ======================================================

    @staticmethod
    def _deduplicate(
        risks: list[RiskFlag],
    ) -> list[RiskFlag]:

        unique: list[RiskFlag] = []

        seen_titles: set[tuple[str, str]] = set()

        for risk in risks:

            title_key = (
                risk.title.strip().lower(),
                risk.category.strip().lower(),
            )

            # ------------------------------------------------
            # Exact duplicate
            # ------------------------------------------------

            if title_key in seen_titles:

                continue

            # ------------------------------------------------
            # Placeholder overlap
            #
            # Prefer deterministic rule-based detection
            # over an AI finding describing the same issue.
            # ------------------------------------------------

            if (
                risk.category
                in {
                    "missing_information",
                    "ambiguity",
                }
            ):

                risk_text = (
                    f"{risk.title} "
                    f"{risk.explanation} "
                    f"{risk.evidence}"
                ).lower()

                placeholder_signals = [
                    "placeholder",
                    "xxx",
                    "______",
                    "incomplete",
                    "blank",
                    "unspecified",
                    "undefined",
                ]

                is_placeholder_risk = any(
                    signal in risk_text
                    for signal in placeholder_signals
                )

                if is_placeholder_risk:

                    rule_duplicate = any(
                        existing.source == "rule"
                        and existing.category
                        in {
                            "missing_information",
                            "ambiguity",
                        }
                        and any(
                            signal in (
                                f"{existing.title} "
                                f"{existing.explanation} "
                                f"{existing.evidence}"
                            ).lower()
                            for signal in placeholder_signals
                        )
                        for existing in unique
                    )

                    if rule_duplicate:

                        continue

            # ------------------------------------------------
            # Keep risk
            # ------------------------------------------------

            seen_titles.add(title_key)

            unique.append(
                risk
            )

        return unique