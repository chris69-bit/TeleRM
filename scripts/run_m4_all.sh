#!/bin/sh
# Runs every Milestone 4 experiment (about 35 minutes on a 2-core machine).
set -e
cd "$(dirname "$0")"
OUT=results/M4
echo "== E1: coordination overhead vs cluster size";   python3 -m experiments.m4_run overhead    --reps 3 --out $OUT
echo "== E2: synchronization delay vs placement";      python3 -m experiments.m4_run placement   --reps 3 --out $OUT
echo "== E3: leader crash and election";               python3 -m experiments.m4_run failover    --reps 10 --out $OUT
echo "== E4: consistency (uncoordinated vs Raft)";     python3 -m experiments.m4_run consistency --reps 3 --out $OUT
echo "== E5: event ordering with skewed clocks";       python3 -m experiments.m4_run clocks      --reps 10 --out $OUT
echo "== E6: whole system, traffic while the leader is killed"
for rep in 1 2 3; do
  python3 -m experiments.m3_run traffic --arch s3 --loads 150 --rep-start $rep --policies tier_aware --out results/M4-traffic
  python3 -m experiments.m3_run traffic --arch s4 --loads 150 --rep-start $rep --policies tier_aware --out results/M4-traffic
  python3 -m experiments.m3_run traffic --arch s4 --loads 150 --rep-start $rep --policies tier_aware --kill-leader-at 8 --tag kill --out results/M4-traffic
done
echo "== all done"
