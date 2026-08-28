// Per-post permalink: /blog/{slug}/ — hidden when draft or future-dated in production.
const { shouldHideInProduction } = require("../../lib/post-visibility");
const { resolveFeaturedImage } = require("../../lib/resolve-featured-image");

module.exports = {
  eleventyComputed: {
    featured_image(data) {
      return resolveFeaturedImage(data.featured_image);
    },
    permalink(data) {
      if (shouldHideInProduction({ date: data.date, draft: data.draft })) {
        return false;
      }
      const raw = data.slug || data.page?.fileSlug || data.title || "";
      const slug = raw
        .toString()
        .toLowerCase()
        .trim()
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/^-+|-+$/g, "");
      return `/blog/${slug}/`;
    },
    eleventyExcludeFromCollections(data) {
      return shouldHideInProduction({ date: data.date, draft: data.draft });
    },
  },
};
