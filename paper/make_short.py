"""Build the eight page short version from the full manuscript sources (drops the earlier studies section, the
desert table and the frame figure)."""
from pathlib import Path
P = Path(__file__).resolve().parent
t = (P / "vectra_paper.tex").read_text()
t = t.replace("\\input{s3_earlier.tex}\n", "")
t = t.replace("\\input{s3_methods.tex}", "\\input{s3_methods_short.tex}").replace("\\input{s3_system.tex}", "\\input{s3_system_short.tex}")
(P / "vectra_paper_short.tex").write_text(t)
m = (P / "s3_methods.tex").read_text()
s = m.index("\\begin{table}[t]\n\\caption{Longest daily window")
e = m.index("\\end{table}", s) + len("\\end{table}\n")
(P / "s3_methods_short.tex").write_text((m[:s] + m[e:]).replace(" (Table~\\ref{tab:deserts})", ""))
y = (P / "s3_system.tex").read_text()
s = y.index("\\begin{figure*}[t]")
e = y.index("\\end{figure*}") + len("\\end{figure*}\n")
(P / "s3_system_short.tex").write_text((y[:s] + y[e:]).replace(" Fig.~\\ref{fig:frames} shows the levels.", ""))
print("short sources written")
