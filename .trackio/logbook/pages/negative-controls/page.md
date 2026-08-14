# Negative controls

Status: supporting controls for the scoped gate.


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_1b323d734537", "created_at": "2026-07-20T07:49:43+00:00", "title": "Boundary and interface controls"}
-->
# Negative controls

Changing source tail condition `<= 1/sqrt(b)` to strict `<` moves the quantile from 0 to 255 and threshold from 16 to 271. Introducing an illegal error-aware input makes the threshold vary across truths, while the source threshold stays fixed.
