# LTE-Carrier-Throughput-Balancing
Finding the candidates of LTE throughput balancing based on carriers per LTE sites.

## Goal
Sometimes you will see huge gap in the performance of different cells in a sector of LTE sites. 
It is too time-consuming for optimizer to find these cells one by one. So, the optimizer should check all cells with their different features to make sector balanced.<br />
In this project we are going to find such cells automatically and share candidates with optimization engineer to accelerate the job. You also might face different items to be chosen as a metric for balancing the carriers load of one site.<br />

Main LTE KPI candidates to balance carriers situation in a site are:

###### Payload #####
As different carriers have different features from MIMO, TX, BW ,... point of views, there is not logical to compare them based on their traffic (Payload).<br />
Differnt features make them to have different spectral efficiencies. <br />

##### PRB Utilization rate #####
As explain different features of different cells make them have various capabilities.<br />
As an examples, there is not fair to compare the utilization rate of 50% for cellA with BW=10MHz and cellB with BW=20MHz.
Because the number of free PRBs in cell A is 25 while this is 50 for cellB. So this is not good metric to make them balance.<br />


##### Throughput #####
I have selected this KPIs to make cells balance, because this item is relevant to users' experience (although we have limitation in our network to work exactly with the user throughput perception, there is a good reference to select balance candidates with site throughput.)<br />
