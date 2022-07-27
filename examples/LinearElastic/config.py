config = {
    #    "env_variables": {"EDELWEISS_PATH": "your_custom_path_to/EdelweissFE"},
    "scipysettings": {
        "method": "trust-constr",
        "options": {"disp": True, "verbose": 2, "gtol": 1e-6},
    },
    "identification": {
        "YOUNGS_MODULUS": {"idx": 0, "start": 35000, "min": 20000, "max": 50000}
    },
    "simulations": {
        "sim1": {
            "type": "edelweiss",
            "input": "sim1.inp",
            "simX": "disp",
            "simY": "force",
            "data": "data_sim1.csv",
            "active": True,
            "errorType": "absolute",
        },
        "sim2": {
            "type": "edelweiss",
            "input": "sim2.inp",
            "simX": "disp",
            "simY": "force",
            "data": "data_sim2.csv",
            "active": True,
            "errorType": "absolute",
        },
    },
}
