import axios from "axios";


const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://localhost:8000";


const api =
  axios.create({
    baseURL:
      API_BASE_URL,
    headers: {
      Accept:
        "application/json",
    },
  });


/* =====================================================
   UPLOAD DOCUMENT
===================================================== */

export async function uploadDocument(
  file
) {
  const formData =
    new FormData();

  formData.append(
    "file",
    file
  );

  const response =
    await api.post(
      "/upload",
      formData,
      {
        headers: {
          "Content-Type":
            "multipart/form-data",
        },
      }
    );

  return response.data;
}


/* =====================================================
   GET DOCUMENT STATUS
===================================================== */

export async function getDocumentStatus(
  fileId
) {
  const response =
    await api.get(
      `/status/${fileId}`
    );

  return response.data;
}


/* =====================================================
   GET ALL DOCUMENTS
===================================================== */

export async function getDocuments() {
  const response =
    await api.get(
      "/files"
    );

  return response.data;
}


/* =====================================================
   GET SINGLE DOCUMENT
===================================================== */

export async function getDocument(
  fileId
) {
  const response =
    await api.get(
      `/files/${fileId}`
    );

  return response.data;
}


/* =====================================================
   DOCUMENT INTELLIGENCE
===================================================== */

export async function analyzeDocument(
  fileId,
  analysisType = "contract"
) {
  const response =
    await api.post(
      "/analyze",
      {
        file_id:
          fileId,

        analysis_type:
          analysisType,
      }
    );

  return response.data;
}


/* =====================================================
   WORKFLOW AGENT
===================================================== */

export async function generateWorkflow(
  fileId,
  objective
) {
  const response =
    await api.post(
      "/workflow",
      {
        file_id:
          fileId,

        objective:
          objective,
      }
    );

  return response.data;
}


/* =====================================================
   AI ASSISTANT
===================================================== */

export async function askDocument(
  fileId,
  question
) {
  const response =
    await api.post(
      "/chat",
      {
        file_id:
          fileId,

        question:
          question,
      }
    );

  return response.data;
}


export default api;