# About Spice Kernels

Spice requies Kernels to access measuremental
data (see [JPL's Kernel Repository](https://naif.jpl.nasa.gov/pub/naif/))

1. These Kernels can be loaded using Spicepy's furnsh API.
2. Once loaded, the functions can directly access the records
for computation

---

This commit, creating a module to compute Earth's position at the current
day's midnight, utilizes a LSK Kernel - naif0012.tls and SPK Kernel - de432s.bsp for computing Ephimeris calculations

See:

1. [LSK Kernel - naif0012.tls](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls)

2. [SPK Kernel - de432s.bsp](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de432.pdf)