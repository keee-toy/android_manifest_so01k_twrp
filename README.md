# Sony Xperia XZ1 SO-01K TWRP 12.1 public manifest

Target: `poplar_docomo` (SO-01K), custom recovery kernel, logical recovery
target backed by FOTAKernel. **P4.51 is the current frozen SO-01K recovery
baseline, functionally ready for ROM handoff.** This repository records public
source checkout inputs only. It does not contain the frozen recovery image,
stock Sony/QTI crypto binaries, vendor repositories, or private firmware.

## Source checkout pins

The source evidence is `SO01K_TWRP_12_1_LOCAL_MANIFEST.xml` and
`SO01K_TWRP_12_1_VTS_FUZZER_LOCAL_MANIFEST.xml`. The original device manifest
used a machine-local file URL and an older device commit; this public template
replaces that URL and pins the normalized P4.51 device commit. The VTS fuzzer
entry preserves the AOSP 12.1 r4 tag from the original local manifest.

| Input | Revision |
| --- | --- |
| minimal-manifest-twrp `platform_manifest_twrp_aosp`, `default.xml` including `twrp-default.xml` | `6dc117d9cbd08430daa16db2013560e1c4017fa8` (observed local manifest HEAD) |
| [`keee-toy/android_device_sony_poplar_docomo-twrp`](https://github.com/keee-toy/android_device_sony_poplar_docomo-twrp) | `ee171c098acbc770127778f20d3e210f5494ac15` |
| [`keee-toy/android_twrp_so01k_patches`](https://github.com/keee-toy/android_twrp_so01k_patches) | `6082a6c5869549b336818679ca516101f938ed96` |
| Kernel base [`ATI-Experiments/android_kernel_sony_msm8998`](https://github.com/ATI-Experiments/android_kernel_sony_msm8998), `lineage-22.1` | `7a4c7d73f8ec401b89bd1ab815d2b4ccf801ec3f` plus two patches in `external/so01k-patches/kernel-source/` |
| TeamWin `android_system_vold` | `a164ba05c5fef288059774a776b2e6e1119957cf` |
| TeamWin `android_device_qcom_twrp-common` | `98506f7919102378c8d52ee7d6a94a867f1b4c55` |
| TeamWin `android_bootable_recovery` | `5c3d206a5eeb3d446bcda8248a405a4b278bab5c` |
| AOSP `platform/test/vts-testcase/fuzz` | `refs/tags/android-12.1.0_r4` |

`local_manifests/so01k-p451-public.xml` targets the manifest's `default.xml`,
which includes TeamWin `twrp-default.xml`. It points to the intended public
repositories under the verified owner `keee-toy`; those repositories must be
created and populated before a public sync. Copy the XML into a fresh
checkout's `.repo/local_manifests/` before syncing. The base manifest
revision above is recorded for compatibility; unrelated projects are not
individually pinned here, so this is a pinned patch-input manifest rather than
a complete lockfile for every project in a TWRP checkout.

For a local checkout before publication, render a separate file URL manifest
from the two requested local repositories. The renderer checks their pinned
HEADs and writes the machine-specific URL only to the selected output file:

```sh
python3 render-local-manifest.py /path/to/local-repos > /path/to/twrp-12.1/.repo/local_manifests/so01k-p451-local.xml
```

Do not commit the rendered file; it contains the local filesystem path. The
renderer does not sync or build.

When the public repositories are available, the source-only process is:

```sh
repo init -u https://github.com/minimal-manifest-twrp/platform_manifest_twrp_aosp.git -b twrp-12.1 -m default.xml
git -C .repo/manifests checkout 6dc117d9cbd08430daa16db2013560e1c4017fa8
# Copy local_manifests/so01k-p451-public.xml into .repo/local_manifests/.
repo sync
external/so01k-patches/apply-p451-public.sh "$PWD"
```

The setup script rejects unexpected project
HEADs and does not copy private blobs, download them, or build automatically.
The custom kernel prebuilt is tracked in the device repository; its SHA-256 is
`c6d8affd56de7e72dc9729feb3215b6faacff87b91cc04504851ce5f1379752c`.
The pinned public kernel base, two source patches, extracted build config, and
license/provenance notes are in the [patches repository's kernel source guide](https://github.com/keee-toy/android_twrp_so01k_patches/blob/main/kernel-source/README.md).
No private kernel checkout or fourth GitHub repository is required to obtain
this public source state. The public source setup does not rebuild the kernel.
The public device tree has the P4.51 `/system_root` System backup mapping;
its `twrp.flags` SHA-256 is
`c579edbb131dd7e7e2f2a3b8abfafe30b3172883b2af34fedf986e4c317f2c39`.

P4.51 physical validation proved `/data` mount, plaintext internal storage,
and a real decrypted-file read. System appeared in Backup; Boot/System/Vendor
backups and digest generation succeeded; Boot-only restore and subsequent
Android boot succeeded. TWRP still reports formal FBE user-0 decrypt failure
and a default-password warning. Credential/PIN decrypt, System restore,
Vendor restore, and Format Data were not tested. Source-state reproducibility
does not imply a self-contained or bit-for-bit image build.
