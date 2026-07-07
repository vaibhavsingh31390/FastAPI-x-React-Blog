import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";

const blockRegistry = {
  heading({ level = 2, text = "" }) {
    const tag = `h${level}`;
    return createElement(tag, null, text);
  },
  paragraph({ text = "" }) {
    return createElement("p", null, text);
  },
  cta({ label = "", href = "#" }) {
    return createElement("a", { href, className: "content-cta" }, label);
  },
  image({ src = "", alt = "" }) {
    return createElement("img", { src, alt, loading: "lazy" });
  },
};

function renderBlocks(blocks) {
  return blocks
    .map((block) => {
      const renderer = blockRegistry[block.type];
      if (!renderer) {
        throw new Error(`Unsupported block type: ${block.type}`);
      }
      return renderToStaticMarkup(renderer(block.props ?? {}));
    })
    .join("");
}

async function main() {
  const input = await new Promise((resolve, reject) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => {
      data += chunk;
    });
    process.stdin.on("end", () => resolve(data));
    process.stdin.on("error", reject);
  });

  const blocks = JSON.parse(input);
  if (!Array.isArray(blocks)) {
    throw new Error("Blocks payload must be a JSON array");
  }

  process.stdout.write(renderBlocks(blocks));
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
