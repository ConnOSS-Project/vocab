# Upstream sync

ConnOSS follows two upstream vocabularies, schema.org and CodeMeta. When those vocabularies publish
a new release, the `upstream-sync` workflow works out what changed, what of that affects
ConnOSS, applies the safe changes and opens a pull request with a changelog.

## Files

|File|Role|Edited by|
|-|-|-|
|`schema/connoss\_Software.jsonld`|Vocabulary (source of truth)|people + sync|
|`schema/connoss\_profiles\_shapes.ttl`|SHACL profiles (source of truth)|people + sync|
|`schema/connoss\_Software.ttl`|Turtle copy of the vocabulary|generated|
|`schema/connoss\_profiles.jsonld`|JSON Schema (`$validation`) profiles, Bioschemas style|generated|
|`upstream/sources.yml`|Which upstream sources to follow and how to read them|people|
|`upstream/sources.lock.json`|Upstream version each source was last synced to|sync|
|`CHANGELOG.md`|One entry per sync|sync|



The generated files are rebuilt by `python src/build\_artifacts.py` (the deploy workflow does this too, so the website is always consistent). Don't edit them by hand.



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
4. **Sort every relevant change into one of three groups:**

   * **Applied automatically**: version pins, `schema:schemaVersion`, and descriptions that
ConnOSS copied verbatim from the old upstream release (they now follow the new text).
Edits are made on the file text, so formatting is kept and the diff is minimal.
   * **Needs review** (a checklist in the PR): descriptions ConnOSS rewrote itself, changed
expected types, removed domains, deprecated/superseded/removed terms, namespace changes,
reused terms that don't exist upstream (with a "did you mean" hint), and profile properties
not defined in the vocabulary.
   * **Candidates**: new upstream properties on the types ConnOSS builds on, and upstream terms
with the same name as a `connoss:` term (a sign the extension could be replaced).
5. **Write the result.** Patch the two source files, bump the lock file, add a changelog entry,
rebuild the generated files, and open (or update) the `upstream-sync` pull request with the
full report. If no source has a new release, no PR is opened; the report still appears in
the workflow run summary.

Nothing is decided for you: auto-applied changes are limited to text ConnOSS took over
unchanged, and they're visible in the PR diff. Marginality (required/recommended/optional) and
expected types in the profiles are never changed automatically.

## Running it

* **Scheduled:** every 3 months (`.github/workflows/upstream-sync.yml`). To change the interval,
edit the cron line; `\*/6` in the month field means every 6 months.
* **Manually:** Actions → upstream-sync → Run workflow.
* **Locally:** `pip install rdflib pyyaml`, then
`python src/upstream\_sync.py --dry-run` to only see the report, or without `--dry-run` to
change the files.

## Reviewing the PR

Work through the "Needs review" checklist on the PR branch: edit the vocabulary or shapes,
run `python src/build\_artifacts.py`, commit, and merge. Merging triggers the website deploy.
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

