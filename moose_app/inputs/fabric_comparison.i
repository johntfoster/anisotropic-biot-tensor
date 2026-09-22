# SPDX-License-Identifier: Apache-2.0
# Constrained strip: ramp traction from rest, then hold through drainage.
# Both vertical sides constrain horizontal displacement; the right side drains.
# The scalar variant preserves Cd, storage and mobility and replaces B reciprocally.
[Mesh]
  [base]
    type = GeneratedMeshGenerator
    dim = 2
    nx = 20
    ny = 4
    xmin = 0
    xmax = 1
    ymin = 0
    ymax = 0.1
    elem_type = QUAD9
  []
  [anchor]
    type = ExtraNodesetGenerator
    input = base
    new_boundary = anchor
    coord = '0 0 0'
  []
[]
[Variables]
  [ux]
    order = SECOND
    family = LAGRANGE
  []
  [uy]
    order = SECOND
    family = LAGRANGE
  []
  [p]
    order = FIRST
    family = LAGRANGE
  []
[]
[Functions]
  [ix]
    type = ParsedFunction
    expression = '0'
  []
  [iy]
    type = ParsedFunction
    expression = '0'
  []
  [load]
    type = ParsedFunction
    expression = '-0.0001*min(t/0.01,1)'
  []
[]
[ICs]
  [ix]
    type = FunctionIC
    variable = ux
    function = ix
  []
  [iy]
    type = FunctionIC
    variable = uy
    function = iy
  []
  [p]
    type = ConstantIC
    variable = p
    value = 0
  []
[]
[AuxVariables]
  [lateral_force]
    family = LAGRANGE
    order = SECOND
  []
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
  [stability]
    family = MONOMIAL
    order = CONSTANT
  []
  [energy]
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
  [mass_reaction]
    family = LAGRANGE
    order = FIRST
  []
  [force_reaction]
    family = LAGRANGE
    order = SECOND
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
  [stability]
    type = MaterialRealAux
    variable = stability
    property = stability
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [energy]
    type = MaterialRealAux
    variable = energy
    property = energy
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
    type = FabricMaterial
    ux = ux
    uy = uy
    pressure = p
    mineral_stiffness = '3.6111111111111116 1.9444444444444444 1.9444444444444444 0 0 0 1.9444444444444444 3.6111111111111116 1.9444444444444444 0 0 0 1.9444444444444444 1.9444444444444444 3.6111111111111116 0 0 0 0 0 0 1.6666666666666667 0 0 0 0 0 0 1.6666666666666667 0 0 0 0 0 0 1.6666666666666667'
    solid_fraction = 0.9
    fabric_volume_modulus = 5.4
    fabric_axial_modulus = 1
    fabric_coupling = 0.4
    fabric_angle = 0
    conformal_limit = false
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
    save_in = lateral_force
  []
  [my]
    type = ReferenceMomentum
    variable = uy
    component = 1
    save_in = force_reaction
  []
  [mass]
    type = ReferenceFluidMass
    variable = p
    save_in = mass_reaction
  []
[]
[BCs]
  [x]
    type = DirichletBC
    variable = ux
    boundary = 'left right'
    value = 0
  []
  [bottom]
    type = DirichletBC
    variable = uy
    boundary = bottom
    value = 0
  []
  [pressure]
    type = DirichletBC
    variable = p
    boundary = 'right'
    value = 0
    preset = false
  []
  [force]
    type = FunctionNeumannBC
    variable = uy
    boundary = top
    function = load
  []
[]
[Postprocessors]
  [top_displacement]
    execute_on = 'INITIAL TIMESTEP_END'
    type = SideAverageValue
    variable = uy
    boundary = top
  []
  [right_reaction]
    execute_on = 'INITIAL TIMESTEP_END'
    type = NodalSum
    variable = lateral_force
    boundary = right
  []
  [mass]
    execute_on = 'INITIAL TIMESTEP_END'
    type = ADElementIntegralMaterialProperty
    mat_prop = fluid_mass
  []
  [outflow_gradient]
    execute_on = 'INITIAL TIMESTEP_END'
    type = ReferenceOutflow
    boundary = 'right'
  []
  [mass_reaction]
    execute_on = 'INITIAL TIMESTEP_END'
    type = DofReactionSum
    variable = mass_reaction
    boundary = 'right'
  []
  [top_reaction]
    execute_on = 'INITIAL TIMESTEP_END'
    type = NodalSum
    variable = force_reaction
    boundary = top
  []
  [platen_min]
    execute_on = 'INITIAL TIMESTEP_END'
    type = NodalExtremeValue
    variable = uy
    boundary = top
    value_type = min
  []
  [platen_max]
    execute_on = 'INITIAL TIMESTEP_END'
    type = NodalExtremeValue
    variable = uy
    boundary = top
    value_type = max
  []
  [center_pressure]
    execute_on = 'INITIAL TIMESTEP_END'
    type = PointValue
    variable = p
    point = '0 0 0'
  []
  [edge_ux]
    execute_on = 'INITIAL TIMESTEP_END'
    type = PointValue
    variable = ux
    point = '1 0 0'
  []
  [J_min]
    execute_on = 'INITIAL TIMESTEP_END'
    type = ElementExtremeMaterialProperty
    mat_prop = J
    value_type = min
  []
  [J_max]
    execute_on = 'INITIAL TIMESTEP_END'
    type = ElementExtremeMaterialProperty
    mat_prop = J
    value_type = max
  []
  [Jbar_min]
    execute_on = 'INITIAL TIMESTEP_END'
    type = ElementExtremeMaterialProperty
    mat_prop = Jbar
    value_type = min
  []
  [Jbar_max]
    execute_on = 'INITIAL TIMESTEP_END'
    type = ElementExtremeMaterialProperty
    mat_prop = Jbar
    value_type = max
  []
  [solid_fraction_min]
    execute_on = 'INITIAL TIMESTEP_END'
    type = ElementExtremeMaterialProperty
    mat_prop = solid_fraction
    value_type = min
  []
  [solid_fraction_max]
    execute_on = 'INITIAL TIMESTEP_END'
    type = ElementExtremeMaterialProperty
    mat_prop = solid_fraction
    value_type = max
  []
  [stability_min]
    execute_on = 'INITIAL TIMESTEP_END'
    type = ElementExtremeMaterialProperty
    mat_prop = stability
    value_type = min
  []
  [stability_max]
    execute_on = 'INITIAL TIMESTEP_END'
    type = ElementExtremeMaterialProperty
    mat_prop = stability
    value_type = max
  []
  [B_par]
    execute_on = 'INITIAL TIMESTEP_END'
    type = ElementExtremeMaterialProperty
    mat_prop = B_par
    value_type = max
  []
  [B_per]
    execute_on = 'INITIAL TIMESTEP_END'
    type = ElementExtremeMaterialProperty
    mat_prop = B_per
    value_type = max
  []
  [B_anisotropy]
    execute_on = 'INITIAL TIMESTEP_END'
    type = ElementExtremeMaterialProperty
    mat_prop = B_anisotropy
    value_type = max
  []
  [ln_h_min]
    execute_on = 'INITIAL TIMESTEP_END'
    type = ElementExtremeMaterialProperty
    mat_prop = ln_h
    value_type = min
  []
  [ln_h_max]
    execute_on = 'INITIAL TIMESTEP_END'
    type = ElementExtremeMaterialProperty
    mat_prop = ln_h
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
  solve_type = NEWTON
  line_search = basic
  dt = 0.0025
  end_time = 0.75
  scheme = implicit-euler
  nl_rel_tol = 1e-9
  nl_abs_tol = 1e-13
  nl_max_its = 15
  l_tol = 1e-9
  l_max_its = 200
  petsc_options_iname = '-pc_type -pc_factor_mat_solver_type'
  petsc_options_value = 'lu mumps'
[]
[Outputs]
  csv = true
  exodus = false
  execute_on = 'INITIAL TIMESTEP_END'
[]
