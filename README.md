# Documentation Princess

Sky Blu DeGrate's IT support and cybersecurity portfolio at https://femalethreat.actor.

## Run locally

```bash
npm install
npm run dev
```

Open the local URL Astro prints in Terminal.

## Add a new case file

Duplicate:

`src/content/posts/001-windows-is-a-snitch.md`

Change the frontmatter and body. New posts automatically appear on the homepage.

## Add screenshots

Put images in:

`public/images/case-001/`

Then reference them in Markdown:

```md
![Description](/images/case-001/example.png)
```

## Search metadata and publication

`src/components/SEO.astro` provides canonical URLs, social metadata and linked Person,
WebSite, ProfilePage and BlogPosting data. Professional identity and profile links live in
`src/data/identity.ts`; the production domain is also set in `astro.config.mjs`.

Case files retain their original titles and text. Optional `seoTitle`, `technicalSummary`
and `labType` frontmatter clarify the topic and training context. Keep summaries faithful
to the article; never describe a personal lab as paid production work.

`/sitemap.xml` is generated from the content collection at build time. `/robots.txt`
advertises it. New posts automatically enter the sitemap without an invented update date.

Before publishing, run `npm run build` and `npm run verify:seo`. Review the changed page
at desktop and phone widths. The GitHub `main` branch publishes through the existing
Vercel integration. Verify the live domain after deployment; a successful local build
does not establish publication or Google indexing. Preserve the Search Console ownership
tag. Search Console can accept the sitemap and indexing requests, but rankings remain
outside this site's control.
