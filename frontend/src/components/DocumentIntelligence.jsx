import {
  AlertTriangle,
  CalendarClock,
  CheckCircle2,
  FileText,
  Landmark,
  Loader2,
  ShieldAlert,
  Users,
} from "lucide-react";

function severityClasses(severity) {
  switch (
    String(severity || "").toLowerCase()
  ) {
    case "high":
      return {
        badge:
          "bg-red-50 text-red-700 ring-red-200",
        icon:
          "bg-red-100 text-red-600",
        border:
          "border-red-200",
      };

    case "medium":
      return {
        badge:
          "bg-amber-50 text-amber-700 ring-amber-200",
        icon:
          "bg-amber-100 text-amber-600",
        border:
          "border-amber-200",
      };

    default:
      return {
        badge:
          "bg-zinc-100 text-zinc-600 ring-zinc-200",
        icon:
          "bg-zinc-100 text-zinc-500",
        border:
          "border-zinc-200",
      };
  }
}

function SectionHeader({
  icon,
  title,
  count,
}) {
  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-2">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-zinc-100 text-zinc-600">
          {icon}
        </div>

        <h3 className="text-sm font-semibold text-zinc-900">
          {title}
        </h3>
      </div>

      {typeof count === "number" && (
        <span className="rounded-full bg-zinc-100 px-2.5 py-1 text-xs font-medium text-zinc-500">
          {count}
        </span>
      )}
    </div>
  );
}

export default function DocumentIntelligence({
  analysis,
  onGenerateWorkflow,
  generatingWorkflow = false,
}) {
  if (!analysis) {
    return null;
  }

  const risks =
    analysis.risks || [];

  const missingInformation =
    analysis.missing_information || [];

  const parties =
    analysis.parties || [];

  const obligations =
    analysis.obligations || [];

  const deadlines =
    analysis.deadlines || [];

  const financialTerms =
    analysis.financial_terms || [];

  const keyTerms =
    analysis.key_terms || [];

  const highRisks =
    risks.filter(
      (risk) =>
        String(
          risk.severity || ""
        ).toLowerCase() === "high"
    ).length;

  return (
    <div className="space-y-6">

      {/* ================================================= */}
      {/* EXECUTIVE OVERVIEW */}
      {/* ================================================= */}

      <div className="rounded-3xl border border-zinc-200 bg-white p-6 shadow-sm">

        <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">

          <div className="max-w-3xl">

            <div className="flex items-center gap-2">

              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-zinc-900 text-white">
                <FileText size={17} />
              </div>

              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-zinc-400">
                  Document intelligence
                </p>

                <p className="text-sm font-semibold text-zinc-900">
                  {analysis.document_type ||
                    "Document"}
                </p>
              </div>

            </div>

            <h2 className="mt-5 text-xl font-semibold tracking-tight text-zinc-900">
              Executive summary
            </h2>

            <p className="mt-2 text-sm leading-7 text-zinc-600">
              {analysis.executive_summary ||
                "No executive summary was returned."}
            </p>

          </div>

          <button
            onClick={
              onGenerateWorkflow
            }
            disabled={
              generatingWorkflow
            }
            className="inline-flex shrink-0 items-center justify-center gap-2 rounded-xl bg-zinc-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-zinc-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {generatingWorkflow ? (
              <>
                <Loader2
                  size={16}
                  className="animate-spin"
                />

                Generating...
              </>
            ) : (
              <>
                <CheckCircle2
                  size={16}
                />

                Generate action plan
              </>
            )}
          </button>

        </div>

      </div>

      {/* ================================================= */}
      {/* SUMMARY CARDS */}
      {/* ================================================= */}

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">

        <SummaryCard
          icon={
            <ShieldAlert
              size={18}
            />
          }
          label="Risks"
          value={risks.length}
          description={
            highRisks
              ? `${highRisks} high priority`
              : "No high priority risks"
          }
          danger={
            highRisks > 0
          }
        />

        <SummaryCard
          icon={
            <AlertTriangle
              size={18}
            />
          }
          label="Missing information"
          value={
            missingInformation.length
          }
          description="Items requiring attention"
          danger={
            missingInformation.length >
            0
          }
        />

        <SummaryCard
          icon={
            <Users size={18} />
          }
          label="Parties"
          value={
            parties.length
          }
          description="Identified participants"
        />

        <SummaryCard
          icon={
            <CalendarClock
              size={18}
            />
          }
          label="Deadlines"
          value={
            deadlines.length
          }
          description="Dates and obligations"
        />

      </div>

      {/* ================================================= */}
      {/* RISKS */}
      {/* ================================================= */}

      {risks.length > 0 && (
        <div className="rounded-3xl border border-zinc-200 bg-white p-6 shadow-sm">

          <SectionHeader
            icon={
              <ShieldAlert
                size={16}
              />
            }
            title="Risk assessment"
            count={
              risks.length
            }
          />

          <div className="mt-5 space-y-3">

            {risks.map(
              (risk, index) => {
                const styles =
                  severityClasses(
                    risk.severity
                  );

                return (
                  <div
                    key={`${risk.title}-${index}`}
                    className={`rounded-2xl border ${styles.border} p-4`}
                  >

                    <div className="flex items-start gap-3">

                      <div
                        className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl ${styles.icon}`}
                      >
                        <AlertTriangle
                          size={17}
                        />
                      </div>

                      <div className="min-w-0 flex-1">

                        <div className="flex flex-wrap items-center gap-2">

                          <h4 className="text-sm font-semibold text-zinc-900">
                            {risk.title}
                          </h4>

                          <span
                            className={`rounded-full px-2 py-0.5 text-[11px] font-semibold ring-1 ${styles.badge}`}
                          >
                            {risk.severity ||
                              "medium"}
                          </span>

                          {risk.category && (
                            <span className="rounded-full bg-zinc-100 px-2 py-0.5 text-[11px] text-zinc-500">
                              {risk.category}
                            </span>
                          )}

                        </div>

                        <p className="mt-2 text-sm leading-6 text-zinc-600">
                          {risk.explanation}
                        </p>

                        {risk.evidence && (
                          <div className="mt-3 rounded-xl bg-zinc-50 p-3">

                            <p className="text-[11px] font-semibold uppercase tracking-wider text-zinc-400">
                              Evidence
                            </p>

                            <p className="mt-1 text-xs leading-5 text-zinc-600">
                              “{risk.evidence}”
                            </p>

                          </div>
                        )}

                      </div>

                    </div>

                  </div>
                );
              }
            )}

          </div>

        </div>
      )}

      {/* ================================================= */}
      {/* MISSING INFORMATION */}
      {/* ================================================= */}

      {missingInformation.length >
        0 && (
        <div className="rounded-3xl border border-amber-200 bg-amber-50/40 p-6">

          <SectionHeader
            icon={
              <AlertTriangle
                size={16}
              />
            }
            title="Missing information"
            count={
              missingInformation.length
            }
          />

          <div className="mt-5 grid gap-3 lg:grid-cols-2">

            {missingInformation.map(
              (item, index) => (
                <div
                  key={`${item.item}-${index}`}
                  className="rounded-2xl border border-amber-200 bg-white p-4"
                >

                  <p className="text-sm font-semibold text-zinc-900">
                    {item.item}
                  </p>

                  <p className="mt-2 text-xs leading-5 text-zinc-600">
                    {item.reason}
                  </p>

                </div>
              )
            )}

          </div>

        </div>
      )}

      {/* ================================================= */}
      {/* PARTIES + KEY TERMS */}
      {/* ================================================= */}

      <div className="grid gap-6 lg:grid-cols-2">

        <div className="rounded-3xl border border-zinc-200 bg-white p-6 shadow-sm">

          <SectionHeader
            icon={
              <Users size={16} />
            }
            title="Parties"
            count={
              parties.length
            }
          />

          <div className="mt-5 space-y-3">

            {parties.length ===
            0 ? (
              <EmptyText text="No parties identified." />
            ) : (
              parties.map(
                (party, index) => (
                  <div
                    key={`${party.name}-${index}`}
                    className="rounded-2xl bg-zinc-50 p-4"
                  >

                    <p className="text-sm font-semibold text-zinc-900">
                      {party.name}
                    </p>

                    <p className="mt-1 text-xs text-zinc-500">
                      {party.role}
                    </p>

                  </div>
                )
              )
            )}

          </div>

        </div>

        <div className="rounded-3xl border border-zinc-200 bg-white p-6 shadow-sm">

          <SectionHeader
            icon={
              <Landmark size={16} />
            }
            title="Key terms"
            count={
              keyTerms.length
            }
          />

          <div className="mt-5 flex flex-wrap gap-2">

            {keyTerms.length ===
            0 ? (
              <EmptyText text="No key terms identified." />
            ) : (
              keyTerms.map(
                (term, index) => (
                  <span
                    key={`${term}-${index}`}
                    className="rounded-full bg-zinc-100 px-3 py-1.5 text-xs font-medium text-zinc-700"
                  >
                    {term}
                  </span>
                )
              )
            )}

          </div>

        </div>

      </div>

      {/* ================================================= */}
      {/* OBLIGATIONS */}
      {/* ================================================= */}

      <div className="rounded-3xl border border-zinc-200 bg-white p-6 shadow-sm">

        <SectionHeader
          icon={
            <CheckCircle2
              size={16}
            />
          }
          title="Obligations"
          count={
            obligations.length
          }
        />

        <div className="mt-5 space-y-3">

          {obligations.length ===
          0 ? (
            <EmptyText text="No obligations identified." />
          ) : (
            obligations.map(
              (item, index) => (
                <div
                  key={`${item.party}-${index}`}
                  className="grid gap-3 rounded-2xl bg-zinc-50 p-4 md:grid-cols-[160px_1fr]"
                >

                  <div>

                    <p className="text-xs font-semibold text-zinc-900">
                      {item.party}
                    </p>

                    {item.deadline && (
                      <p className="mt-1 text-xs text-zinc-400">
                        {item.deadline}
                      </p>
                    )}

                  </div>

                  <div>

                    <p className="text-sm leading-6 text-zinc-700">
                      {item.obligation}
                    </p>

                    {item.evidence && (
                      <p className="mt-2 text-xs italic leading-5 text-zinc-400">
                        “{item.evidence}”
                      </p>
                    )}

                  </div>

                </div>
              )
            )
          )}

        </div>

      </div>

      {/* ================================================= */}
      {/* FINANCIAL TERMS + DEADLINES */}
      {/* ================================================= */}

      <div className="grid gap-6 lg:grid-cols-2">

        <div className="rounded-3xl border border-zinc-200 bg-white p-6 shadow-sm">

          <SectionHeader
            icon={
              <Landmark size={16} />
            }
            title="Financial terms"
            count={
              financialTerms.length
            }
          />

          <div className="mt-5 space-y-3">

            {financialTerms.length ===
            0 ? (
              <EmptyText text="No financial terms identified." />
            ) : (
              financialTerms.map(
                (term, index) => (
                  <div
                    key={`${term.description}-${index}`}
                    className="rounded-2xl bg-zinc-50 p-4"
                  >

                    <p className="text-sm font-medium text-zinc-900">
                      {term.description}
                    </p>

                    <div className="mt-2 flex flex-wrap gap-3 text-xs text-zinc-500">

                      {term.amount && (
                        <span>
                          Amount:{" "}
                          <strong className="text-zinc-700">
                            {term.amount}
                          </strong>
                        </span>
                      )}

                      {term.frequency && (
                        <span>
                          Frequency:{" "}
                          <strong className="text-zinc-700">
                            {term.frequency}
                          </strong>
                        </span>
                      )}

                    </div>

                    {term.evidence && (
                      <p className="mt-2 text-xs italic text-zinc-400">
                        “{term.evidence}”
                      </p>
                    )}

                  </div>
                )
              )
            )}

          </div>

        </div>

        <div className="rounded-3xl border border-zinc-200 bg-white p-6 shadow-sm">

          <SectionHeader
            icon={
              <CalendarClock
                size={16}
              />
            }
            title="Deadlines"
            count={
              deadlines.length
            }
          />

          <div className="mt-5 space-y-2">

            {deadlines.length ===
            0 ? (
              <EmptyText text="No explicit deadlines identified." />
            ) : (
              deadlines.map(
                (deadline, index) => (
                  <div
                    key={`${deadline}-${index}`}
                    className="flex items-center gap-3 rounded-xl bg-zinc-50 px-4 py-3"
                  >

                    <CalendarClock
                      size={16}
                      className="shrink-0 text-zinc-400"
                    />

                    <p className="text-sm text-zinc-700">
                      {deadline}
                    </p>

                  </div>
                )
              )
            )}

          </div>

        </div>

      </div>

    </div>
  );
}

function SummaryCard({
  icon,
  label,
  value,
  description,
  danger = false,
}) {
  return (
    <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm">

      <div className="flex items-center justify-between">

        <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-zinc-100 text-zinc-600">
          {icon}
        </div>

        {danger && (
          <span className="h-2 w-2 rounded-full bg-red-500" />
        )}

      </div>

      <p className="mt-4 text-xs font-medium text-zinc-400">
        {label}
      </p>

      <p className="mt-1 text-2xl font-semibold tracking-tight text-zinc-900">
        {value}
      </p>

      <p className="mt-1 text-xs text-zinc-500">
        {description}
      </p>

    </div>
  );
}

function EmptyText({
  text,
}) {
  return (
    <p className="rounded-xl bg-zinc-50 p-4 text-sm text-zinc-400">
      {text}
    </p>
  );
}