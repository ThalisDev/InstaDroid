import pickle

with open('contador_hashtags.pkl', 'wb') as handle:
    load = 0
    pickle.dump(load, handle)
    print(load)