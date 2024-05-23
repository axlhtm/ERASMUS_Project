# =============================================================================
# GVS AND OASIS ANALYSIS: PLOTS
# =============================================================================

# =============================================================================
# GVS AND OASIS ANALYSIS: PLOTS FOR PRESSURE BEFORE AND AFTER GVS IN EACH REGIONS
# =============================================================================
# Define pressure differences ante and post gv in each region
def pressure_dif_gv(): 
    global max_P_anteGV_EAST, max_P_postGV_EAST, max_P_anteGV_WEST, max_P_postGV_WEST
    max_P_anteGV_EAST = [0] * 17520  
    max_P_postGV_EAST = [0] * 17520
    for column_EAST in range(P_net_EAST.shape[0]):
        max_P_anteGV_EAST[column_EAST] = max(Pressure_EAST_concatenated.iloc[column_EAST, :])
        max_P_postGV_EAST[column_EAST] = max(P_net_EAST.iloc[column_EAST, :])
    max_P_anteGV_WEST = [0] * 17520  
    max_P_postGV_WEST = [0] * 17520
    for column_WEST in range(P_net_WEST.shape[0]):
        max_P_anteGV_WEST[column_WEST] = max(Pressure_WEST_concatenated.iloc[column_WEST, :])
        max_P_postGV_WEST[column_WEST] = max(P_net_WEST.iloc[column_WEST, :])
    # Replace nan with 0 
    max_P_postGV_EAST = list(map(lambda x: 0 if pd.isna(x) else x, max_P_postGV_EAST))
    max_P_postGV_WEST = list(map(lambda x: 0 if pd.isna(x) else x, max_P_postGV_WEST))    
pressure_dif_gv()
# Plot pressure differences 
def plot_pressure_dif_gv_EAST(): 
    # Define the X-Axis range as the month
    x = list(range(0, 17520))  # Create list from 1 to 17520
    custom_ticks = [720, 2160, 3600, 5040, 6480, 7920, 9360, 10800, 12240, 13680, 15120, 16560]
    custom_labels = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    # Create the high-resolution figure
    plt.figure(figsize=(8, 6), dpi=300)  # Adjust figure size and resolution as needed
    # Plot the EAST Region
    ## Plot the pressure distribution before the GVS
    for i in range(P_net_EAST.shape[1]):
        plt.plot(x, P_net_EAST.iloc[:, i ], 'bo')
    ## Plot the pressure distribution after the GVS
    for i in range(Pressure_EAST_concatenated.shape[1]):
        plt.plot(x, Pressure_EAST_concatenated.iloc[:, i ], 'ro')
    plt.plot(x, max_P_anteGV_EAST, 'r', label='Before GV Installation', linewidth=2)
    plt.plot(x, max_P_postGV_EAST[:], 'b', label='Before GV Installation', linewidth=2)
    # Set X-Axis range and ticks
    plt.xticks(custom_ticks, custom_labels, rotation=90)
    # Set Y-Axis range and ticks
    plt.ylim(0, 100)  # Set y-axis limits from 0 to 100
    plt.yticks(range(0, 121, 10)) 
    # Set figure information remaining customizations (e.g., labels, title, legend)
    plt.ylabel('Pressure (m)')
    plt.title('Pressure Distribution within Eastern Network')
    plt.legend(loc='upper left') 
plot_pressure_dif_gv_EAST()
def plot_pressure_dif_gv_WEST(): 
    # Define the X-Axis range as the month
    x = list(range(0, 17520))  # Create list from 1 to 17520
    custom_ticks = [720, 2160, 3600, 5040, 6480, 7920, 9360, 10800, 12240, 13680, 15120, 16560]
    custom_labels = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    # Create the high-resolution figure
    plt.figure(figsize=(8, 6), dpi=300)  # Adjust figure size and resolution as needed
    # Plot the WEST Region
    ## Plot the pressure distribution before the GVS
    for i in range(P_net_WEST.shape[1]):
        plt.plot(x, P_net_WEST.iloc[:, i ], 'bo')
    ## Plot the pressure distribution after the GVS
    for i in range(Pressure_WEST_concatenated.shape[1]):
        plt.plot(x, Pressure_WEST_concatenated.iloc[:, i ], 'ro')
    plt.plot(x, max_P_anteGV_WEST, 'r', label='Before GV Installation', linewidth=2)
    plt.plot(x, max_P_postGV_WEST[:], 'b', label='Before GV Installation', linewidth=2)
    # Set X-Axis range and ticks
    plt.xticks(custom_ticks, custom_labels, rotation=90)
    # Set Y-Axis range and ticks
    plt.ylim(0, 100)  # Set y-axis limits from 0 to 100
    plt.yticks(range(0, 121, 10)) 
    # Set figure information remaining customizations (e.g., labels, title, legend)
    plt.ylabel('Pressure (m)')
    plt.title('Pressure Distribution within WESTern Network')
    plt.legend(loc='upper left') 
plot_pressure_dif_gv_WEST()

# =============================================================================
# GVS AND OASIS ANALYSIS: PLOTS FOR GVS ENERGETIC BALANCE IN EACH REGIONS
# =============================================================================
def plot_gvs_energy_bal(): 
    # Calculate y-axis limits 
    EAST_min = min(min(final_consumption_GV_EAST), min(final_recovery_GV_EAST))
    EAST_max = max(max(final_consumption_GV_EAST), max(final_recovery_GV_EAST))
    WEST_min = min(min(final_consumption_GV_WEST), min(final_recovery_GV_WEST))
    WEST_max = max(max(final_consumption_GV_WEST), max(final_recovery_GV_WEST))
    y_min = min(EAST_min, WEST_min)
    y_max = max(EAST_max, WEST_max)
    y_buffer = (y_max - y_min) * 0.1  # Add a 10% buffer for better visualization

    # Define the X-Axis range as the month
    x = list(range(0, 17520))  # Create list from 1 to 17520
    custom_ticks = [720, 2160, 3600, 5040, 6480, 7920, 9360, 10800, 12240, 13680, 15120, 16560]
    custom_labels = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    # Create the high-resolution figure for EAST region
    plt.figure(figsize=(8, 6), dpi=300)
    # Plot the EAST Region
    plt.subplot(1, 2, 1)  # Create first subplot occupying 1 row, 2 columns, position 1
    plt.plot(x, final_consumption_GV_EAST, 'r', label='Consumption', linewidth=2)
    plt.plot(x, final_recovery_GV_EAST, 'b', label='Recovery', linewidth=2)
    # Set X-Axis range and ticks
    plt.xticks(custom_ticks, custom_labels, rotation=90)  # Adjust rotation if needed
    # Set Y-Axis range and ticks
    plt.ylim(y_min - y_buffer, y_max + y_buffer)
    # Set figure information remaining customizations (e.g., labels, title, legend)
    plt.ylabel('Cumulative Energy [Wh]')
    plt.title('East Network')
    plt.legend(loc='upper left')
    
    # Create the high-resolution figure for WEST region
    plt.subplot(1, 2, 2)  # Create second subplot occupying 1 row, 2 columns, position 2
    # Plot the WEST Region
    plt.plot(x, final_consumption_GV_WEST, 'r', label='Consumption', linewidth=2)
    plt.plot(x, final_recovery_GV_WEST, 'b', label='Recovery', linewidth=2)
    # Set X-Axis range and ticks
    plt.xticks(custom_ticks, custom_labels, rotation=90)  # Adjust rotation if needed
    # Set Y-Axis range and ticks
    plt.ylim(y_min - y_buffer, y_max + y_buffer)
    # Set figure information remaining customizations (e.g., labels, title, legend)
    plt.ylabel('Cumulative Energy [Wh]')
    plt.title('West Network')  # Change to 'Central Network' if applicable
    plt.legend(loc='upper left')
    
    # Add main title for the entire figure
    plt.suptitle('Green Valve Energetic Balance', fontsize=14)  # Adjust font size as desired
    # Adjust layout (optional)
    plt.tight_layout()
plot_gvs_energy_bal()

# =============================================================================
# GVS AND OASIS ANALYSIS: PLOTS FOR OASIS ENERGETIC BALANCE IN EACH REGIONS
# =============================================================================
# Define OASIS energetic balances in each region
def oasis_energy_bal_EAST(): 
    global cum_rec_0_50_EAST, cum_rec_50_100_EAST, cum_rec_100_150_EAST, cum_rec_150_200_EAST, cum_rec_200_250_EAST, cum_rec_250_300_EAST, cum_max_consumption_EAST 
    rec_0_50_EAST       = np.zeros(17520, dtype=float)
    rec_50_100_EAST     = np.zeros(17520, dtype=float)
    rec_100_150_EAST    = np.zeros(17520, dtype=float)
    rec_150_200_EAST    = np.zeros(17520, dtype=float)
    rec_200_250_EAST    = np.zeros(17520, dtype=float)
    rec_250_300_EAST    = np.zeros(17520, dtype=float)

    for i in range(num_columns):
        print(i)
        rec_0_50_EAST[i]     = np.nanmean(Recovery_less_than_50_EAST[:, i])
        rec_50_100_EAST[i]   = np.nanmean(Recovery_50_100_EAST[:, i])
        rec_100_150_EAST[i]  = np.nanmean(Recovery_100_150_EAST[:, i])
        rec_150_200_EAST[i]  = np.nanmean(Recovery_150_200_EAST[:, i])
        rec_200_250_EAST[i]  = np.nanmean(Recovery_200_250_EAST[:, i])
        rec_250_300_EAST[i]  = np.nanmean(Recovery_more_than_250_EAST[:,i])
    
    cum_rec_0_50_EAST    = np.cumsum(rec_0_50_EAST)
    cum_rec_50_100_EAST  = np.cumsum(rec_50_100_EAST)
    cum_rec_100_150_EAST = np.cumsum(rec_100_150_EAST)
    cum_rec_150_200_EAST = np.cumsum(rec_150_200_EAST)
    cum_rec_200_250_EAST = np.cumsum(rec_200_250_EAST)
    cum_rec_250_300_EAST = np.cumsum(rec_250_300_EAST)
    
    max_consumption_EAST       = np.zeros(17520)  
    max_consumption_nodes_EAST = np.sum(consumption_EAST, axis=1)
    index_max                  = np.argmax(max_consumption_nodes_EAST)
    max_consumption_EAST       = consumption_EAST[index_max, :]
    cum_max_consumption_EAST   = np.cumsum(max_consumption_EAST)
oasis_energy_bal_EAST()

def plot_oasis_energy_bal_EAST(): 
    # Create the high-resolution figure for EAST region
    plt.figure(figsize=(8, 6), dpi=300)
    # Define the X-Axis range as the month
    x = list(range(0, 17520))  # Create list from 1 to 17520
    custom_ticks = [720, 2160, 3600, 5040, 6480, 7920, 9360, 10800, 12240, 13680, 15120, 16560]
    custom_labels = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    # Plot the EAST Region
    plt.plot(x, cum_rec_0_50_EAST, color=(0, 0.4470, 0.7410), linestyle='-', linewidth=1.5, label='Operating Hours < 50')
    plt.plot(x, cum_rec_50_100_EAST, color=(0.8500, 0.3250, 0.0980), linestyle='-', linewidth=1.5, label='Operating Hours between 50-100')
    plt.plot(x, cum_rec_100_150_EAST, color=(0.9290, 0.6940, 0.1250), linestyle='-', linewidth=1.5, label='Operating Hours between 100-150')
    plt.plot(x, cum_rec_150_200_EAST, color=(0.4940, 0.1840, 0.5560), linestyle='-', linewidth=1.5, label='Operating Hours between 150-200')
    plt.plot(x, cum_rec_200_250_EAST, color=(0.4660, 0.6740, 0.1880), linestyle='-', linewidth=1.5, label='Operating Hours between 200-250')
    plt.plot(x, cum_rec_250_300_EAST, color=(0.3010, 0.7450, 0.9330), linestyle='-', linewidth=1.5, label='Operating Hours between 250-300')
    plt.plot(x, cum_max_consumption_EAST, color='red', linestyle='--', linewidth=1.5, label='Maximum Node Consumption')
    # Set X-Axis range and ticks
    plt.xticks(custom_ticks, custom_labels, rotation=90)  # Adjust rotation if needed
    # Set Y-Axis range and ticks
    plt.ylim(0, 35000)  # Set y-axis limits (0 to 35000)
    plt.yticks(range(0, 35001, 5000))  # Set y-axis ticks with increment of 5000
    # Set figure information remaining customizations (e.g., labels, title, legend)
    plt.legend(loc='upper left') 
    plt.title('OAS Energetic Balance within Eastern Network')
    plt.ylabel('Cumulated Energy [Wh]')
    plt.grid(True)
plot_oasis_energy_bal_EAST()

def oasis_energy_bal_WEST(): 
    global cum_rec_0_50_WEST, cum_rec_50_100_WEST, cum_rec_100_150_WEST, cum_rec_150_200_WEST, cum_rec_200_250_WEST, cum_rec_250_300_WEST, cum_max_consumption_WEST 
    rec_0_50_WEST       = np.zeros(17520, dtype=float)
    rec_50_100_WEST     = np.zeros(17520, dtype=float)
    rec_100_150_WEST    = np.zeros(17520, dtype=float)
    rec_150_200_WEST    = np.zeros(17520, dtype=float)
    rec_200_250_WEST    = np.zeros(17520, dtype=float)
    rec_250_300_WEST    = np.zeros(17520, dtype=float)

    for i in range(num_columns):
        print(i)
        rec_0_50_WEST[i]     = np.nanmean(Recovery_less_than_50_WEST[:, i])
        rec_50_100_WEST[i]   = np.nanmean(Recovery_50_100_WEST[:, i])
        rec_100_150_WEST[i]  = np.nanmean(Recovery_100_150_WEST[:, i])
        rec_150_200_WEST[i]  = np.nanmean(Recovery_150_200_WEST[:, i])
        rec_200_250_WEST[i]  = np.nanmean(Recovery_200_250_WEST[:, i])
        rec_250_300_WEST[i]  = np.nanmean(Recovery_more_than_250_WEST[:,i])
    
    cum_rec_0_50_WEST    = np.cumsum(rec_0_50_WEST)
    cum_rec_50_100_WEST  = np.cumsum(rec_50_100_WEST)
    cum_rec_100_150_WEST = np.cumsum(rec_100_150_WEST)
    cum_rec_150_200_WEST = np.cumsum(rec_150_200_WEST)
    cum_rec_200_250_WEST = np.cumsum(rec_200_250_WEST)
    cum_rec_250_300_WEST = np.cumsum(rec_250_300_WEST)
    
    max_consumption_WEST       = np.zeros(17520)  
    max_consumption_nodes_WEST = np.sum(consumption_WEST, axis=1)
    index_max                  = np.argmax(max_consumption_nodes_WEST)
    max_consumption_WEST       = consumption_WEST[index_max, :]
    cum_max_consumption_WEST   = np.cumsum(max_consumption_WEST)
oasis_energy_bal_WEST()

def plot_oasis_energy_bal_WEST(): 
    # Create the high-resolution figure for WEST region
    plt.figure(figsize=(8, 6), dpi=300)
    # Define the X-Axis range as the month
    x = list(range(0, 17520))  # Create list from 1 to 17520
    custom_ticks = [720, 2160, 3600, 5040, 6480, 7920, 9360, 10800, 12240, 13680, 15120, 16560]
    custom_labels = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    # Plot the WEST Region
    plt.plot(x, cum_rec_0_50_WEST, color=(0, 0.4470, 0.7410), linestyle='-', linewidth=1.5, label='Operating Hours < 50')
    plt.plot(x, cum_rec_50_100_WEST, color=(0.8500, 0.3250, 0.0980), linestyle='-', linewidth=1.5, label='Operating Hours between 50-100')
    plt.plot(x, cum_rec_100_150_WEST, color=(0.9290, 0.6940, 0.1250), linestyle='-', linewidth=1.5, label='Operating Hours between 100-150')
    plt.plot(x, cum_rec_150_200_WEST, color=(0.4940, 0.1840, 0.5560), linestyle='-', linewidth=1.5, label='Operating Hours between 150-200')
    plt.plot(x, cum_rec_200_250_WEST, color=(0.4660, 0.6740, 0.1880), linestyle='-', linewidth=1.5, label='Operating Hours between 200-250')
    plt.plot(x, cum_rec_250_300_WEST, color=(0.3010, 0.7450, 0.9330), linestyle='-', linewidth=1.5, label='Operating Hours between 250-300')
    plt.plot(x, cum_max_consumption_WEST, color='red', linestyle='--', linewidth=1.5, label='Maximum Node Consumption')
    # Set X-Axis range and ticks
    plt.xticks(custom_ticks, custom_labels, rotation=90)  # Adjust rotation if needed
    # Set Y-Axis range and ticks
    plt.ylim(0, 35000)  # Set y-axis limits (0 to 35000)
    plt.yticks(range(0, 35001, 5000))  # Set y-axis ticks with increment of 5000
    # Set figure information remaining customizations (e.g., labels, title, legend)
    plt.legend(loc='upper left') 
    plt.title('OAS Energetic Balance within Western Network')
    plt.ylabel('Cumulated Energy [Wh]')
    plt.grid(True)
plot_oasis_energy_bal_WEST()