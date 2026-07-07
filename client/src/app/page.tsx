export default function Home() {
  return (
    <main className="page-shell flex-1">
      <p className="text-sm font-medium uppercase tracking-[0.2em] text-accent">
        FastAPI x Next.js
      </p>
      <h1 className="page-title">Blog frontend is ready</h1>
      <p className="page-lead">
        Next.js 16 with Tailwind CSS and SCSS is configured. Connect it to the
        FastAPI backend at{" "}
        <code className="rounded bg-black/5 px-2 py-1 text-sm dark:bg-white/10">
          {process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}
        </code>{" "}
        and start building public pages, auth, and the dashboard.
      </p>
    </main>
  );
}
