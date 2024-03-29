# ThermoState
A CoolProp GUI for calculating Thermodynamics properties of fluids. 

By - [Shihabus Sakib Rad](https://github.com/Shihabus-Sakib-Rad)

Go to the [download page.](https://thermo-state.github.io )


ThermoState uses CoolProp Library to calculate properties. It provides a GUI for the library with some added convenient features. It doesn't support fluid mixtures yet.

![alt text](https://thermo-state.github.io/assets/img/Main-GUI.png)

Following Fluids are included.
```python
from CoolProp import CoolProp
CoolProp.FluidsList()
```
> ['1-Butene', 'Acetone', 'Air', 'Ammonia', 'Argon', 'Benzene', 'CarbonDioxide', 'CarbonMonoxide', 'CarbonylSulfide', 'cis-2-Butene', 'CycloHexane', 'Cyclopentane', 'CycloPropane', 'D4', 'D5', 'D6', 'Deuterium', 'Dichloroethane', 'DiethylEther', 'DimethylCarbonate', 'DimethylEther', 'Ethane', 'Ethanol', 'EthylBenzene', 'Ethylene', 'EthyleneOxide', 'Fluorine', 'HeavyWater', 'Helium', 'HFE143m', 'Hydrogen', 'HydrogenChloride', 'HydrogenSulfide', 'IsoButane', 'IsoButene', 'Isohexane', 'Isopentane', 'Krypton', 'm-Xylene', 'MD2M', 'MD3M', 'MD4M', 'MDM', 'Methane', 'Methanol', 'MethylLinoleate', 'MethylLinolenate', 'MethylOleate', 'MethylPalmitate', 'MethylStearate', 'MM', 'n-Butane', 'n-Decane', 'n-Dodecane', 'n-Heptane', 'n-Hexane', 'n-Nonane', 'n-Octane', 'n-Pentane', 'n-Propane', 'n-Undecane', 'Neon', 'Neopentane', 'Nitrogen', 'NitrousOxide', 'Novec649', 'o-Xylene', 'OrthoDeuterium', 'OrthoHydrogen', 'Oxygen', 'p-Xylene', 'ParaDeuterium', 'ParaHydrogen', 'Propylene', 'Propyne', 'R11', 'R113', 'R114', 'R115', 'R116', 'R12', 'R123', 'R1233zd(E)', 'R1234yf', 'R1234ze(E)', 'R1234ze(Z)', 'R124', 'R1243zf', 'R125', 'R13', 'R134a', 'R13I1', 'R14', 'R141b', 'R142b', 'R143a', 'R152A', 'R161', 'R21', 'R218', 'R22', 'R227EA', 'R23', 'R236EA', 'R236FA', 'R245ca', 'R245fa', 'R32', 'R365MFC', 'R40', 'R404A', 'R407C', 'R41', 'R410A', 'R507A', 'RC318', 'SES36', 'SulfurDioxide', 'SulfurHexafluoride', 'Toluene', 'trans-2-Butene', 'Water', 'Xenon']

These imput combinations are supported for water/steam (HEOS Backend) and most other fluids.
> [{'T', 'P'}, {'T', 'ρ'}, {'T', 's'}, {'T', 'x'}, {'ρ', 'P'}, {'s', 'P'}, {'h', 'P'}, {'u', 'P'}, {'x', 'P'}, {'s', 'ρ'}, {'h', 'ρ'}, {'u', 'ρ'}, {'x', 'ρ'}, {'s', 'h'}]

ThermoState calculates/ Tabulates the followings results from CoolProp
> Temperature, Pressure, Sp Volume, Density, Entropy, Enthalpy, Internal Energy, Quality
> Phase, Cp, Cv, Conductivity, Prandtl Number, Viscosity, Compressibility Factor, Surface Tension, Gibbs Energy, Helmholtz Energy


Keywords
```
Thermophysical properties calculator
Thermodynamic and Transport Properties database
Thermodynamic State diagrams: Ts, Ph, hs
Steam table calculator
Refirigerents
Thermodynamic problems solver
CoolProp GUI
REFPROP alternative
```
