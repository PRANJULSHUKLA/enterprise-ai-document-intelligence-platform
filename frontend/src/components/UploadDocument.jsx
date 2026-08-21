import {
  useRef,
  useState,
} from "react";

import {
  Upload,
  FileText,
  X,
  Loader2,
  CheckCircle2,
  AlertCircle,
} from "lucide-react";

import {
  uploadDocument,
  getDocumentStatus,
} from "../services/documentService";


function normalizeStatus(
  status
) {
  if (!status) {
    return "queued";
  }

  const value =
    String(status)
      .toLowerCase()
      .trim();

  const statusMap = {
    saving: "queued",
    queued: "queued",
    processing: "processing",

    "extracting text":
      "extracting_text",

    "creating knowledge base":
      "creating_knowledge_base",

    "creating chunk embeddings":
      "creating_chunk_embeddings",

    completed:
      "completed",

    failed:
      "failed",
  };

  return (
    statusMap[value] ||
    value
  );
}


export default function UploadDocument({
  onUploaded,
}) {
  const inputRef =
    useRef(null);

  const [
    selectedFile,
    setSelectedFile,
  ] = useState(null);

  const [
    uploading,
    setUploading,
  ] = useState(false);

  const [
    status,
    setStatus,
  ] = useState("");

  const [
    error,
    setError,
  ] = useState("");


  const statusLabels = {
    queued:
      "Queued for processing",

    processing:
      "Processing document",

    extracting_text:
      "Extracting text with AI",

    creating_knowledge_base:
      "Building knowledge base",

    creating_chunk_embeddings:
      "Creating embeddings",

    completed:
      "Document ready",

    failed:
      "Processing failed",
  };


  async function pollStatus(
    fileId
  ) {
    const maxAttempts =
      240;

    for (
      let attempt = 0;
      attempt <
      maxAttempts;
      attempt++
    ) {
      try {
        const result =
          await getDocumentStatus(
            fileId
          );

        const normalizedStatus =
          normalizeStatus(
            result.status
          );

        setStatus(
          normalizedStatus
        );

        console.log(
          `[Pipeline ${
            attempt + 1
          }]`,
          result.status,
          "→",
          normalizedStatus
        );


        if (
          normalizedStatus ===
          "completed"
        ) {
          setUploading(
            false
          );

          onUploaded?.({
            file_id:
              fileId,

            _id:
              fileId,

            filename:
              selectedFile?.name ||
              "Uploaded document",

            status:
              "completed",
          });

          return;
        }


        if (
          normalizedStatus ===
          "failed"
        ) {
          setUploading(
            false
          );

          setError(
            "Document processing failed."
          );

          return;
        }


        await new Promise(
          (resolve) =>
            setTimeout(
              resolve,
              2500
            )
        );

      } catch (err) {
        console.error(
          "Status polling failed:",
          err
        );

        setUploading(
          false
        );

        setError(
          err?.response?.data
            ?.detail ||
            "Unable to check document status."
        );

        return;
      }
    }


    setUploading(
      false
    );

    setError(
      "Document processing is taking longer than expected."
    );
  }


  async function handleUpload() {
    if (
      !selectedFile
    ) {
      return;
    }

    try {
      setUploading(
        true
      );

      setError("");

      setStatus(
        "queued"
      );


      const result =
        await uploadDocument(
          selectedFile
        );


      const fileId =
        result.file_id;

      if (!fileId) {
        throw new Error(
          "Backend did not return a file ID."
        );
      }


      await pollStatus(
        fileId
      );

    } catch (err) {
      console.error(
        "Upload failed:",
        err
      );

      setUploading(
        false
      );

      setError(
        err?.response?.data
          ?.detail ||
          err?.message ||
          "Unable to upload document."
      );
    }
  }


  function clearFile() {
    setSelectedFile(
      null
    );

    setStatus("");

    setError("");

    if (
      inputRef.current
    ) {
      inputRef.current.value =
        "";
    }
  }


  function handleFileSelect(
    event
  ) {
    const file =
      event.target.files?.[0];

    if (!file) {
      return;
    }

    setError("");

    setStatus("");

    setSelectedFile(
      file
    );
  }


  return (
    <div className="mx-auto w-full max-w-3xl">

      <div className="flex justify-center">

        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-zinc-100">
          <Upload
            size={22}
          />
        </div>

      </div>


      <h3 className="mt-4 text-center font-semibold">
        Analyze a new document
      </h3>

      <p className="mx-auto mt-2 max-w-md text-center text-sm text-zinc-500">
        Upload a contract, policy, report, or other business document to start the intelligence pipeline.
      </p>


      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.doc,.docx"
        onChange={
          handleFileSelect
        }
        className="hidden"
      />


      {!selectedFile &&
        !uploading && (
          <div className="flex justify-center">

            <button
              onClick={() =>
                inputRef.current?.click()
              }
              className="mt-5 inline-flex items-center gap-2 rounded-xl bg-zinc-900 px-5 py-2.5 text-sm font-medium text-white hover:bg-zinc-700"
            >
              <Upload
                size={16}
              />

              Choose document

            </button>

          </div>
        )}


      {selectedFile && (
        <div className="mx-auto mt-6 max-w-md rounded-2xl border border-zinc-200 bg-zinc-50 p-4">

          <div className="flex items-center justify-between">

            <div className="flex min-w-0 items-center gap-3">

              <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-white">
                <FileText
                  size={17}
                />
              </div>

              <div className="min-w-0">

                <p className="truncate text-sm font-medium">
                  {
                    selectedFile.name
                  }
                </p>

                <p className="text-xs text-zinc-400">
                  {(
                    selectedFile.size /
                    1024 /
                    1024
                  ).toFixed(
                    2
                  )}{" "}
                  MB
                </p>

              </div>

            </div>


            {!uploading && (
              <button
                onClick={
                  clearFile
                }
                className="rounded-lg p-2 text-zinc-400 hover:bg-white hover:text-zinc-900"
              >
                <X
                  size={16}
                />
              </button>
            )}

          </div>


          {!uploading &&
            !status && (
              <button
                onClick={
                  handleUpload
                }
                className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl bg-zinc-900 px-4 py-2.5 text-sm font-medium text-white hover:bg-zinc-700"
              >

                <Upload
                  size={16}
                />

                Start analysis

              </button>
            )}

        </div>
      )}


      {/* PROCESSING */}

      {uploading && (
        <div className="mx-auto mt-6 max-w-md rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm">

          <div className="flex items-center gap-4">

            <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-zinc-100">

              <Loader2
                size={21}
                className="animate-spin"
              />

            </div>

            <div className="min-w-0">

              <p className="text-sm font-semibold">
                Processing document
              </p>

              <p className="mt-1 text-sm text-zinc-500">
                {
                  statusLabels[
                    status
                  ] ||
                  "Processing..."
                }
              </p>

            </div>

          </div>


          <div className="mt-5 h-2 overflow-hidden rounded-full bg-zinc-100">

            <div
              className="h-full rounded-full bg-zinc-900 transition-all duration-700"
              style={{
                width:
                  status ===
                  "queued"
                    ? "10%"
                    : status ===
                      "processing"
                    ? "25%"
                    : status ===
                      "extracting_text"
                    ? "45%"
                    : status ===
                      "creating_knowledge_base"
                    ? "65%"
                    : status ===
                      "creating_chunk_embeddings"
                    ? "85%"
                    : "95%",
              }}
            />

          </div>


          <div className="mt-4 space-y-2 text-xs">

            <PipelineStep
              label="Document uploaded"
              active
              completed={
                status !==
                "queued"
              }
            />

            <PipelineStep
              label="AI text extraction"
              completed={[
                "creating_knowledge_base",
                "creating_chunk_embeddings",
                "completed",
              ].includes(
                status
              )}
              active={
                status ===
                "extracting_text"
              }
            />

            <PipelineStep
              label="Knowledge base"
              completed={[
                "creating_chunk_embeddings",
                "completed",
              ].includes(
                status
              )}
              active={
                status ===
                "creating_knowledge_base"
              }
            />

            <PipelineStep
              label="Embeddings"
              completed={
                status ===
                "completed"
              }
              active={
                status ===
                "creating_chunk_embeddings"
              }
            />

          </div>

        </div>
      )}


      {/* COMPLETED */}

      {!uploading &&
        status ===
          "completed" && (
          <div className="mx-auto mt-6 max-w-md rounded-2xl border border-emerald-200 bg-emerald-50 p-6">

            <div className="flex items-center gap-3">

              <CheckCircle2
                size={24}
                className="text-emerald-600"
              />

              <div>

                <p className="font-semibold text-emerald-900">
                  Document ready
                </p>

                <p className="mt-1 text-sm text-emerald-700">
                  AI processing has completed successfully.
                </p>

              </div>

            </div>

          </div>
        )}


      {/* ERROR */}

      {error && (
        <div className="mx-auto mt-4 flex max-w-md items-center gap-2 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">

          <AlertCircle
            size={17}
          />

          <span>
            {error}
          </span>

        </div>
      )}

    </div>
  );
}


function PipelineStep({
  label,
  active = false,
  completed = false,
}) {
  return (
    <div className="flex items-center gap-2">

      <div
        className={`flex h-5 w-5 items-center justify-center rounded-full ${
          completed
            ? "bg-emerald-100 text-emerald-600"
            : active
            ? "bg-zinc-900 text-white"
            : "bg-zinc-100 text-zinc-400"
        }`}
      >
        {completed
          ? "✓"
          : "•"}
      </div>

      <span
        className={
          completed ||
          active
            ? "text-zinc-800"
            : "text-zinc-400"
        }
      >
        {label}
      </span>

    </div>
  );
}