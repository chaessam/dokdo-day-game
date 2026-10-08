// 빌드: src/game.html → index.html (+ vendor/three.module.min.js)
// 학교 태블릿처럼 오래된 브라우저에서도 돌도록 자바스크립트·CSS 문법을 낮춰서 내보낸다.
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import * as esbuild from "esbuild";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const TARGETS = ["chrome70", "safari12", "ios12", "firefox68", "edge79"];

// esbuild가 낮추지 못하는 CSS를 오래된 브라우저용으로 보완한다.
// 1) clamp()/min()/max() 앞에 단순한 대체값을 한 줄 더 넣는다 (크롬 79·사파리 13.1 미만 대비)
// 2) padding-inline / padding-block 을 left·right / top·bottom 으로 풀어 쓴다 (크롬 87·사파리 14.1 미만 대비)
function splitTop(str) {
  const out = []; let depth = 0, cur = "";
  for (const ch of str) {
    if (ch === "(") depth++;
    if (ch === ")") depth--;
    if ((ch === "," || ch === " ") && depth === 0) { if (cur.trim()) out.push(cur.trim()); cur = ""; if (ch === ",") out.push(","); continue; }
    cur += ch;
  }
  if (cur.trim()) out.push(cur.trim());
  return out;
}
function simpleValue(v) {
  // 함수 안의 첫 번째 단순 값(px, %, vw 등)을 고른다
  return v.replace(/(clamp|min|max)\(([^()]*(?:\([^()]*\)[^()]*)*)\)/g, (m, fn, inner) => {
    const parts = inner.split(",").map((x) => x.trim());
    const px = parts.filter((x) => /^-?[\d.]+px$/.test(x)).map(parseFloat);
    if (fn === "clamp" && px.length >= 2) return Math.round((px[0] + px[px.length - 1]) / 2) + "px";
    if (fn === "clamp" && px.length === 1) return parts[2] && /^-?[\d.]+px$/.test(parts[2]) ? parts[2] : px[0] + "px";
    if (fn === "min") return parts.find((x) => /(%|vw|vh)$/.test(x) && !x.includes("(")) || parts.find((x) => /px$/.test(x) && !x.includes("(")) || parts[0];
    if (fn === "max") return parts.find((x) => /px$/.test(x)) || parts[0];
    return parts[0];
  });
}
function legacyCss(css) {
  css = css.replace(/(^|[;{\s])(padding-inline|padding-block):\s*([^;}]+)/g, (m, pre, prop, val) => {
    const parts = splitTop(val.trim()).filter((x) => x !== ",");
    const a = parts[0], b = parts[1] || parts[0];
    const [s1, s2] = prop === "padding-inline" ? ["padding-left", "padding-right"] : ["padding-top", "padding-bottom"];
    return `${pre}${s1}: ${a}; ${s2}: ${b}`;
  });
  css = css.replace(/(^|[;{\s])([a-z-]+):\s*([^;}]*\b(?:clamp|min|max)\([^;}]*)/g, (m, pre, prop, val) => {
    if (prop.startsWith("--")) return m;
    const fb = simpleValue(val);
    if (/\b(clamp|min|max)\(/.test(fb)) return m;
    return `${pre}${prop}: ${fb}; ${prop}: ${val}`;
  });
  return css;
}


let src = readFileSync(join(root, "src/game.html"), "utf8");

// 실제로 있는 사진만 남긴다
src = src
  .split("\n")
  .filter((line) => {
    const m = line.match(/^\s+"((?:r|s)-[a-z]+)": \{ src: "(assets\/photos\/[^"]+)"/);
    return !m || existsSync(join(root, m[2]));
  })
  .join("\n");

// <style> 과 <script type="module"> 을 각각 변환
const styleRe = /<style>([\s\S]*?)<\/style>/;
const css = src.match(styleRe)[1];
const cssOut = legacyCss((await esbuild.transform(css, { loader: "css", target: TARGETS, charset: "utf8" })).code);
src = src.replace(styleRe, () => `<style>\n${cssOut}</style>`);

const scriptRe = /<script type="module">([\s\S]*?)<\/script>/;
const js = src.match(scriptRe)[1];
const jsOut = (await esbuild.transform(js, { loader: "js", target: TARGETS, charset: "utf8" })).code;
src = src.replace(scriptRe, () => `<script type="module">\n${jsOut}</script>`);

const nomodule = `<script nomodule>document.getElementById("loadMsg").className = "err"; document.getElementById("loadMsg").textContent = "이 브라우저는 너무 오래되어 게임을 열 수 없어요. 크롬, 삼성 인터넷, 사파리를 최신 버전으로 바꿔 주세요.";</script>\n`;
const body = src + "\n" + nomodule;

mkdirSync(join(root, "dist"), { recursive: true });
writeFileSync(join(root, "dist/artifact.html"), body);
writeFileSync(
  join(root, "index.html"),
  `<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="theme-color" content="#07111f">\n</head>\n<body>\n${body}</body>\n</html>\n`
);

// 3D 엔진(three.js r162: WebGL2가 없으면 WebGL1로 동작)도 같은 기준으로 변환해 함께 배포
mkdirSync(join(root, "vendor"), { recursive: true });
await esbuild.build({
  entryPoints: [join(root, "node_modules/three/build/three.module.js")],
  outfile: join(root, "vendor/three.module.min.js"),
  format: "esm", minify: true, target: TARGETS, legalComments: "inline", logLevel: "warning",
});
console.log("built index.html, dist/artifact.html, vendor/three.module.min.js");
