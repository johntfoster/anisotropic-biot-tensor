#pragma once
#include "MooseApp.h"
class AnisotropicBiotApp : public MooseApp
{
public:
  static InputParameters validParams();
  AnisotropicBiotApp(const InputParameters &);
  static void registerAll(Factory &, ActionFactory &, Syntax &);
  static void registerApps();
};
