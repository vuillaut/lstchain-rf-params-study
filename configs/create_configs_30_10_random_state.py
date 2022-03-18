from pathlib import Path
from lstchain.io import get_standard_config
from copy import deepcopy
import json
import lstchain
from packaging import version
import numpy as np
import shutil


outdir = 'config-random-state-30-10'
if Path(outdir).exists():
    shutil.rmtree(outdir)
Path(outdir).mkdir(exist_ok=True)


random_state = [int(r) for r in np.random.randint(100, size=5, dtype=np.int32)]

standard_config = get_standard_config()
d = 30
mss = 10
n_jobs = 32



def write_config(config, filename):
    with open(filename, 'w') as file_handle:
        json.dump(config, file_handle, indent=4)

        
# write_config(standard_config, Path(outdir, 'std_config.json'))

    
for r in random_state:
    print(r)
    config = deepcopy(standard_config)
    if version.parse(lstchain.__version__) >= version.parse("0.8"):
        config['random_forest_disp_regressor_args']['random_state'] = r
        config['random_forest_disp_classifier_args']['random_state'] = r
        config['random_forest_energy_regressor_args']['random_state'] = r
        config['random_forest_particle_classifier_args']['random_state'] = r
        config['random_forest_disp_regressor_args']['n_jobs'] = n_jobs
        config['random_forest_disp_classifier_args']['n_jobs'] = n_jobs
        config['random_forest_energy_regressor_args']['n_jobs'] = n_jobs
        config['random_forest_particle_classifier_args']['n_jobs'] = n_jobs
        config['random_forest_disp_regressor_args']['max_depth'] = d
        config['random_forest_disp_regressor_args']['min_samples_split'] = mss
        config['random_forest_disp_classifier_args']['max_depth'] = d
        config['random_forest_disp_classifier_args']['min_samples_split'] = mss
        config['random_forest_energy_regressor_args']['max_depth'] = d
        config['random_forest_particle_classifier_args']['max_depth'] = d
        config['random_forest_energy_regressor_args']['min_samples_split'] = mss
        config['random_forest_particle_classifier_args']['min_samples_split'] = mss

    else:
        config['random_forest_regressor_args']['random_state'] = r
        config['random_forest_classifier_args']['random_state'] = r
        config['random_forest_regressor_args']['n_jobs'] = n_jobs
        config['random_forest_classifier_args']['n_jobs'] = n_jobs
        config['random_forest_regressor_args']['min_samples_split'] = mss
        config['random_forest_regressor_args']['max_depth'] = d
        config['random_forest_classifier_args']['min_samples_split'] = mss
        config['random_forest_classifier_args']['max_depth'] = d
        
    filename = f'config_{r}.json'
    write_config(config, Path(outdir).joinpath(filename))

    
