// Builds ATS-friendly single-column CVs (.docx) from cv_content.js.
// Usage: node build_cv.js <outdir>
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat, BorderStyle,
  TabStopType, ExternalHyperlink,
} = require("docx");
const { EN, FR } = require("./cv_content");

const FONT = "Calibri";
const SZ = 19;       // 9.5pt body
const RIGHT = 10466; // A4 width 11906 - margins 720*2

const p = (children, opts = {}) => new Paragraph({ children, ...opts });
const t = (text, o = {}) => new TextRun({ text, font: FONT, size: SZ, ...o });
// rich text: string, or [[text, url?], ...] — segments with a url become clickable links
const rich = (x, o = {}) => (typeof x === "string" ? [t(x, o)] : x.map(([text, url]) => (url
  ? new ExternalHyperlink({ link: url, children: [t(text, { ...o, color: "1F4E99", underline: {} })] })
  : t(text, o))));

function heading(text) {
  return p([t(text, { bold: true, size: 21, color: "1F3864" })], {
    spacing: { before: 120, after: 40 },
    keepNext: true,
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "1F3864", space: 1 } },
  });
}

function titleLine(left, right, bold = true, italic = false) {
  const kids = rich(left, { bold, italics: italic });
  if (right) kids.push(t("\t" + right, { bold: false, italics: italic }));
  return p(kids, {
    tabStops: [{ type: TabStopType.RIGHT, position: RIGHT }],
    spacing: { before: 60, after: 0 },
    keepNext: true,
  });
}

function bullet(text) {
  return p(rich(text), { numbering: { reference: "bullets", level: 0 }, spacing: { after: 10 } });
}

function entry(e) {
  const out = [titleLine(e.title, e.right, true)];
  if (e.sub) out.push(titleLine(e.sub, e.subRight || "", false, true));
  (e.bullets || []).forEach((b) => out.push(bullet(b)));
  if (e.stack) out.push(p([t(e.stack, { italics: true, color: "404040" })], { spacing: { after: 20 } }));
  return out;
}

function build(C) {
  const kids = [];
  kids.push(p([t(C.name, { bold: true, size: 36 })], { alignment: AlignmentType.CENTER, spacing: { after: 0 } }));
  kids.push(p([t(C.headline, { bold: true, size: 21, color: "1F3864" })], { alignment: AlignmentType.CENTER, spacing: { after: 20 } }));
  kids.push(p(rich(C.contact, { size: 18 }), { alignment: AlignmentType.CENTER, spacing: { after: 40 } }));
  kids.push(p([t(C.seeking, { bold: true, size: 20 })], {
    alignment: AlignmentType.CENTER, spacing: { after: 0 },
    shading: { type: "clear", fill: "E8EEF7", color: "auto" },
  }));
  kids.push(p([t(C.seekingSub, { italics: true, size: 18 })], {
    alignment: AlignmentType.CENTER, spacing: { after: 40 },
    shading: { type: "clear", fill: "E8EEF7", color: "auto" },
  }));

  kids.push(heading(C.h.profile));
  kids.push(p([t(C.profile)], { alignment: AlignmentType.JUSTIFIED }));

  kids.push(heading(C.h.edu));
  C.education.forEach((e) => kids.push(...entry(e)));

  kids.push(heading(C.h.exp));
  C.experience.forEach((e) => kids.push(...entry(e)));

  kids.push(heading(C.h.proj));
  C.projects.forEach((e) => kids.push(...entry(e)));

  kids.push(heading(C.h.skills));
  C.skills.forEach(([k, v]) => kids.push(p([t(k + ": ", { bold: true }), t(v)], { spacing: { after: 10 } })));

  kids.push(heading(C.h.cert));
  C.certs.forEach((c) => kids.push(bullet(c)));

  kids.push(heading(C.h.lang));
  kids.push(p([t(C.languages)]));

  return new Document({
    creator: "Hazem Ilahi",
    title: `CV ${C.name}`,
    styles: { default: { document: { run: { font: FONT, size: SZ } } } },
    numbering: {
      config: [{
        reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 284, hanging: 200 } } },
        }],
      }],
    },
    sections: [{
      properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 600, bottom: 600, left: 720, right: 720 } } },
      children: kids,
    }],
  });
}

const outDir = process.argv[2] || ".";
(async () => {
  for (const [C, name] of [[EN, "Hazem_Ilahi_CV_EN.docx"], [FR, "Hazem_Ilahi_CV_FR.docx"]]) {
    const buf = await Packer.toBuffer(build(C));
    fs.writeFileSync(path.join(outDir, name), buf);
    console.log("wrote", name);
  }
})();
