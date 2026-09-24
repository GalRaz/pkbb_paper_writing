# A stimulus-computable rational model of visual habituation in infants and adults

Manuscript sources, data, cached models and figures for the RANCH (Rational Action, Noisy Choice for Habituation) paper by Gal Raz, Anjie Cao, Rebecca Saxe and Michael C. Frank. Project OSF page: https://osf.io/d7jz8/

## Layout

| Path | Contents |
|---|---|
| `00_main.Rmd` | Bookdown driver: loads packages, data and cached models, then includes the section files below in order. |
| `01_abstract.Rmd` … `10_supplementary.Rmd` | One file per section. Statistics are computed in R chunks and inserted inline, so every number in the text is reproducible from `data/`. |
| `data/infants/` | Infant looking-time data (Experiment 1, Experiment 2 Zoom and CHS samples, control experiment), cross-validation results, full-data fits, generalization predictions and unscaled-embedding simulations. |
| `data/adults/` | Adult self-paced looking data, k-fold and full-data fits, generalization predictions. |
| `data/results_plots/` | Summaries used for the results figures. |
| `data/joint_scaling_fits.csv`, `data/param_info.csv` | Joint infant/adult scaling fits and the parameter grid. |
| `cached_models/` | Fitted `lme4` models (the chunks that fit them are `eval=FALSE`; delete a cache and set `eval=TRUE` to refit). |
| `figs/` | Figure images read into the manuscript. |
| `00_main_files/figure-latex/` | Figure PDFs produced by the last knit. |
| `library.bib` | Bibliography. |

## Building

Open `pkbb_paper_writing.Rproj` and knit `00_main.Rmd` (bookdown `pdf_book`, biblatex). Required packages are listed at the top of `00_main.Rmd`. Knitting writes `00_main.tex` and `00_main.pdf`.

The RANCH model code itself (PyTorch) and the simulation outputs that feed `data/` live on the OSF page.

## Versions

| Git tag | Manuscript |
|---|---|
| `elife-v1` | eLife reviewed preprint v1 (https://elifesciences.org/reviewed-preprints/102713v1). |
| `elife-revision` | Revised manuscript submitted in response to the eLife reviews: title scoped to *visual* habituation, added scope paragraphs, an explicit statement on why competing models cannot be compared directly, cross-validated R² added to Table 1 and the fit-metric discussion, and the remaining reviewer-requested clarifications. `00_main.tex` at this tag is the compiled manuscript as edited on Overleaf. |

Figures and all reported statistics are identical across the two versions; only the text changed.
