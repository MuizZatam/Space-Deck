# Importing requirements
import spiceypy
import datetime
import math


# The main function
def main():

    compute_position()
    

def compute_position():

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


    # Loading Kernels (ref. notes/kernels.md)
    spiceypy.furnsh("./kernels/lsk/naif0012.tls")
    spiceypy.furnsh("./kernels/spk/de432s.bsp")

    # Converting to Ephimeris Timestamp
    ephimeris_date_time = spiceypy.utc2et(current_date_time)
    print(f"Ephimeris Timestamp: {ephimeris_date_time}")

    # Computing state of Earth
    earth_state_wrt_sun, earth_sun_light_time = spiceypy.spkgeo(

        targ = 399,
        et = ephimeris_date_time,
        ref = "ECLIPJ2000", # Plane of reference with respect to Earth
        obs = 10 
    )

    # State vector returns the x, y, z position of Earth with respect to Sun
    print(f"State Vector: {earth_state_wrt_sun}")
    # Light Time is the time taken by Light to reach Earth from Sun
    print(f"Light Time: {earth_sun_light_time}")
    print(f"Light Time in Minutes: {earth_sun_light_time / 60.0}")

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


if __name__ == "__main__":

    main()