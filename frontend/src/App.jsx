import { useState, useRef, useCallback } from "react";
import ReactMarkdown from "react-markdown";
import {
  Upload,
  Briefcase,
  Brain,
  Sparkles,
  Loader2,
  CheckCircle2,
  MapPin,
  FileText,
  ArrowRight,
  ShieldCheck,
  Star,
  BadgeCheck,
  AlertCircle,
  Search,
  Target,
  TrendingUp,
} from "lucide-react";

const API_URL = import.meta.env.VITE_API_URL;

const loadingSteps = [
  "Parsing resume...",
  "Extracting skills...",
  "Running semantic search...",
  "Ranking opportunities...",
  "Preparing AI recommendations...",
];

function ScoreBadge({ score }) {
  return (
    <div className="relative flex h-16 w-16 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-blue-600 to-blue-500 shadow-lg shadow-blue-200">
      <span className="text-lg font-bold text-white">{score}%</span>
    </div>
  );
}

function SkillPill({ label, kind }) {
  const isMatched = kind === "matched";
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-medium ${
        isMatched
          ? "bg-emerald-50 text-emerald-700 ring-1 ring-inset ring-emerald-200"
          : "bg-red-50 text-red-700 ring-1 ring-inset ring-red-200"
      }`}
    >
      {isMatched ? (
        <CheckCircle2 className="h-3.5 w-3.5" />
      ) : (
        <AlertCircle className="h-3.5 w-3.5" />
      )}
      {label}
    </span>
  );
}

export default function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState("");

  const [adviceLoading, setAdviceLoading] = useState(false);
  const [advice, setAdvice] = useState("");
  const [adviceError, setAdviceError] = useState("");

  const [activeJobIndex, setActiveJobIndex] = useState(null);
  const [loadingStepIndex, setLoadingStepIndex] = useState(0);
  const [isDragging, setIsDragging] = useState(false);

  const fileInputRef = useRef(null);
  const uploadSectionRef = useRef(null);
  const careerCoachRef = useRef(null);
  const stepTimerRef = useRef(null);

  const scrollToUpload = () => {
    uploadSectionRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const startLoadingSequence = () => {
    setLoadingStepIndex(0);
    let step = 0;
    stepTimerRef.current = setInterval(() => {
      step = Math.min(step + 1, loadingSteps.length - 1);
      setLoadingStepIndex(step);
    }, 900);
  };

  const stopLoadingSequence = () => {
    if (stepTimerRef.current) {
      clearInterval(stepTimerRef.current);
      stepTimerRef.current = null;
    }
  };

  const handleFileSelect = (selected) => {
    if (!selected) return;
    setFile(selected);
    setError("");
    setResults(null);
    setAdvice("");
    setAdviceError("");
  };

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
    const dropped = e.dataTransfer.files?.[0];
    if (dropped) handleFileSelect(dropped);
  }, []);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError("");
    setResults(null);
    setAdvice("");
    setAdviceError("");
    startLoadingSequence();

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_URL}/jobs/match`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed with status ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(
        err?.message || "We couldn't analyze your resume. Please try again."
      );
    } finally {
      stopLoadingSequence();
      setLoading(false);
    }
  };

  const handleGetAdvice = async (jobIndex) => {
    setActiveJobIndex(jobIndex);
    setAdviceLoading(true);
    setAdviceError("");
    setAdvice("");

    try {
      const response = await fetch(
        `${API_URL}/career-coach/?job_index=${jobIndex}`,
        { method: "POST" }
      );

      if (!response.ok) {
        throw new Error(`Career coach request failed with status ${response.status}`);
      }

      const data = await response.json();
      setAdvice(data.career_advice || "");
      setTimeout(() => {
        careerCoachRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 100);
    } catch (err) {
      setAdviceError(
        err?.message || "We couldn't generate career advice right now."
      );
    } finally {
      setAdviceLoading(false);
    }
  };

  const progressPercent = ((loadingStepIndex + 1) / loadingSteps.length) * 100;

  return (
    <div className="min-h-screen bg-white text-slate-900 antialiased">
      {/* NAV */}
      <header className="sticky top-0 z-50 border-b border-slate-100 bg-white/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600">
              <Sparkles className="h-4 w-4 text-white" />
            </div>
            <span className="text-base font-semibold tracking-tight">SmartJob AI</span>
          </div>
          <button
            onClick={scrollToUpload}
            className="hidden items-center gap-1.5 rounded-full bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-800 sm:inline-flex"
          >
            Analyze Resume
            <ArrowRight className="h-3.5 w-3.5" />
          </button>
        </div>
      </header>

      {/* HERO */}
      <section className="relative overflow-hidden">
        <div className="pointer-events-none absolute inset-0 bg-gradient-to-b from-blue-50 via-white to-white" />
        <div className="pointer-events-none absolute -right-32 -top-32 h-96 w-96 rounded-full bg-blue-100/60 blur-3xl" />
        <div className="pointer-events-none absolute -left-24 top-40 h-72 w-72 rounded-full bg-blue-50 blur-3xl" />

        <div className="relative mx-auto max-w-6xl px-6 pb-20 pt-20 sm:pt-28">
          <div className="mx-auto max-w-3xl text-center">
            <div className="mx-auto inline-flex items-center gap-1.5 rounded-full border border-blue-200 bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700">
              <Sparkles className="h-3.5 w-3.5" />
              AI-Powered Career Intelligence
            </div>

            <h1 className="mt-6 text-4xl font-bold tracking-tight text-slate-900 sm:text-6xl">
              SmartJob AI
            </h1>

            <p className="mx-auto mt-5 max-w-xl text-lg leading-relaxed text-slate-500">
              AI-powered resume analysis, semantic job matching, and personalized
              career coaching.
            </p>

            <div className="mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row">
              <button
                onClick={scrollToUpload}
                className="inline-flex w-full items-center justify-center gap-2 rounded-full bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-200 transition hover:scale-[1.02] hover:bg-blue-700 sm:w-auto"
              >
                Analyze Resume
                <ArrowRight className="h-4 w-4" />
              </button>
            </div>

            <div className="mt-10 flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-xs font-medium text-slate-400">
              <span className="inline-flex items-center gap-1.5">
                <ShieldCheck className="h-3.5 w-3.5" /> Private &amp; secure
              </span>
              <span className="inline-flex items-center gap-1.5">
                <Target className="h-3.5 w-3.5" /> Semantic matching
              </span>
              <span className="inline-flex items-center gap-1.5">
                <TrendingUp className="h-3.5 w-3.5" /> Actionable coaching
              </span>
            </div>
          </div>

          {/* Decorative illustration */}
          <div className="relative mx-auto mt-16 hidden max-w-2xl sm:block">
            <div className="rounded-3xl border border-slate-100 bg-white p-6 shadow-2xl shadow-blue-100">
              <div className="flex items-center gap-3 border-b border-slate-100 pb-4">
                <div className="h-10 w-10 rounded-xl bg-blue-100" />
                <div className="flex-1 space-y-2">
                  <div className="h-2.5 w-1/3 rounded-full bg-slate-200" />
                  <div className="h-2 w-1/2 rounded-full bg-slate-100" />
                </div>
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-blue-600 to-blue-400 text-xs font-bold text-white">
                  94%
                </div>
              </div>
              <div className="grid grid-cols-3 gap-3 pt-4">
                {[0, 1, 2].map((i) => (
                  <div key={i} className="space-y-2 rounded-xl bg-slate-50 p-3">
                    <div className="h-2 w-2/3 rounded-full bg-slate-200" />
                    <div className="h-2 w-1/2 rounded-full bg-slate-200" />
                    <div className="h-6 w-6 rounded-full bg-blue-100" />
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* UPLOAD SECTION */}
      <section ref={uploadSectionRef} className="mx-auto max-w-3xl px-6 py-16 scroll-mt-20">
        <div
          onDragOver={(e) => {
            e.preventDefault();
            setIsDragging(true);
          }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleDrop}
          className={`group relative rounded-3xl border-2 border-dashed px-8 py-14 text-center transition ${
            isDragging
              ? "border-blue-400 bg-blue-50"
              : "border-slate-200 bg-slate-50/60 hover:border-blue-300 hover:bg-blue-50/40"
          }`}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            className="hidden"
            id="resume-upload"
            onChange={(e) => handleFileSelect(e.target.files?.[0])}
          />

          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-100 transition group-hover:scale-105">
            <Upload className="h-7 w-7 text-blue-600" />
          </div>

          <h2 className="mt-6 text-xl font-semibold text-slate-900">
            Drag &amp; Drop Resume
          </h2>
          <p className="mt-2 text-sm text-slate-500">Supports PDF</p>

          <label
            htmlFor="resume-upload"
            className="mt-6 inline-flex cursor-pointer items-center gap-2 rounded-full border border-slate-200 bg-white px-5 py-2.5 text-sm font-medium text-slate-700 shadow-sm transition hover:border-blue-300 hover:text-blue-700"
          >
            <FileText className="h-4 w-4" />
            Choose file
          </label>

          {file && (
            <div className="mx-auto mt-5 inline-flex items-center gap-2 rounded-full bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm ring-1 ring-slate-100">
              <FileText className="h-4 w-4 text-blue-600" />
              {file.name}
            </div>
          )}

          <div className="mt-8">
            <button
              onClick={handleUpload}
              disabled={!file || loading}
              className="inline-flex w-full items-center justify-center gap-2 rounded-full bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-200 transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-200 disabled:text-slate-400 disabled:shadow-none sm:w-auto"
            >
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Search className="h-4 w-4" />
              )}
              Analyze Resume
            </button>
          </div>
        </div>

        {error && (
          <div className="mt-6 flex items-start gap-3 rounded-2xl border border-red-200 bg-red-50 px-5 py-4">
            <AlertCircle className="mt-0.5 h-5 w-5 shrink-0 text-red-500" />
            <div>
              <p className="text-sm font-semibold text-red-700">
                Something went wrong
              </p>
              <p className="mt-0.5 text-sm text-red-600">{error}</p>
            </div>
          </div>
        )}

        {!results && !loading && !error && (
          <div className="mt-10 flex flex-col items-center text-center">
            <div className="flex -space-x-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-blue-100 ring-4 ring-white">
                <Briefcase className="h-5 w-5 text-blue-600" />
              </div>
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-blue-50 ring-4 ring-white">
                <Target className="h-5 w-5 text-blue-500" />
              </div>
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-blue-100 ring-4 ring-white">
                <TrendingUp className="h-5 w-5 text-blue-600" />
              </div>
            </div>
            <p className="mt-4 max-w-sm text-sm text-slate-500">
              Upload your resume to discover your best career opportunities.
            </p>
          </div>
        )}
      </section>

      {/* LOADING */}
      {loading && (
        <section className="mx-auto max-w-2xl px-6 pb-16">
          <div className="rounded-3xl border border-blue-100 bg-blue-50/50 px-8 py-12 text-center">
            <Loader2 className="mx-auto h-9 w-9 animate-spin text-blue-600" />
            <p
              key={loadingStepIndex}
              className="mt-5 animate-[fadeIn_0.4s_ease-in-out] text-base font-medium text-slate-700"
            >
              {loadingSteps[loadingStepIndex]}
            </p>
            <div className="mx-auto mt-6 h-1.5 w-full max-w-sm overflow-hidden rounded-full bg-blue-100">
              <div
                className="h-full rounded-full bg-blue-600 transition-all duration-700 ease-out"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
          </div>
          <style>{`
            @keyframes fadeIn {
              from { opacity: 0; transform: translateY(4px); }
              to { opacity: 1; transform: translateY(0); }
            }
          `}</style>
        </section>
      )}

      {/* RESULTS */}
      {results && (
        <section className="mx-auto max-w-6xl px-6 pb-20">
          <div className="mx-auto max-w-xl text-center">
            <h2 className="text-3xl font-bold tracking-tight text-slate-900">
              Best Job Matches
            </h2>
            <p className="mt-2 text-sm text-slate-500">
              We found opportunities aligned with your skills.
            </p>
          </div>

          <div className="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {results.matches?.map((job, index) => (
              <div
                key={index}
                className="flex flex-col rounded-3xl border border-slate-100 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-xl hover:shadow-blue-100"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="min-w-0">
                    <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-50">
                      <Briefcase className="h-4 w-4 text-blue-600" />
                    </div>
                    <h3 className="mt-3 truncate text-base font-semibold text-slate-900">
                      {job.title}
                    </h3>
                    <p className="text-sm text-slate-500">{job.company}</p>
                    <p className="mt-1 flex items-center gap-1 text-xs text-slate-400">
                      <MapPin className="h-3.5 w-3.5" />
                      {job.location}
                    </p>
                  </div>
                  <ScoreBadge score={job.overall_score} />
                </div>

                {job.matched_skills?.length > 0 && (
                  <div className="mt-5">
                    <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                      Matched Skills
                    </p>
                    <div className="mt-2 flex flex-wrap gap-2">
                      {job.matched_skills.map((skill, i) => (
                        <SkillPill key={i} label={skill} kind="matched" />
                      ))}
                    </div>
                  </div>
                )}

                {job.missing_skills?.length > 0 && (
                  <div className="mt-4">
                    <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                      Missing Skills
                    </p>
                    <div className="mt-2 flex flex-wrap gap-2">
                      {job.missing_skills.map((skill, i) => (
                        <SkillPill key={i} label={skill} kind="missing" />
                      ))}
                    </div>
                  </div>
                )}

                <button
                  onClick={() => handleGetAdvice(index)}
                  disabled={adviceLoading && activeJobIndex === index}
                  className="mt-6 inline-flex items-center justify-center gap-2 rounded-full border border-blue-200 bg-blue-50 px-4 py-2.5 text-sm font-semibold text-blue-700 transition hover:bg-blue-100 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {adviceLoading && activeJobIndex === index ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Brain className="h-4 w-4" />
                  )}
                  Get AI Career Advice
                </button>
              </div>
            ))}
          </div>
        </section>
      )}

{/* CAREER COACH */}
      {(advice || adviceError) && (
        <section ref={careerCoachRef} className="mx-auto max-w-4xl px-6 pb-24 scroll-mt-20">
          <div className="rounded-3xl border border-blue-100 bg-blue-50/50 p-8 sm:p-10">
            <div className="flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-600 shadow-lg shadow-blue-200">
                <Brain className="h-6 w-6 text-white" />
              </div>
              <div>
                <h2 className="text-xl font-bold tracking-tight text-slate-900">
                  AI Career Coach
                </h2>
                <p className="text-sm text-slate-500">
                  Personalized recommendations generated from your resume.
                </p>
              </div>
            </div>

            {adviceError ? (
              <div className="mt-6 flex items-start gap-3 rounded-2xl border border-red-200 bg-red-50 px-5 py-4">
                <AlertCircle className="mt-0.5 h-5 w-5 shrink-0 text-red-500" />
                <div>
                  <p className="text-sm font-semibold text-red-700">
                    Couldn't generate advice
                  </p>
                  <p className="mt-0.5 text-sm text-red-600">{adviceError}</p>
                </div>
              </div>
            ) : (
              <div className="mt-6 max-w-none rounded-2xl bg-white p-6 text-slate-700 leading-relaxed [&_h1]:text-2xl [&_h1]:font-bold [&_h1]:mt-6 [&_h1]:mb-3 [&_h1]:text-slate-900 [&_h2]:text-xl [&_h2]:font-bold [&_h2]:mt-6 [&_h2]:mb-3 [&_h2]:text-slate-900 [&_h3]:text-lg [&_h3]:font-semibold [&_h3]:mt-4 [&_h3]:mb-2 [&_h3]:text-slate-900 [&_p]:mb-3 [&_ul]:list-disc [&_ul]:pl-5 [&_ul]:mb-3 [&_ol]:list-decimal [&_ol]:pl-5 [&_ol]:mb-3 [&_li]:mb-1 [&_strong]:font-semibold [&_strong]:text-slate-900 [&_code]:rounded [&_code]:bg-slate-100 [&_code]:px-1.5 [&_code]:py-0.5 [&_code]:text-sm [&_hr]:my-6 [&_hr]:border-slate-200">
                <ReactMarkdown>{advice}</ReactMarkdown>
              </div>
            )}
          </div>
        </section>
      )}

      {/* FOOTER */}
      <footer className="border-t border-slate-100">
        <div className="mx-auto max-w-6xl px-6 py-12">
          <div className="flex flex-col items-center justify-between gap-6 sm:flex-row">
            <div>
              <div className="flex items-center gap-2">
                <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-blue-600">
                  <Sparkles className="h-3.5 w-3.5 text-white" />
                </div>
                <span className="text-sm font-semibold tracking-tight">
                  SmartJob AI
                </span>
              </div>
              <p className="mt-2 max-w-xs text-xs text-slate-400">
                AI-powered resume analysis and semantic job matching for
                modern job seekers.
              </p>
            </div>

            <div className="flex items-center gap-6 text-xs font-medium text-slate-500">
              <a href="#" className="transition hover:text-blue-600">
                Privacy
              </a>
              <a href="#" className="transition hover:text-blue-600">
                Terms
              </a>
              <a href="#" className="transition hover:text-blue-600">
                GitHub
              </a>
              <a href="#" className="transition hover:text-blue-600">
                LinkedIn
              </a>
            </div>
          </div>

          <div className="mt-8 flex items-center justify-center gap-1.5 border-t border-slate-100 pt-6 text-xs text-slate-400 sm:justify-start">
            <BadgeCheck className="h-3.5 w-3.5" />
            <span>&copy; {new Date().getFullYear()} SmartJob AI. All rights reserved.</span>
          </div>
        </div>
      </footer>
    </div>
  );
}