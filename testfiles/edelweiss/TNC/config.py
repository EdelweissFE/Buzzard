config = {
    #    "env_variables": {"EDELWEISS_PATH": "your_custom_path_to/EdelweissFE"},
    "scipysettings": {
        "method": "TNC",
        "options": {},
    },
    "identification": {"YOUNGS_MODULUS": {"start": 35000, "min": 20000, "max": 50000, "active": True}},
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
