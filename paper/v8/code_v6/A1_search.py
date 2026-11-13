# SCRIPT: NU-V6-SEARCH  sequential bisection (one simulation at a time) with v5.1's endpoint rule: only 'BH' (detected
# horizon) or 'dispersed' moves a bracket; 'crash' / 'BH_breakdown' get one retry at the lower Courant number, then are
# reported and skipped.  Both ends of the starting bracket are run first; an end with the other outcome extends the bracket.
# Resumable: progress is saved after every run in prog_<tag>.json.
import sys, os, json, time, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)

def main():
    tag, runner = sys.argv[1], sys.argv[2]
    center, half, tol = float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
    kw = json.loads(sys.argv[6]); cretry = float(sys.argv[7])
    mod = importlib.import_module(runner)
    pf = os.path.join(HERE, f'prog_{tag}.json'); lf = os.path.join(HERE, f'log_{tag}.txt'); master = os.path.join(HERE, 'RUNLOG.txt')
    if os.path.exists(pf):
        P = json.load(open(pf))
    else:
        P = dict(tag=tag, runner=runner, kw=kw, lo=None, hi=None, lo_try=center-half, hi_try=center+half, log=[], t_used=0.0)
    def save(): json.dump(P, open(pf, 'w'), indent=1)
    def say(s):
        line = time.strftime('%H:%M:%S ') + s
        print(line, flush=True); open(lf, 'a').write(line + '\n'); open(master, 'a').write(f'[{tag}] ' + line + '\n')
    def one(d):
        t1 = time.time(); o = mod.run(d, **kw); s = o['status']; note = ''
        if s not in ('BH', 'dispersed'):
            o = mod.run(d, **dict(kw, cfl_r=cretry, cfl_mu=cretry)); note = f' (retry at Courant {cretry} after {s})'; s = o['status']
        dtm = time.time() - t1; P['t_used'] += dtm
        rec = (d, s, float(o['eps']), float(o['Imin']), float(o['max2MR']), note, round(dtm, 1))
        P['log'].append(rec); save()
        say(f'{tag} delta={d:.8f}: {s} eps={o["eps"]:.4f} minI={o["Imin"]:.3e} steps={o["steps"]}{note} ({dtm:.0f}s)')
        return s
    # 1) the lower end must disperse
    while P['lo'] is None:
        d = P['lo_try']; s = one(d)
        if s == 'dispersed': P['lo'] = d
        elif s == 'BH': P['hi'] = d if P['hi'] is None else min(P['hi'], d); P['lo_try'] = d - 2*half
        else: say('lower end undecided after retry; stop'); save(); return
        save()
    # 2) the upper end must form a horizon
    while P['hi'] is None:
        d = P['hi_try']; s = one(d)
        if s == 'BH': P['hi'] = d
        elif s == 'dispersed': P['lo'] = max(P['lo'], d); P['hi_try'] = d + 2*half
        else: say('upper end undecided after retry; stop'); save(); return
        save()
    # 3) bisect
    while P['hi'] - P['lo'] > tol:
        lo, hi = P['lo'], P['hi']; moved = False
        for f in (0.5, 0.4, 0.6):
            d = lo + f*(hi - lo); s = one(d)
            if s == 'BH': P['hi'] = d; moved = True; break
            if s == 'dispersed': P['lo'] = d; moved = True; break
        save()
        if not moved: say('three points undecided; stop'); return
        if P['lo'] >= P['hi']: say('inconsistent outcomes; stop'); return
    lo, hi = P['lo'], P['hi']
    say(f'RESULT {tag}: delta_c = {0.5*(lo+hi):.8f} +- {0.5*(hi-lo):.8f}  bracket [{lo:.8f}, {hi:.8f}]  ({P["t_used"]/60:.1f} min of runs)')
    json.dump(dict(tag=tag, runner=runner, kw=kw, dc=0.5*(lo+hi), w=hi-lo, lo=lo, hi=hi, log=P['log']), open(os.path.join(HERE, f'res_{tag}.json'), 'w'), indent=1)

if __name__ == '__main__':
    main()
