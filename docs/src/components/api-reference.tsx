import { fileURLToPath } from "node:url";

import { createOpenAPI } from "fumadocs-openapi/server";
import { createOpenAPIPage } from "fumadocs-openapi/ui";

/**
 * `spec.json` lives in `packages/sdks/common`, outside the docs app root.
 * We resolve it through `import.meta.url` so the docs build can load the shared
 * OpenAPI spec without hardcoding a runtime-relative path.
 */
const specPath = fileURLToPath(new URL("../../../packages/sdks/common/spec.json", import.meta.url));

/**
 * Fumadocs OpenAPI server wrapper for the shared Devopness spec.
 * The spec is loaded from the generated shared JSON file and exposed as
 * virtual Fumadocs pages under `/docs/api`.
 */
const openapi = createOpenAPI({
  input: {
    devopness: specPath,
  },
});

const OpenAPIPage = createOpenAPIPage();

/**
 * Generate the virtual OpenAPI source once at module load.
 * This keeps the page component simple and lets the build render the API docs
 * from the shared spec without additional runtime wiring.
 */
const apiSourcePromise = openapi.staticSource({
  baseDir: "api",
  per: "file",
  name: () => "index",
});

export async function ApiReference() {
  const apiSource = await apiSourcePromise;
  const page = apiSource.files.find(
    (file) => file.type === "page" && file.path === "api/index.mdx",
  );

  if (!page || page.type !== "page") {
    return null;
  }

  return <OpenAPIPage {...page.data.getOpenAPIPageProps()} />;
}
