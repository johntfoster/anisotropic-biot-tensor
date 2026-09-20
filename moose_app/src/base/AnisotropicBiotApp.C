// SPDX-License-Identifier: Apache-2.0
#include "AnisotropicBiotApp.h"
#include "AppFactory.h"
#include "MooseSyntax.h"
InputParameters AnisotropicBiotApp::validParams() { return MooseApp::validParams(); }
AnisotropicBiotApp::AnisotropicBiotApp(const InputParameters & p) : MooseApp(p)
{ registerAll(_factory, _action_factory, _syntax); }
void AnisotropicBiotApp::registerAll(Factory & f, ActionFactory & a, Syntax &)
{ Registry::registerObjectsTo(f, {"AnisotropicBiotApp"}); Registry::registerActionsTo(a, {"AnisotropicBiotApp"}); }
void AnisotropicBiotApp::registerApps() { registerApp(AnisotropicBiotApp); }
