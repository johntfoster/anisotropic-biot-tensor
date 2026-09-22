// SPDX-License-Identifier: Apache-2.0
#pragma once

// Reference-state (linearized) axisymmetric pore-fabric distention law.
//
// Implements the extension of sections/pore_fabric.tex of the manuscript:
//   * kinematics      A = R_A G^{1/2}, G = a^{2/3} H, H unimodular (det H = 1)
//                     E_d = ln(a)/3 I + ln(h) (1/2 I - 3/2 m (x) m)
//   * work conjugate  S_d = 2 dW_d/dG, used here through S_d = D4 : E_d
//   * restriction     (C^d)^{-1} = (phi_s0 C_s)^{-1} + D4^+
//                     (Moore-Penrose inverse; D4 is positive semidefinite)
//   * Biot tensor     B = I - C^d : C_s^{-1} : I  ->  B_par m (x) m + B_per (I - m (x) m)
//
// The distention strain E_d is restricted to the axisymmetric (volumetric and
// axial-deviatoric) subspace span(e1, e2) = range(D4); the four complementary
// symmetric modes are frozen into the mineral. Restricting E_d is what makes
// the transverse-isotropy ansatz hold exactly: with E_d = x1 e1 + x2 e2 the
// reconstructed fabric H = exp(2 E_d) equals h^{-2} m (x) m + h (I - m (x) m)
// with h = exp(ln h), so the reported ln_h IS the logarithm of the unimodular
// transverse fabric eigenvalue h.
//
// The reported distention scalars follow the manuscript convention. Writing
// E_d = sum_i x_i e_i in the basis below,
//   ln a = sqrt(3) x1      (e1 = I/sqrt(3))
//   ln h = -x2/sqrt(1.5)   because  1/2 I - 3/2 m (x) m = -sqrt(3/2) e2
// so that the reported ln_h equals the paper's ln h, and distention_h = h.
//
// The distention stiffness D4 is written in an orthonormal basis of the
// transversely isotropic invariant subspaces of symmetric tensors (Mandel
// metric), so that D4 = sum_ij Dd[i][j] e_i (x) e_j with
//   e1 = I/sqrt(3)                                  (volumetric)
//   e2 = sqrt(3/2) (m (x) m - I/3)                  (axial, degree-2)
// where m is the fabric axis. Dd is the positive definite two-by-two
// distention stiffness on the retained subspace with moduli
//   Dd[0][0] = fabric_volume_modulus      (pore volume change)
//   Dd[1][1] = fabric_axial_modulus       (pore shape change along m)
//   Dd[0][1] = Dd[1][0] = fabric_coupling (volume-shape coupling)
// D4 vanishes on the four complementary modes, which are frozen into the
// mineral (equivalently, their modulus is infinite). A modulus tending to
// infinity freezes the corresponding retained mode as well.
//
// The equilibrium of the internal variable is the stationary point of
//   W_d(E_d) + phi_s0/2 (eps - E_d) : C_s : (eps - E_d) + phi_s0 p tr(eps - E_d)
// over E_d in span(e1, e2), i.e.  (Dd + phi_s0 G) x = phi_s0 (g + p sqrt(3) e1_hat)
// with G_ij = e_i : C_s : e_j and g_i = e_i : C_s : eps. The system is linear
// in the deformation and pressure, so its solution carries exact AD
// derivatives.

#include "RankTwoTensor.h"
#include "MooseTypes.h"

#include <array>
#include <cmath>
#include <stdexcept>
#include <vector>

namespace Fabric
{
using Matrix = ADRankTwoTensor;
using Stiffness = std::array<std::array<Real, 6>, 6>;
static constexpr unsigned NDIR = 2;

inline Matrix
identity()
{
  Matrix x;
  for (unsigned i = 0; i < 3; ++i)
    x(i, i) = 1.;
  return x;
}

inline std::array<ADReal, 6>
mandel(const Matrix & x)
{
  return {x(0, 0),
          x(1, 1),
          x(2, 2),
          std::sqrt(2.) * x(1, 2),
          std::sqrt(2.) * x(0, 2),
          std::sqrt(2.) * x(0, 1)};
}

inline Matrix
tensor(const std::array<ADReal, 6> & x)
{
  Matrix a;
  for (unsigned i = 0; i < 3; ++i)
    a(i, i) = x[i];
  a(1, 2) = a(2, 1) = x[3] / std::sqrt(2.);
  a(0, 2) = a(2, 0) = x[4] / std::sqrt(2.);
  a(0, 1) = a(1, 0) = x[5] / std::sqrt(2.);
  return a;
}

inline ADReal
contract(const Matrix & a, const Matrix & b)
{
  ADReal r = 0;
  for (unsigned i = 0; i < 3; ++i)
    for (unsigned j = 0; j < 3; ++j)
      r += a(i, j) * b(i, j);
  return r;
}

inline Matrix
stiffness(const Stiffness & c, const Matrix & x)
{
  auto v = mandel(x);
  std::array<ADReal, 6> t{};
  for (unsigned i = 0; i < 6; ++i)
    for (unsigned j = 0; j < 6; ++j)
      t[i] += c[i][j] * v[j];
  return tensor(t);
}

// ---------------------------------------------------------------------------
// Real linear algebra in the Mandel basis (parameter dependent, no AD).
// ---------------------------------------------------------------------------
struct M6
{
  Real a[6][6];
  M6()
  {
    for (unsigned i = 0; i < 6; ++i)
      for (unsigned j = 0; j < 6; ++j)
        a[i][j] = 0.;
  }
};

inline M6
scale(const M6 & m, Real s)
{
  M6 r;
  for (unsigned i = 0; i < 6; ++i)
    for (unsigned j = 0; j < 6; ++j)
      r.a[i][j] = s * m.a[i][j];
  return r;
}

inline M6
add(const M6 & x, const M6 & y)
{
  M6 r;
  for (unsigned i = 0; i < 6; ++i)
    for (unsigned j = 0; j < 6; ++j)
      r.a[i][j] = x.a[i][j] + y.a[i][j];
  return r;
}

inline M6
outer(const std::array<Real, 6> & u, const std::array<Real, 6> & v)
{
  M6 r;
  for (unsigned i = 0; i < 6; ++i)
    for (unsigned j = 0; j < 6; ++j)
      r.a[i][j] = u[i] * v[j];
  return r;
}

inline Real
dot(const std::array<Real, 6> & u, const std::array<Real, 6> & v)
{
  Real s = 0.;
  for (unsigned i = 0; i < 6; ++i)
    s += u[i] * v[i];
  return s;
}

inline std::array<Real, 6>
mul(const M6 & m, const std::array<Real, 6> & v)
{
  std::array<Real, 6> r{};
  for (unsigned i = 0; i < 6; ++i)
  {
    Real s = 0.;
    for (unsigned k = 0; k < 6; ++k)
      s += m.a[i][k] * v[k];
    r[i] = s;
  }
  return r;
}

inline std::array<ADReal, 6>
mul(const M6 & m, const std::array<ADReal, 6> & v)
{
  std::array<ADReal, 6> r{};
  for (unsigned i = 0; i < 6; ++i)
  {
    ADReal s = 0.;
    for (unsigned k = 0; k < 6; ++k)
      s += m.a[i][k] * v[k];
    r[i] = s;
  }
  return r;
}

// General dense inverse/linear solve used for the small real systems.
inline void
invN(const Real * in, Real * out, unsigned n)
{
  std::vector<Real> aug(n * 2 * n, 0.);
  for (unsigned i = 0; i < n; ++i)
    for (unsigned j = 0; j < n; ++j)
    {
      aug[i * 2 * n + j] = in[i * n + j];
      aug[i * 2 * n + n + j] = (i == j) ? 1. : 0.;
    }
  for (unsigned c = 0; c < n; ++c)
  {
    unsigned piv = c;
    Real best = std::abs(aug[c * 2 * n + c]);
    for (unsigned r = c + 1; r < n; ++r)
      if (std::abs(aug[r * 2 * n + c]) > best)
      {
        best = std::abs(aug[r * 2 * n + c]);
        piv = r;
      }
    if (!(best > 0.))
      throw std::runtime_error("Singular fabric system; check the distention moduli");
    if (piv != c)
      for (unsigned j = 0; j < 2 * n; ++j)
      {
        Real t = aug[c * 2 * n + j];
        aug[c * 2 * n + j] = aug[piv * 2 * n + j];
        aug[piv * 2 * n + j] = t;
      }
    Real d = aug[c * 2 * n + c];
    for (unsigned j = 0; j < 2 * n; ++j)
      aug[c * 2 * n + j] /= d;
    for (unsigned r = 0; r < n; ++r)
      if (r != c)
      {
        Real f = aug[r * 2 * n + c];
        if (f != 0.)
          for (unsigned j = 0; j < 2 * n; ++j)
            aug[r * 2 * n + j] -= f * aug[c * 2 * n + j];
      }
  }
  for (unsigned i = 0; i < n; ++i)
    for (unsigned j = 0; j < n; ++j)
      out[i * n + j] = aug[i * 2 * n + n + j];
}

inline M6
inv6(const M6 & m)
{
  Real in[36], out[36];
  for (unsigned i = 0; i < 6; ++i)
    for (unsigned j = 0; j < 6; ++j)
      in[i * 6 + j] = m.a[i][j];
  invN(in, out, 6);
  M6 r;
  for (unsigned i = 0; i < 6; ++i)
    for (unsigned j = 0; j < 6; ++j)
      r.a[i][j] = out[i * 6 + j];
  return r;
}

inline Stiffness
toStiffness(const M6 & m)
{
  Stiffness s;
  for (unsigned i = 0; i < 6; ++i)
    for (unsigned j = 0; j < 6; ++j)
      s[i][j] = m.a[i][j];
  return s;
}

inline std::array<Real, 6>
mandelReal(const std::array<std::array<Real, 3>, 3> & x)
{
  return {x[0][0], x[1][1], x[2][2], std::sqrt(2.) * x[1][2], std::sqrt(2.) * x[0][2],
          std::sqrt(2.) * x[0][1]};
}

inline std::array<std::array<Real, 3>, 3>
realTensor(const std::array<Real, 6> & x)
{
  std::array<std::array<Real, 3>, 3> a{};
  for (unsigned i = 0; i < 3; ++i)
    a[i][i] = x[i];
  a[1][2] = a[2][1] = x[3] / std::sqrt(2.);
  a[0][2] = a[2][0] = x[4] / std::sqrt(2.);
  a[0][1] = a[1][0] = x[5] / std::sqrt(2.);
  return a;
}

struct State
{
  Matrix P, sigma, B;
  ADReal J, y, mass, energy, stability, solid;
  ADReal ln_a, ln_h, distention_a, distention_h;
  ADRealVectorValue flux;
};

class Law
{
public:
  Real phi, Ks, Kf, rho0, mobility, angle_mineral, angle_fabric;
  bool conformal;
  Stiffness cs, cd;
  M6 csm, cdm;
  std::array<Real, 6> bvec{};
  std::array<Real, 6> eI{{1., 1., 1., 0., 0., 0.}};
  std::array<std::array<Real, 6>, NDIR> e{};
  Real dd[NDIR][NDIR]{};
  Real solve[NDIR][NDIR]{}; // inverses of (Dd + phi G), and of Dd
  Real dinv[NDIR][NDIR]{};
  Real b_par = 0., b_per = 0., anisotropy = 0., storage = 0.;

  Law(const std::vector<Real> & entries,
      Real fraction,
      Real volume_modulus,
      Real axial_modulus,
      Real coupling,
      Real fluid_bulk,
      Real density,
      Real mob,
      Real angle,
      Real fangle,
      bool conformal_limit)
    : phi(fraction),
      Kf(fluid_bulk),
      rho0(density),
      mobility(mob),
      angle_mineral(angle),
      angle_fabric(fangle),
      conformal(conformal_limit)
  {
    if (entries.size() != 36)
      throw std::runtime_error("Fabric mineral stiffness requires 36 row-major Mandel entries");

    Stiffness original;
    for (unsigned i = 0; i < 6; ++i)
      for (unsigned j = 0; j < 6; ++j)
        original[i][j] = entries[6 * i + j];
    for (unsigned i = 0; i < 6; ++i)
      for (unsigned j = 0; j < 6; ++j)
        if (!std::isfinite(original[i][j]) ||
            std::abs(original[i][j] - original[j][i]) >
                1e-12 * std::max(1., std::abs(original[i][j])))
          throw std::runtime_error("Mineral stiffness must be finite symmetric");

    Real chol[6][6]{};
    for (unsigned i = 0; i < 6; ++i)
      for (unsigned j = 0; j <= i; ++j)
      {
        Real v = original[i][j];
        for (unsigned k = 0; k < j; ++k)
          v -= chol[i][k] * chol[j][k];
        if (i == j)
        {
          if (!(v > 0.))
            throw std::runtime_error("Mineral stiffness must be positive definite");
          chol[i][j] = std::sqrt(v);
        }
        else
          chol[i][j] = v / chol[j][j];
      }

    if (!std::isfinite(angle) || !std::isfinite(fangle))
      throw std::runtime_error("Material angles must be finite");

    Matrix R = identity();
    Real th = angle_mineral * M_PI / 180.;
    R(0, 0) = R(1, 1) = std::cos(th);
    R(0, 1) = -std::sin(th);
    R(1, 0) = std::sin(th);
    for (unsigned j = 0; j < 6; ++j)
    {
      std::array<ADReal, 6> ej{};
      ej[j] = 1.;
      auto response = mandel(R * stiffness(original, R.transpose() * tensor(ej) * R) * R.transpose());
      for (unsigned i = 0; i < 6; ++i)
        cs[i][j] = MetaPhysicL::raw_value(response[i]);
    }
    Ks = 0.;
    for (unsigned i = 0; i < 3; ++i)
      for (unsigned j = 0; j < 3; ++j)
        Ks += cs[i][j] / 9.;

    if (!(phi > 0. && phi < 1. && Ks > 0. && Kf > 0. && rho0 > 0. && mobility >= 0.))
      throw std::runtime_error("Invalid fabric constitutive parameters");

    // Fabric axis m in the x-y plane.
    Real fa = angle_fabric * M_PI / 180.;
    Real m[3] = {std::cos(fa), std::sin(fa), 0.};

    auto symOuter = [](const Real * a, const Real * b, Real s) {
      std::array<std::array<Real, 3>, 3> t{};
      for (unsigned i = 0; i < 3; ++i)
        for (unsigned j = 0; j < 3; ++j)
          t[i][j] = s * 0.5 * (a[i] * b[j] + a[j] * b[i]);
      return t;
    };
    auto addT = [](std::array<std::array<Real, 3>, 3> & a,
                   const std::array<std::array<Real, 3>, 3> & b,
                   Real s) {
      for (unsigned i = 0; i < 3; ++i)
        for (unsigned j = 0; j < 3; ++j)
          a[i][j] += s * b[i][j];
    };

    std::array<std::array<Real, 3>, 3> mm{}, I3{};
    for (unsigned i = 0; i < 3; ++i)
      I3[i][i] = 1.;
    mm = symOuter(m, m, 1.);                     // m (x) m

    auto unit = [](std::array<Real, 6> & v) {
      Real n = std::sqrt(dot(v, v));
      if (!(n > 1.e-14))
        throw std::runtime_error("Degenerate fabric invariant direction");
      for (unsigned i = 0; i < 6; ++i)
        v[i] /= n;
    };

    // e1, volumetric direction.
    e[0] = {1. / std::sqrt(3.), 1. / std::sqrt(3.), 1. / std::sqrt(3.), 0., 0., 0.};
    // e2, axial (degree-2) direction.
    {
      std::array<std::array<Real, 3>, 3> t{};
      addT(t, mm, 1.);
      addT(t, I3, -1. / 3.);
      e[1] = mandelReal(t);
      unit(e[1]);
    }

    // Sanity: the retained directions are orthonormal in the Mandel metric.
    for (unsigned i = 0; i < NDIR; ++i)
      for (unsigned j = 0; j < NDIR; ++j)
      {
        Real d = dot(e[i], e[j]);
        if (std::abs(d - ((i == j) ? 1. : 0.)) > 1e-9)
          throw std::runtime_error("Fabric invariant basis is not orthonormal");
      }

    // Axisymmetric distention stiffness on span(e1, e2). In the conformal
    // (spherical distention) limit the axial shape mode is frozen, which is
    // the limit of infinite axial modulus.
    if (conformal)
    {
      axial_modulus = 1.e12;
      coupling = 0.;
    }
    for (unsigned i = 0; i < NDIR; ++i)
      for (unsigned j = 0; j < NDIR; ++j)
        dd[i][j] = 0.;
    dd[0][0] = volume_modulus;
    dd[1][1] = axial_modulus;
    dd[0][1] = dd[1][0] = coupling;
    for (unsigned i = 0; i < NDIR; ++i)
      if (!(dd[i][i] > 0.))
        throw std::runtime_error("Fabric distention moduli must be positive");
    {
      Real in[NDIR * NDIR], out[NDIR * NDIR];
      for (unsigned i = 0; i < NDIR; ++i)
        for (unsigned j = 0; j < NDIR; ++j)
          in[i * NDIR + j] = dd[i][j];
      invN(in, out, NDIR);
      for (unsigned i = 0; i < NDIR; ++i)
        for (unsigned j = 0; j < NDIR; ++j)
          dinv[i][j] = out[i * NDIR + j];
      const Real det = dd[0][0] * dd[1][1] - dd[0][1] * dd[1][0];
      if (!(det > 0.))
        throw std::runtime_error("Fabric distention stiffness must be positive definite");
    }

    // Distention compliance D4^+ = sum_ij dinv[i][j] e_i (x) e_j.
    M6 Dp;
    for (unsigned i = 0; i < NDIR; ++i)
      for (unsigned j = 0; j < NDIR; ++j)
      {
        if (dinv[i][j] == 0.)
          continue;
        M6 o = outer(e[i], e[j]);
        Dp = add(Dp, scale(o, dinv[i][j]));
      }

    csm = M6();
    for (unsigned i = 0; i < 6; ++i)
      for (unsigned j = 0; j < 6; ++j)
        csm.a[i][j] = cs[i][j];

    // (C^d)^{-1} = (phi C_s)^{-1} + D4^+
    M6 A6 = add(inv6(scale(csm, phi)), Dp);
    cdm = inv6(A6);
    cd = toStiffness(cdm);

    M6 csinv = inv6(csm);
    auto bv = mul(cdm, mul(csinv, eI));
    for (unsigned i = 0; i < 6; ++i)
      bvec[i] = eI[i] - bv[i];

    auto Bt = realTensor(bvec);
    std::array<std::array<Real, 3>, 3> mmat{};
    for (unsigned i = 0; i < 3; ++i)
      for (unsigned j = 0; j < 3; ++j)
        mmat[i][j] = m[i] * m[j];
    b_par = 0.;
    for (unsigned i = 0; i < 3; ++i)
      for (unsigned j = 0; j < 3; ++j)
        b_par += mmat[i][j] * Bt[i][j];
    Real traceB = Bt[0][0] + Bt[1][1] + Bt[2][2];
    b_per = 0.5 * (traceB - b_par);
    anisotropy = b_par - b_per;
    // Fixed-strain storage follows the same retained mineral-volume
    // equilibrium for isotropic and anisotropic mineral stiffnesses.
    const auto pressure_compliance = mul(csinv, eI);
    storage = (1. - phi) / Kf + phi * dot(eI, pressure_compliance)
              - dot(pressure_compliance, mul(cdm, pressure_compliance));

    for (unsigned i = 0; i < 6; ++i)
      if (!(std::isfinite(bvec[i]) && std::isfinite(cd[i][i])))
        throw std::runtime_error("Fabric reference tensors are not finite");

    // Equilibrium operator: (Dd + phi G) with G_ij = e_i : C_s : e_j.
    Real op[NDIR * NDIR];
    for (unsigned i = 0; i < NDIR; ++i)
      for (unsigned j = 0; j < NDIR; ++j)
      {
        Real g = dot(e[i], mul(csm, e[j]));
        op[i * NDIR + j] = dd[i][j] + phi * g;
      }
    Real out[NDIR * NDIR];
    invN(op, out, NDIR);
    for (unsigned i = 0; i < NDIR; ++i)
      for (unsigned j = 0; j < NDIR; ++j)
        solve[i][j] = out[i * NDIR + j];
  }

  State
  evaluate(const Matrix & F,
           const ADReal & p,
           const ADRealVectorValue & gradp,
           bool linear = false) const
  {
    if (!linear)
      throw std::runtime_error(
          "FabricLaw implements the reference-state response; set linear_reference = true");

    for (unsigned i = 0; i < 3; ++i)
      for (unsigned j = 0; j < 3; ++j)
        if (!std::isfinite(MetaPhysicL::raw_value(F(i, j))))
          throw std::runtime_error("Deformation must be finite");
    if (!std::isfinite(MetaPhysicL::raw_value(p)))
      throw std::runtime_error("Pressure must be finite");

    const Matrix I = identity();
    State s;
    Matrix eps = (F + F.transpose()) * 0.5 - I;
    auto ev = mandel(eps);
    auto ce = mul(csm, ev);

    // E_d = sum x_i e_i with (Dd + phi G) x = phi (g + p sqrt(3) e1_hat),
    // g_i = e_i : C_s : eps. The system is linear in (eps, p), so the
    // solution below carries exact derivatives.
    ADReal x[NDIR];
    ADReal wdist = 0.;
    std::array<ADReal, 6> edv{};
    for (unsigned k = 0; k < 6; ++k)
      edv[k] = 0.;
    for (unsigned i = 0; i < NDIR; ++i)
    {
      ADReal xi = phi * std::sqrt(3.) * p * solve[i][0];
      for (unsigned j = 0; j < NDIR; ++j)
      {
        if (solve[i][j] == 0.)
          continue;
        ADReal gj = 0.;
        for (unsigned k = 0; k < 6; ++k)
          gj += e[j][k] * ce[k];
        xi += phi * solve[i][j] * gj;
      }
      x[i] = xi;
      for (unsigned k = 0; k < 6; ++k)
        edv[k] += xi * e[i][k];
      if (i == 0)
        s.ln_a = std::sqrt(3.) * xi;
      if (i == 1)
        // e2 carries (1/2 I - 3/2 m (x) m) = -sqrt(3/2) e2, so the reported
        // scalar is -x2/sqrt(1.5) = ln h (manuscript eq. fabric-transverse-strain).
        s.ln_h = -xi / std::sqrt(1.5);
    }
    for (unsigned i = 0; i < NDIR; ++i)
      for (unsigned j = 0; j < NDIR; ++j)
        wdist += 0.5 * dd[i][j] * x[i] * x[j];

    Matrix Ed = tensor(edv);
    std::array<ADReal, 6> bvv{};
    for (unsigned i = 0; i < 6; ++i)
      bvv[i] = ev[i] - edv[i];
    Matrix epsbar = tensor(bvv);

    Matrix sig = stiffness(cs, epsbar) * phi - I * ((1. - phi) * p);
    s.sigma = sig;
    s.P = sig;
    s.B = tensor(std::array<ADReal, 6>{bvec[0], bvec[1], bvec[2], bvec[3], bvec[4], bvec[5]});

    s.J = 1. + eps.trace();
    s.y = 1. + epsbar.trace();
    s.solid = phi * s.y / s.J;
    s.distention_a = exp(s.ln_a);
    s.distention_h = exp(s.ln_h);
    s.energy = 0.5 * phi * contract(epsbar, stiffness(cs, epsbar)) + wdist;
    s.stability = Ks;

    ADReal b_double_e = 0.;
    for (unsigned i = 0; i < 6; ++i)
      b_double_e += bvec[i] * ev[i];
    s.mass = rho0 * ((1. - phi) + b_double_e + storage * p);

    s.flux = -rho0 * mobility * gradp;
    return s;
  }
};
} // namespace Fabric
