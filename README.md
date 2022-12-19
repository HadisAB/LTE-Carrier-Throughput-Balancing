# LTE-Carrier-Throughput-Balancing
Finding the candidates of LTE throughput balancing based on carriers per LTE sites.

## Goal
Sometimes you will see huge gap in the performance of different cells in a sector of LTE sites. 
It is too time-consuming for optimizer to find these cells one by one and make them balance.<br />
In this project we are going to find such cells automatically and share candidates with optimization engineer to accelerate the job. You also might face different items to be chosen as a metric for balancing the carriers load of one site which are explained in the following part.<br />

## Balancing Metrics
Main LTE KPI candidates to balance carriers situation in a site are:

##### Payload #####
> As different carriers have different features from MIMO, TX, BW ,... point of views, there is not logical to compare them based on their traffic (Payload).
Actually different features make them to have different spectral efficiencies. <br />

##### PRB Utilization rate #####
> As explain different features of different cells make them have various capabilities.<br />
As an examples, there is not fair to compare the utilization rate of 50% for cellA with BW=10MHz and cellB with BW=20MHz.
Because the number of free PRBs in cell A is 25 while this is 50 for cellB. So this is not good metric to make them balance.<br />


##### Throughput #####
> Troughput has been selected as a balancing metric in current project. Balancing the throughput between cells of a sector leads to better quality of experience (QoE) or Mean Opinion Score (MOS) of users - which is called ‘Net Promoter Score (NPS)’ in our mobile operatoe network. However this balancing may not lead to higher total throughput of the sector, but it leads to better QoE. To clarify this issue, consider the logarithmic relation between throughput and MOS in different services in below references. As an example you can see this relation for web service in the following figure. (There is also logarithmic relation for other services (audio, video), which are shown in mentioned references in more details.) <br />

References: 
 - *[M. Rugelj, U. Sedlar, M. Volk, J. Sterle, M. Hajdinjak, and A. Kos, “Novel cross-layer QoE-aware radio resource allocation algorithms in multiuser OFDMA systems,” IEEE Transactions on Communications, vol. 62, no. 9, pp. 3196-3208, Sep. 2014.](https://ieeexplore.ieee.org/document/6877621)*
 - *[H. Abarghouyi, S. M. Razavizadeh and E. Björnson, "QoE-Aware Beamforming Design for Massive MIMO Heterogeneous Networks," in IEEE Transactions on Vehicular Technology, vol. 67, no. 9, pp. 8315-8323, Sept. 2018, doi: 10.1109/TVT.2018.2843355.](https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=QoE-Aware%20Beamforming%20Design%20for%20Massive%20MIMO%20Heterogeneous%20Networks&newsearch=true&type=alt1)*


### QoE and Throughput Relation (web service) ###
𝑀𝑂𝑆<sub>𝑤𝑒𝑏</sub>  represents the user perceived quality expressed in real numbers ranging from 1 to 5 (i.e., the score 1 represents “extremely low quality” whereas score 5 represents “excellent quality”).<br />

𝑀𝑂𝑆<sub>𝑤𝑒𝑏</sub>=−𝐾<sub>1</sub>ln⁡(𝑑(𝑅<sub>𝑤𝑒𝑏</sub> ))+𝐾<sub>2</sub> <br />
𝑑(𝑅<sub>𝑤𝑒𝑏</sub> )=3𝑅𝑇𝑇+𝐹𝑆/𝑅<sub>𝑤𝑒𝑏</sub> +L(MSS/R<sub>web</sub> +RTT)−2MSS(2<sup>L</sup>−1)/R<sub>web</sub> <br />
<br />
𝑲<sub>𝟏</sub> and 𝑲<sub>𝟐</sub> : These constants are selected in such a way that the value of MOS falls in the range of 1 to 5.<br />
𝑹<sub>𝒘𝒆𝒃</sub> [bit/s] : Throughput<br />
 𝑹𝑻𝑻 [s] : Round Trip Time<br />
 𝑭𝑺 [bit] : Web page size <br />
 𝑴𝑺𝑺 [bit] : Maximum Segment Size<br />
 𝑳 : Number of slow start cycles with idle periods.
 <br />
 <br />
 <img src=https://github.com/HadisAB/LTE-Carrier-Throughput-Balancing/blob/main/MOS_Web.png/>
 
 
#### Analysis of LOG relation with one example: ####
Consider two users with throughput 2.5 (green) and 23 (red) Mbps in the network. As shown if you balance the throughput in the network, the cells with poor throughput/MOS will receive better throughput/MOS and vice versa. As shown although there is no change in the average throughput (in this example), the logarithmic relation leads to higher average MOS in the network, the poor users are more happier, where the rich ones may even not experience huge changes.<br />

Pre average MOS: (2.2+4.8)/2=3.5 <br />
Post average MOS : (3.2+4.65)/2=3.925 <br />
In above example there were 12% improvement. 
 <br />

<img src=https://github.com/HadisAB/LTE-Carrier-Throughput-Balancing/blob/main/MOS_Example.png/>

 <br /> <br />
 ## Innovated Method
Based on different investigations, we have provided a method to select all cells which are not balanced (through the throughput point of view) in our network to increase our users’ experience.  Below are the list of criteria in our method. 

Criteria:
1. The hourly data for 24hours has been considered.
2. The three cells of each sector(L1800 , L2600_1 and L2100) has been considered.
3.  The unbalanced cases are the ones with below criteria for at least 70% of our hourly data :<br />
 Thp_good_cell: consider we are going to check throughput balancing between two cells, the ones with better throughput is called good_cell and vice versa. <br />
 > - (Thp_good_cell - Thp_poor_cell) > THR_limitation<br />
    *We will select the cells with throughput difference more than THR_limitation.
THR_limitation is 5000 and 4500 for cases to import into the unbalanced report and the ones to be exported from the report, respectively. (to refuse ping pong)*
 > - Thp_good_cell > min_THR<br />
  *It is needed to make sure about the good performance of good_cell.<br />*
  *We consider min_THR =10000 Mbps in our network.*
 > - Thp_poor_cell < minimum_THR_band   <br />
  *It is needed to ensure about the poor performance of poor_cell.<br />*
  *We consider minimum_THR_band =10000 Mbps in our network.*
 > - PRB Utilization Rate of good_cell <PRB_limitation.<br />
  *It is needed to  ensure about the free capacity of good_cell.*
<br /> 

 ## Python Programme of Project
 To solve the problem, we are going to use python programming, you can find the [scripts]() in this repository and use it with below instructions.<br /> 
 -There are some input excels which are necessary to be in the folder of your python code.<br />
 -Due to confidential issues just the excel samples have been added as input and you should extend it based on your data in the LTE network.<br />
 -We are using MAPS system to export LTE KPIs per cells. 
 
 #### Inputs: ####
1.	The csv files with name ‘Cell_Hourly’, which consists hourly KPIs in below columns:
'Time', '4G LTE CELL',   '4G_Throughput_UE_DL_kbps_IR(Kbps)',     '4G_PRB_Util_Rate_PDSCH_Avg_IR(#)'
2.	The csv files with name ‘CFG-’ for exporting some features.
3.	The csv files with name ‘Cell_Daily’, which consists daily ‘cell_avail_man’ .
4.	tracker.xlsx : A tracker consists of the history of Layer_balancing cases.
5.	unbalanced_cells.xlsx : The list of open cells in previous produced layer_balancing report.
6.	tracker-closed.xlsx: The list of total closed/parked cells in previous produced layer_balancing report.
7.	trend.xlsx: The summation of open cases in layer_balancing till now. This is kept to show the trend of total open cases per region per day. 
8.	trend -new- close.xlsx: The number of new close cases per region per day.. 
9.	Parked_cells.xlsx: This is a list of total parked cases of layer_balancing report. 
10.	CFG_3.csv: This is another cfg fike that is used to fill the 4G cfg missings.
11.	Site Priority OPT list.xlsx: The list of Priority sites to select P1 and P2 cases (apply another filtering on data).



 #### Outputs: ####
The parts of 4 to 8 of mentioned inputs, are the outputs, too. In other words, we are using the output of each report as the input of next report.

### Different Phases of project:

The python code has been written in different python cells (sections) in bellow main phases:<br />

**Phase 1: Insert data** <br />
-	Backup: In this part we are taking a backup of previous report output. It may be useful for further investigations.
-	Reading the input files 


**Phase 2: Preprocessing**<br />
We will do some preprocessing for all data to make them ready for analysis. 

**Phase 3: Layer balancing process**
-	Applying the layer balancing criteria and check the cases.
-	The unbalanced cases are the ones who are unbalance in last three days based on above mentioned criteria (for at least 70% of hours in a day):<br />
	Desired throughput difference to select the unbalance cases is 5 Mbps.<br />
	Desired high PRB utilization rate and throughput of better cell is 50% and 10Mbps, respectively.<br />
	The hourly Throughput of selected cases is less than 10 Mbps.<br />

-	The close cases are the ones who have improved for last two days based on below criteria:<br />
	The hourly throughput difference of unbalanced cases has been decreased to less than 4.5Mbps (for at least 50% of hours in a day).<br />
	The hourly throughput of poor cell (the cell with less throughput) has been improved to more than 11.5Mbps (for at least 80% of hours in a day).<br />


**Phase 4: Output**<br />
-	Saving the output excel files and plots of layer balancing project.


