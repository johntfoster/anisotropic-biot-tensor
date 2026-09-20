#include "DofReactionSum.h"
#include "MooseVariable.h"
#include "SystemBase.h"
registerMooseObject("AnisotropicBiotApp",DofReactionSum);
InputParameters DofReactionSum::validParams(){auto p=NodalVariablePostprocessor::validParams();p.set<bool>("unique_node_execute")=true;return p;}
void DofReactionSum::execute()
{
 auto &v=*mooseVariable();
 if(_current_node->n_dofs(v.sys().number(),v.number()))_sum+=_u[_qp];
}
