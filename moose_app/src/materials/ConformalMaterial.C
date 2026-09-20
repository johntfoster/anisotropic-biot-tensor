// SPDX-License-Identifier: Apache-2.0
#include "ConformalMaterial.h"
registerMooseObject("AnisotropicBiotApp",ConformalMaterial);
InputParameters ConformalMaterial::validParams()
{
 auto p=Material::validParams();p.addRequiredCoupledVar("ux","Horizontal displacement");p.addRequiredCoupledVar("uy","Vertical displacement");p.addRequiredCoupledVar("pressure","Pore pressure");
 p.addRequiredParam<std::vector<Real>>("mineral_stiffness","36 row-major Mandel entries");
 p.addParam<Real>("solid_fraction",.6,"Reference solid fraction");p.addParam<Real>("drained_bulk",7,"Spherical strain modulus");p.addParam<Real>("fluid_bulk",8,"Fluid bulk modulus");p.addParam<Real>("fluid_density",1,"Reference fluid density");p.addParam<Real>("mobility",1.5,"Constant isotropic spatial mobility");p.addParam<Real>("angle",0,"Mineral rotation about z, degrees");p.addParam<unsigned>("log_quadrature",24,"Resolvent integration order");p.addParam<bool>("linear_reference",false,"Use frozen reference tangent instead of finite constitutive response");return p;
}
ConformalMaterial::ConformalMaterial(const InputParameters & p):Material(p),_gx(adCoupledGradient("ux")),_gy(adCoupledGradient("uy")),_gp(adCoupledGradient("pressure")),_p(adCoupledValue("pressure")),
_law(getParam<std::vector<Real>>("mineral_stiffness"),getParam<Real>("solid_fraction"),getParam<Real>("drained_bulk"),getParam<Real>("fluid_bulk"),getParam<Real>("fluid_density"),getParam<Real>("mobility"),getParam<Real>("angle"),getParam<unsigned>("log_quadrature")),_linear(getParam<bool>("linear_reference")),
_P(declareADProperty<ADRankTwoTensor>("first_piola")),_flux(declareADProperty<RealVectorValue>("mass_flux")),_mass(declareADProperty<Real>("fluid_mass")),_J(declareProperty<Real>("J")),_y(declareProperty<Real>("Jbar")),_solid(declareProperty<Real>("solid_fraction")),_stab(declareProperty<Real>("stability")),_energy(declareProperty<Real>("energy")),_b12(declareProperty<Real>("B12")),_s11(declareProperty<Real>("sigma11")),_s22(declareProperty<Real>("sigma22")),_s12(declareProperty<Real>("sigma12")),_p22(declareProperty<Real>("P22")){}
void ConformalMaterial::initQpStatefulProperties(){computeQpProperties();}
void ConformalMaterial::computeQpProperties()
{
 auto F=Conformal::identity();for(unsigned j=0;j<3;++j){F(0,j)+=_gx[_qp](j);F(1,j)+=_gy[_qp](j);}
 try{
 auto s=_law.evaluate(F,_p[_qp],_gp[_qp],_linear);_P[_qp]=s.P;_flux[_qp]=s.flux;_mass[_qp]=s.mass;
 _J[_qp]=MetaPhysicL::raw_value(s.J);_y[_qp]=MetaPhysicL::raw_value(s.y);_solid[_qp]=MetaPhysicL::raw_value(s.solid);_stab[_qp]=MetaPhysicL::raw_value(s.stability);_energy[_qp]=MetaPhysicL::raw_value(s.energy);_b12[_qp]=MetaPhysicL::raw_value(s.B(0,1));_s11[_qp]=MetaPhysicL::raw_value(s.sigma(0,0));_s22[_qp]=MetaPhysicL::raw_value(s.sigma(1,1));_s12[_qp]=MetaPhysicL::raw_value(s.sigma(0,1));_p22[_qp]=MetaPhysicL::raw_value(s.P(1,1));
 }catch(const std::exception &e){mooseException(e.what());}
}
