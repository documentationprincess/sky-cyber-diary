# How I Tricked AI Into Doing My Bidding

An Astro starter for Sky's cybersecurity diary.

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

## Before deployment

1. Replace `https://example.com` in `astro.config.mjs`.
2. Replace the GitHub link in `src/layouts/BaseLayout.astro`.
3. Edit the About page.
4. Replace the placeholder root-cause text in Case 001.
5. Run `npm run build`.
