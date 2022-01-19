import joblib
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt



models_path = '/fefs/aswg/data/models/20200629_prod5_trans_80/zenith_20deg/south_pointing/20210923_v0.7.5_prod5_trans_80_dynamic_cleaning/'
print(os.listdir(models_path))


models = [{'path': Path(models_path).joinpath(filename)} for filename in os.listdir(models_path) if filename.endswith('.sav')]

for model in models:
    model['model'] = joblib.load(model['path'])


def get_events_per_leaves(forests):
    all_leaves = []
    for estimator in forests.estimators_:
        leaves = estimator.tree_.children_left == -1
        all_leaves.extend(estimator.tree_.n_node_samples[leaves])
    return all_leaves


for model in models:
    print(model['path'])
    print(np.mean([est.get_depth() for est in model['model'].estimators_]))
    n_leaves = [est.get_n_leaves() for est in model['model'].estimators_]
    print(np.mean(n_leaves))
    estimator = model['model'].estimators_[0]
    # events_per_leaves = get_events_per_leaves(model['model'])
    # getting histogram for a single estimator is enough
    leaves = estimator.tree_.children_left == -1
    events_per_leaves = estimator.tree_.n_node_samples[leaves]
    plt.hist(events_per_leaves, bins=np.linspace(1, 40, 40))
    plt.yscale('log')
    plt.title(model['path'].name)
    plt.show()
