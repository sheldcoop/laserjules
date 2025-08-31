import pytest
from laser_calculator_app.core.material_analyzer import get_material_properties, MATERIALS

def test_get_material_properties_valid():
    """Tests retrieving properties for a valid material."""
    properties = get_material_properties("Acrylic (PMMA)")
    assert properties == MATERIALS["Acrylic (PMMA)"]

def test_get_material_properties_invalid():
    """Tests that a ValueError is raised for an invalid material."""
    with pytest.raises(ValueError):
        get_material_properties("Unobtanium")
