#!/usr/bin/env python3

# The Expat License
#
# Copyright (c) 2020, Shlomi Fish
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys
import time


global stop
stop = False


def _my_alarm_handler(signum, frame):
    global stop
    stop = True


def mytest(run_mode, p, verbose=False):
    def verbose_print(*args, **e):
        if verbose:
            print(*args, **e)
    global stop
    start = time.time()
    pint2p = p << p
    reached = top = 1000
    myrange = range(top)
    if run_mode == "builtinpow":
        ret = pow(2, (1 << p), pint2p)
    elif run_mode == "gmpy":
        from gmpy2 import mpz
        ret = mpz(2)
        pint2p = mpz(pint2p)
        mod = mpz(10 ** 20)
        for i in myrange:
            verbose_print('sq', i, flush=True)
            ret *= ret
            verbose_print('mod', i, flush=True)
            ret %= pint2p
            verbose_print('after mod', i, (ret % mod), flush=True)
    elif run_mode == "builtinops":
        ret = 2
        for i in myrange:
            if stop:
                reached = i
                break
            verbose_print('sq', i, flush=True)
            ret *= ret
            verbose_print('mod', i, flush=True)
            ret %= pint2p
            verbose_print('after mod', i, (ret % 10 ** 20), flush=True)
    else:
        from shift_divmod import ShiftDivMod
        ret = 2
        display = ShiftDivMod.from_int(10 ** 20)
        if run_mode == "test":
            for m in range(2, 10000):
                verbose_print("Testing m =", m, flush=True)
                modder = ShiftDivMod.from_int(m)
                for x in range(10*m):
                    d, mod = modder.divmod(x)
                    assert x == d*modder.n + mod
                    assert 0 <= mod < modder.n
                    assert (d, mod) == divmod(x, m)

        elif run_mode == "shiftmodpre":
            m = ShiftDivMod(p, p)
            for i in myrange:
                verbose_print('sq', i, flush=True)
                ret *= ret
                verbose_print('mod', i, flush=True)
                # m = ShiftDivMod.from_int(pint2p)
                d, mod = m.divmod(ret)
                if 0:
                    assert ret == d*m.n + mod
                    assert 0 <= mod < m.n
                ret = mod
                # ret = m.mod(ret)
                verbose_print('after mod', i, display.mod(ret), flush=True)
        elif run_mode == "gen_shift_mod":
            m = ShiftDivMod.from_int(pint2p)
            for i in myrange:
                verbose_print('sq', i, flush=True)
                ret *= ret
                verbose_print('mod', i, flush=True)
                ret = m.mod(ret)
                verbose_print('after mod', i, display.mod(ret), flush=True)
        elif run_mode == "jitshift":
            for i in myrange:
                verbose_print('sq', i, flush=True)
                ret *= ret
                verbose_print('mod', i, flush=True)
                ret = ShiftDivMod.from_int(pint2p).mod(ret)
                verbose_print('after mod', i, display.mod(ret), flush=True)
    ret = ret % (p*p) // p
    stopped = stop
    stop = False
    end = time.time()
    return {
        'val': ret, 'time': (end-start),
        'reached': reached,
        'interrupted': stopped, 'mode': run_mode,
    }


def main(which):
    run_mode = which
    '''
    if which == "builtinpow":
        OPT = 1
    elif which == "builtinops":
        OPT = 0
    elif which == "shiftmod":
        OPT = 2
    else:
        raise Exception("unknown choice")
    '''
    if run_mode == "bench":
        import signal
        bench = mytest(run_mode='gen_shift_mod', p=9816593)
        print(bench)
        bench = mytest(run_mode='shiftmodpre', p=9816593)
        print(bench)
        signal.signal(signal.SIGALRM, _my_alarm_handler)
        signal.alarm(100)
        bench = mytest(run_mode='builtinops', p=9816593)
        print(bench)
    else:
        x = mytest(run_mode=run_mode, p=9816593)
        print(x)


if __name__ == "__main__":
    main(sys.argv[1])
