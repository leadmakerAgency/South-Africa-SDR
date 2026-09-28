// Resolve /media/ featured_image paths to actual files in content/media/.
// n8n often commits images with a numeric suffix (e.g. -220375) while the
// post frontmatter references the unsuffixed filename.
const fs = require("fs");
const path = require("path");

const MEDIA_DIR = path.join(__dirname, "..", "content", "media");
const PUBLIC_PREFIX = "/media/";

let cachedMediaFiles = null;

const getMediaFiles = () => {
  if (cachedMediaFiles) return cachedMediaFiles;

  if (!fs.existsSync(MEDIA_DIR)) {
    cachedMediaFiles = [];
    return cachedMediaFiles;
  }

  cachedMediaFiles = fs
    .readdirSync(MEDIA_DIR)
    .filter((name) => name && !name.startsWith("."));

  return cachedMediaFiles;
};

const isAbsoluteUrl = (value) => /^https?:\/\//i.test(value);

const toPublicPath = (filename) => `${PUBLIC_PREFIX}${filename}`;

const findMediaMatch = (filename) => {
  const mediaFiles = getMediaFiles();
  if (!filename || mediaFiles.length === 0) return null;

  if (mediaFiles.includes(filename)) return filename;

  const ext = path.extname(filename);
  const stem = path.basename(filename, ext);
  if (!stem || !ext) return null;

  const escapedStem = stem.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const suffixPattern = new RegExp(`^${escapedStem}(-\\d+)?${ext.replace(".", "\\.")}$`);
  const suffixedMatches = mediaFiles.filter((name) => suffixPattern.test(name));
  if (suffixedMatches.length === 1) return suffixedMatches[0];

  const prefixMatches = mediaFiles.filter(
    (name) => name.startsWith(`${stem}-`) && path.extname(name) === ext
  );
  if (prefixMatches.length === 1) return prefixMatches[0];

  return null;
};

const resolveFeaturedImage = (featuredImage) => {
  if (!featuredImage || typeof featuredImage !== "string") return featuredImage || "";

  const trimmed = featuredImage.trim();
  if (!trimmed || isAbsoluteUrl(trimmed)) return trimmed;

  const normalized = trimmed.startsWith(PUBLIC_PREFIX)
    ? trimmed.slice(PUBLIC_PREFIX.length)
    : trimmed.replace(/^\/+/, "");

  const match = findMediaMatch(normalized);
  return match ? toPublicPath(match) : trimmed.startsWith("/") ? trimmed : toPublicPath(normalized);
};

const absoluteUrl = (url, siteUrl) => {
  if (!url) return "";
  if (isAbsoluteUrl(url)) return url;
  const base = (siteUrl || "").replace(/\/$/, "");
  const pathPart = url.startsWith("/") ? url : `/${url}`;
  return `${base}${pathPart}`;
};

module.exports = {
  resolveFeaturedImage,
  absoluteUrl,
  findMediaMatch,
  getMediaFiles,
};
