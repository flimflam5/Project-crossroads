# HNS kiln delivery mechanism

This infrastructure is dormant until `feature/hns-kiln-delivery-01` is created
and pushed. It is not evidence that a candidate has been built or tested.
It packages the **exact locally tested** ROM using the already published QA10
game as a SHA256-verified base, an explicitly generated small binary delta, and
the hosted GitHub runner's repository token. No game ROM or save is committed.

After completing tests, commit and push the game source first. Preserve the
actual ROM and matching ELF used for the test. Create and commit an independent
verification record, release notes, and chosen native screenshots; do not commit
saves, snapshots, memory dumps, ELF files or ROMs. The verification record must
contain the actual `source_commit`, actual `rom_sha256`, and the booleans
`automated_checks_passed` and `runtime_checks_passed`. Set those booleans true
only after the corresponding checks actually pass. State scope and limitations
in the record and release notes. The evidence commit can differ from the game
source commit. Both commits must be accessible from the remote.

Generate the patch locally, using the actual tested candidate and QA10 ROM:

```sh
python3 crossroads/tools/make_hns_kiln_delta.py \
  --base-rom /workspace/BlackLedger-Olivine-Aqua-QA10-A1.gba \
  --tested-rom /path/to/tested/pokeemerald.gba \
  --output crossroads/delivery/hns-kiln/qa10-to-tested.patch
```

The command tests the reconstruction before writing the patch and prints both
SHA256 values. It stages ROMs only in a temporary Git repository and cleans it.
It rejects a delta over 4 MiB; if that happens, use a verified CI artifact instead
of committing a near-complete ROM as a patch.

Create `crossroads/delivery/hns-kiln/spec.json` with **actual** values:

```json
{
  "source_commit": "40-hex-game-commit",
  "source_tree": "40-hex-tree-of-game-commit",
  "evidence_commit": "40-hex-evidence-commit",
  "rom_sha256": "64-hex-tested-rom-sha256",
  "patch_sha256": "64-hex-patch-sha256",
  "stem": "BlackLedger-HNS-Kiln-QA01",
  "tag": "hns-kiln-qa01",
  "verification_record": "path/to/verification-summary.json",
  "release_notes": "path/to/release-notes.md",
  "evidence_files": ["path/to/native-screenshot.png"]
}
```

The paths must exist in the evidence commit. Add every intended public evidence
file explicitly. Only image/video/Markdown/JSON/text extensions are accepted.
Release notes must accurately describe the tested scope, Delta checklist,
deferred work and donor credit chain. Do not claim owner visual acceptance.

Before pushing the delivery branch, run the recovery locally and compare the
recovered `.gba` checksum with the emulator-tested one:

```sh
python3 crossroads/tools/prepare_hns_kiln_delivery.py \
  --base-rom /workspace/BlackLedger-Olivine-Aqua-QA10-A1.gba \
  --output /dev/shm/hns-kiln-delivery-check
```

Commit the spec and patch in the dedicated delivery branch only after that
verification. Its push activates `.github/workflows/hns-kiln-delivery.yml`,
which downloads the public QA10 base, validates all hashes, source identity,
test record and archive CRCs, and publishes a unique public GitHub prerelease.
It refuses to replace an existing release or mismatched assets. Confirm an
anonymous download of each asset and verify its hash before giving links.
