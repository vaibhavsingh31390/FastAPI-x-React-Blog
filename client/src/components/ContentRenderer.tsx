import type { ContentComponent } from "@/lib/content";

type ComponentRegistry = Record<
  string,
  (data: Record<string, unknown>) => React.ReactNode
>;

function renderHeading(data: Record<string, unknown>) {
  const level = Math.min(6, Math.max(1, Number(data.level ?? 2)));
  const text = String(data.text ?? "");

  switch (level) {
    case 1:
      return <h1>{text}</h1>;
    case 2:
      return <h2>{text}</h2>;
    case 3:
      return <h3>{text}</h3>;
    case 4:
      return <h4>{text}</h4>;
    case 5:
      return <h5>{text}</h5>;
    default:
      return <h6>{text}</h6>;
  }
}

const registry: ComponentRegistry = {
  Heading: renderHeading,
  Paragraph(data) {
    return <p>{String(data.text ?? "")}</p>;
  },
};

function renderComponent(component: ContentComponent, index: number) {
  const renderer = registry[component.name];

  if (!renderer) {
    return (
      <div
        key={`${component.name}-${index}`}
        className="rounded border border-red-300 p-3 text-sm"
      >
        Unknown component: {component.name}
      </div>
    );
  }

  return <div key={`${component.name}-${index}`}>{renderer(component.data)}</div>;
}

type ContentRendererProps = {
  components: ContentComponent[];
};

export function ContentRenderer({ components }: ContentRendererProps) {
  return (
    <article className="space-y-4">
      {components.map((component, index) => renderComponent(component, index))}
    </article>
  );
}
