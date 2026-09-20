#pragma once
#include "Material.h"
#include "ConformalLaw.h"
class ConformalMaterial : public Material
{
public:
 static InputParameters validParams();
 ConformalMaterial(const InputParameters &);
protected:
 void computeQpProperties() override;
 void initQpStatefulProperties() override;
 const ADVariableGradient &_gx,&_gy,&_gp;
 const ADVariableValue &_p;
 Conformal::Law _law;
 bool _linear;
 ADMaterialProperty<ADRankTwoTensor> &_P;
 ADMaterialProperty<RealVectorValue> &_flux;
 ADMaterialProperty<Real> &_mass;
 MaterialProperty<Real> &_J,&_y,&_solid,&_stab,&_energy,&_b12,&_s11,&_s22,&_s12,&_p22;
};
