# change the directories
from astropy.table import Table
import numpy as np
import pickle
import matplotlib as mpl
import matplotlib.pyplot as plt
import statistics


mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['axes.linewidth'] = 1.5
mpl.rcParams['axes.xmargin'] = 1
mpl.rcParams['xtick.labelsize'] = 'x-large'
mpl.rcParams['xtick.major.size'] = 5
mpl.rcParams['xtick.major.width'] = 1.5
mpl.rcParams['ytick.labelsize'] = 'x-large'
mpl.rcParams['ytick.major.size'] = 5
mpl.rcParams['ytick.major.width'] = 1.5
mpl.rcParams['legend.frameon'] = False

#read in estimated values
noise="legacy"
dust_noise=Table.read("results.fits")

#print(dust_noise.keys())
# parameters that we are interested in
var_name=["bayes.stellar.m_star","bayes.stellar.metallicity","bayes.sfh.age_main"]
var_name_err=["bayes.stellar.m_star_err","bayes.stellar.metallicity_err","bayes.sfh.age_main_err"]

#read in input values
inputfile = pickle.load(open("../../lgal.mini_mocha.bc03.meta.p", 'rb')) 

# parameters that we are interested in
input_var=["logM_total","Z_MW", "t_age_MW"]

print("mean(Minput-Minfer)", np.mean(abs(inputfile["logM_total"]-np.log10(dust_noise["bayes.stellar.m_star"]))))
print("mean(Merr)", np.mean(np.log10(dust_noise["bayes.stellar.m_star"][i])-np.log10(dust_noise["bayes.stellar.m_star"][i]-dust_noise["bayes.stellar.m_star_err"][i])))

print("mean(Ageinput-Ageinfer)", np.mean(abs(inputfile["t_age_MW"]-dust_noise["bayes.sfh.age_main"]/1000)))
print("mean(Ageerr)", np.mean(dust_noise["bayes.sfh.age_main_err"]/1000))

print("mean(Zinput-Zinfer)", np.mean(abs(inputfile["Z_MW"]-dust_noise["bayes.stellar.metallicity"])))
print("mean(Zerr)", np.mean(dust_noise["bayes.stellar.metallicity_err"]))


figure = plt.figure(figsize=(15,4))
for i,var,var_err,input in zip(range(1,len(var_name)+1),var_name,var_name_err,input_var):
	#print(i,var,var_err,input)
	ax = figure.add_subplot(1,3,i)
	x = np.linspace(0, 100, 1000)
	ax.plot(x,x, '--k')
	if input == "logM_total": #estimated mass is not log
		ax.errorbar(inputfile[input],np.log10(dust_noise[var]),yerr=np.log10(dust_noise[var])-np.log10(dust_noise[var]-dust_noise[var_err]),fmt=".C0")
		#ax.errorbar(inputfile[input],np.log10(1.7*dust_noise[var]),yerr=np.log10(dust_noise[var])-np.log10(dust_noise[var]-dust_noise[var_err]),fmt=".C0")
		ax.set_ylim(9,12)
		ax.set_xlim(9,12)
		ax.set_xlabel(r'input $\log~M_{\rm tot}$', fontsize=25)
		ax.set_ylabel(r'inferred $\log~M_{\rm tot}$', fontsize=25)
	elif input == "t_age_MW": #estimated age in Myr
		ax.errorbar(inputfile[input],dust_noise[var]/1000,yerr=dust_noise[var_err]/1000,fmt=".C0")
		ax.set_xlabel(r'input MW $t_{\rm age}$', fontsize=20)
		ax.set_xlim(0, 13) 
		ax.set_ylabel(r'inferred MW $t_{\rm age}$', fontsize=20)
		ax.set_ylim(0, 13) 
	else:
		ax.errorbar(inputfile[input],dust_noise[var],yerr=dust_noise[var_err],fmt=".C0")
		ax.set_xlabel(r'input MW $Z$', fontsize=20)
		ax.set_xscale('log') 
		ax.set_xlim(1e-3, 5e-2) 
		ax.set_ylabel(r'inferred MW $Z$', fontsize=20)
		ax.set_yscale('log') 
		ax.set_ylim(1e-3, 5e-2) 



#figure.suptitle("%s %s" %(dust,noise))
figure.subplots_adjust(wspace=0.4)

figure.savefig("mini_mocha_cigale_%s.pdf" %(noise), bbox_inches='tight')
plt.close(figure)
