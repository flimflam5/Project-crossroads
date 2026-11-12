# Exact QA10 downloads

This is delivery infrastructure only. Game source and all public evidence remain
pinned to3138de89d9e57b816d3b7d03e727f04d69c2d168. The existing tested ROM is not
rebuilt or altered. The iPhone Codex binary viewer fails to decode workspace links;
File Service download signatures expire in minutes; the workspace credential
cannot upload to GitHub's release-asset endpoint. A trusted hosted Actions runner
publishes persistent public prerelease assets with its own repository token.

The CI artifact13924772308 contains a separately compiled cartridge. The small
Git binary delta here accounts for compiler differences and recovers exactly the
emulator-tested ee2d81d5d0b55b7f1f9d36d1c9b055700164da439f51af7a66b5fb2d2147f90b
cartridge. Input artifact, input ROM, patch and output ROM all have SHA256 guards.
No ROM or base ROM is committed. No commercial cartridge is downloaded.

The evidence is read from the immutable source tree. ZIPs are repackaged with
fixed metadata; their current checksums are included. The game bytes match the
verified local build; archive container hashes may differ from earlier packages.
Local verification preserved2370 original evidence files byte-for-byte, passed
both archive CRCs, and rejected a wrong base before producing any output.

Normal CI behavior is retained. Only a push on the dedicated delivery branch or
an explicit delivery_only workflow dispatch skips compilation and runs delivery.
The hosted token has contents:write/actions:read only for this trusted job. Existing
release assets are compared and never silently replaced; upload failure retains
an Actions artifact. No source branch is merged.

The source CI artifact has retention limits; complete initial publication before
its expiry. Published release assets have stable URLs independent of short-lived
File Service links. Owner Delta/visual acceptance remains pending.
