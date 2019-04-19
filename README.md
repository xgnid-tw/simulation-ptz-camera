PTZ camera simulator
======

The goal of this project is to simulate PTZ camera scheduling of [VSS (Vision Splitting Scheduling)](https://drive.google.com/file/d/1fYSZnkw17IxDMPwCX5b55vwKcNYcTDkN/view?usp=sharing) and the algorithm in [this paper](https://ieeexplore.ieee.org/document/6965869).

Because of the characteristics of fixed position, there are many restrictions when traditional surveillance system is deploying. It will increase overall cost for redeploying if a new target needs to be monitored by system.

We make use of the feature of field of view overlapping and avoid detection dead angle when cameras rotate. Furthermore, for closing to the reality situation, we consider splitting vision of camera and quantify the experiment result.

Simulation Model
====
We have the following assumptions
* Each target has its minimun detection time
* The field of vision of each camera split to center and side with its own weight (as following pictures)

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
                <img src="https://i.imgur.com/yNvWDCW.png" width="400">
            </a>
        </td>
    </tr>
</table>

Simulation result
====
We set the score is the sum of the product of each object and its covered weight.
The field of view is 60° and the center is 20°. The camera period is 10s. All result is the averge of 100 kind of different minimun time.

More figure with different camera number or restrict see [pp.29-35](/paper.pdf)
<table border="0">
    <tr>
        <td>Vision spliting diagram</td>
    </tr>
    <tr>
        <td border=0>
            <a href="https://i.imgur.com/468Xu4Y.png">
                <img src="https://i.imgur.com/468Xu4Y.png">
            </a>
        </td>
    </tr>
</table>