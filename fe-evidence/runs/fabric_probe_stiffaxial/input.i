# SPDX-License-Identifier: Apache-2.0
# Uniform prescribed-deformation probe of the reference-state fabric law.
#
# A single QUAD4 element whose four nodes are all constrained, so the material
# point state is exactly eps = diag(e11, e22, 0) with uniform pressure p0.
# The reported B_par and B_per are the axial and transverse Biot coefficients
# of sections/pore_fabric.tex (eq. fabric-transverse-biot).
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
  [B_par]
    family = MONOMIAL
    order = CONSTANT
  []
  [B_per]
    family = MONOMIAL
    order = CONSTANT
  []
  [B_anisotropy]
    family = MONOMIAL
    order = CONSTANT
  []
  [ln_a]
    family = MONOMIAL
    order = CONSTANT
  []
  [ln_h]
    family = MONOMIAL
    order = CONSTANT
  []
  [distention_a]
    family = MONOMIAL
    order = CONSTANT
  []
  [distention_h]
    family = MONOMIAL
    order = CONSTANT
  []
  [Jbar]
    family = MONOMIAL
    order = CONSTANT
  []
  [J]
    family = MONOMIAL
    order = CONSTANT
  []
  [energy]
    family = MONOMIAL
    order = CONSTANT
  []
  [drained_c11]
    family = MONOMIAL
    order = CONSTANT
  []
  [drained_c12]
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
  [solid_fraction]
    family = MONOMIAL
    order = CONSTANT
  []
[]
[AuxKernels]
  [B_par]
    type = MaterialRealAux
    variable = B_par
    property = B_par
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [B_per]
    type = MaterialRealAux
    variable = B_per
    property = B_per
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [B_anisotropy]
    type = MaterialRealAux
    variable = B_anisotropy
    property = B_anisotropy
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [ln_a]
    type = MaterialRealAux
    variable = ln_a
    property = ln_a
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [ln_h]
    type = MaterialRealAux
    variable = ln_h
    property = ln_h
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [distention_a]
    type = MaterialRealAux
    variable = distention_a
    property = distention_a
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [distention_h]
    type = MaterialRealAux
    variable = distention_h
    property = distention_h
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [Jbar]
    type = MaterialRealAux
    variable = Jbar
    property = Jbar
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [J]
    type = MaterialRealAux
    variable = J
    property = J
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [energy]
    type = MaterialRealAux
    variable = energy
    property = energy
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [drained_c11]
    type = MaterialRealAux
    variable = drained_c11
    property = drained_c11
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [drained_c12]
    type = MaterialRealAux
    variable = drained_c12
    property = drained_c12
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
  [solid_fraction]
    type = MaterialRealAux
    variable = solid_fraction
    property = solid_fraction
    execute_on = 'INITIAL TIMESTEP_END'
  []
[]
[Materials]
  [law]
    type = FabricMaterial
    ux = ux
    uy = uy
    pressure = p
    mineral_stiffness = '3.6111111111111116 1.9444444444444444 1.9444444444444444 0 0 0 1.9444444444444444 3.6111111111111116 1.9444444444444444 0 0 0 1.9444444444444444 1.9444444444444444 3.6111111111111116 0 0 0 0 0 0 1.6666666666666667 0 0 0 0 0 0 1.6666666666666667 0 0 0 0 0 0 1.6666666666666667'
    solid_fraction = 0.9
    fabric_volume_modulus = 1
    fabric_axial_modulus = 1
    fabric_coupling = 0
    fabric_angle = 0
    conformal_limit = false
    fluid_bulk = 8
    mobility = 1.5
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
  [B_par]
    type = ElementExtremeValue
    variable = B_par
    value_type = max
  []
  [B_per]
    type = ElementExtremeValue
    variable = B_per
    value_type = max
  []
  [B_anisotropy]
    type = ElementExtremeValue
    variable = B_anisotropy
    value_type = max
  []
  [ln_a]
    type = ElementExtremeValue
    variable = ln_a
    value_type = max
  []
  [ln_h]
    type = ElementExtremeValue
    variable = ln_h
    value_type = max
  []
  [Jbar]
    type = ElementExtremeValue
    variable = Jbar
    value_type = max
  []
  [J]
    type = ElementExtremeValue
    variable = J
    value_type = max
  []
  [energy]
    type = ElementExtremeValue
    variable = energy
    value_type = max
  []
  [drained_c11]
    type = ElementExtremeValue
    variable = drained_c11
    value_type = max
  []
  [drained_c12]
    type = ElementExtremeValue
    variable = drained_c12
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
  [solid_fraction]
    type = ElementExtremeValue
    variable = solid_fraction
    value_type = max
  []
  [mass]
    type = ADElementIntegralMaterialProperty
    mat_prop = fluid_mass
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
