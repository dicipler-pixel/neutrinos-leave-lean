# SCRIPT: NU-V4-QUEUE-AB  admissible shear test (A1), then endpoint audit (B1)
: "${SIMDIR:?set SIMDIR to PBH_neutrino_simulation/simulation}"
cd "$(dirname "$0")"
B='{"fnu":0.409,"N":400,"K":32,"eps0":0.1,"eps_dec":2.0,"eps_max":15.0,"nexp":3'
python3 trisect_v2.py A1_shear_r12 run_shear_v2 0.5080 0.5105 1e-6 "$B,\"rr\":1.2}" > log_A1_shear_r12.txt 2>&1
python3 trisect_v2.py A1_shear_r083 run_shear_v2 0.5110 0.5135 1e-6 "$B,\"rr\":0.8333333333333334}" > log_A1_shear_r083.txt 2>&1
python3 trisect_v2.py A1_all_r12 run_split_v2 0.5085 0.5105 1e-6 "$B,\"rr\":1.2}" > log_A1_all_r12.txt 2>&1
python3 trisect_v2.py A1_all_r083 run_split_v2 0.5108 0.5128 1e-6 "$B,\"rr\":0.8333333333333334}" > log_A1_all_r083.txt 2>&1
python3 edge_audit.py > log_B1_edges.txt 2>&1
tail -1 log_A1_*.txt; cat log_B1_edges.txt
