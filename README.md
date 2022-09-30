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

References: <br />
- [M. Rugelj, U. Sedlar, M. Volk, J. Sterle, M. Hajdinjak, and A. Kos, “Novel cross-layer QoE-aware radio resource allocation algorithms in multiuser OFDMA systems,” IEEE Transactions on Communications, vol. 62, no. 9, pp. 3196-3208, Sep. 2014.](https://ieeexplore.ieee.org/document/6877621)
- [H. Abarghouyi, S. M. Razavizadeh and E. Björnson, "QoE-Aware Beamforming Design for Massive MIMO Heterogeneous Networks," in IEEE Transactions on Vehicular Technology, vol. 67, no. 9, pp. 8315-8323, Sept. 2018, doi: 10.1109/TVT.2018.2843355.](https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=QoE-Aware%20Beamforming%20Design%20for%20Massive%20MIMO%20Heterogeneous%20Networks&newsearch=true&type=alt1)


## QoE and Throughput Relation (web service)
𝑀𝑂𝑆_𝑤𝑒𝑏  represents the user perceived quality expressed in real numbers ranging from 1 to 5 (i.e., the score 1 represents “extremely low quality” whereas score 5 represents “excellent quality”).<br />

𝑀𝑂𝑆_𝑤𝑒𝑏=−𝐾~1~ln⁡(𝑑(𝑅~𝑤𝑒𝑏~ ))+𝐾~2~ <br />
𝑑(𝑅_𝑤𝑒𝑏 )=3𝑅𝑇𝑇+𝐹𝑆/𝑅_𝑤𝑒𝑏 +L(MSS/R_web +RTT)−2MSS(2^L−1)/R_web <br />

𝑲_𝟏 and 𝑲_𝟐 : These constants are selected in such a way that the value of MOS falls in the range of 1 to 5.
𝑹_𝒘𝒆𝒃 [bit/s] : Throughput
 𝑹𝑻𝑻 [s] : Round Trip Time
 𝑭𝑺 [bit] : Web page size 
 𝑴𝑺𝑺 [bit] : Maximum Segment Size
 𝑳 : Number of slow start cycles with idle periods.







