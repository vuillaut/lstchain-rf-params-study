import os
from pathlib import Path
from glob import glob
from subprocess import run




dl1_prod = '/fefs/aswg/data/mc/DL1/20200629_prod5_trans_80/{particle}/zenith_20deg/south_pointing/20210923_v0.7.5_prod5_trans_80_dynamic_cleaning/'


config_grid_dir = 'configs/config-grid/'
configs = os.listdir(config_grid_dir)

results_dir = Path(__file__).parent.joinpath('results').absolute().as_posix()


def outdir_from_config(config, base_outdir = results_dir):
    
    outdir = os.path.join(base_outdir, os.path.basename(config).split('.')[0])

    return outdir



def main():
    
    jobs_dir = 'jobs'
    os.makedirs(jobs_dir, exist_ok=True)
    base_slurm = open('base_slurm.slurm').read()
    
    dl1_gamma_train = glob(dl1_prod.format(particle='gamma-diffuse') + '/*train*.h5')[0]
    dl1_proton_train = glob(dl1_prod.format(particle='proton') + '/*train*.h5')[0]

    dl1_gamma_test = glob(dl1_prod.format(particle='gamma') + '/off0.4deg/*test*.h5')[0]
    dl1_proton_test = glob(dl1_prod.format(particle='proton') + '/*test*.h5')[0]
    dl1_electron_test = glob(dl1_prod.format(particle='electron') + '/*test*.h5')[0]

    for file in [dl1_gamma_test, dl1_electron_test, dl1_proton_test, dl1_gamma_train, dl1_proton_train]:
        assert os.path.exists(file)
    
    
    for config in configs:

        config_path = Path(config_grid_dir, config).absolute().as_posix()
        
        outdir = outdir_from_config(config)
        
        cmds = '\n\n'
        cmds += f'lstchain_mc_trainpipe --fg {dl1_gamma_train} --fp {dl1_proton_train} -c {config_path} -o {outdir} \n\n'
        
        cmds += f'lstchain_dl1_to_dl2 -f {dl1_gamma_test}  -o {outdir} -p {outdir} -c {config_path}\n\n'
        cmds += f'lstchain_dl1_to_dl2 -f {dl1_proton_test}  -o {outdir} -p {outdir} -c {config_path}\n\n'
        cmds += f'lstchain_dl1_to_dl2 -f {dl1_electron_test} -o {outdir} -p {outdir} -c {config_path}\n\n'
        

        dl2_gamma_test = os.path.join(outdir, os.path.basename(os.path.realpath(dl1_gamma_test)).replace('dl1', 'dl2'))
        dl2_proton_test = os.path.join(outdir, os.path.basename(os.path.realpath(dl1_proton_test)).replace('dl1', 'dl2'))
        dl2_electron_test = os.path.join(outdir, os.path.basename(os.path.realpath(dl1_electron_test)).replace('dl1', 'dl2'))
        sens_file = os.path.join(outdir, f"sens_{config.split('.')[0]}.fits.gz")
        
        
        cmds += f'lstmcpipe_dl2_to_sensitivity -g {dl2_gamma_test} -p {dl2_proton_test} -e {dl2_electron_test} -o {sens_file}\n\n'
        
        
        job_sh = os.path.join(jobs_dir, f"{config.split('.')[0]}.slurm")

        with open(job_sh, 'w') as job_file:
            job_file.write(base_slurm.format(JOB_NAME=config.split('.')[0]))
            job_file.write(cmds)
                                 
        run(['sbatch', job_sh])
        
    
if __name__ == '__main__':
    main()
