// SPDX-License-Identifier: Apache-2.0
#pragma once
#include "RankTwoTensor.h"
#include "MooseTypes.h"
#include <array>
#include <cmath>
#include <stdexcept>

namespace Conformal
{
using Matrix = ADRankTwoTensor;
using Stiffness = std::array<std::array<Real, 6>, 6>;
inline Matrix identity() { Matrix x; for (unsigned i=0;i<3;++i) x(i,i)=1.; return x; }
inline std::array<ADReal,6> mandel(const Matrix & x)
{ return {x(0,0),x(1,1),x(2,2),std::sqrt(2.)*x(1,2),std::sqrt(2.)*x(0,2),std::sqrt(2.)*x(0,1)}; }
inline Matrix tensor(const std::array<ADReal,6> & x)
{ Matrix a; for(unsigned i=0;i<3;++i) a(i,i)=x[i]; a(1,2)=a(2,1)=x[3]/std::sqrt(2.); a(0,2)=a(2,0)=x[4]/std::sqrt(2.); a(0,1)=a(1,0)=x[5]/std::sqrt(2.); return a; }
inline Matrix stiffness(const Stiffness & c, const Matrix & x)
{ auto v=mandel(x); std::array<ADReal,6> t{}; for(unsigned i=0;i<6;++i) for(unsigned j=0;j<6;++j) t[i]+=c[i][j]*v[j]; return tensor(t); }
inline ADReal contract(const Matrix & a,const Matrix & b)
{ ADReal r=0; for(unsigned i=0;i<3;++i) for(unsigned j=0;j<3;++j) r+=a(i,j)*b(i,j); return r; }
struct Quadrature
{
  std::vector<Real> x,w;
  explicit Quadrature(unsigned n=24)
  {
    if(n<4 || n>128) throw std::runtime_error("Require 4 <= matrix logarithm quadrature order <= 128");
    x.resize(n); w.resize(n);
    for(unsigned i=0;i<(n+1)/2;++i)
    {
      Real z=std::cos(M_PI*(i+.75)/(n+.5)), dp=0;
      for(unsigned k=0;k<30;++k)
      {
        Real p=1,pold=0;
        for(unsigned j=1;j<=n;++j) { Real tmp=p; p=((2*j-1)*z*p-(j-1)*pold)/j; pold=tmp; }
        dp=n*(z*p-pold)/(z*z-1); Real dz=p/dp; z-=dz; if(std::abs(dz)<2e-15) break;
      }
      x[i]=(1-z)/2; x[n-1-i]=(1+z)/2; w[i]=w[n-1-i]=1/((1-z*z)*dp*dp);
    }
  }
};
struct State
{
  Matrix P,sigma,B;
  ADReal J,y,mass,energy,stability,solid;
  ADRealVectorValue flux;
};
class Law
{
public:
  Stiffness cs{},cd{};
  Real phi=.6,K=7,Ks=0,alpha=0,Kf=8,rho0=1,mobility=1.5;
  Quadrature quad;
  Law(const std::vector<Real> & entries,Real fraction,Real bulk,Real fluid_bulk,Real density,Real mob,Real angle,unsigned nq)
  : phi(fraction),K(bulk),Kf(fluid_bulk),rho0(density),mobility(mob),quad(nq)
  {
    if(entries.size()!=36) throw std::runtime_error("Cs requires 36 row-major Mandel entries");
    Stiffness original; for(unsigned i=0;i<6;++i) for(unsigned j=0;j<6;++j) original[i][j]=entries[6*i+j];
    Real chol[6][6]{};
    for(unsigned i=0;i<6;++i)for(unsigned j=0;j<6;++j)
      if(!std::isfinite(original[i][j]) || std::abs(original[i][j]-original[j][i])>1e-12*std::max(1.,std::abs(original[i][j])))throw std::runtime_error("Mineral stiffness must be finite symmetric");
    for(unsigned i=0;i<6;++i)for(unsigned j=0;j<=i;++j)
    {Real v=original[i][j];for(unsigned k=0;k<j;++k)v-=chol[i][k]*chol[j][k];if(i==j){if(!(v>0))throw std::runtime_error("Mineral stiffness must be positive definite");chol[i][j]=std::sqrt(v);}else chol[i][j]=v/chol[j][j];}
    if(!std::isfinite(angle))throw std::runtime_error("Material angle must be finite");
    Matrix R=identity(); Real th=angle*M_PI/180; R(0,0)=R(1,1)=std::cos(th); R(0,1)=-std::sin(th);R(1,0)=std::sin(th);
    for(unsigned j=0;j<6;++j)
    {
      std::array<ADReal,6> ej{};ej[j]=1.; auto response=mandel(R*stiffness(original,R.transpose()*tensor(ej)*R)*R.transpose());
      for(unsigned i=0;i<6;++i) cs[i][j]=MetaPhysicL::raw_value(response[i]);
    }
    for(unsigned i=0;i<3;++i)for(unsigned j=0;j<3;++j)Ks+=cs[i][j]/9;
    if(!(phi>0&&phi<1&&K>0&&K<phi*Ks&&Kf>0&&rho0>0&&mobility>=0)) throw std::runtime_error("Invalid constitutive parameters");
    alpha=1-K/(phi*Ks);
    for(unsigned i=0;i<6;++i)for(unsigned j=0;j<6;++j)
    { Real ci=0,cj=0;for(unsigned k=0;k<3;++k){ci+=cs[i][k];cj+=cs[j][k];}cd[i][j]=phi*cs[i][j]-phi*alpha/(9*Ks)*ci*cj; }
  }
  State evaluate(const Matrix & F,const ADReal & p,const ADRealVectorValue & gradp,bool linear=false) const
  {
    const Matrix I=identity(); State s;
    if(!std::isfinite(MetaPhysicL::raw_value(p)))throw std::runtime_error("Pressure must be finite");
    for(unsigned i=0;i<3;++i)for(unsigned j=0;j<3;++j)if(!std::isfinite(MetaPhysicL::raw_value(F(i,j))))throw std::runtime_error("Deformation must be finite");
    if(linear)
    {
      Matrix e=(F+F.transpose())*.5-I;
      s.B=I-tensorRowCdInverseCs();
      s.sigma=stiffness(cd,e)-s.B*p;s.P=s.sigma;
      Real storage=(1-phi)/Kf+phi*alpha/Ks;
      s.mass=rho0*((1-phi)+contract(s.B,e)+storage*p);
      s.flux=-rho0*mobility*gradp;
      s.J=1+e.trace();s.y=1+K/(phi*Ks)*e.trace()-alpha/(3*Ks)*stiffness(cs,e-I*e.trace()/3).trace()-alpha*p/Ks;
      s.solid=phi*s.y/s.J;s.stability=Ks;s.energy=.5*contract(e,stiffness(cd,e)); return s;
    }
    s.J=F.det(); if(MetaPhysicL::raw_value(s.J)<=0)throw std::runtime_error("Nonpositive J");
    const Matrix C=F.transpose()*F,D=C-I;
    Matrix logC;
    std::vector<Matrix> inverses;inverses.reserve(quad.x.size());
    for(unsigned n=0;n<quad.x.size();++n){auto inv=(I+D*quad.x[n]).inverse();inverses.push_back(inv);logC+=D*inv*quad.w[n];}
    Matrix e=logC*.5,dev=e-I*(e.trace()/3);
    ADReal target=K/(phi*Ks)*log(s.J)-alpha/(3*Ks)*stiffness(cs,dev).trace();
    Real tv=MetaPhysicL::raw_value(target),pv=MetaPhysicL::raw_value(p),shift=0;
    if(pv!=0)
    {
      Real mag=std::log(alpha*std::abs(pv)/Ks)+tv,lo,hi;
      if(pv<0){hi=-mag;lo=0;if(hi<=1)throw std::runtime_error("Lost stable mineral branch");}
      else {lo=-std::max(1.,mag+1.);hi=mag>0?-mag+std::log1p(mag):0.;}
      for(unsigned n=0;n<100;++n){shift=(lo+hi)*.5;Real r=shift+(pv>0?1.:-1.)*std::exp(mag+shift);if(r>0)hi=shift;else lo=shift;if(hi-lo<2e-15)break;}
    }
    Real q0=tv+shift,y0=std::exp(q0),den=Ks+alpha*pv*y0;
    if(!(std::isfinite(y0)&&std::isfinite(den)&&den>0))throw std::runtime_error("Invalid stable mineral root");
    ADReal residual=Ks*(q0-target)+alpha*p*y0;
    ADReal q=q0-(residual-MetaPhysicL::raw_value(residual))/den;
    s.y=exp(q);s.stability=Ks+alpha*p*s.y;s.solid=phi*s.y/s.J;
    if(!(MetaPhysicL::raw_value(s.solid)>0&&MetaPhysicL::raw_value(s.solid)<1))throw std::runtime_error("Invalid phase volumes");
    Matrix em=dev+I*(q/3),T=stiffness(cs,em),L,LB;
    Matrix devCsI=stiffness(cs,I)-I*(3*Ks);
    for(unsigned n=0;n<quad.x.size();++n){L+=inverses[n]*T*inverses[n]*quad.w[n];LB+=inverses[n]*devCsI*inverses[n]*quad.w[n];}
    Matrix tau=F*L*F.transpose();
    s.sigma=phi/s.J*tau-I*((1-s.solid)*p);
    s.P=s.J*s.sigma*F.inverse().transpose();
    s.B=I-s.y/(s.J*s.stability)*(K*I-phi*alpha/3*F*LB*F.transpose());
    s.energy=K/(2*alpha)*pow(log(s.J)-q,2)+phi*.5*contract(em,T);
    ADReal rho=rho0*exp(p/Kf);s.mass=rho*(s.J-phi*s.y);
    Matrix invF=F.inverse();s.flux=-mobility*s.J*rho*(invF*invF.transpose())*gradp;
    return s;
  }
private:
  Matrix tensorRowCdInverseCs() const
  {
    // Cd:Cs^{-1}:I = phi I - phi alpha/(3 Ks) Cs:I.
    return phi*identity()-phi*alpha/(3*Ks)*stiffness(cs,identity());
  }
};
}
