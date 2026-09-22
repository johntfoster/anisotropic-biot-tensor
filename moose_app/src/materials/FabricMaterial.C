// SPDX-License-Identifier: Apache-2.0
#include "FabricMaterial.h"

registerMooseObject("AnisotropicBiotApp", FabricMaterial);

InputParameters
FabricMaterial::validParams()
{
  auto p = Material::validParams();
  p.addRequiredCoupledVar("ux", "Horizontal displacement");
  p.addRequiredCoupledVar("uy", "Vertical displacement");
  p.addRequiredCoupledVar("pressure", "Pore pressure");
  p.addRequiredParam<std::vector<Real>>("mineral_stiffness", "36 row-major Mandel entries");
  p.addParam<Real>("solid_fraction", .6, "Reference solid fraction");
  p.addParam<Real>("fabric_volume_modulus", 1., "Distention modulus for pore volume change");
  p.addParam<Real>("fabric_axial_modulus", 1., "Distention modulus for pore shape change along the fabric axis");
  p.addParam<Real>("fabric_coupling", 0., "Volume-axial coupling in the distention energy");
  p.addParam<Real>("fabric_angle", 0., "Fabric axis orientation in the material frame, degrees");
  p.addParam<bool>("conformal_limit",
                   false,
                   "Restrict the distention to volume change (conformal model limit)");
  p.addParam<Real>("fluid_bulk", 8, "Fluid bulk modulus");
  p.addParam<Real>("fluid_density", 1, "Reference fluid density");
  p.addParam<Real>("mobility", 1.5, "Constant isotropic spatial mobility");
  p.addParam<Real>("angle", 0, "Mineral rotation about z, degrees");
  p.addParam<bool>("linear_reference",
                   true,
                   "Use the reference-state fabric response (required by the implemented law)");
  p.addParam<bool>("scalar_coupling", false,
                  "Comparison potential: replace B by trace(B)/3 I in both stress and mass, "
                  "preserving drained stiffness and fixed-strain storage");
  return p;
}

FabricMaterial::FabricMaterial(const InputParameters & p)
  : Material(p),
    _gx(adCoupledGradient("ux")),
    _gy(adCoupledGradient("uy")),
    _gp(adCoupledGradient("pressure")),
    _p(adCoupledValue("pressure")),
    _law(getParam<std::vector<Real>>("mineral_stiffness"),
         getParam<Real>("solid_fraction"),
         getParam<Real>("fabric_volume_modulus"),
         getParam<Real>("fabric_axial_modulus"),
         getParam<Real>("fabric_coupling"),
         getParam<Real>("fluid_bulk"),
         getParam<Real>("fluid_density"),
         getParam<Real>("mobility"),
         getParam<Real>("angle"),
         getParam<Real>("fabric_angle"),
         getParam<bool>("conformal_limit")),
    _linear(getParam<bool>("linear_reference")),
    _scalar_coupling(getParam<bool>("scalar_coupling")),
    _P(declareADProperty<ADRankTwoTensor>("first_piola")),
    _flux(declareADProperty<RealVectorValue>("mass_flux")),
    _mass(declareADProperty<Real>("fluid_mass")),
    _J(declareProperty<Real>("J")),
    _y(declareProperty<Real>("Jbar")),
    _solid(declareProperty<Real>("solid_fraction")),
    _stab(declareProperty<Real>("stability")),
    _energy(declareProperty<Real>("energy")),
    _p22(declareProperty<Real>("P22")),
    _b_par(declareProperty<Real>("B_par")),
    _b_per(declareProperty<Real>("B_per")),
    _b_aniso(declareProperty<Real>("B_anisotropy")),
    _ln_a(declareProperty<Real>("ln_a")),
    _ln_h(declareProperty<Real>("ln_h")),
    _a(declareProperty<Real>("distention_a")),
    _h(declareProperty<Real>("distention_h")),
    _cd11(declareProperty<Real>("drained_c11")),
    _cd12(declareProperty<Real>("drained_c12")),
    _s11(declareProperty<Real>("sigma11")),
    _s22(declareProperty<Real>("sigma22"))
{
}

void
FabricMaterial::initQpStatefulProperties()
{
  computeQpProperties();
}

void
FabricMaterial::computeQpProperties()
{
  auto F = Fabric::identity();
  for (unsigned j = 0; j < 3; ++j)
  {
    F(0, j) += _gx[_qp](j);
    F(1, j) += _gy[_qp](j);
  }
  try
  {
    auto s = _law.evaluate(F, _p[_qp], _gp[_qp], _linear);
    if (_scalar_coupling)
    {
      // Both substitutions follow the same quadratic poroelastic potential.
      // Internal fabric and energy outputs retain the parent law; they are
      // not states or energy of this phenomenological comparison.
      const auto I = Fabric::identity();
      const auto difference = s.B - I * (s.B.trace() / 3.);
      const auto eps = (F + F.transpose()) * 0.5 - I;
      s.P += difference * _p[_qp];
      s.sigma = s.P;
      s.mass -= _law.rho0 * Fabric::contract(difference, eps);
    }
    _P[_qp] = s.P;
    _flux[_qp] = s.flux;
    _mass[_qp] = s.mass;
    _J[_qp] = MetaPhysicL::raw_value(s.J);
    _y[_qp] = MetaPhysicL::raw_value(s.y);
    _solid[_qp] = MetaPhysicL::raw_value(s.solid);
    _stab[_qp] = MetaPhysicL::raw_value(s.stability);
    _energy[_qp] = MetaPhysicL::raw_value(s.energy);
    _p22[_qp] = MetaPhysicL::raw_value(s.P(1, 1));
    _ln_a[_qp] = MetaPhysicL::raw_value(s.ln_a);
    _ln_h[_qp] = MetaPhysicL::raw_value(s.ln_h);
    _a[_qp] = MetaPhysicL::raw_value(s.distention_a);
    _h[_qp] = MetaPhysicL::raw_value(s.distention_h);
    _b_par[_qp] = _scalar_coupling ? (_law.b_par + 2. * _law.b_per) / 3. : _law.b_par;
    _b_per[_qp] = _scalar_coupling ? _b_par[_qp] : _law.b_per;
    _b_aniso[_qp] = _scalar_coupling ? 0. : _law.anisotropy;
    _cd11[_qp] = _law.cd[0][0];
    _cd12[_qp] = _law.cd[0][1];
    _s11[_qp] = MetaPhysicL::raw_value(s.sigma(0, 0));
    _s22[_qp] = MetaPhysicL::raw_value(s.sigma(1, 1));
  }
  catch (const std::exception & e)
  {
    mooseException(e.what());
  }
}
