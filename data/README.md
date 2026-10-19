# Data

No dataset files are stored in this repository. Raw and converted data stay on local disk and are listed in .gitignore.

Each dataset used in the project must have an entry in docs/source_log.md that records the link, the access date, the licence as stated on the official page (or "not stated"), and the intended use. A dataset without such an entry is not used.

Planned local layout (not committed):

    data/raw/<dataset_name>/        original downloads, never modified
    data/converted/<dataset_name>/  output of the adapters in src/dataset_adapters
