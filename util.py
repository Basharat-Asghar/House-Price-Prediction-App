import json
import joblib
import numpy as np

__locations = None
__data_columns = None
__model = None


def load_saved_artifacts():
    print("Loading saved artifacts...start")
    global __data_columns
    global __locations

    with open("./artifacts/columns.json", 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[5:]

    global __model
    with open("./artifacts/xgb_tuned.joblib", 'rb') as f:
        __model = joblib.load(f)
    print("Loading saved artifacts...done")


def get_location_names():
    return __locations


def get_data_columns():
    return __data_columns


def get_estimated_price(location, bath, balcony, bhk, total_sqft, room_size_avg):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = bath
    x[1] = balcony
    x[2] = bhk
    x[3] = total_sqft
    x[4] = room_size_avg

    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)



if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar',2, 1, 3, 1000, 333.33))
    print(get_estimated_price('1st Phase JP Nagar', 3, 1, 5, 2000, 400.0))
    print(get_estimated_price('Kalhalli', 1, 0, 2, 800, 400.0))
    print(get_estimated_price('Ejipura', 1, 1, 3, 1200, 400.0))