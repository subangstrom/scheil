import os
import numpy as np
from pycalphad import Database, variables as v
from scheil import simulate_scheil_solidification

def test_solidification_result_consistency():
    """Test that SolidificationResult objects produces aligned results."""

    dbf = Database(os.path.join(os.path.dirname(__file__), 'alzn_mey.tdb'))
    comps = ['AL', 'ZN', 'VA']
    phases = sorted(dbf.phases.keys())

    liquid_phase_name = 'LIQUID'
    initial_composition = {v.X('ZN'): 0.3}
    start_temperature = 850

    sol_res = simulate_scheil_solidification(dbf, comps, phases, initial_composition, start_temperature, step_temperature=10.0)

    num_temperatures = len(sol_res.temperatures)
    assert num_temperatures == len(sol_res.x_liquid)
    assert num_temperatures == len(sol_res.fraction_liquid)
    assert all([num_temperatures == len(np) for np in sol_res.phase_amounts.values()])

    # final phase amounts are correct
    assert sol_res.fraction_liquid[-1] == 0.0
    assert sol_res.fraction_solid[-1] == 1.0

    # total of final phase amounts is 1
    assert np.isclose(np.sum([amnts[-1] for amnts in sol_res.phase_amounts.values()]), 1.0)