from bson import ObjectId

from app.agents.document_intelligence import (
    DocumentIntelligenceAgent,
)
from app.agents.risk_engine import RiskEngine

from app.db.collections.files import files_collection

from app.schemas.document_analysis import DocumentAnalysis


class DocumentAnalysisService:

    def __init__(self):

        self.agent = DocumentIntelligenceAgent()
        self.risk_engine = RiskEngine()

    async def analyze(
        self,
        file_id: str,
        analysis_type: str = "contract",
    ) -> DocumentAnalysis:

        # ----------------------------------------------
        # Validate file ID
        # ----------------------------------------------

        try:

            object_id = ObjectId(file_id)

        except Exception:

            raise ValueError(
                "Invalid file_id."
            )

        # ----------------------------------------------
        # Retrieve processed document
        # ----------------------------------------------

        document = await files_collection.find_one(
            {
                "_id": object_id
            }
        )

        if document is None:

            raise FileNotFoundError(
                "Document not found."
            )

        # ----------------------------------------------
        # Ensure processing is complete
        # ----------------------------------------------

        status = document.get(
            "status"
        )

        if status != "completed":

            raise RuntimeError(
                f"Document is not ready for analysis. "
                f"Current status: {status}"
            )

        # ----------------------------------------------
        # Extract Markdown
        # ----------------------------------------------

        markdown = document.get(
            "markdown",
            ""
        )

        if not markdown.strip():

            raise RuntimeError(
                "Processed document contains no extracted text."
            )

        # ----------------------------------------------
        # Stage 1 — AI Document Intelligence
        # ----------------------------------------------

        analysis = self.agent.analyze(
            document=markdown,
            analysis_type=analysis_type,
        )

        # ----------------------------------------------
        # Stage 2 — Hybrid Risk Analysis
        # ----------------------------------------------

        analysis.risks = self.risk_engine.analyze(
            analysis=analysis,
            document=markdown,
        )

        # ----------------------------------------------
        # Return final structured analysis
        # ----------------------------------------------

        return analysis