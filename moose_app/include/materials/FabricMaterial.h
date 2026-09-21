// SPDX-License-Identifier: Apache-2.0
#pragma once
#include "Material.h"
#include "FabricLaw.h"

class FabricMaterial : public Material
{
public:
  static InputParameters validParams();
  FabricMaterial(const InputParameters &);

protected:
  void computeQpProperties() override;
  void initQpStatefulProperties() override;
  const ADVariableGradient & _gx, &_gy, &_gp;
  const ADVariableValue & _p;
  Fabric::Law _law;
  bool _linear;
  ADMaterialProperty<ADRankTwoTensor> & _P;
  ADMaterialProperty<RealVectorValue> & _flux;
  ADMaterialProperty<Real> & _mass;
  MaterialProperty<Real> & _J, &_y, &_solid, &_stab, &_energy, &_p22;
  MaterialProperty<Real> & _b_par, &_b_per, &_b_aniso, &_ln_a, &_ln_h, &_a, &_h, &_cd11, &_cd12;
  MaterialProperty<Real> & _s11, &_s22;
};
