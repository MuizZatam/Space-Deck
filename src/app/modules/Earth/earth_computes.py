# Importing requirements
import spiceypy
import datetime
import math
import numpy as np
import os

kernel_path = os.path.abspath("/kernel_meta.txt")

spiceypy.furnsh(kernel_path)

# Loading all required kernels at once

# The main function
def main():

    computes()
    

def computes():

    # Constructing a datetime object that returns the current date.
    current_date_time = datetime.datetime.today()

    # Formatting to the UTC Timestamp as it is better supported by Spicepy
    current_date_time = current_date_time.strftime(r"%Y-%m-%dT00:00:00")

    print(f"UTC Timestamp: {current_date_time}")

    # Converting to Ephimeris Timestamp:
    # UTC Timestamps provide valid calculations for measurements on Earth
    # However, measuring stellar objects from an observer's point of view
    # requires Ephimeris Timestamps as it adjusts for relativistic effects 
    # and astronomical measurements.

    # Emphimeris Timestamps measure the time in seconds for the current date
    # So 1st Jan 2000 in Ephimeris Timestamp indicates the 2000th second on 
    # the 1st of Jan


    # This commit removed the use of furnsh multiple times. 
    # Kernel loading is now handled by kernel_meta.txt
    # This file loads up all the kernels specified during the runtime of spice

    # Converting to Ephimeris Timestamp
    ephimeris_date_time = spiceypy.utc2et(current_date_time)
    print(f"Ephimeris Timestamp: {ephimeris_date_time}")

    # Computing state of Earth
    earth_state_wrt_sun, earth_sun_light_time = spiceypy.spkgeo(

        targ = 399, # Setting the Target to Earth
        et = ephimeris_date_time,
        ref = "ECLIPJ2000", # Plane of reference with respect to Earth
        obs = 10 # As observed from Sun
    )

    # State vector returns the x, y, z position of Earth with respect to Sun
    print(f"State Vector: {earth_state_wrt_sun}")
    # Light Time is the time taken by Light to reach Earth from Sun
    print(f"Light Time: {earth_sun_light_time}")
    light_time_in_minutes = earth_sun_light_time / 60.0
    print(f"Light Time in Minutes: {light_time_in_minutes}")

    # Calculating Euclidean distance from Co-Ords
    earth_sun_distance = math.sqrt(
        earth_state_wrt_sun[0] ** 2.0 
        + earth_state_wrt_sun[1] ** 2.0
        + earth_state_wrt_sun[2] ** 2.0
    )

    print(f"Distance of Earth from Sun: {earth_sun_distance}")

    # Converting to AU
    distance_in_au = spiceypy.convrt(earth_sun_distance, "km", "au")

    print(f"Distance in AU: {distance_in_au}")


    # This section is all about computing Earth's Orbital and Tangential velocity

    # Converting to np array for faster calculations
    earth_state_wrt_sun = np.array(earth_state_wrt_sun)

    # Using the state vector to compute distance by normalizing the x, y and z coords
    # earth_sun_distance = math.sqrt(
    #     earth_state_wrt_sun[0] ** 2.0 
    #     + earth_state_wrt_sun[1] ** 2.0
    #     + earth_state_wrt_sun[2] ** 2.0
    # )
    # Essentially performig euclidean distance calculation but through np protocol
    earth_sun_distance = np.linalg.norm(earth_state_wrt_sun[:3])

    print(f"Earth through Sun distance calculated through np: {earth_sun_distance}")

    # Calculation of orbital velocity (Km/s)
    orbital_velocity = np.linalg.norm(earth_state_wrt_sun[3:])

    print(f"Orbital Velocity: {orbital_velocity}")


    # gm_de431 kernel is now loaded by kernel_meta
    # Here, it is used to calculate Gravitation x Mass of the Sun
    _, GM_SUN = spiceypy.bodvcd(bodyid=10, item="GM", maxn=1)

    # The velocity calculated on line 90 (orbital_velocity = np.linalg.norm(earth_state_wrt_sun[3:]))
    # can be verified through the mathematical equation: orbital_velocity = (GM/R) ^ 1/2
    verify_orbital_velocity = lambda gm, r: np.sqrt(gm/r)

    # To verify the orbital velocity:
    print(f"Verified Orbital Velocity: {verify_orbital_velocity(GM_SUN[0], earth_sun_distance)} Km/s")

    # This section allows us to compute the angular distance that has been covered by Earth
    # Since Vernal Equinox

    # The vernal equinox, also known as the spring equinox, marks the beginning of spring 
    # in the Northern Hemisphere and occurs when the Sun crosses the celestial equator 
    # moving northward, making day and night approximately equal in length
    # On this day, the state vector if normalized, represents (x, y, z) as (1, 0, 0)
    earth_position_wrt_sun = earth_state_wrt_sun[:3]

    # Normalizing the co-ordinate distances
    earth_state_wrt_sun_normalized = earth_position_wrt_sun / earth_sun_distance
    
    # Actual normalized state vector on Vernal Equinox
    earth_state_wrt_sun_normed_autumn = [1.0, 0.0, 0.0]

    # Calculating the Angular Distance
    # The angular distance of Earth is dot of normalized Earth Vector (Today) with Vernal Equinox state
    angular_distance = np.degrees(
        np.arccos(np.dot(
            earth_state_wrt_sun_normalized, earth_state_wrt_sun_normed_autumn
        ))
    )

    print(f"Angular distance since Vernal Equinox: {angular_distance}degrees")

    return {
        "state": earth_state_wrt_sun, 
        "distance" : round(earth_sun_distance, ndigits=3),
        "distance_au": round(distance_in_au, ndigits=3),
        "light_time": round(earth_sun_light_time, ndigits=3), 
        "light_time_minutes": round(light_time_in_minutes, ndigits=3),
        "orbital_velocity": round(orbital_velocity, ndigits=3),
        "angular_distance": round(angular_distance, ndigits=3)
    }

    # Note: I am not returning the verified values as they are not
    # required to be showcased for the deck


if __name__ == "__main__":

    main()