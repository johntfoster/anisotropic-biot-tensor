#pragma once
#include "SideIntegralPostprocessor.h"
class ReferenceOutflow:public SideIntegralPostprocessor
{
public: static InputParameters validParams(){return SideIntegralPostprocessor::validParams();}
 ReferenceOutflow(const InputParameters &p):SideIntegralPostprocessor(p),_flux(getADMaterialProperty<RealVectorValue>("mass_flux")){}
protected: Real computeQpIntegral()override{return MetaPhysicL::raw_value(_flux[_qp]*_normals[_qp]);}
 const ADMaterialProperty<RealVectorValue> &_flux;
};
