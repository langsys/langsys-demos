# Shorts sources

The source pages of the 14 social Shorts, kept here so they live on the remote. The working copy is the
`langsys-demo-videos` repo, which has no remote yet; edit and render there, then copy the changes here.
Once that repo has a remote, this folder can go.

The finished videos are in `../../videos/<sdk>/social/`, which is where `upload.py` reads them from.

- `shared/social/<demo>/<demo>.html`: Translation Manager and explainer stories, no SDK code.
- `svelte/social/<demo>/<demo>.html`: Svelte stories.
- `assets/social-kit.css`, `assets/social-kit.js`: the visual system and frame engine every page loads.
- `assets/capture.py`: renders a page frame by frame (`python assets/capture.py svelte/social/phrase --ratio=9x16`).
- `assets/narration/narrate_shorts.py`: narration for the 9:16 YouTube cuts; it imports `narrate.py`.

A page only renders correctly when served over HTTP; `capture.py` starts its own server. `narrate.py` still
points `REPO` and `BASE` at `langsys-demo-videos` and a local scratch folder.
