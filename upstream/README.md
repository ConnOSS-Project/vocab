# Upstream sync

ConnOSS follows two upstream vocabularies, schema.org and CodeMeta. When those vocabularies publish
a new release, the `upstream-sync` workflow works out what changed, what of that affects
ConnOSS, applies the safe changes and opens a pull request with a changelog.

## Files

| File | Role | Edited by |
|---|---|---|
| `schema/connoss_Software.jsonld` | Vocabulary (source of truth) | manually + sync |
| `schema/connoss_profiles_shapes.ttl` | SHACL profiles (source of truth) | manually + sync |
| `schema/connoss_Software.ttl` | Turtle copy of the vocabulary | generated at sync |
| `schema/connoss_profiles.jsonld` | JSON Schema (`$validation`) profiles, Bioschemas style | generated at sync |
| `upstream/sources.yml` | Which upstream sources to follow and how to read them | manually |
| `src/upstream_sync.py` | Main sync script: compares upstream releases with ConnOSS, updates the schema and profile, writes the report and changelog | – |
| `src/upstream_sources.py` | Helper module: finds upstream releases and loads their terms (used by the sync) | – |
| `src/schema_editor.py` | Helper module: edits single entries in the `.jsonld` and `.ttl` source files (used by the sync) | – |
| `src/build_artifacts.py` | Generates `connoss_Software.ttl` and `connoss_profiles.jsonld` from the two source files | – |
| `upstream/sources.lock.json` | Upstream version each source was last synced to | sync |
| `CHANGELOG.md` | One entry per sync | sync |

The generated files are rebuilt by `python src/build_artifacts.py` (the deploy workflow does this too, so the website is always consistent).

## How a sync works

1. **Find new releases.** For each source, list its released versions (schema.org
   `versions.json`, CodeMeta git tags) and compare the newest one with
   the version in `sources.lock.json`.
2. **Diff the two releases.** Each release is loaded into the same structure (label,
   description, domain, range, superseded-by, pending/attic status per term) and compared term
   by term.
3. **Find what ConnOSS uses.** Every IRI in the vocabulary (defined terms, ranges, parent
   classes/properties) and in the profiles (`sh:path`, `sh:class`) is collected and matched to a
   source by namespace. Namespace aliases (`http`/`https` schema.org, the old and new CodeMeta
   namespaces) count as the same term.
4. **Update the schema and profile.** ConnOSS follows upstream wherever its current value is
   still the old upstream value. These changes are written into both
   `connoss_Software.jsonld` and `connoss_profiles_shapes.ttl`:
   - **Descriptions** that ConnOSS took over unchanged get the new upstream text.
   - **Expected types (ranges):** the vocabulary's `schema:rangeIncludes` and the profile's
     type constraint (`sh:class` / `sh:node` / `sh:or`, plus the "of type …" part of
     `sh:message`) are rewritten to the new range. Data types use the profile's value shapes
     (`TextValue`, `URLValue`, `DateValue`, …).
   - **Deprecated terms with one replacement** (as with `codemeta:maintainer` →
     `schema:maintainer` in CodeMeta 4.0) are renamed: `@id`, references, label, `sh:path`,
     `sh:name` and `sh:message`; description and range are taken over from the new term
     where ConnOSS had the old upstream values.
   - **New terms** of sources with `add_new_terms: true` (CodeMeta) are added to the
     vocabulary and to the Software profile, in the Optional group.
   - **Version pins** and `schema:schemaVersion`.

   Only the affected entries are rewritten, so the rest of each file (formatting, comments,
   order) stays as it is and the PR diff is small.
5. **List what needs a decision.** Where ConnOSS deliberately differs from upstream (its own
   description, a narrower or wider range), nothing is overwritten; the upstream change goes into
   the PR's "Needs review" checklist. So do removed terms, deprecations without a single
   replacement, namespace changes, renamed terms whose own description may no longer fit, new
   properties (to choose Required/Recommended/Optional), and profile properties not defined in
   the vocabulary. New schema.org properties on the watched types are listed as candidates only.
6. **Write the result.** Bump the lock file, add a changelog entry, rebuild the generated files,
   and open (or update) the `upstream-sync` pull request with the full report. If nothing
   changed, no PR is opened; the report still appears in the workflow run summary.

Every automatic change is visible in the PR diff and listed in the PR description, so you
review it before it reaches `main`.

## Running it

- **Scheduled:** every 3 months (`.github/workflows/upstream-sync.yml`). To change the interval,
  edit the cron line; `*/6` in the month field means every 6 months.
- **Manually:** Actions → upstream-sync → Run workflow.
- **Locally:** `pip install rdflib pyyaml`, then
  `python src/upstream_sync.py --dry-run` to only see the report, or without `--dry-run` to
  change the files.

## Reviewing the PR

Work through the "Needs review" checklist on the PR branch: edit the vocabulary or shapes,
run `python src/build_artifacts.py`, commit, and merge. Merging triggers the website deploy.
Merge or close the PR before the next scheduled run, because the run rebuilds the branch from
`main` and would overwrite edits made on it.

## Adding a source

Add an entry to `sources.yml` and its current version to `sources.lock.json`. Any source that
publishes an RDF file per release can use `format: rdf`; version discovery works with git tags
(`git-tags`), release folders (`git-dirs`) or a JSON list of versions (`json`).

## One-time setup

In the repository settings, under **Actions → General → Workflow permissions**, enable
"Allow GitHub Actions to create and approve pull requests". Without it the workflow can
update the branch but cannot open the PR.
