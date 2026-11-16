# Job Openings Page

The jobs page lists the lab's open and past positions. It is built from a single data file, so adding or closing an offer never requires touching the page template.

## How the page is built

Every offer lives in `_data/jobs.yml`, under the `jobs:` key, as one entry with bilingual `fr` and `en` texts. The page template, `jobs.md`, renders one card per entry and one modal window with the full offer. The French page at `/fr/jobs/` is generated automatically by `jekyll-multiple-languages-plugin`, which picks the `fr` texts; the English page at `/jobs/` picks the `en` texts. Offers appear in the order of the data file, so new offers go at the top.

An offer with `active: true` is shown as open: its card has a "View offer" button and, when PDFs are provided, a "PDF" button, and its modal ends with an "Apply" button that opens an email to the `contact` address. An offer with `active: false` stays on the page, greyed out with a "Filled" badge, and its modal can no longer be opened. The sidebar filters cards by status (open, all, archived) and by `type`, whose accepted values are `internship`, `phd`, `postdoc` and `research assistant`.

## Adding an offer

Copy the block from `job_template.yml`, paste it right under the `jobs:` line of `_data/jobs.yml`, and fill in both languages. The template lists every field the page displays and marks which ones are required; anything not listed there is ignored by the page. Long texts are Markdown blocks, rendered with kramdown in GFM mode, so headings, bold text and lists all work, and a list can directly follow a paragraph line.

If the offer comes with PDF versions, copy them into `assets/jobs/` and point the `pdf` field at them with absolute paths such as `/assets/jobs/my_offer_fr.pdf`. The card then shows a PDF button in the page language, and the modal footer links to both language versions. The files open in a new browser tab, from which they can be downloaded.

To close an offer, set `active: false`. Nothing else needs to change.

## How the fields are rendered

The card shows the title, the optional subtitle, the type badge, the open or closed status, the `start` value and a one-line excerpt. The excerpt is the first sentence of the first paragraph of `your_mission`; headings are skipped because they render as `<h2>` or `<h3>` rather than paragraphs. Older offers that still use the legacy `mission` field show that field instead.

The modal starts with four boxes for `location`, `duration`, `start` and the optional `onsite`. The long fields follow in a fixed order: `our_mission`, `your_mission`, `profile`, `skills`, `supervision`, `working_conditions` and `application`. The first two are rendered exactly as written, so their text should start with its own `## ...` heading. The other five receive a section title from the page itself ("Profile", "Skills You Will Develop", "Supervision", "Working Conditions", "Application" and their French equivalents), so their text should not repeat it.

A few legacy fields remain supported for older entries but should not be used for new ones. `project` and `mission` are only rendered when `our_mission` and `your_mission` are absent, `tasks` is a plain list, and `process` is only rendered when `application` is absent.

## Checking a change before it goes live

Every push to `master` deploys the site to production on Netlify, so offers should be changed on a separate branch and merged through a pull request. Each pull request gets a Netlify deploy preview, which is the easiest place to check both the English and the French page, open the modals, and follow the PDF links. To build locally instead, run `bundle install` and then `bundle exec jekyll serve`, as described in the main README.
