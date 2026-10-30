# scoop-clipforge

A [Scoop](https://scoop.sh) bucket for [ClipForge](https://github.com/DrummingBird1/clipforge-app), a local video studio for Windows.

## Install

```powershell
scoop bucket add clipforge https://github.com/DrummingBird1/scoop-clipforge
scoop install clipforge
```

Then start **ClipForge** from the Start menu; it opens in your browser.

## Update and uninstall

```powershell
scoop update clipforge
scoop uninstall clipforge
```

Your settings and videos (`data` and `workspace`) live in Scoop's persist folder (`~\scoop\persist\clipforge`), so they survive updates. `scoop uninstall clipforge --purge` removes them too.

The manifest takes each new version, and its SHA-256 from `SHA256SUMS.txt`, from the [ClipForge releases](https://github.com/DrummingBird1/clipforge-app/releases).
