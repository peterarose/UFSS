import yaml
import os
import itertools
import copy
import shutil
import math

def convert_simple_dict(vib_dict):
    site = vib_dict['site_label']
    d = vib_dict['displacement']
    try:
        alpha = vib_dict['alpha']
    except KeyError:
        alpha = 1
    p0 = [1]
    p1 = [alpha**2]
    k0 = [1]
    k1 = [1]
    try:
        l = vib_dict['reorganization']
    except KeyError:
        l = -alpha**2 * d**2
    
    k_modifier = [alpha**(i/4) for i in range(2,len(k0)+2)]
    new_k0 = [a*b for a,b in zip(k0,k_modifier)]
    new_k1 = [a*b for a,b in zip(k1,k_modifier)]
    
    p_modifier = [alpha**(-i/4) for i in range(2,len(p0)+2)]
    new_p0 = [a*b for a,b in zip(p0,p_modifier)]
    new_p1 = [a*b for a,b in zip(p1,p_modifier)]
    
    new_d = d*alpha**(1/4)/2

    potential1 = new_p1
    kinetic1 = new_k1

    new_vib_dict = {'displacement':[-new_d,new_d],'reorganization':[0,l],
                    'omega_g':vib_dict['omega_g'],'kinetic':[new_k0,new_k1],
                    'potential':[new_p0,new_p1],'site_label':site}
    try:
        new_vib_dict['condon_violation'] = vib_dict['condon_violation']
    except KeyError:
        pass
    return new_vib_dict

def convert(base_path,*,convert_type='simple'):
    simple_file_name = os.path.join(base_path,'simple_params.yaml')
    parameter_file_name = os.path.join(base_path,'params.yaml')
    with open(simple_file_name,'r') as yamlstream:
        simple = yaml.load(yamlstream,Loader=yaml.SafeLoader)
    
    params = dict()
    params['dipoles'] = simple['dipoles']
    params['site_energies'] = simple['site_energies']
    params['site_couplings'] = simple['site_couplings']
    params['initial truncation size'] = simple['truncation_size']
    try:
        params['number eigenvalues'] = simple['num_eigenvalues']
        params['eigenvalue precision'] = simple['eigenvalue_precision']
    except KeyError:
        pass
    
    try:
        params['maximum_manifold'] = simple['maximum_manifold']
    except KeyError:
        pass

    try:
        params['bath'] = simple['bath']
    except KeyError:
        pass

    simple_vibrations = simple['vibrations']
    n = len(simple['site_energies'])
    
    if convert_type == 'simple':
        vibrations = [convert_simple_dict(vib) for vib in simple_vibrations]
        
    params['vibrations'] = vibrations

    with open(parameter_file_name,'w+') as yamlstream:
        yamlstream.write('### This file was generated by UFSS, do not modify unless you know what you are doing \n')
        yaml.dump(params,yamlstream)

    
