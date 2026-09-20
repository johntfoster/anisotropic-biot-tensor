#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Objective mineral and volume-only conformal distention constitutive model.

Energy is per reference mixture volume; mineral energy is per reference mineral
volume. Stresses, stiffnesses, pressure, and energies share an arbitrary stress
unit. F, a, mineral volume ratio, fractions, rotations, and B are dimensionless.
Mandel order is (11, 22, 33, sqrt(2)*23, sqrt(2)*13, sqrt(2)*12).
"""
from dataclasses import dataclass, field
import numpy as np
from scipy.optimize import brentq

I = np.eye(3)
BASIS = np.zeros((6, 3, 3))
for n in range(3):
    BASIS[n, n, n] = 1
for n, (i, j) in enumerate(((1, 2), (0, 2), (0, 1)), 3):
    BASIS[n, i, j] = BASIS[n, j, i] = 1 / np.sqrt(2)
ONE = np.array([1., 1., 1., 0., 0., 0.])
DEFAULT_CS = np.diag([50., 60., 70., 20., 24., 28.])
DEFAULT_CS[:3, :3] = [[50., 12., 10.], [12., 60., 14.], [10., 14., 70.]]


def vec(t):
    return np.einsum('aij,ij->a', BASIS, t)


def mat(v):
    return np.einsum('a,aij->ij', v, BASIS)


def log_symmetric(c):
    values, vectors = np.linalg.eigh(c)
    if np.min(values) <= 0:
        raise ValueError('The metric must be positive definite.')
    return (vectors * np.log(values)) @ vectors.T


def log_frechet(c, direction):
    """Exact spectral logarithm derivative, including repeated eigenvalues."""
    values, vectors = np.linalg.eigh(c)
    if np.min(values) <= 0:
        raise ValueError('The metric must be positive definite.')
    midpoint = (values[:, None] + values[None, :]) / 2
    z = (values[:, None] - values[None, :]) / (2 * midpoint)
    divided = np.empty((3, 3))
    small = np.abs(z) < 1e-4
    divided[small] = (1 + z[small]**2/3 + z[small]**4/5) / midpoint[small]
    divided[~small] = 2*np.arctanh(z[~small]) / (2*midpoint[~small]*z[~small])
    return vectors @ (divided * (vectors.T @ direction @ vectors)) @ vectors.T


def isotropic_stiffness(ks, mu):
    return ks*np.outer(ONE, ONE) + 2*mu*(np.eye(6)-np.outer(ONE, ONE)/3)


@dataclass
class Model:
    cs: np.ndarray = field(default_factory=lambda: DEFAULT_CS.copy())
    phi: float = .6
    k: float = 7.

    def __post_init__(self):
        self.cs = np.asarray(self.cs, dtype=float)
        if self.cs.shape != (6, 6) or not np.allclose(self.cs, self.cs.T):
            raise ValueError('Mineral Mandel stiffness must be symmetric 6 by 6.')
        if np.min(np.linalg.eigvalsh(self.cs)) <= 0:
            raise ValueError('Mineral stiffness must be positive definite.')
        self.ks = float(ONE @ self.cs @ ONE / 9)
        if not (0 < self.phi < 1 and 0 < self.k < self.phi*self.ks):
            raise ValueError('Require 0 < phi < 1 and 0 < K < phi*Ks.')
        self.alpha = 1-self.k/(self.phi*self.ks)
        self.ka = self.k/self.alpha
        row = self.cs @ ONE
        self.cd = self.phi*self.cs-self.phi*self.alpha/(9*self.ks)*np.outer(row, row)
        # The isotropic comparison retains Ks and the average deviatoric stiffness.
        self.mu_average = float(np.trace((np.eye(6)-np.outer(ONE, ONE)/3) @ self.cs)/10)

    def mineral(self, fbar):
        """Mineral energy and true-frame Kirchhoff stress (log-Hooke law)."""
        ebar = .5*log_symmetric(fbar.T @ fbar)
        stress_log = mat(self.cs @ vec(ebar))
        tau = fbar @ log_frechet(fbar.T @ fbar, stress_log) @ fbar.T
        return float(.5*np.sum(ebar*stress_log)), tau

    def state(self, f, p, rotation=I):
        """Solve eq:anisotropic-mineral-eos and evaluate the full spatial stress.

        The conformal internal rotation is a frame choice at fixed physical F.
        eq:rotated-mineral-kirchhoff converts its mineral stress to spatial axes.
        eq:anisotropic-biot-explicit gives B; the reduced pressure potential is
        W + phi*p*Jbar - p*J and its F derivative gives total Piola stress.
        """
        f, rotation = np.asarray(f), np.asarray(rotation)
        j = float(np.linalg.det(f))
        if not j > 0:
            raise ValueError('Require det(F) > 0.')
        if (np.linalg.norm(rotation.T @ rotation-I) > 1e-10
                or abs(np.linalg.det(rotation)-1) > 1e-10):
            raise ValueError('The internal rotation must be proper orthogonal.')
        e = .5*log_symmetric(f.T @ f)
        dev = e-np.trace(e)*I/3
        shape = float(ONE @ self.cs @ vec(dev))
        target = self.k/(self.phi*self.ks)*np.log(j)-self.alpha/(3*self.ks)*shape
        if not np.isfinite(p):
            raise ValueError('Pressure must be finite.')
        # Shift q by its zero-pressure value. The scaled residual is
        # z + sign(p)*exp(log_magnitude + z), with z = q - target.
        # Negative pressure has a turning point; only its increasing branch
        # is continuous from p=0 and has positive scalar stability.
        if p == 0:
            shift = 0.
        else:
            log_magnitude = np.log(self.alpha)+np.log(abs(p))-np.log(self.ks)+target
            def shifted_residual(z):
                return z+np.sign(p)*np.exp(log_magnitude+z)
            if p < 0:
                turning_point = -log_magnitude
                if turning_point <= 1:
                    raise ValueError('No strictly stable scalar branch exists at this pressure.')
                lower, upper = 0., turning_point
            else:
                # These bounds straddle the unique root without evaluating
                # the exponential at a potentially overflowing z=0.
                lower = -max(1., log_magnitude+1.)
                upper = (-log_magnitude+np.log1p(log_magnitude)
                         if log_magnitude > 0 else 0.)
            shift = brentq(shifted_residual, lower, upper, xtol=5e-15)
        q = target+shift
        def residual(q):
            return self.ks*(q-target)+self.alpha*p*np.exp(q)
        y = float(np.exp(q))
        a = j/y
        solid = self.phi*y/j
        denominator = self.ks+self.alpha*p*y
        if not (0 < solid < 1):
            raise ValueError('State violates positive solid and fluid volume fractions.')
        if not denominator > 0:
            raise ValueError('State is not on the strictly stable scalar branch.')
        fbar = a**(-1/3)*rotation.T @ f
        wm, tau_true = self.mineral(fbar)
        tau_space = rotation @ tau_true @ rotation.T
        sigma = self.phi/j*tau_space-(1-solid)*p*I
        # eq:equivalent-anisotropic-energy, energy per reference mixture volume.
        w = self.ka*np.log(a)**2/2+self.phi*wm
        dev_cs_i = mat(self.cs @ ONE)-3*self.ks*I
        b = I-y/(j*denominator)*(self.k*I-self.phi*self.alpha/3
                *f @ log_frechet(f.T @ f, dev_cs_i) @ f.T)
        storage = self.phi*self.alpha*y*y/denominator
        return dict(J=j, y=y, a=a, q=q, solid_fraction=solid, Fbar=fbar,
                    tau_true=tau_true, tau_space=tau_space, W=float(w),
                    potential=float(w+self.phi*p*y-p*j), sigma=sigma, B=b,
                    storage=float(storage), residual=float(residual(q)),
                    stability=denominator)


def shear_gradient(gamma):
    """Isochoric finite stretch plus simple shear, material axes fixed."""
    return np.array([[np.exp(.12), gamma, 0.],
                     [0., np.exp(-.04), 0.], [0., 0., np.exp(-.08)]])


def rotation_z(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s, 0.], [s, c, 0.], [0., 0., 1.]])
