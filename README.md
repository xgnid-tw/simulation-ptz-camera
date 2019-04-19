PTZ camera simulator
======

The goal of this project is to simulate PTZ camera scheduling of [VSS (Vision Splitting Scheduling)](https://drive.google.com/file/d/1fYSZnkw17IxDMPwCX5b55vwKcNYcTDkN/view?usp=sharing) and the algorithm in [this paper](https://ieeexplore.ieee.org/document/6965869).

Simulation Model
====
We determinate the minimum detecting time of each object, and set the weights to different angel of field of vision. 

<table border="0">
    <tr>
        <td>Vision spliting diagram</td>
        <td>Weight defination</td>
    </tr>
    <tr>
        <td border=0>
            <a href="https://i.imgur.com/Hthv1iK.png">
                <img src="https://i.imgur.com/Hthv1iK.png">
            </a>
        </td>
        <td>
            <a href="https://i.imgur.com/yNvWDCW.png">
                <img src="https://i.imgur.com/yNvWDCW.png">
            </a>
        </td>
    </tr>
</table>
