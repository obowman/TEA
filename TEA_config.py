# TEA_config.py
# Config file containing booleans/params for TEA to use to prevent 
#  in-line testing / modifications.

# ### Change below to control how TEA runs
maxiter   = 20  # (Def: 100) Iteration each TP should stop at. More 
                 #   iterations ensure more accurate results but will 
                 #   increase calculation time
forceiter = True # (Def: True) Force TEA to perform all iterations 
exp       =  40  # (Def: 40) Decimal digit to limit mole fraction 
                 #   precision on if forceiter = False. Not working
                 #   as intended.

# ### Change below to control output files / displays
doprint = False # (Def: False) Enable various debug printouts 
times   = False # (Def: False) Enable time printing for speed tests 

save_headers = True # (Def: False) Preserve headers for multi-TP 
                    #   pre-atm files 
save_outputs = True # (Def: False) Preserve intermediate outputs for 
                    #   multi-TP pre-atm files 
clean        = True # (Def: True) Erase any intermediate files made 
                    #   after production
nofile       = True # (Def: True) Use main loop using no intermediate
                    #   files created


# ### DEGRADED, DO NOT CHANGE FOR NOW
dex     = False

# ########################################################## #
# ############## DO NOT EDIT BELOW THIS POINT ############## #
# ########################################################## #
if (save_headers or save_outputs):
    clean  = False
    nofile = False

# End of file
