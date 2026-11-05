# SCRIPT: NU-V4-REPRODUCE-FINAL  one command sequence for every final threshold of the paper (strict v2 rule: only a detected horizon or a dispersal moves a bracket), then the endpoint audit, then the ruler check with full corner enumeration.
: "${SIMDIR:?set SIMDIR to PBH_neutrino_simulation/simulation (McCormick, commit 41a0f83)}"
cd "$(dirname "$0")"
set -e
B='"fnu":0.409,"N":400,"K":32,"eps0":0.1,"eps_dec":2.0,"eps_max":15.0,"nexp":3'
# each line: tag  runner  bracket-lo  bracket-hi  tolerance  kwargs   (brackets are the published bracket widened by 1e-3 each side; the result lands in res_<tag>.json, the log in log_<tag>.txt)
python3 trisect_v2.py E_fnu020_ed2_n3 run_nuc_n_v2 0.50293 0.50500 3.15e-05 "{$B,\"fnu\":0.2}" > log_E_fnu020_ed2_n3_repro.txt 2>&1
python3 trisect_v2.py F_r025 run_split_v2 0.51546 0.51754 3.79e-05 "{$B,\"rr\":0.25}" > log_F_r025_repro.txt 2>&1
python3 trisect_v2.py F_r4 run_split_v2 0.50440 0.50648 3.79e-05 "{$B,\"rr\":4.0}" > log_F_r4_repro.txt 2>&1
python3 trisect_v2.py F2_r1o16 run_split_v2 0.52045 0.52252 3.77e-05 "{$B,\"rr\":0.0625}" > log_F2_r1o16_repro.txt 2>&1
python3 trisect_v2.py F2_r16 run_split_v2 0.50065 0.50270 2.53e-05 "{$B,\"rr\":16.0}" > log_F2_r16_repro.txt 2>&1
python3 trisect_v2.py H1_r1 run_split_v2 0.50972 0.51176 1.85e-05 "{$B,\"rr\":1.0}" > log_H1_r1_repro.txt 2>&1
python3 trisect_v2.py I_r025_dt4 run_split_dt_v2 0.51548 0.51752 1.85e-05 "{$B,\"rr\":0.25,\"dtk\":4.0}" > log_I_r025_dt4_repro.txt 2>&1
python3 trisect_v2.py J_r2 run_split_v2 0.50696 0.50898 1.03e-05 "{$B,\"rr\":2.0}" > log_J_r2_repro.txt 2>&1
python3 trisect_v2.py J_r05 run_split_v2 0.51265 0.51467 1.03e-05 "{$B,\"rr\":0.5}" > log_J_r05_repro.txt 2>&1
python3 trisect_v2.py K_r125_clean run_split_v2 0.50884 0.51084 1e-06 "{$B,\"rr\":1.25}" > log_K_r125_clean_repro.txt 2>&1
python3 trisect_v2.py K_r08_clean run_split_v2 0.51070 0.51270 1e-06 "{$B,\"rr\":0.8}" > log_K_r08_clean_repro.txt 2>&1
python3 trisect_v2.py L_r4 run_shear_v2 0.50423 0.50624 3.7e-06 "{$B,\"rr\":4.0}" > log_L_r4_repro.txt 2>&1
python3 trisect_v2.py L_r025 run_shear_v2 0.51609 0.51810 3.7e-06 "{$B,\"rr\":0.25}" > log_L_r025_repro.txt 2>&1
python3 trisect_v2.py M_r4_K48 run_split_v2 0.50449 0.50650 8.2e-06 "{$B,\"rr\":4.0,\"K\":48}" > log_M_r4_K48_repro.txt 2>&1
python3 trisect_v2.py M_r025_K48 run_split_v2 0.51555 0.51756 4.1e-06 "{$B,\"rr\":0.25,\"K\":48}" > log_M_r025_K48_repro.txt 2>&1
python3 trisect_v2.py A1_shear_r12 run_shear_v2 0.50895 0.51095 1e-06 "{$B,\"rr\":1.2}" > log_A1_shear_r12_repro.txt 2>&1
python3 trisect_v2.py A1_shear_r083 run_shear_v2 0.51057 0.51257 1e-06 "{$B,\"rr\":0.8333333333333334}" > log_A1_shear_r083_repro.txt 2>&1
python3 trisect_v2.py A1_all_r12 run_split_v2 0.50901 0.51102 1e-06 "{$B,\"rr\":1.2}" > log_A1_all_r12_repro.txt 2>&1
python3 trisect_v2.py A1_all_r083 run_split_v2 0.51051 0.51251 1e-06 "{$B,\"rr\":0.8333333333333334}" > log_A1_all_r083_repro.txt 2>&1
python3 edge_audit.py > log_B1_edges_repro.txt 2>&1          # 30 endpoints: lower edge must be a dispersal, upper edge a detected horizon
python3 ruler/ruler_state.py > ruler/out_state_repro.txt 2>&1   # ruler (e) and controls
python3 ruler/ruler_corners.py > ruler/out_corners_repro.txt 2>&1  # every statistic at all 2^15 bracket corners
python3 ../witness/prod_log_to_json.py && python3 ../main/make_fig6_door.py && python3 make_fig7_link_v5.py   # figures from the shipped logs
echo done
