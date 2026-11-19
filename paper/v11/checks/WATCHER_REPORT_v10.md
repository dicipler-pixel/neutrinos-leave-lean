# WATCHER report, phase 2 (v9 -> v10)

Verdict: SLIPS FOUND (four small ones; no wrong number, no unagreed change, no stale sentence left in the paper text)

Base B = <session>
My scripts: B/nu6/harness10/watcher_work/recompute.py (numbers), textcheck.py (PDF/HTML text); hashes in watcher_work/h9.txt, h10.txt.

## 1. Diff (my own: sha256 of every file in both trees, diff and word-diff of the .tex)

Trees: 290 files (v9 frozen), 292 (v10). Every file present in both is byte-identical except five:
- app_new_evidence.tex, sec_new_mcc.tex (agreed cuts C16, C15)
- code/A6/PREREGISTERED.txt (append only, section 3), code/A6/RUNLOG.txt (now the full log; equals A6_refine2/RUNLOG.txt; the v9 lines are all still in it)
- code/v7/build_html.py: 4 lines, file names v9 -> v10 only
New in v10: code/A6/res_L3_r08.json, level3_rates.py, level3_rates_out.txt (each byte-equal to A6_refine2), and the built files under v10 names. Only in v9: the v9 built files and build.log (v10 has no build.log).

Changed lines, all of them:
- neutrinos_v10.tex l.15 (C1), l.22 (C2, C3), l.236 (C4), l.238 (C5), l.240 (C6 as amended, C7-C11), l.262 (C12), l.293 (C13, C14)
- sec_new_mcc.tex l.11 (C15)
- app_new_evidence.tex l.68 (C16) and three listing lines inserted after l.73 (C16)
Nothing changed that is not on the list. Nothing on the list for the .tex was left undone. The word-diff matches my proposed text word for word, with the coordinator's amendment to C6. guard.py agrees (13 change blocks, 0 unregistered).

## 2. Numbers and reading

Every number in the changed sentences recomputed from res_L3_r08.json, res_L3_r125.json and the level-1/2 thresholds: 0.5117877 +- 0.0000063; rises 3.1e-5 each against 7.5 and 6.4e-5; 0.42 (0.33-0.50), 0.49 (0.39-0.59); 0.51179917, 0.51178492, 0.51177780 with inside/outside as stated; 1.1013, [1.0938, 1.1088]; -0.0007 against -0.0082; +-0.0075; order 6.2 outside 0.5 to 4; 0.0091 and 0.015; 1.101 against 1.102; 1.094-1.109; 1.1102 is 0.0002 above 1.11. All correct.
Traps T1-T11: T1 fixed (band sentence names what is inside, and says 1.1102 is 0.0002 above). T2 held (no "bound"). T3 caption says first-level. T4 no extrapolated number. T5 no "converged" claim; sign stated unresolved. T6 both factors quoted. T7 r=0.8 time-step exclusion stated. T8 "resolution budget" gone from abstract, section, Summary, Zenodo. T9 0.51179917 used. T10 stamp corrected (section 3). T11 no Richardson spread printed.

SLIP 1 (grammar, in my own proposed text). neutrinos_v10.tex l.236-240, PDF p. with equation (13): "... and the whole bracket range of the finest, lie in  odd rate = 1.10 +- 0.01,  the first-level values, 1.1066 and 1.1102, sit at its upper edge, ..." Two full clauses joined by the equation's comma. Fix: end the equation with a semicolon (l.238 `1.10\pm0.01;`), nothing else. Smaller point in the same clause: 1.1066 is 0.0034 inside the band, so "sit at its upper edge" is loose for it; "sit at and just above its upper edge" would be exact. The author's call.

Notes, not slips:
- "range 0.39-0.59": from the 8-digit thresholds printed in the paper the upper end is 0.58502; from the unrounded level-1/2 midpoints it is 0.58496. The second decimal sits on the rounding edge. claims.py accepts either.
- l.236 still says "Three systematics are larger than the brackets" (true of levels 1 and 2) and l.240 says the budget is led by the third-level brackets. Both are true where they stand; a reader may feel the turn.

## 3. Appended preregistration block

First 4675 bytes of A6_refine2/PREREGISTERED.txt equal PREREGISTERED_before_result_2026-11-13.txt and the frozen v9 copy, byte for byte: only an append. Stamp 2026-11-13T22:01Z equals the file's write time (22:01Z). Numbers all right, including "about 1.0992". Kill line, sign flag and the "marked untrustworthy" Richardson line are stated in the file's own terms.

SLIP 2 (small). The block was first written at 21:56Z and rewritten in place at 22:01Z; the file's rule is that appended results are not edited. No trace of the first wording remains. Harmless here (the stamp is now true and nothing above it moved), but the honest form is one line saying so, or leave as is and record it in the v10 change record. Also: the file fixed that the error on R_inf be reported in two parts; the block reports R_inf = 1.10126 as untrustworthy without them. From A6_refine2/richardson.py they are 0.041 (bracket part, defined in 2 of 8 combinations) and 0.001 (order part). richardson.py is not in paper_v10/code/A6; level3_rates.py's "four corners" Richardson line is a different construction from the preregistered one. Suggest adding richardson.py to the archive, or one appended line with the two parts.

## 4. Harness (harness10/claims.py: 12 checks, 0 failed on v10)

C6 recomputes both brackets, the six predictions and their inside/outside status from the two result files, and requires the printed strings. C7 forbids the removed phrases. C11 recomputes the three rates, corner range, changes, kill line at every corner, sign spread, order, budget and band membership, and requires the printed strings. They test what they say.

SLIP 3 (gaps: places where a check can pass with the text wrong):
- The conclusion sentence C10 ("at r=0.8 one purely first order in the time step ... agree with second order in the cell size") is not asserted as text; neither are "its sign is not resolved", "inside the kill line written first", "3.1e-5 each against 7.5 and 6.4e-5", or "sit at its upper edge".
- The count of remaining "1.11" mentions (3: l.222, caption, sec_new_mcc l.19) is printed, not asserted; a stray new 1.11 would pass.
- `1.09 <= 1.1066 <= 1.11` compares two constants; 1.1066 is not recomputed. The 0.0038 and 0.0036 in the budget are typed in, not recomputed.
- C7 reads only the .tex files. README, Zenodo text and the HTML are outside it (I checked those by hand, sections 5 and 6). It does not forbid "extrapolates to" or "$1.099$".
- First lines still read "# SCRIPT: NU-V9-CLAIMS" and "# SCRIPT: NU-V9-GUARD".
The v9 harness files (B/nu6/harness/claims.py, README_v9.md) are untouched (equal to the copies in the v9 package).

## 5. README_v10.md and ZENODO_DESCRIPTION_v10.txt

Zenodo: version 10 in the title; l.9 is C18 word for word; no "v9" left; numbers agree with the abstract.
README: version 10 throughout; the only "v9" strings are `lean_build_v9.log` / `lean_build_v9_first_84.log` (the real build logs; correct while the Lean sources are unchanged) and the `v9/` record folder.

SLIP 4. README_v10.md names `paper/art/` ("holds its builder and check") and `checks/v9/`. B/nu6/paper_v10/ has no art/ folder, and no package folder exists yet under B/out_v10/. Both lines are true only if the package is assembled with those folders; check at assembly.

## 6. Built files

PDF (B/out_v10/..._v10_2026-11-13.pdf, byte-equal to paper_v10/neutrinos_v10.pdf): 129 pages, no Type 3 fonts. pdftotext contains every new sentence (24 probes, none missing), the full run log, the level-3 script and output, and the appended block with the 22:01Z stamp. None of the removed sentences is present. The remaining hits for old words are all inside printed archive listings: 1.0983 and 1.0995 in PREREGISTERED.txt, "extrapolation(s)" in PREREGISTERED.txt and level3_rates.py, and "now dominated by resolution" in code_v6/A1_PREREGISTERED.txt (the earlier test's own record; stays).
Plain HTML and art HTML: `1.10\pm0.01` 4 times each, `1.11\pm0.01` and `1.094–1.098` 0 times, new sentences present in both.
Art edition against plain HTML, text with tags stripped: identical body. Three differences only: the art page adds the subtitle on its cover, adds a table of contents, and prints the AI-assisted line above the abstract where the plain page prints it after the abstract. I did not compare the plain page's order with v9's.

## 7. Anything else made stale

Scanned all v10 .tex for untested / in progress / unfinished / one refinement / extrapol / third level / converged: every hit is either new agreed text or unrelated (l.181, sec_new_door l.28, start-time and grid-or-time-step "untested", which stand). Nothing further found in the paper.
Still open from phase 1, unchanged by this surgery: the abstract and Appendix C say every verdict's arithmetic is machine-checked in Lean; the second- and third-level verdicts are not in Lean (T12). Figure fig:link's image still carries the legend "rate 1.11 (inner pairs)"; the caption now says first-level (T3).

## Phase 3

Final verdict: SLIPS FOUND (three small leftovers, none in the paper's text or numbers; the paper itself is CLEAN)

Package checked: B/out_v10/When_the_Neutrinos_Leave_v10_package/

Confirmed
1. Equation: neutrinos_v10.tex l.238 ends with a semicolon; l.240 reads "sit near its upper edge, the second $0.0002$ above it". Present in the PDF and both HTML files; "sit at its upper edge" is gone from all three.
2. Diff against paper_v9_frozen, re-hashed: the same five differing files as in phase 2 and nothing else. neutrinos_v10.tex differs on the same seven lines (15, 22, 236, 238, 240, 262, 293); sec_new_mcc.tex one line; app_new_evidence.tex l.68 (now also naming richardson.py and oddrate.py) plus five listing lines. New files in code/A6: res_L3_r08.json, level3_rates.py and its output, richardson.py, richardson_out.json, oddrate.py; each byte-equal to A6_refine2. code/A6/oddrate.py is byte-identical to code_v6/A1_oddrate.py, as B.27 says.
3. Preregistration: first 4675 bytes still equal the frozen v9 copy; the RESULT block is unchanged in length and content from phase 2; the NOTE is a pure append, stamped 22:07Z, equal to the file's write time. richardson.py rerun in paper_v10/code/A6 reproduces richardson_out.json byte for byte: bracket part 0.04139, order part 0.00126, sum 0.04265, order 6.23, R_inf 1.10126, kill False. The NOTE's 0.041, 0.001, 0.043 are right.
4. Harness: claims.py run from inside the package (cd checks && python3 -W ignore claims.py): 12 checks, 0 failed. C11 now asserts the conclusion sentence, the sign clause, the kill-line clause, the upper-edge clause and the count of 1.11 mentions (3), recomputes 0.0038 and 0.0036, and reads the README and Zenodo text. Tags renamed.
5. Package: every paper file equals B/nu6/paper_v10 (built intermediates left out; art/ added). PDF, both HTML files, Zenodo text, README and claims.py equal their sources. lean/ and mixer/ are byte-identical to the v9 package; checks/v9/ is byte-identical to the v9 package's checks/. README statements about folders and files checked one by one: all present as named.
6. PDF: 131 pages, no Type 3 fonts; carries the final wording, the NOTE, richardson.py and its output; none of the removed sentences. Plain and art HTML likewise; their texts still differ only by the cover subtitle, the table of contents and the position of the AI-assisted line.

Leftovers
L1. checks/guard.py does not run as the README describes. README l.19 says it "needs the version 9 source: set NU_OLD"; inside the package it also needs NU_NEW, because its default is ../paper_v10 and the package folder is ../paper. With NU_OLD only it stops with FileNotFoundError. With NU_NEW=../paper it passes (13 change blocks, 0 unregistered; run on a copy so the package was not written to). Fix: default NU_NEW to ../paper, or name NU_NEW in the README line.
L2. The NOTE's explanation of the large bracket part is worded for the four-corner picture of level3_rates.py, not for what richardson.py does. richardson.py takes the eight combinations of range ends; six give no extrapolation (the shift does not shrink) and the other two give fitted orders 0.14 and 0.36, below 0.5. The NOTE says "at one corner ... the shift does not shrink ... and at another the fitted order is far outside [0.5, 4]". The numbers are right; the sentence describes the wrong script. Also "richardson.py (written 2026-11-11, before the runs)": its file time is 14:45:17 local, 18 s after the queue was launched and 69 min before the first run ended. "Before any run finished" is the exact statement. Any fix must be a further appended line, not an edit.
L3. paper/art/check_same_text.py takes two file arguments and stops with IndexError when run bare; the README calls it "its check" without saying how to run it. Not checked further (outside the surgery). And checks/WATCHER_REPORT_v10.md in the package is the phase-2 copy: recopy it after this section.

Unchanged notes from phase 2: the 0.59 rounding edge; the Lean scope sentence (T12); the "rate 1.11 (inner pairs)" legend inside the Figure 7 image, covered by the caption.
