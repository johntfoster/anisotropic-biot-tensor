# SPDX-License-Identifier: Apache-2.0
# Cross-check deck: the reviewed spherical-distention ConformalMaterial at the
# same prescribed uniform deformation and pressure as fabric_probe.i, used to
# verify that the fabric law reduces to the conformal model in its
# conformal_limit with the parameter mapping
#   drained_bulk = K  <->  fabric_volume_modulus = 3 K / alpha,
#   alpha = 1 - K / (phi Ks).
[Mesh]
  [base]
    type = GeneratedMeshGenerator
    dim = 2
    nx = 1
    ny = 1
    xmin = 0
    xmax = 1
    ymin = 0
    ymax = 1
    elem_type = QUAD4
  []
[]
[Variables]
  [ux]
    order = FIRST
    family = LAGRANGE
  []
  [uy]
    order = FIRST
    family = LAGRANGE
  []
  [p]
    order = FIRST
    family = LAGRANGE
  []
[]
[Functions]
  [uxr]
    type = ParsedFunction
    expression = '0.01*x'
  []
  [uyt]
    type = ParsedFunction
    expression = '-0.005*y'
  []
[]
[AuxVariables]
  [J]
    family = MONOMIAL
    order = CONSTANT
  []
  [Jbar]
    family = MONOMIAL
    order = CONSTANT
  []
  [solid_fraction]
    family = MONOMIAL
    order = CONSTANT
  []
  [sigma11]
    family = MONOMIAL
    order = CONSTANT
  []
  [sigma22]
    family = MONOMIAL
    order = CONSTANT
  []
[]
[AuxKernels]
  [J]
    type = MaterialRealAux
    variable = J
    property = J
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [Jbar]
    type = MaterialRealAux
    variable = Jbar
    property = Jbar
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [solid_fraction]
    type = MaterialRealAux
    variable = solid_fraction
    property = solid_fraction
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [sigma11]
    type = MaterialRealAux
    variable = sigma11
    property = sigma11
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [sigma22]
    type = MaterialRealAux
    variable = sigma22
    property = sigma22
    execute_on = 'INITIAL TIMESTEP_END'
  []
[]
[Materials]
  [law]
    type = ConformalMaterial
    ux = ux
    uy = uy
    pressure = p
    mineral_stiffness = '3.6111111111111116 1.9444444444444444 1.9444444444444444 0 0 0 1.9444444444444444 3.6111111111111116 1.9444444444444444 0 0 0 1.9444444444444444 1.9444444444444444 3.6111111111111116 0 0 0 0 0 0 1.6666666666666667 0 0 0 0 0 0 1.6666666666666667 0 0 0 0 0 0 1.6666666666666667'
    solid_fraction = 0.9
    drained_bulk = 1
    fluid_bulk = 8
    mobility = 1.5
    angle = 0
    linear_reference = true
  []
[]
[Kernels]
  [mx]
    type = ReferenceMomentum
    variable = ux
    component = 0
  []
  [my]
    type = ReferenceMomentum
    variable = uy
    component = 1
  []
  [mass]
    type = ReferenceFluidMass
    variable = p
  []
[]
[BCs]
  [left_ux]
    type = DirichletBC
    variable = ux
    boundary = left
    value = 0
  []
  [right_ux]
    type = FunctionDirichletBC
    variable = ux
    boundary = right
    function = uxr
  []
  [bottom_uy]
    type = DirichletBC
    variable = uy
    boundary = bottom
    value = 0
  []
  [top_uy]
    type = FunctionDirichletBC
    variable = uy
    boundary = top
    function = uyt
  []
  [left_p]
    type = DirichletBC
    variable = p
    boundary = left
    value = 0.02
  []
  [right_p]
    type = DirichletBC
    variable = p
    boundary = right
    value = 0.02
  []
[]
[Postprocessors]
  [J]
    type = ElementExtremeValue
    variable = J
    value_type = max
  []
  [Jbar]
    type = ElementExtremeValue
    variable = Jbar
    value_type = max
  []
  [solid_fraction]
    type = ElementExtremeValue
    variable = solid_fraction
    value_type = max
  []
  [sigma11]
    type = ElementExtremeValue
    variable = sigma11
    value_type = max
  []
  [sigma22]
    type = ElementExtremeValue
    variable = sigma22
    value_type = max
  []
[]
[Preconditioning]
  [full]
    type = SMP
    full = true
  []
[]
[Executioner]
  type = Transient
  solve_type = PJFNK
  dt = 1
  end_time = 1
  scheme = implicit-euler
  nl_rel_tol = 1e-10
  nl_abs_tol = 1e-12
  nl_max_its = 15
  l_tol = 1e-10
  l_max_its = 200
  petsc_options_iname = '-pc_type -pc_factor_mat_solver_type'
  petsc_options_value = 'lu mumps'
[]
[Outputs]
  csv = true
  execute_on = 'INITIAL TIMESTEP_END'
[]
