from bson import ObjectId

from app.agents.workflow_agent import WorkflowAgent
from app.db.collections.files import files_collection
from app.services.document_analysis import DocumentAnalysisService
from app.schemas.workflow import WorkflowPlan


class WorkflowService:

    def __init__(self):

        self.analysis_service = (
            DocumentAnalysisService()
        )

        self.agent = WorkflowAgent()

    async def create_plan(
        self,
        file_id: str,
        objective: str,
    ) -> WorkflowPlan:

        # ----------------------------------------------
        # Validate file ID
        # ----------------------------------------------

        try:

            ObjectId(file_id)

        except Exception:

            raise ValueError(
                "Invalid file_id."
            )

        # ----------------------------------------------
        # Ensure document exists and is ready
        # ----------------------------------------------

        document = await files_collection.find_one(
            {
                "_id": ObjectId(file_id)
            }
        )

        if document is None:

            raise FileNotFoundError(
                "Document not found."
            )

        if document.get("status") != "completed":

            raise RuntimeError(
                "Document is not ready for workflow planning. "
                f"Current status: {document.get('status')}"
            )

        # ----------------------------------------------
        # Agent 2
        # ----------------------------------------------

        analysis = await self.analysis_service.analyze(
            file_id=file_id,
            analysis_type="contract",
        )

        # ----------------------------------------------
        # Agent 3
        # ----------------------------------------------

        return self.agent.analyze(
            analysis=analysis.model_dump(
                mode="json"
            ),
            objective=objective,
        )