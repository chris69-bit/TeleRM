"""Single entry point. Run from the repository root.

  python run.py demo [args]            M1 admission demo
  python run.py perf [args]            M2 load sweep
  python run.py sweep [args]           Docker sweep (M3+)
  python run.py milestone N [args]     experiment runner for milestone N (3-6)
  python run.py analyze N [args]       charts/tables for milestone N (2-6)
  python run.py cluster | real-sites   M5 helpers
  python run.py smoke                  quick smoke test
"""
import importlib.util
import runpy
import sys

FIXED = {"demo": "experiments.run_demo",
         "perf": "experiments.perf_experiment",
         "sweep": "experiments.docker_sweep",
         "cluster": "experiments.cluster",
         "real-sites": "experiments.real_sites",
         "smoke": "tests.test_smoke"}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return
    cmd, rest = sys.argv[1], sys.argv[2:]
    if cmd in ("milestone", "analyze"):
        if not rest:
            sys.exit("usage: python run.py %s N [args]" % cmd)
        n, rest = rest[0], rest[1:]
        if cmd == "milestone":
            mod = "experiments.m%s_run" % n
        else:
            mod = "analysis.analyze" if n == "2" else "analysis.analyze_m%s" % n
    elif cmd in FIXED:
        mod = FIXED[cmd]
    else:
        sys.exit("unknown command %r\n%s" % (cmd, __doc__))
    if importlib.util.find_spec(mod) is None:
        sys.exit("%s is not part of this version of the project" % mod)
    sys.argv = [mod] + rest
    runpy.run_module(mod, run_name="__main__", alter_sys=True)


if __name__ == "__main__":
    main()
