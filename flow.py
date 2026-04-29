from metaflow import FlowSpec, conda, step


def _probe():
    import sys
    import llvmlite
    from numba import __version__ as nbv, njit

    @njit
    def f(x):
        return x ** 2

    x = 94906267
    py_ans = x ** 2
    jit_ans = f(x)

    return {
        "py": sys.version.split()[0],
        "numba": nbv,
        "llvmlite": llvmlite.__version__,
        "py_ans": py_ans,
        "jit_ans": int(jit_ans),
        "diff": int(jit_ans) - py_ans,
    }


class NumbaIssue9931(FlowSpec):

    @step
    def start(self):
        self.next(
            self.py310_nb061,
            self.py311_nb061,
            self.py311_nb063,
            self.py311_nb064,
            self.py312_nb061,
            self.py312_nb063,
            self.py312_nb064,
        )

    @conda(python="3.10", packages={"numba": "0.61.0"})
    @step
    def py310_nb061(self):
        self.result = _probe()
        self.next(self.join)

    @conda(python="3.11", packages={"numba": "0.61.0"})
    @step
    def py311_nb061(self):
        self.result = _probe()
        self.next(self.join)

    @conda(python="3.11", packages={"numba": "0.63"})
    @step
    def py311_nb063(self):
        self.result = _probe()
        self.next(self.join)

    @conda(python="3.11", packages={"numba": "0.64"})
    @step
    def py311_nb064(self):
        self.result = _probe()
        self.next(self.join)

    @conda(python="3.12", packages={"numba": "0.61.0"})
    @step
    def py312_nb061(self):
        self.result = _probe()
        self.next(self.join)

    @conda(python="3.12", packages={"numba": "0.63"})
    @step
    def py312_nb063(self):
        self.result = _probe()
        self.next(self.join)

    @conda(python="3.12", packages={"numba": "0.64"})
    @step
    def py312_nb064(self):
        self.result = _probe()
        self.next(self.join)

    @step
    def join(self, inputs):
        self.results = sorted(
            [i.result for i in inputs],
            key=lambda r: (r["py"], r["numba"]),
        )
        self.next(self.end)

    @step
    def end(self):
        x = 94906267
        py_ans = x ** 2
        print(f"  x={x}  x**2 (python)={py_ans}\n")
        print(f"{'python':<10}{'numba':<10}{'llvmlite':<12}"
              f"{'jit(x**2)':<22}{'diff':<6}")
        print("-" * 60)
        for r in self.results:
            print(f"{r['py']:<10}{r['numba']:<10}{r['llvmlite']:<12}"
                  f"{r['jit_ans']:<22}{r['diff']:<6}")


if __name__ == "__main__":
    NumbaIssue9931()
