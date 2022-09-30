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


## QoE and Throughput Relation (web service)
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
 ## Python Programe of Project
Based on different investigations, we have provided a method to select all cells which are not balanced (through the throughput point of view) in our network to increase our users’ experience.  Below are the list of criteria in our method. 

Criteria *:
- The hourly data for 24hours has been considered.
- The three cells of each sector(L1800 , L2600_1 and L2100) has been considered.
- The unbalanced cases are the ones with below criteria for at least 70% of our hourly data :
 Thp_good_cell: consider we are going to check throughput balancing between two cells, the ones with better throughput is called good_cell and vice versa. 
 - (Thp_good_cell - Thp_poor_cell) > THR_limitation
 - Thp_good_cell > min_THR
-- Thp_poor_cell < minimum_THR_band   
-- Number of free PRB of good_cell <PRB_limitation.

 
 The unbalanced cases are the ones which satisfy below criteria for at least 70% of our hourly data :

(Thp_good_cell - Thp_poor_cell) > THR_limitation
Thp_good_cell > min_THR
Thp_poor_cell < minimum_THR_band  
Number of free PRB of good_cell<PRB_limitation.

(Thp_good_cell - Thp_poor_cell) > THR_limitation
We will select the cells with throughput difference more than THR_limitation.
THR_limitation is 5.2 and 4.8 for cases to import into the unbalanced report and the ones to be exported from the report, respectively. (to refuse ping pong)

2. Thp_good_cell > min_THR
It is needed to make sure about the good performance of good_cell.
We consider min_THR =12Mbps in our network. 

3. Thp_poor_cell < minimum_THR_band
 It is needed to ensure about the poor performance of poor_cell.
 ‘minimum_THR_band’  of each cell has been selected based on the distribution of all cells in that band per time and province. (for example, the throughput of LN4240XA1 in Tehran has been compared with the throughput of all L1800 cells in Tehran in different hours. Therefore there is a fair limitation for each cell based on  the distribution of its same cells.
 We have considered ‘minimum_THR_band ‘ as ‘percentile(15)’ of mentioned distribution. 
![image](https://user-images.githubusercontent.com/58902718/193329704-aaaa8012-8447-42fd-b5d2-10fa4a31aa6e.png)



 
 To solve the problem, we are going to use python programming, you can find the [scripts]() in this repository and use it with below instructions.<br /> 
 -There are some input excels which are necessary to be in the folder of your python code.<br />
 -Due to security issues just the excel samples have been added as input and you should extend it based on your data in the LTE network.<br />
 -We are using MAPS system to export LTE KPIs per cells. 
 
 #### Inputs: ####
1.	The csv files with name ‘4GFDD_Cell_4KPI_Hourly’, which consists hourly KPIs in below columns and located in FTP:
'Time', '4G LTE CELL',   '4G_Throughput_UE_DL_kbps_IR(Kbps)',     '4G_PRB_Util_Rate_PDSCH_Avg_IR(#)'
2.	The csv files with name ‘CellCFG-4GFDD’, which are in FTP.
3.	The csv files with name ‘4G_Cell_Daily’, which consists daily ‘cell_avail_man’ KPI and located in FTP.
4.	tracker.xlsx : A tracker consists of the history of Layer_balancing cases.
5.	unbalanced_cells.xlsx : The list of open cells in previous produced layer_balancing report.
6.	tracker-closed.xlsx: The list of total closed/parked cells in previous produced layer_balancing report.
7.	trend.xlsx: The summation of open cases in layer_balancing till now. This is kept to show the trend of total open cases per region per day. 
8.	trend -new- close.xlsx: The number of new close cases per region per day.. 
9.	Parked_cells.xlsx: This is a list of total parked cases of layer_balancing report by the approval of MTN OPT engineer. The comment column in this report clarifies the reason of parking. The cases of this list have been added by the approval and comment of MTN OPT engineer. We should keep the email of their approval (and the reason of parking case) as an evidence and fill this list manually (exactly as same as previous cases in list) not automatically.
10.	atoll_lte_fdd_cells.csv: This is the Atoll stats and is used to fill the 4G cellcfg missings.
11.	Site Priority OPT list.xlsx: The list of Priority sites to select P1 and P2 cases.



 #### Outputs: ####
1.	The parts of 4 to 8 of mentioned inputs, are the outputs, too. In other words, we are using the output of each report as the input of next report.
2.	‘missed_per_thr.xlsx’ is one output that shows the stats of MAPS per hour and day. It can be checked to find the missing in MAPS. 

### Different Phases of project:


The python code has been written in different python cells (sections). It’s better to run it cell by cell to check both the MAPS stats for any missing and solve the probability occurred errors.
•	Run each cell and check the ‘CHECK’ (with capital alphabet) comments and the explanation in front of it. It clarifies in which parts you need to double check the MAPS missing stats or where you should update your email.
•	If you face error after running each cell, you can use the ‘ERROR’ (with capital alphabet) comment in that cell. It may help you to find the reason of error.



Phase 1: Insert data
•	Backup: In this part we are taking a backup of previous report output. It may be useful for further investigations.
•	Reading the input files from FTP: We are using the hourly stats of 4G KPIs for this report as the input, which are downloaded directly from FTP. They are 24 csv files consists of the data of 24 hours of yesterday.
•	Checking the MAPS missing stats: We will import the input files and check the downloaded files to ensure about their completion.

Phase 2: Preprocessing
We will do some preprocessing for all data to make them ready for analysis. 

Phase 3: Layer balancing process
•	Applying the layer balancing criteria and check the cases.
•	The unbalanced cases are the ones who are unbalance in last three days based on below criteria (for at least 70% of hours in a day):
	Desired throughput difference to select the unbalance cases is 5.2 Mbps.
	Desired high PRB utilization rate and throughput of better cell is 50% and 10Mbps, respectively.
	The hourly Throughput of selected cases is less than 8 Mbps.

•	The close cases are the ones who have improved for last two days based on below criteria:
	The hourly throughput difference of unbalanced cases has been decreased to less than 4.5Mbps (for at least 50% of hours in a day).
	The hourly throughput of poor cell (the cell with less throughput) has been improved to more than 9.5Mbps (for at least 80% of hours in a day).




Phase 4: Output
•	Saving the output excel files and plots of layer balancing project.
•	Sending the automated email of layer balancing report.

