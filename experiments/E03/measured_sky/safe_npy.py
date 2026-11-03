"""Load an object .npy with a restricted unpickler that only allows numpy array reconstruction and plain types."""
import pickle, sys
import numpy as np
ALLOWED = {("numpy.core.multiarray", "_reconstruct"), ("numpy._core.multiarray", "_reconstruct"),
           ("numpy", "ndarray"), ("numpy", "dtype"), ("numpy.core.multiarray", "scalar"),
           ("numpy._core.multiarray", "scalar"), ("datetime", "datetime"), ("builtins", "str")}
class R(pickle.Unpickler):
    def find_class(self, m, n):
        if (m, n) in ALLOWED:
            return super().find_class(m, n)
        raise pickle.UnpicklingError(f"blocked {m}.{n}")
def load(path):
    f = open(path, "rb")
    v = np.lib.format.read_magic(f)
    np.lib.format.read_array_header_1_0(f) if v == (1, 0) else np.lib.format.read_array_header_2_0(f)
    return R(f).load()
if __name__ == "__main__":
    a = load(sys.argv[1])
    print(type(a), a.shape)
    for j in range(a.shape[1]):
        x = a[0, j]
        print(j, type(x), getattr(x, "shape", None), getattr(x, "dtype", None), str(x)[:80] if not hasattr(x, "shape") else "")
