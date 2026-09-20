#pragma once
#include "NodalVariablePostprocessor.h"
class DofReactionSum:public NodalVariablePostprocessor
{
public: static InputParameters validParams();DofReactionSum(const InputParameters &p):NodalVariablePostprocessor(p){}
 void initialize() override{_sum=0;}
 void execute() override;
 void finalize() override{gatherSum(_sum);}
 void threadJoin(const UserObject &y)override{_sum+=static_cast<const DofReactionSum &>(y)._sum;}
 Real getValue()const override{return _sum;}
protected: Real _sum=0;
};
