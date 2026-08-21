import {
  AlertCircle,
  CheckCircle2,
  Eye,
  ShieldCheck,
  Zap,
  Clock3,
  ArrowRight,
} from "lucide-react";

function priorityClasses(priority) {
  switch (
    String(priority || "").toLowerCase()
  ) {
    case "critical":
      return {
        badge:
          "bg-red-50 text-red-700 ring-red-200",
        border:
          "border-red-200",
        dot:
          "bg-red-500",
      };

    case "high":
      return {
        badge:
          "bg-orange-50 text-orange-700 ring-orange-200",
        border:
          "border-orange-200",
        dot:
          "bg-orange-500",
      };

    case "medium":
      return {
        badge:
          "bg-amber-50 text-amber-700 ring-amber-200",
        border:
          "border-amber-200",
        dot:
          "bg-amber-500",
      };

    default:
      return {
        badge:
          "bg-zinc-100 text-zinc-600 ring-zinc-200",
        border:
          "border-zinc-200",
        dot:
          "bg-zinc-400",
      };
  }
}

function ActionCard({
  action,
}) {
  const styles =
    priorityClasses(
      action.priority
    );

  return (
    <div
      className={`rounded-2xl border ${styles.border} bg-white p-4`}
    >

      <div className="flex items-start gap-3">

        <span
          className={`mt-1 h-2.5 w-2.5 shrink-0 rounded-full ${styles.dot}`}
        />

        <div className="min-w-0 flex-1">

          <div className="flex flex-wrap items-center gap-2">

            <h4 className="text-sm font-semibold text-zinc-900">
              {action.title ||
                "Action"}
            </h4>

            <span
              className={`rounded-full px-2 py-0.5 text-[11px] font-semibold ring-1 ${styles.badge}`}
            >
              {action.priority ||
                "medium"}
            </span>

            {action.requires_human_approval && (
              <span className="inline-flex items-center gap-1 rounded-full bg-purple-50 px-2 py-0.5 text-[11px] font-medium text-purple-700">
                <ShieldCheck
                  size={11}
                />
                Human approval
              </span>
            )}

          </div>

          <p className="mt-2 text-sm leading-6 text-zinc-600">
            {action.action}
          </p>

          {action.reason && (
            <div className="mt-3">

              <p className="text-[11px] font-semibold uppercase tracking-wider text-zinc-400">
                Why
              </p>

              <p className="mt-1 text-xs leading-5 text-zinc-500">
                {action.reason}
              </p>

            </div>
          )}

          {action.evidence && (
            <div className="mt-3 rounded-xl bg-zinc-50 p-3">

              <p className="text-[11px] font-semibold uppercase tracking-wider text-zinc-400">
                Evidence
              </p>

              <p className="mt-1 text-xs leading-5 text-zinc-600">
                “{action.evidence}”
              </p>

            </div>
          )}

          {action.source && (
            <p className="mt-3 text-[11px] text-zinc-400">
              Source:{" "}
              <span className="font-medium text-zinc-500">
                {action.source}
              </span>
            </p>
          )}

        </div>

      </div>

    </div>
  );
}

function ActionSection({
  icon,
  title,
  description,
  actions,
}) {
  return (
    <div>

      <div className="mb-4 flex items-start gap-3">

        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-zinc-100 text-zinc-600">
          {icon}
        </div>

        <div>

          <h3 className="text-sm font-semibold text-zinc-900">
            {title}
          </h3>

          <p className="mt-1 text-xs text-zinc-400">
            {description}
          </p>

        </div>

      </div>

      <div className="space-y-3">

        {actions.length ===
        0 ? (
          <div className="rounded-2xl bg-zinc-50 p-4 text-sm text-zinc-400">
            No actions identified.
          </div>
        ) : (
          actions.map(
            (action, index) => (
              <ActionCard
                key={`${action.title}-${index}`}
                action={action}
              />
            )
          )
        )}

      </div>

    </div>
  );
}

export default function WorkflowPanel({
  workflow,
}) {
  if (!workflow) {
    return null;
  }

  const readiness =
    workflow.readiness_status ||
    "insufficient_information";

  const readinessConfig = {
    ready: {
      label: "Ready",
      className:
        "bg-emerald-50 text-emerald-700",
      icon:
        <CheckCircle2 size={18} />,
    },

    conditionally_ready: {
      label:
        "Conditionally ready",
      className:
        "bg-amber-50 text-amber-700",
      icon:
        <AlertCircle size={18} />,
    },

    not_ready: {
      label: "Not ready",
      className:
        "bg-red-50 text-red-700",
      icon:
        <AlertCircle size={18} />,
    },

    insufficient_information: {
      label:
        "Insufficient information",
      className:
        "bg-zinc-100 text-zinc-600",
      icon:
        <Eye size={18} />,
    },
  };

  const readinessData =
    readinessConfig[
      readiness
    ] ||
    readinessConfig.insufficient_information;

  const immediateActions =
    workflow.immediate_actions ||
    [];

  const upcomingActions =
    workflow.upcoming_actions ||
    [];

  const monitoringItems =
    workflow.monitoring_items ||
    [];

  return (
    <div className="space-y-6">

      {/* ================================================= */}
      {/* HEADER */}
      {/* ================================================= */}

      <div className="rounded-3xl border border-zinc-200 bg-white p-6 shadow-sm">

        <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">

          <div className="max-w-3xl">

            <div className="flex items-center gap-2">

              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-zinc-900 text-white">
                <Zap size={18} />
              </div>

              <div>

                <p className="text-xs font-semibold uppercase tracking-wider text-zinc-400">
                  Workflow Agent
                </p>

                <h2 className="text-lg font-semibold text-zinc-900">
                  Action plan
                </h2>

              </div>

            </div>

            <p className="mt-4 text-sm leading-6 text-zinc-600">
              {workflow.overall_assessment ||
                "No overall assessment was returned."}
            </p>

          </div>

          <div
            className={`flex shrink-0 items-center gap-2 rounded-full px-4 py-2 text-sm font-semibold ${readinessData.className}`}
          >
            {readinessData.icon}
            {readinessData.label}
          </div>

        </div>

      </div>

      {/* ================================================= */}
      {/* HUMAN APPROVAL */}
      {/* ================================================= */}

      {workflow.human_approval_required && (
        <div className="rounded-3xl border border-purple-200 bg-purple-50/50 p-6">

          <div className="flex items-start gap-3">

            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-purple-100 text-purple-700">
              <ShieldCheck
                size={19}
              />
            </div>

            <div>

              <h3 className="text-sm font-semibold text-purple-900">
                Human approval required
              </h3>

              <p className="mt-1 text-sm leading-6 text-purple-800">
                {workflow.approval_reason ||
                  "One or more actions require human review before execution."}
              </p>

            </div>

          </div>

        </div>
      )}

      {/* ================================================= */}
      {/* ACTION SUMMARY */}
      {/* ================================================= */}

      <div className="grid gap-4 sm:grid-cols-3">

        <WorkflowMetric
          icon={
            <Zap size={17} />
          }
          label="Immediate"
          value={
            immediateActions.length
          }
        />

        <WorkflowMetric
          icon={
            <ArrowRight
              size={17}
            />
          }
          label="Upcoming"
          value={
            upcomingActions.length
          }
        />

        <WorkflowMetric
          icon={
            <Clock3
              size={17}
            />
          }
          label="Monitor"
          value={
            monitoringItems.length
          }
        />

      </div>

      {/* ================================================= */}
      {/* ACTIONS */}
      {/* ================================================= */}

      <div className="rounded-3xl border border-zinc-200 bg-white p-6 shadow-sm">

        <div className="space-y-8">

          <ActionSection
            icon={
              <Zap size={16} />
            }
            title="Immediate actions"
            description="Resolve these items first."
            actions={
              immediateActions
            }
          />

          <div className="border-t border-zinc-100" />

          <ActionSection
            icon={
              <ArrowRight
                size={16}
              />
            }
            title="Upcoming actions"
            description="Actions to complete after the immediate issues are addressed."
            actions={
              upcomingActions
            }
          />

          <div className="border-t border-zinc-100" />

          <ActionSection
            icon={
              <Eye size={16} />
            }
            title="Monitoring"
            description="Information that should continue to be watched."
            actions={
              monitoringItems
            }
          />

        </div>

      </div>

    </div>
  );
}

function WorkflowMetric({
  icon,
  label,
  value,
}) {
  return (
    <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm">

      <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-zinc-100 text-zinc-600">
        {icon}
      </div>

      <p className="mt-4 text-xs text-zinc-400">
        {label}
      </p>

      <p className="mt-1 text-2xl font-semibold">
        {value}
      </p>

    </div>
  );
}