"""Unit tests for bioprocess kinetics, scale-up, and microbial consortium simulation."""

import numpy as np
import pytest
from scipy.integrate import odeint

from src.core.scale_up import BioreactorScaleUp
from src.models.consortium import BioproductSimulator
from src.models.kinetics import FermentationKinetics


def test_scale_up_geometry_and_criteria():
    scaler = BioreactorScaleUp(v1=20, v2=200, d_t1=0.3, d_i1=0.1, n1=400, vvm=1.0)
    assert np.isclose(scaler.scale_factor, 10.0 ** (1.0 / 3.0))

    rpm_pv = scaler.constant_power_volume()
    rpm_tip = scaler.constant_tip_speed()
    assert 0.0 < rpm_tip < rpm_pv < 400.0

    kla = scaler.calculate_kla(p_v=1500.0, vs=0.01)
    assert kla > 0.0

    tm = scaler.calculate_mixing_time(Dt=scaler.Dt1, Di=scaler.Di1, N_rps=scaler.N1)
    assert tm > 0.0

    av_small = scaler.calculate_cooling_area_ratio(scaler.Dt1)
    av_large = scaler.calculate_cooling_area_ratio(scaler.Dt2)
    assert av_small > av_large > 0.0

    report = scaler.generate_report()
    assert "Criterio P/V Constante" in report
    assert "Criterio v_tip Constante" in report

    with pytest.raises(ValueError):
        BioreactorScaleUp(v1=0, v2=200, d_t1=0.3, d_i1=0.1, n1=400)


def test_fermentation_kinetics_and_ode():
    kin = FermentationKinetics(mu_max=0.35, Ks=3.0, Yxs=0.15, Yps=0.45, kd=0.0)
    d_pos = kin.get_derivatives([0.5, 50.0, 0.0], 0.0)
    assert d_pos[0] > 0.0
    assert d_pos[1] < 0.0
    assert d_pos[2] > 0.0

    d_zero = kin.get_derivatives([0.5, 0.0, 1.0], 0.0)
    assert d_zero[1] == 0.0

    t = np.linspace(0.0, 48.0, 100)
    sol = odeint(kin.get_derivatives, [0.1, 100.0, 0.0], t)
    assert sol[-1, 0] > sol[0, 0]
    assert sol[-1, 1] < sol[0, 1]
    assert sol[-1, 2] > sol[0, 2]

    with pytest.raises(ValueError):
        FermentationKinetics(mu_max=-0.1, Ks=2.5, Yxs=0.1, Yps=0.4, kd=0.01)


def test_bioproduct_consortium_simulator():
    feedstock = {
        "azucares_simples": 120.0,
        "celulosa": 40.0,
        "nitrogeno_organico": 15.0,
        "minerales": 5.0,
    }
    yeast_only = BioproductSimulator(feedstock, ["Levadura"]).run_fermentation()
    full_consortium = BioproductSimulator(
        feedstock, ["Bacillus", "Levadura", "Lactobacillus"]
    ).run_fermentation()

    assert yeast_only["etanol"] > 0.0
    assert yeast_only["acido_lactico"] == 0.0
    assert full_consortium["celulosa_residual"] < feedstock["celulosa"]
    assert full_consortium["aminoacidos_libres"] > 0.0
    assert full_consortium["acido_lactico"] > 10.0
    assert full_consortium["ph_estimado"] == 3.8

    report = BioproductSimulator(feedstock, ["Bacillus", "Levadura", "Lactobacillus"]).generate_report()
    assert "REPORTE DE COMPOSICIÓN DE BIOPRODUCTO" in report
