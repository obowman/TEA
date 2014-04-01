# TEA_config.py
# Config file containing booleans/params for TEA to use to prevent 
#  in-line testing / modifications.

# ### Change below to control how TEA runs
maxiter   = 100  # (Def: 100) Iteration each TP should stop at. More 
                 #   iterations ensure more accurate results but will 
                 #   increase calculation time
forceiter = True # (Def: True) Force TEA to perform all iterations 
exp       =  40  # (Def: 40) Decimal digit to limit mole fraction 
                 #   precision on if forceiter = False. Not working
                 #   as intended.
                 
# ### Change below to control output files / displays
doprint = False # (Def: False) Enable various debug printouts 
times   = False # (Def: False) Enable time printing for speed tests 

save_headers = False # (Def: False) Preserve headers for multi-TP 
                    #   pre-atm files 
save_outputs = True # (Def: False) Preserve intermediate outputs for 
                    #   multi-TP pre-atm files

# ### Change below to control lambda correction method
explore = False  # Allow for lambda exploration (smart find, two directions)
lower   = -20    # lowest exponent for lambda array
steps   =  30    # Steps in lambda array

abun_scale = 1  # (Def: 1) Multiplicative scaling for mole numbers.  
                 # Use values >= 10 if TEA reports inconsistent abundances 
                 # at low temperatures.

# ########################################################## #
# ############## DO NOT EDIT BELOW THIS POINT ############## #
# ########################################################## #

# ########################
# ### DEPRECATED, DO NOT CHANGE FOR NOW
#nofile  = True # (Def: True) Use main loop using no intermediate
                    #   files created
#clean        = False # (Def: True) Erase any intermediate files made 
                    #   after production
#testbool = False # Proven no effect...



