// Tags injected by automation (e.g. n8n) that should never appear on the site.
const BLOCKED_TAGS = new Set(["airbnb", "cambridge"]);
const INTERNAL_TAGS = new Set(["posts"]);

const normalizeTag = (tag) => (tag || "").toString().trim().toLowerCase();

const sanitizeTags = (tags) => {
  if (!Array.isArray(tags)) return [];

  return tags.filter((tag) => {
    const normalized = normalizeTag(tag);
    return normalized && !BLOCKED_TAGS.has(normalized) && !INTERNAL_TAGS.has(normalized);
  });
};

module.exports = {
  BLOCKED_TAGS,
  INTERNAL_TAGS,
  normalizeTag,
  sanitizeTags,
};
