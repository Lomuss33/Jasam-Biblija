# Word & Light

An open reading book beneath a gold cross. A project identity mark; it does not imply institutional endorsement or change editorial scope.

- `icon.svg`: editable vector master, 64-unit grid; no fonts or external assets.
- `icon.png`: transparent 512 × 512 PNG for app/project icons and general reuse.
- `icon-192.png`: 192 × 192 PNG for web manifests.
- `apple-touch-icon.png`: 180 × 180 PNG for home-screen shortcuts.
- `../../favicon.ico`: Windows/browser icon with 16, 24, 32, 48, 64, 128 and 256 pixel sizes.

T3 Code uses `assets/brand/icon.png` through its project settings. These files are also suitable for desktop-launcher icons. A platform may place its own mask/background around a home-screen icon.

To regenerate PNGs from the SVG using installed ImageMagick: `magick -background none icon.svg icon.png`. Resize from the 512 px image with a high-quality filter. The ICO contains multiple raster sizes; retain all sizes when replacing it.

## Validation

SVG parsing and self-contained assets, PNG dimensions (512/192/180), all seven ICO sizes, and `git diff --check` passed. The six marks were visually inspected at 16, 32, 48 and 112 pixels.

`node --test --test-name-pattern="local viewer exposes only explicit documents" web/server.test.mjs` passed. An ephemeral local-server request returned the exact SVG with `image/svg+xml`, while unrelated asset paths remained blocked (404). Python/schema tests were not run for this static-asset and viewer-route change.
