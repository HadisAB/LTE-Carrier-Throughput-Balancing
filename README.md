# LTE-Carrier-Throughput-Balancing
Finding the candidates of LTE throughput balancing based on carriers per LTE sites.

## Goal
If you are working with a LTE wireless communication netweork, you might face different items to be chosen as a metric for balancing the carriers load of one site.

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
