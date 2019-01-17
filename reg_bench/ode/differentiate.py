from functools import partial

import numpy as np
import scipy as sp
from finitediff import interpolate_by_finite_diff as ifd
from scipy import sparse
from scipy.sparse import linalg as splin


def diff(t, x, kind="simple_finite_diff", **kwargs):
    if kind == "tvregdiff":
        method = tvregdiff
    elif kind == "finitediff":
        method = finitediff
    elif kind == "simple_finite_diff":
        method = simple_finite_diff
    else:
        raise NotImplemented(f"Method {kind} not available.")
    return method(t, x, **kwargs)


def simple_finite_diff(t, x):
    """
    Compute time-derivative of the data matrix X along first axis.
    x : array-like, shape (n_samples, n_features)
        Input variables to be derived.
    """

    dt = t[1] - t[0]
    dx = np.zeros_like(x)
    dx[1:-1, :] = (x[2:, :] - x[:-2, :]) / (2.0 * dt)

    dx[0, :] = (x[1, :] - x[0, :]) / dt
    dx[-1, :] = (x[-1, :] - x[-2, :]) / dt

    return dx


def finitediff(t, x, order=2, n_points=1, n_fit_ratio=10):
    """Compute time-derivative of the data matrix X along first axis.

    Args:
        t : shape(n_samples)
        x : array-like, shape (n_samples, n_features)
            Input variables to be derived.
    """

    t_fit = np.linspace(t[0], t[-1], num=len(t) * n_fit_ratio, endpoint=True)

    t_fit[0] = t_fit[0] + (t_fit[1] - t_fit[0]) / 2
    t_fit[-1] = t_fit[-2] + (t_fit[-1] - t_fit[-2]) / 2
    return ifd(t, x, t_fit, order, n_points, n_points)[::n_fit_ratio, ..., 1:]


def tvregdiff(t, x, **kwargs):
    dt = t[1] - t[0]
    reshape = len(x.shape) == 1
    if reshape:
        x = x.reshape(-1, 1)
    dx = np.apply_along_axis(_tvregdiff, 0, x, dx=dt, **kwargs)[:-1]
    if reshape:
        dx = dx.reshape(-1)
    return dx


def _tvregdiff(data, itern=25, alph=0.05, u0=None, scale="small", ep=1e-6, dx=None, diagflag=0):
    # u = TVRegDiff( data, iter, alph, u0, scale, ep, dx, plotflag, diagflag );
    #
    # Rick Chartrand (rickc@lanl.gov), Apr. 10, 2011
    # Please cite Rick Chartrand, "Numerical differentiation of noisy,
    # nonsmooth data," ISRN Applied Mathematics, Vol. 2011, Article ID 164564,
    # 2011.
    #
    # Inputs:  (First three required; omitting the final N parameters for N < 7
    #           or passing in [] results in default values being used.)
    #       data        Vector of data to be differentiated.
    #
    #       iter        Number of iterations to run the main loop.  A stopping
    #                   condition based on the norm of the gradient vector g
    #                   below would be an easy modification.  No default value.
    #
    #       alph        Regularization parameter.  This is the main parameter
    #                   to fiddle with.  Start by varying by orders of
    #                   magnitude until reasonable results are obtained.  A
    #                   value to the nearest power of 10 is usally adequate.
    #                   No default value.  Higher values increase
    #                   regularization strenght and improve conditioning.
    #
    #       u0          Initialization of the iteration.  Default value is the
    #                   naive derivative (without scaling), of appropriate
    #                   length (this being different for the two methods).
    #                   Although the solution is theoretically independent of
    #                   the initialization, a poor choice can exacerbate
    #                   conditioning issues when the linear system is solved.
    #
    #       scale       'large' or 'small' (case insensitive).  Default is
    #                   'small'.  'small' has somewhat better boundary
    #                   behavior, but becomes unwieldly for data larger than
    #                   1000 entries or so.  'large' has simpler numerics but
    #                   is more efficient for large-scale problems.  'large' is
    #                   more readily modified for higher-order derivatives,
    #                   since the implicit differentiation matrix is square.
    #
    #       ep          Parameter for avoiding division by zero.  Default value
    #                   is 1e-6.  Results should not be very sensitive to the
    #                   value.  Larger values improve conditioning and
    #                   therefore speed, while smaller values give more
    #                   accurate results with sharper jumps.
    #
    #       dx          Grid spacing, used in the definition of the derivative
    #                   operators.  Default is the reciprocal of the data size.
    #
    #       plotflag    Flag whether to display plot at each iteration.
    #                   Default is 1 (yes).  Useful, but adds significant
    #                   running time.
    #
    #       diagflag    Flag whether to display diagnostics at each
    #                   iteration.  Default is 1 (yes).  Useful for diagnosing
    #                   preconditioning problems.  When tolerance is not met,
    #                   an early iterate being best is more worrying than a
    #                   large relative residual.
    #
    # Output:
    #
    #       u           Estimate of the regularized derivative of data.  Due to
    #                   different grid assumptions, length( u ) =
    #                   length( data ) + 1 if scale = 'small', otherwise
    #                   length( u ) = length( data ).

    # Copyright notice:
    # Copyright 2010. Los Alamos National Security, LLC. This material
    # was produced under U.S. Government contract DE-AC52-06NA25396 for
    # Los Alamos National Laboratory, which is operated by Los Alamos
    # National Security, LLC, for the U.S. Department of Energy. The
    # Government is granted for, itself and others acting on its
    # behalf, a paid-up, nonexclusive, irrevocable worldwide license in
    # this material to reproduce, prepare derivative works, and perform
    # publicly and display publicly. Beginning five (5) years after
    # (March 31, 2011) permission to assert copyright was obtained,
    # subject to additional five-year worldwide renewals, the
    # Government is granted for itself and others acting on its behalf
    # a paid-up, nonexclusive, irrevocable worldwide license in this
    # material to reproduce, prepare derivative works, distribute
    # copies to the public, perform publicly and display publicly, and
    # to permit others to do so. NEITHER THE UNITED STATES NOR THE
    # UNITED STATES DEPARTMENT OF ENERGY, NOR LOS ALAMOS NATIONAL
    # SECURITY, LLC, NOR ANY OF THEIR EMPLOYEES, MAKES ANY WARRANTY,
    # EXPRESS OR IMPLIED, OR ASSUMES ANY LEGAL LIABILITY OR
    # RESPONSIBILITY FOR THE ACCURACY, COMPLETENESS, OR USEFULNESS OF
    # ANY INFORMATION, APPARATUS, PRODUCT, OR PROCESS DISCLOSED, OR
    # REPRESENTS THAT ITS USE WOULD NOT INFRINGE PRIVATELY OWNED
    # RIGHTS.

    # BSD License notice:
    # Redistribution and use in source and binary forms, with or without
    # modification, are permitted provided that the following conditions
    # are met:
    #
    #      Redistributions of source code must retain the above
    #      copyright notice, this list of conditions and the following
    #      disclaimer.
    #      Redistributions in binary form must reproduce the above
    #      copyright notice, this list of conditions and the following
    #      disclaimer in the documentation and/or other materials
    #      provided with the distribution.
    #      Neither the name of Los Alamos National Security nor the names of its
    #      contributors may be used to endorse or promote products
    #      derived from this software without specific prior written
    #      permission.
    #
    # THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
    # CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
    # INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
    # MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    # DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
    # CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    # SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
    # LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
    # USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
    # AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
    # LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
    # ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    # POSSIBILITY OF SUCH DAMAGE.
    #
    #########################################################
    #                                                       #
    # Python translation by Simone Sturniolo                #
    # Rutherford Appleton Laboratory, STFC, UK (2014)       #
    # simonesturniolo@gmail.com                             #
    #                                                       #
    #########################################################

    def chop(v):
        return v[1:]

    # code starts here
    # Make sure we have a column vector
    data = np.array(data)
    if len(data.shape) != 1:
        print("Error - data is not a column vector")
        return
    # Get the data size.
    n = len(data)

    # Default checking. (u0 is done separately within each method.)
    if dx is None:
        dx = 1.0 / n

    # Different methods for small- and large-scale problems.
    if scale.lower() == "small":

        # Construct differentiation matrix.
        c = np.ones(n + 1) / dx
        D = sparse.spdiags([-c, c], [0, 1], n, n + 1)

        DT = D.transpose()

        # Construct antidifferentiation operator and its adjoint.
        def A(x):
            return chop(np.cumsum(x) - 0.5 * (x + x[0])) * dx

        def AT(w):
            return (
                sum(w) * np.ones(n + 1)
                - np.transpose(np.concatenate(([sum(w) / 2.0], np.cumsum(w) - w / 2.0)))
            ) * dx

        # Default initialization is naive derivative

        if u0 is None:
            u0 = np.concatenate(([0], np.diff(data), [0]))

        u = u0
        # Since Au( 0 ) = 0, we need to adjust.
        ofst = data[0]
        # Precompute.
        ATb = AT(ofst - data)  # input: size n

        # Main loop.
        for ii in range(1, itern + 1):
            # Diagonal matrix of weights, for linearizing E-L equation.
            Q = sparse.spdiags(1.0 / (np.sqrt((D * u) ** 2 + ep)), 0, n, n)
            # Linearized diffusion matrix, also approximation of Hessian.
            L = dx * DT * Q * D

            # Gradient of functional.
            g = AT(A(u)) + ATb + alph * L * u

            # Prepare to solve linear equation.
            tol = 1e-4
            maxit = 100
            # Simple preconditioner.
            P = alph * sparse.spdiags(L.diagonal() + 1, 0, n + 1, n + 1)

            def linop(v):
                return alph * L * v + AT(A(v))

            linop = splin.LinearOperator((n + 1, n + 1), linop)

            if diagflag:
                [s, info_i] = sparse.linalg.cg(linop, g, x0=None, tol=tol, maxiter=maxit, callback=None, M=P)
                print(
                    "iteration {0:4d}: relative change = {1:.3e}, "
                    "gradient norm = {2:.3e}\n".format(
                        ii, np.linalg.norm(s[0]) / np.linalg.norm(u), np.linalg.norm(g)
                    )
                )
                if info_i > 0:
                    print("WARNING - convergence to tolerance not achieved!")
                elif info_i < 0:
                    print("WARNING - illegal input or breakdown")
            else:
                [s, info_i] = sparse.linalg.cg(linop, g, x0=None, tol=tol, maxiter=maxit, callback=None, M=P)
            # Update solution.
            u = u - s

    elif scale.lower() == "large":

        # Construct antidifferentiation operator and its adjoint.
        def A(v):
            return np.cumsum(v)

        def AT(w):
            return sum(w) * np.ones(len(w)) - np.transpose(np.concatenate(([0.0], np.cumsum(w[:-1]))))

        # Construct differentiation matrix.
        c = np.ones(n)
        D = sparse.spdiags([-c, c], [0, 1], n, n) / dx
        mask = np.ones((n, n))
        mask[-1, -1] = 0.0
        D = sparse.dia_matrix(D.multiply(mask))
        DT = D.transpose()
        # Since Au( 0 ) = 0, we need to adjust.
        data = data - data[0]
        # Default initialization is naive derivative.
        if u0 is None:
            u0 = np.concatenate(([0], np.diff(data)))
        u = u0
        # Precompute.
        ATd = AT(data)

        # Main loop.
        for ii in range(1, itern + 1):
            # Diagonal matrix of weights, for linearizing E-L equation.
            Q = sparse.spdiags(1.0 / np.sqrt((D * u) ** 2.0 + ep), 0, n, n)
            # Linearized diffusion matrix, also approximation of Hessian.
            L = DT * Q * D
            # Gradient of functional.
            g = AT(A(u)) - ATd
            g = g + alph * L * u
            # Build preconditioner.
            c = np.cumsum(range(n, 0, -1))
            B = alph * L + sparse.spdiags(c[::-1], 0, n, n)
            # droptol = 1.0e-2
            R = sparse.dia_matrix(np.linalg.cholesky(B.todense()))
            # Prepare to solve linear equation.
            tol = 1.0e-4
            maxit = 100

            def linop(v):
                return alph * L * v + AT(A(v))

            linop = splin.LinearOperator((n, n), linop)

            if diagflag:
                [s, info_i] = sparse.linalg.cg(
                    linop, -g, x0=None, tol=tol, maxiter=maxit, callback=None, M=np.dot(R.transpose(), R)
                )
                print(
                    "iteration {0:4d}: relative change = {1:.3e}, "
                    "gradient norm = {2:.3e}\n".format(
                        ii, np.linalg.norm(s[0]) / np.linalg.norm(u), np.linalg.norm(g)
                    )
                )
                if info_i > 0:
                    print("WARNING - convergence to tolerance not achieved!")
                elif info_i < 0:
                    print("WARNING - illegal input or breakdown")

            else:
                [s, info_i] = sparse.linalg.cg(
                    linop, -g, x0=None, tol=tol, maxiter=maxit, callback=None, M=np.dot(R.transpose(), R)
                )
            # Update current solution
            u = u + s
        u = u / dx

    return u
