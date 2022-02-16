from pathlib import Path
from lstchain.io import get_standard_config
from copy import deepcopy
import json
import lstchain
from packaging import version


outdir = 'config-grid'
Path(outdir).mkdir(exist_ok=True)


depths = [10, 30, 50]
min_samples_split = [5, 10, 40, 100]

standard_config = get_standard_config()


def write_config(config, filename):
    with open(filename, 'w') as file_handle:
        json.dump(config, file_handle, indent=4)

        
write_config(standard_config, Path(outdir, 'std_config.json'))
        

for d in depths:
    for mss in min_samples_split:
        config = deepcopy(standard_config)
        ### lstchain >= v0.8
        if version.parse(lstchain.__version__) >= version.parse("0.8"):
            config['random_forest_disp_regressor_args']['max_depth'] = d
            config['random_forest_disp_regressor_args']['min_samples_split'] = mss
            config['random_forest_disp_classifier_args']['max_depth'] = d
            config['random_forest_disp_classifier_args']['min_samples_split'] = mss
            config['random_forest_energy_regressor_args']['max_depth'] = d
            config['random_forest_particle_classifier_args']['max_depth'] = d
            config['random_forest_energy_regressor_args']['min_samples_split'] = mss
            config['random_forest_particle_classifier_args']['min_samples_split'] = mss

        else:
            config['random_forest_regressor_args']['min_samples_split'] = mss
            config['random_forest_regressor_args']['max_depth'] = d
            config['random_forest_classifier_args']['min_samples_split'] = mss
            config['random_forest_classifier_args']['max_depth'] = d
        
        
        filename = f'config_{d}_{mss}.json'
        write_config(config, Path(outdir).joinpath(filename))
