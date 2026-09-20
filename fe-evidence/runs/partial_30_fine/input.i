[Mesh]
  [base]
    type = GeneratedMeshGenerator
    dim = 2
    nx = 16
    ny = 16
    xmin = -1
    xmax = 1
    ymin = -1
    ymax = 1
    elem_type = QUAD9
  []
  [drain]
    type = ParsedGenerateSideset
    input = base
    combinatorial_geometry = 'x > 0.99999 & y > -0.25 & y < 0.25'
    new_sideset_name = drain
  []
  [anchor]
    type = ExtraNodesetGenerator
    input = drain
    new_boundary = anchor
    coord = '-1 -1 0'
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
    expression = '0*x'
  []
  [iy]
    type = ParsedFunction
    expression = '0*y'
  []
  [load]
    type = ParsedFunction
    expression = '-0.69999999999999996*min(t/0.002,1)'
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
  [B12]
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
  [sigma12]
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
  [B12]
    type = MaterialRealAux
    variable = B12
    property = B12
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
  [sigma12]
    type = MaterialRealAux
    variable = sigma12
    property = sigma12
    execute_on = 'INITIAL TIMESTEP_END'
  []
[]
[Materials]
  [law]
    type = ConformalMaterial
    ux = ux
    uy = uy
    pressure = p
    mineral_stiffness = '50 12 10 0 0 0 12 60 14 0 0 0 10 14 70 0 0 0 0 0 0 20 0 0 0 0 0 0 24 0 0 0 0 0 0 28'
    solid_fraction = 0.6
    drained_bulk = 7
    fluid_bulk = 8
    mobility = 1.5
    angle = 30.0
    linear_reference = false
    log_quadrature = 12
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
    boundary = anchor
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
    boundary = 'drain'
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
[Constraints]
  [platen]
    type = EqualValueBoundaryConstraint
    variable = uy
    secondary = top
    formulation = kinematic
    penalty = 1
  []
[]
[Postprocessors]
  [mass]
    type = ADElementIntegralMaterialProperty
    mat_prop = fluid_mass
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [outflow_gradient]
    type = ReferenceOutflow
    boundary = 'drain'
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [mass_reaction]
    type = DofReactionSum
    variable = mass_reaction
    boundary = 'drain'
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [top_reaction]
    type = DofReactionSum
    variable = force_reaction
    boundary = top
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [platen_min]
    type = NodalExtremeValue
    variable = uy
    boundary = top
    value_type = min
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [platen_max]
    type = NodalExtremeValue
    variable = uy
    boundary = top
    value_type = max
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [center_pressure]
    type = PointValue
    variable = p
    point = '0 0 0'
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [edge_ux]
    type = PointValue
    variable = ux
    point = '1 0 0'
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [J_min]
    type = ElementExtremeMaterialProperty
    mat_prop = J
    value_type = min
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [J_max]
    type = ElementExtremeMaterialProperty
    mat_prop = J
    value_type = max
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [Jbar_min]
    type = ElementExtremeMaterialProperty
    mat_prop = Jbar
    value_type = min
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [Jbar_max]
    type = ElementExtremeMaterialProperty
    mat_prop = Jbar
    value_type = max
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [solid_fraction_min]
    type = ElementExtremeMaterialProperty
    mat_prop = solid_fraction
    value_type = min
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [solid_fraction_max]
    type = ElementExtremeMaterialProperty
    mat_prop = solid_fraction
    value_type = max
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [stability_min]
    type = ElementExtremeMaterialProperty
    mat_prop = stability
    value_type = min
    execute_on = 'INITIAL TIMESTEP_END'
  []
  [stability_max]
    type = ElementExtremeMaterialProperty
    mat_prop = stability
    value_type = max
    execute_on = 'INITIAL TIMESTEP_END'
  []
[]
[VectorPostprocessors]
  [profile]
    type = LineValueSampler
    variable = 'p ux uy'
    start_point = '-1 0 0'
    end_point = '1 0 0'
    num_points = 101
    sort_by = x
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
  line_search = basic
  dt = 0.0005
  end_time = 0.1
  scheme = implicit-euler
  nl_rel_tol = 1e-9
  nl_abs_tol = 1e-12
  nl_max_its = 15
  l_tol = 1e-9
  l_max_its = 200
  petsc_options_iname = '-pc_type -pc_factor_mat_solver_type'
  petsc_options_value = 'lu mumps'
[]
[Outputs]
  csv = true
  exodus = true
  execute_on = 'INITIAL TIMESTEP_END'
[]
