# Google Search Console Setup

## 1. Property

Add URL-prefix property:

`https://worldvape.mykindredai.com`

## 2. Verification

Recommended order:

1. HTML file verification if hosting allows root upload.
2. DNS TXT verification for durable ownership.
3. HTML meta tag only if file/DNS access is unavailable.

## 3. Sitemap Submission

Submit:

`https://worldvape.mykindredai.com/sitemap.xml`

## 4. Indexing Checklist

- Before requesting indexing, confirm `curl -I https://worldvape.mykindredai.com/sitemap.xml` returns `200 OK` without certificate errors. Current post-deploy check found a certificate subject mismatch, so GitHub Pages custom-domain SSL must be repaired first.
- Request indexing for `/`, `/kwangwoon-vape/`, `/nowon-vape/`, `/입호흡액상추천/`, `/노원액상추천/`, `/faq/`, `/guide/`, `/liquid-guide/`, `/beginner-guide/`, and `/blog/`.
- Inspect one Korean slug URL to confirm Google can crawl encoded Korean paths.
- Check Coverage/Pages report after 48-72 hours.
- Check Enhancements for FAQ, Breadcrumb, and LocalBusiness parsing.
