// SPDX-License-Identifier: Apache-2.0
#include "AnisotropicBiotApp.h"
#include "MooseMain.h"
#include "ConformalLaw.h"
#include <fstream>
#include <iomanip>
#include <iostream>
int main(int argc, char ** argv)
{
 if(argc>=3 && std::string(argv[1])=="--constitutive-table")
 {
  unsigned nq=argc>3?std::stoul(argv[3]):24;
  Real angle=argc>4?std::stod(argv[4]):0;
  std::vector<Real> c={50,12,10,0,0,0,12,60,14,0,0,0,10,14,70,0,0,0,0,0,0,20,0,0,0,0,0,0,24,0,0,0,0,0,0,28};
  Conformal::Law law(c,.6,7,8,1,1.5,angle,nq);std::ifstream input(argv[2]);std::cout<<std::setprecision(17);
  Real value;
  while(input>>value)
  {
   Conformal::Matrix f;f(0,0)=value;
   for(unsigned n=1;n<9;++n){input>>value;f(n/3,n%3)=value;}
   for(unsigned n=0;n<9;++n)Moose::derivInsert(f(n/3,n%3).derivatives(),n,1.);
   input>>value;ADReal p=value;Moose::derivInsert(p.derivatives(),9,1.);
   try{
    auto s=law.evaluate(f,p,ADRealVectorValue());
    std::vector<ADReal> result={s.J,s.y,s.mass,s.energy,s.stability,s.solid};
    for(unsigned n=0;n<9;++n)result.push_back(s.sigma(n/3,n%3));
    for(unsigned n=0;n<9;++n)result.push_back(s.B(n/3,n%3));
    for(unsigned n=0;n<9;++n)result.push_back(s.P(n/3,n%3));
    for(auto &v:result)std::cout<<MetaPhysicL::raw_value(v)<<' ';
    for(auto &v:result)for(unsigned d=0;d<10;++d)std::cout<<v.derivatives()[d]<<' ';
    std::cout<<'\n';
   }catch(const std::exception &e){std::cerr<<e.what()<<'\n';return 2;}
  }return 0;
 }
 return Moose::main<AnisotropicBiotApp>(argc,argv);
}
